#!/bin/sh
# Install only this fork's exact templates; never edit primary-session configuration.
set -eu

fail() { printf '%s\n' "ERROR: $*" >&2; exit 1; }
usage() {
  cat <<'EOF'
Usage: install-agents.sh [--target-dir PATH] [--check] [--check-role ROLE ...]

Install Codex Advisor's native templates without overwriting existing files.
The default target is "$CODEX_HOME/agents", or "$HOME/.codex/agents".
  --target-dir PATH  Use an explicit destination directory.
  --check            Check all shipped roles without modifying the destination.
  --check-role ROLE  Check advisor, luna, sol, or reviewer; repeatable; implies --check.
  --help            Show this help text.
EOF
}

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
template_dir=$script_dir/../agents
target_dir=${CODEX_HOME:-${HOME:?HOME or CODEX_HOME is required}/.codex}/agents
check_only=0
selected=''
all_roles='advisor luna sol reviewer'
while [ "$#" -gt 0 ]; do
  case "$1" in
    --target-dir)
      [ "$#" -ge 2 ] && [ -n "$2" ] || fail "--target-dir requires a path."
      case "$2" in --*) fail "--target-dir requires an explicit path." ;; esac
      target_dir=$2
      shift 2 ;;
    --check) check_only=1; shift ;;
    --check-role)
      [ "$#" -ge 2 ] || fail "--check-role requires a role."
      case "$2" in advisor|luna|sol|reviewer) ;; *) fail "unknown role: $2 (expected advisor, luna, sol, or reviewer)" ;; esac
      selected="$selected $2"
      check_only=1
      shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) fail "unknown argument: $1" ;;
  esac
done
[ -n "$selected" ] || selected=$all_roles
case "$target_dir" in /*) ;; *) target_dir=$(pwd -P)/$target_dir ;; esac
# Reject unsafe ancestors too; lexical dot segments must not bypass this check.
case "$target_dir/" in *'/../'*|*'/./'*) fail "dot path segments are not supported." ;; esac
target_dir=${target_dir%/}
case "$target_dir" in *[!/]*) ;; *) fail "refusing the filesystem root." ;; esac

check_directory() {
  ancestor=$target_dir
  while [ -n "$ancestor" ]; do
    [ ! -L "$ancestor" ] || fail "symlinked target or ancestor: $ancestor"
    if [ -e "$ancestor" ] && [ ! -d "$ancestor" ]; then
      fail "target or ancestor is not a directory: $ancestor"
    fi
    ancestor=${ancestor%/*}
  done
}

role_file() {
  case "$1" in
    advisor) printf '%s\n' codex-advisor-astra-advisor.toml ;;
    luna) printf '%s\n' codex-advisor-luna-implementer.toml ;;
    sol) printf '%s\n' codex-advisor-sol-implementer.toml ;;
    reviewer) printf '%s\n' codex-advisor-astra-reviewer.toml ;;
  esac
}

check_file() {
  template=$template_dir/$(role_file "$1")
  destination=$target_dir/$(role_file "$1")
  [ -f "$template" ] && [ ! -L "$template" ] || fail "shipped template missing or unsafe: $template"
  if [ -L "$destination" ] || { [ -e "$destination" ] && [ ! -f "$destination" ]; }; then
    fail "unsafe destination: $destination"
  fi
  if [ -f "$destination" ]; then
    cmp -s "$template" "$destination" || fail "modified or conflicting destination: $destination"
  elif [ "$check_only" -eq 1 ]; then
    fail "missing role: $destination"
  fi
}

check_directory
for role in $selected; do check_file "$role"; done
if [ "$check_only" -eq 1 ]; then
  printf '%s\n' "CHECK PASSED: selected templates match exactly."
  exit 0
fi

mkdir -p "$target_dir" || fail "could not create target directory."
check_directory
for role in $selected; do check_file "$role"; done
for role in $selected; do
  check_directory
  check_file "$role"
  if [ -f "$destination" ]; then
    printf '%s\n' "ALREADY CURRENT: $destination"
    continue
  fi
  staged=$(mktemp "$target_dir/.codex-advisor-agent.XXXXXX") || fail "could not stage template."
  if ! cp "$template" "$staged"; then
    rm -f "$staged"
    fail "could not copy template."
  fi
  if ! ln "$staged" "$destination"; then
    rm -f "$staged"
    fail "destination changed after preflight; existing files were not overwritten."
  fi
  rm -f "$staged"
  printf '%s\n' "INSTALLED: $destination"
done
check_only=1
for role in $selected; do check_file "$role"; done
printf '%s\n' "INSTALL PASSED: shipped templates match exactly."
