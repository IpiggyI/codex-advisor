#!/bin/sh
# Install only this fork's exact templates; never edit primary-session configuration.
set -eu

plugin_prefix=ca-

fail() { printf '%s\n' "ERROR: $*" >&2; exit 1; }
usage() {
  cat <<'EOF'
Usage: install-agents.sh [--target-dir PATH] [--check] [--check-role ROLE ...]

Install Codex Advisor's native templates: overwrite this plugin's own files,
remove retired names, and leave everything else untouched.
The default target is "$CODEX_HOME/agents", or "$HOME/.codex/agents".
  --target-dir PATH  Use an explicit destination directory.
  --check            Report drift (differing or missing manifest files) and
                     residue (present retire files) without writing.
  --check-role ROLE  Check a template by filename stem minus the plugin prefix
                     (for example explorer-mainstay-m, advisor-rescue);
                     repeatable; implies --check. Retire files are not part of
                     a selective check.
  --help            Show this help text.
EOF
}

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
template_dir=$script_dir/../agents
retire_list=$template_dir/retire.txt
target_dir=${CODEX_HOME:-${HOME:?HOME or CODEX_HOME is required}/.codex}/agents
check_only=0
selected=''
while [ "$#" -gt 0 ]; do
  case "$1" in
    --target-dir)
      [ "$#" -ge 2 ] && [ -n "$2" ] || fail "--target-dir requires a path."
      case "$2" in --*) fail "--target-dir requires an explicit path." ;; esac
      target_dir=$2
      shift 2 ;;
    --check) check_only=1; shift ;;
    --check-role)
      [ "$#" -ge 2 ] && [ -n "$2" ] || fail "--check-role requires a role."
      case "$2" in --*) fail "--check-role requires a role." ;; esac
      case "$2" in *[!A-Za-z0-9_-]*|'') fail "unknown role: $2" ;; esac
      selected="$selected $2"
      check_only=1
      shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) fail "unknown argument: $1" ;;
  esac
done

# Exact basenames to delete if present. Later tickets edit retire.txt.
retired_files=''
if [ -L "$retire_list" ]; then
  fail "unsafe retire list: $retire_list"
fi
if [ -f "$retire_list" ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in ''|'#'*) continue ;; esac
    case "$line" in */*|*..*) fail "invalid retire name: $line" ;; esac
    retired_files="$retired_files $line"
  done < "$retire_list"
fi

if [ -n "$selected" ]; then
  for role in $selected; do
    template=$template_dir/${plugin_prefix}${role}.toml
    [ -f "$template" ] && [ ! -L "$template" ] || fail "unknown role: $role"
  done
fi

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

note_problem() {
  printf '%s\n' "ERROR: $*" >&2
  check_problems=1
}

preflight_dest() {
  destination=$target_dir/$1
  if [ -L "$destination" ] || { [ -e "$destination" ] && [ ! -f "$destination" ]; }; then
    fail "unsafe destination: $destination"
  fi
}

want_name() {
  stem=${1#"$plugin_prefix"}
  stem=${stem%.toml}
  if [ -z "$selected" ]; then
    return 0
  fi
  for role in $selected; do
    [ "$role" = "$stem" ] && return 0
  done
  return 1
}

check_directory
check_problems=0
for path in "$template_dir"/*.toml; do
  [ -f "$path" ] && [ ! -L "$path" ] || fail "shipped template missing or unsafe: $path"
  name=${path##*/}
  if want_name "$name"; then
    preflight_dest "$name"
    if [ "$check_only" -eq 1 ]; then
      destination=$target_dir/$name
      if [ ! -f "$destination" ]; then
        note_problem "missing: $destination"
      elif ! cmp -s "$path" "$destination"; then
        note_problem "differs: $destination"
      fi
    fi
  fi
done

if [ "$check_only" -eq 1 ]; then
  if [ -z "$selected" ] && [ -n "$retired_files" ]; then
    for name in $retired_files; do
      destination=$target_dir/$name
      if [ -e "$destination" ] || [ -L "$destination" ]; then
        note_problem "residue: $destination"
      fi
    done
  fi
  [ "$check_problems" -eq 0 ] || exit 1
  printf '%s\n' "CHECK PASSED: selected templates match exactly."
  exit 0
fi

mkdir -p "$target_dir" || fail "could not create target directory."
check_directory
for path in "$template_dir"/*.toml; do
  [ -f "$path" ] && [ ! -L "$path" ] || fail "shipped template missing or unsafe: $path"
  name=${path##*/}
  preflight_dest "$name"
done
if [ -n "$retired_files" ]; then
  for name in $retired_files; do
    preflight_dest "$name"
  done
fi

for path in "$template_dir"/*.toml; do
  name=${path##*/}
  destination=$target_dir/$name
  preflight_dest "$name"
  if [ -f "$destination" ] && cmp -s "$path" "$destination"; then
    printf '%s\n' "UNCHANGED: $destination"
    continue
  fi
  staged=$(mktemp "$target_dir/.codex-advisor-agent.XXXXXX") || fail "could not stage template."
  if ! cp "$path" "$staged"; then
    rm -f "$staged"
    fail "could not copy template."
  fi
  if ! mv -f "$staged" "$destination"; then
    rm -f "$staged"
    fail "could not install $destination"
  fi
  printf '%s\n' "INSTALLED: $destination"
done

if [ -n "$retired_files" ]; then
  for name in $retired_files; do
    destination=$target_dir/$name
    if [ -f "$destination" ] && [ ! -L "$destination" ]; then
      rm -f "$destination" || fail "could not remove $destination"
      printf '%s\n' "REMOVED: $destination"
    fi
  done
fi

printf '%s\n' "INSTALL PASSED: shipped templates match exactly."
