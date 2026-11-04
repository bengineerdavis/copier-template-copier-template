#!/usr/bin/env bash
# Report prerequisite status for this repository's tool-update setup.
#
# This repo's strategy is github-app (see docs/tool-updates.md): the Mend
# Renovate app schedules renovate.json bumps, and the tool-bump workflow
# schedules the opencode pin that Renovate cannot own. This is an informant,
# not a gate: it always exits 0. `set -e` is deliberately omitted so one
# failed network check never truncates the report.
set -uo pipefail

ok() { printf '  OK       %s\n' "$1"; }
missing() { printf '  MISSING  %s\n' "$1"; }
unknown() { printf '  UNKNOWN  %s\n' "$1"; }
info() { printf '  INFO     %s\n' "$1"; }

# gh resolves PR and repo-view commands against the parent repository for
# fork checkouts, so every gh call targets the repo explicitly, derived
# from the origin remote rather than gh's own resolution.
repo_from_origin() {
  local url repo
  url=$(git remote get-url origin 2> /dev/null) || return 1
  repo="${url#*github.com[:/]}"
  repo="${repo%.git}"
  [[ -n $repo ]] || return 1
  printf '%s' "$repo"
}

gh_ready() {
  command -v gh > /dev/null 2>&1 || return 1
  gh auth status > /dev/null 2>&1 || return 1
}

workflow_pushed() {
  local file="$1"
  [[ -f $file ]] || {
    missing "$file (not stamped or deleted)"
    return 0
  }
  ok "$file present"
  if gh_ready; then
    repo=$(repo_from_origin) || repo=""
    default_branch=$(gh api "repos/$repo" --jq .default_branch 2> /dev/null || true)
    if [[ -n $repo ]] && [[ -n $default_branch ]] \
      && gh api "repos/$repo/contents/$file?ref=$default_branch" > /dev/null 2>&1; then
      ok "$file is on the default branch ($default_branch); the schedule will run"
    else
      missing "$file not found on the default branch of origin"
      info "  fix: commit and push it (scheduled workflows only run from there)"
    fi
  else
    unknown "cannot verify $file is pushed (gh missing or unauthenticated)"
    info "  manual: it must exist on the default branch of origin; push it if missing"
  fi
}

echo "Renovate (hosted app — schedules renovate.json bumps):"
if [[ -f renovate.json ]]; then
  ok "renovate.json present"
else
  missing "renovate.json present"
fi
if gh_ready; then
  repo=$(repo_from_origin) || repo=""
  if [[ -n $repo ]] && gh pr list -R "$repo" --author "app/renovate" --state all --limit 1 2> /dev/null | grep -q .; then
    ok "Mend Renovate app installed and active (its PRs are on this repository)"
  else
    missing "Mend Renovate app not detected on this repository"
    info "  fix: open https://github.com/apps/renovate/installations/new (browser consent; no CLI/API install path exists)"
    info "  choose All repositories (zero-touch for future repos) or Only select repositories + this repo"
  fi
else
  unknown "cannot verify the app install (gh missing or unauthenticated)"
  info "  manual: check this repository's PRs for renovate[bot]; install via https://github.com/apps/renovate/installations/new"
fi

echo "opencode pin (tool-bump workflow — the pin Renovate cannot own):"
workflow_pushed ".github/workflows/tool-bump.yml"
if [[ -f scripts/update-opencode.sh ]] && shellcheck scripts/update-opencode.sh 2> /dev/null; then
  ok "scripts/update-opencode.sh present and shellcheck-clean"
else
  missing "scripts/update-opencode.sh missing or failing shellcheck"
fi
if [[ -f mise.toml ]] && grep -q '^version' mise.toml; then
  version=$(awk -F'"' '/^\[tools\."http:opencode"\]$/ {f = 1; next} f && /^version/ {print $2; exit}' mise.toml)
  ok "opencode pin present in mise.toml (currently $version)"
  info "  run 'mise run tool-bump' to move it, or wait for the scheduled workflow"
else
  missing "opencode pin block missing from mise.toml"
fi

exit 0
