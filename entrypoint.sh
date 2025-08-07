#!/bin/bash
set -e

echo "Iniciando Action..."

BRANCH_NAME="$INPUT_BRANCH_NAME"
GH_TOKEN="$INPUT_GITHUB_TOKEN"
GH_OWNER="$INPUT_GITHUB_OWNER"
GH_REPO="$INPUT_GITHUB_REPO_NAME"
export GH_TOKEN
export GH_OWNER
export GH_REPO
echo "GH_TOKEN recebido: ${GH_TOKEN:0:5}****** e ${GW_REPO} e ${GH_OWNER}"

if [[ "$BRANCH_NAME" == "homolog" ]]; then
  output=$(python3 /scripts/main.py --prerelease)
  echo "$output"
  TAG=$(echo "$output"| grep "TAG:" | awk '{print $2}')
elif [[ "$BRANCH_NAME" == "master" ]]; then
  output=$(python3 /scripts/main.py --release)
  echo "$output"
  TAG=$(echo "$output"| grep "TAG:" | awk '{print $2}')
else
  echo "Branch $BRANCH_NAME não suportada para release"
  exit 1
fi

echo "Tag calculada: $TAG"
echo "tag=$TAG" >> "$GITHUB_OUTPUT"

echo "Release finalizada com sucesso."
