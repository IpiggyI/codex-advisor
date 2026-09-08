#!/bin/sh
# Emit only allowlisted routing metadata from one exact native subagent rollout.

set -eu

usage() {
  cat <<'EOF'
Usage: inspect-agent-runtime.sh [--sessions-dir DIR] [--advisor-effort EFFORT | --luna | --explorer-effort EFFORT | --astra-effort EFFORT | --sol-effort EFFORT] THREAD_ID
       inspect-agent-runtime.sh [--sessions-dir DIR] --review-primary-effort EFFORT [--reviewer-effort EFFORT] THREAD_ID
       inspect-agent-runtime.sh --select-review-effort --review-primary-effort EFFORT [--reviewer-effort EFFORT]

Read the one rollout file whose filename ends with THREAD_ID and emit a compact JSON
object containing only safe routing metadata. Without --sessions-dir, the sessions
root is "$CODEX_HOME/sessions" when CODEX_HOME is already set, otherwise
"$HOME/.codex/sessions".

--advisor-effort requires the native Astra Advisor, the requested effort, and
observable permission metadata. It validates routing evidence, not task completion
or enforced isolation. --luna requires the native Luna Implementer at max with
observable permission metadata. Without a role option, emit generic routing evidence.
--explorer-effort requires the native Luna Explorer at the requested effort, with
observable permission metadata. It does not certify enforced read-only isolation.
--astra-effort requires the native Astra Implementer at the requested effort (pass
medium for the default delegated call), with observable permission metadata.
--sol-effort requires the native Sol Implementer at the requested effort (pass high
for the default delegated call), with observable permission metadata.
--review-primary-effort requires the native Astra Independent reviewer at the
default floor, or the explicit --reviewer-effort at or above the primary effort.
--select-review-effort prints that selection without reading runtime records.
The caller must establish the primary effort from host evidence and confirm host
support. Selection alone proves neither actual invocation nor primary settings.
EOF
}

fail() {
  printf '%s\n' "ERROR: $*" >&2
  exit 1
}

effort_rank() {
  case "$1" in
    low) printf '1\n' ;; medium) printf '2\n' ;; high) printf '3\n' ;;
    xhigh) printf '4\n' ;; max) printf '5\n' ;;
    *) fail "unsupported or unestablished review effort order." ;;
  esac
}

sessions_dir=''
expected_role=''
expected_model=''
expected_effort=''
primary_effort=''
reviewer_effort=''
select_review=0
thread_id=''
while [ "$#" -gt 0 ]; do
  case "$1" in
    --sessions-dir|--advisor-effort|--explorer-effort|--astra-effort|--sol-effort|--review-primary-effort|--reviewer-effort)
      [ "$#" -ge 2 ] && [ -n "$2" ] || fail "option requires a value."
      case "$2" in --*) fail "option requires an explicit value." ;; esac ;;
  esac
  case "$1" in
    --sessions-dir)
      sessions_dir=$2; shift 2 ;;
    --advisor-effort)
      [ -z "$expected_role" ] || fail "select exactly one role contract."
      case "$2" in low|medium|high|xhigh|max|ultra) ;; *) fail "unsupported Advisor effort." ;; esac
      expected_role=codex_advisor_astra_advisor
      expected_model=gpt-6-astra
      expected_effort=$2; shift 2 ;;
    --luna)
      [ -z "$expected_role" ] || fail "select exactly one role contract."
      expected_role=codex_advisor_luna_implementer
      expected_model=gpt-5.6-luna
      expected_effort=max
      shift ;;
    --explorer-effort)
      [ -z "$expected_role" ] || fail "select exactly one role contract."
      case "$2" in low|medium|high|xhigh|max|ultra) ;; *) fail "unsupported Explorer effort." ;; esac
      expected_role=codex_advisor_luna_explorer
      expected_model=gpt-5.6-luna
      expected_effort=$2; shift 2 ;;
    --astra-effort)
      [ -z "$expected_role" ] || fail "select exactly one role contract."
      case "$2" in low|medium|high|xhigh|max|ultra) ;; *) fail "unsupported Astra implementation effort." ;; esac
      expected_role=codex_advisor_astra_implementer
      expected_model=gpt-6-astra
      expected_effort=$2; shift 2 ;;
    --sol-effort)
      [ -z "$expected_role" ] || fail "select exactly one role contract."
      case "$2" in low|medium|high|xhigh|max|ultra) ;; *) fail "unsupported Sol effort." ;; esac
      expected_role=codex_advisor_sol_implementer
      expected_model=gpt-5.6-sol
      expected_effort=$2; shift 2 ;;
    --review-primary-effort)
      [ -z "$expected_role" ] || fail "select exactly one role contract."
      expected_role=codex_advisor_astra_reviewer
      expected_model=gpt-6-astra
      primary_effort=$2; shift 2 ;;
    --reviewer-effort)
      [ -z "$reviewer_effort" ] || fail "supply reviewer effort only once."
      reviewer_effort=$2; shift 2 ;;
    --select-review-effort) select_review=1; shift ;;
    --help|-h) usage; exit 0 ;;
    --*) fail "unknown argument." ;;
    *) [ "$#" -eq 1 ] || fail "exactly one trailing THREAD_ID is required."
       thread_id=$1; shift ;;
  esac
done
if [ -n "$primary_effort" ]; then
  primary_rank=$(effort_rank "$primary_effort")
  expected_effort=high
  [ "$primary_rank" -le 3 ] || expected_effort=$primary_effort
  if [ -n "$reviewer_effort" ]; then
    reviewer_rank=$(effort_rank "$reviewer_effort")
    [ "$reviewer_rank" -ge "$primary_rank" ] || fail "reviewer effort is below the primary session effort."
    expected_effort=$reviewer_effort
  fi
elif [ -n "$reviewer_effort" ] || [ "$select_review" -eq 1 ]; then
  fail "review selection requires the resolved primary effort."
fi
if [ "$select_review" -eq 1 ]; then
  [ -z "$thread_id$sessions_dir" ] || fail "selection does not accept a thread or sessions directory."
  printf '%s\n' "$expected_effort"
  exit 0
fi
[ -n "$thread_id" ] || fail "exactly one THREAD_ID is required."

if ! printf '%s\n' "$thread_id" | LC_ALL=C grep -Eq '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'; then
  fail "THREAD_ID must be a lowercase UUID."
fi

if [ -z "$sessions_dir" ]; then
  if [ -n "${CODEX_HOME-}" ]; then
    sessions_dir=$CODEX_HOME/sessions
  else
    [ -n "${HOME-}" ] || fail "HOME is unset and CODEX_HOME was not supplied; pass --sessions-dir explicitly."
    sessions_dir=$HOME/.codex/sessions
  fi
fi

[ -d "$sessions_dir" ] || fail "sessions directory is unavailable."

tmp_base=${TMPDIR:-/tmp}
case "$tmp_base" in
  /*) ;;
  *) tmp_base=/tmp ;;
esac
matches_file=''

cleanup() {
  if [ -n "$matches_file" ] && [ -f "$matches_file" ]; then
    case "$matches_file" in
      "$tmp_base"/codex-advisor-runtime.*)
        rm -f "$matches_file"
        ;;
      *)
        printf '%s\n' "ERROR: refusing cleanup of unexpected temporary file." >&2
        ;;
    esac
  fi
}

trap cleanup 0 HUP INT TERM

matches_file=$(mktemp "$tmp_base/codex-advisor-runtime.XXXXXX") || fail "could not create a temporary match list."

# Match only the exact rollout filename suffix; do not inspect any rollout contents
# until exactly one filename has been found.
if ! find "$sessions_dir" -type f -name "rollout-*-$thread_id.jsonl" -print > "$matches_file"; then
  fail "could not enumerate rollout filenames under the sessions directory."
fi

match_count=$(awk 'END { print NR + 0 }' "$matches_file")
case "$match_count" in
  0) fail "no rollout filename matched the requested thread id." ;;
  1) ;;
  *) fail "multiple rollout filenames matched the requested thread id." ;;
esac

IFS= read -r rollout_file < "$matches_file" || fail "could not read the matched rollout filename."
[ -f "$rollout_file" ] || fail "matched rollout is unavailable."

# The jq program reads only the matched JSONL and constructs a new allowlisted object.
# It rejects absent or conflicting required routing values instead of inferring them.
if ! jq -ce -s --arg expected_thread_id "$thread_id" --arg expected_role "$expected_role" \
  --arg expected_model "$expected_model" --arg expected_effort "$expected_effort" '
  def string_or_null:
    if type == "string" then . else null end;

  [ .[] | select(.type == "session_meta") | .payload ] as $sessions |
  [ .[] | select(.type == "turn_context") | .payload ] as $turns |
  if ($sessions | length) != 1 then
    error("missing or ambiguous session metadata")
  elif ($turns | length) == 0 then
    error("missing turn context")
  else
    $sessions[0] as $session |
    ($session.id? | string_or_null) as $session_thread_id |
    ($session.parent_thread_id? | string_or_null) as $parent_thread_id |
    ($session.agent_role? | string_or_null) as $agent_role |
    ($session.agent_path? | string_or_null) as $agent_path |
    ($session.model_provider? | string_or_null) as $model_provider |
    [ $turns[] | (.model? | string_or_null) ] as $models |
    [ $turns[] | (.effort? | string_or_null) ] as $efforts |
    [ $turns[] | ((.sandbox_policy? // {}) | .type? | string_or_null) ] as $sandbox_types |
    [ $turns[] | ((.permission_profile? // {}) | .type? | string_or_null) ] as $permission_types |
    [ $turns[] | (.cwd? | string_or_null) ] as $cwds |
    if $session_thread_id == null or $session_thread_id != $expected_thread_id then
      error("session metadata does not identify the requested thread")
    elif $agent_role == null or $agent_role == "" then
      error("missing agent role")
    elif any($models[]; . == null or . == "") then
      error("missing model")
    elif any($efforts[]; . == null or . == "") then
      error("missing effort")
    elif ($models | unique | length) != 1 then
      error("conflicting models")
    elif ($efforts | unique | length) != 1 then
      error("conflicting efforts")
    elif ($sandbox_types | unique | length) != 1 then
      error("conflicting sandbox policy types")
    elif ($permission_types | unique | length) != 1 then
      error("conflicting permission profile types")
    elif ($cwds | unique | length) != 1 then
      error("conflicting working directories")
    elif $expected_role != "" and
      ($agent_role != $expected_role or $models[0] != $expected_model
       or $efforts[0] != $expected_effort) then
      error("role, model, or effort does not match the requested contract")
    elif $expected_role != "" and
      (any($sandbox_types[]; . == null or . == "") or
       any($permission_types[]; . == null or . == "")) then
      error("permission evidence is missing")
    else
      {
        thread_id: $session_thread_id,
        parent_thread_id: $parent_thread_id,
        agent_role: $agent_role,
        agent_path: $agent_path,
        model_provider: $model_provider,
        model: $models[0],
        effort: $efforts[0],
        sandbox_policy_type: $sandbox_types[0],
        permission_profile_type: $permission_types[0],
        cwd: $cwds[0]
      }
    end
  end
' "$rollout_file" 2>/dev/null; then
  fail "missing, ambiguous, invalid, or conflicting routing/permission evidence, or role settings mismatch."
fi
