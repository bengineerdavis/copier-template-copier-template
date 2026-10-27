#!/usr/bin/env bash
# Bump the [tools."http:opencode"] pin in mise.toml to the newest upstream
# stable release and refresh the per-platform sha256 checksums.
#
# Renovate cannot own this pin: opencode's upstream publishes 2.x releases
# as git tags on anomalyco/opencode without GitHub release objects (the
# stock datasources stop at v1.19.4), and Renovate cannot recompute
# checksums at all. This script is run by hand (`mise run tool-bump`) and
# by the scheduled tool-bump workflow. See docs/tool-updates.md.
set -euo pipefail

MISE_TOML=${1:-mise.toml}

# Asset names per platform (parallel arrays: platform[i] <-> assets[i]);
# keep in sync with the block they replace. Indexed arrays, not associative:
# stock macOS still ships bash 3.2, which lacks `declare -A`.
platforms=(linux-x64 linux-arm64 macos-x64 macos-arm64)
assets=(
  opencode-linux-x64-baseline.tar.gz
  opencode-linux-arm64.tar.gz
  opencode-darwin-x64-baseline.zip
  opencode-darwin-arm64.zip
)

# sha256sum is coreutils; macOS only ships shasum.
if command -v sha256sum > /dev/null 2>&1; then
  hash_stdin() { sha256sum | awk '{print $1}'; }
elif command -v shasum > /dev/null 2>&1; then
  hash_stdin() { shasum -a 256 | awk '{print $1}'; }
else
  echo "update-opencode: need sha256sum or shasum on PATH" >&2
  exit 1
fi

# Newest stable v2.x tag on the upstream mirror of opencode.ai's releases.
# git ls-remote needs no auth and has no API rate limit.
latest=$(
  git ls-remote --tags https://github.com/anomalyco/opencode "refs/tags/v2.*" \
    | awk -F/ '{print $NF}' \
    | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' \
    | sed 's/^v//' \
    | sort -V | tail -n 1
)
if [[ -z $latest ]]; then
  echo "update-opencode: no upstream tags found" >&2
  exit 1
fi

current=$(
  awk -F'"' '/^\[tools\."http:opencode"\]$/ {f = 1; next} f && /^version/ {print $2; exit}' \
    "$MISE_TOML"
)
if [[ -z $current ]]; then
  echo 'update-opencode: no [tools."http:opencode"] block found' >&2
  exit 1
fi
if [[ $latest == "$current" ]]; then
  echo "update-opencode: already at $current"
  exit 0
fi
echo "update-opencode: $current -> $latest"

# Stream each asset and hash it; pipefail aborts on a truncated download.
sums=()
for i in "${!platforms[@]}"; do
  url="https://opencode.ai/files/bin/$latest/${assets[$i]}"
  echo "update-opencode: fetching $url"
  sums+=("$(curl -fsSL "$url" | hash_stdin)")
done

# Regenerate the block, then splice it over the old one: from the header
# line up to the next table header that is not one of its subsections.
block=$(mktemp)
trap 'rm -f "$block"' EXIT
{
  echo '[tools."http:opencode"]'
  echo "version = \"$latest\""
  for i in "${!platforms[@]}"; do
    echo
    echo "[tools.\"http:opencode\".platforms.${platforms[$i]}]"
    echo "url = \"https://opencode.ai/files/bin/$latest/${assets[$i]}\""
    echo "checksum = \"sha256:${sums[$i]}\""
  done
  echo
} > "$block"

awk -v blockfile="$block" '
  $0 == "[tools.\"http:opencode\"]" {
    inblock = 1
    while ((getline line < blockfile) > 0) print line
    close(blockfile)
    next
  }
  inblock && /^\[tools\."http:opencode"/ {next}
  inblock && /^\[/ {inblock = 0}
  inblock {next}
  {print}
' "$MISE_TOML" > "$MISE_TOML.tmp"
mv "$MISE_TOML.tmp" "$MISE_TOML"

echo "update-opencode: $MISE_TOML updated to $latest"
