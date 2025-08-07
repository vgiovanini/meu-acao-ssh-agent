#!/bin/bash
set -e

echo "Iniciando Action..."

BRANCH_NAME="$INPUT_BRANCH_NAME"
PRERELEASE_BRANCH_NAME="$INPUT_PRE_RELEASE_BRANCH_NAME"
RELEASE_BRANCH_NAME="$INPUT_RELEASE_BRANCH_NAME"
GH_TOKEN="$INPUT_GITHUB_TOKEN"
GH_OWNER="$INPUT_GITHUB_OWNER"
GH_REPO="$INPUT_GITHUB_REPO_NAME"
export GH_TOKEN
export GH_OWNER
export GH_REPO

if [[ "$BRANCH_NAME" == "$PRERELEASE_BRANCH_NAME" ]]; then
  output=$(python3 /scripts/main.py --prerelease)
  echo "$output" | grep -v "TAG:"
  TAG=$(echo "$output"| grep "TAG:" | awk '{print $2}')
elif [[ "$BRANCH_NAME" == "$RELEASE_BRANCH_NAME" ]]; then
  output=$(python3 /scripts/main.py --release)
  echo "$output" | grep -v "TAG:"
  TAG=$(echo "$output"| grep "TAG:" | awk '{print $2}')
else
  echo "Branch $BRANCH_NAME not supported for release"
  exit 1
fi

echo "Tag calculada: $TAG"
echo "tag=$TAG" >> "$GITHUB_OUTPUT"

echo "Release finalizada com sucesso."
