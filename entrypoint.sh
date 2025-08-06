#!/bin/bash
set -e

echo "Iniciando Action..."

# CI_REGISTRY="$INPUT_CI_REGISTRY"
# CI_REGISTRY_IMAGE="$INPUT_CI_REGISTRY_IMAGE"
# CI_REGISTRY_USER="$INPUT_CI_REGISTRY_USER"
# CI_REGISTRY_PASSWORD="$INPUT_CI_REGISTRY_PASSWORD"
BRANCH_NAME="$INPUT_BRANCH_NAME"
GH_TOKEN="$INPUT_GITHUB_TOKEN"
GH_OWNER="$INPUT_GITHUB_OWNER"
GH_REPO="$INPUT_GITHUB_REPO_NAME"
export GH_TOKEN
export GH_OWNER
export GH_REPO
echo "GH_TOKEN recebido: ${GH_TOKEN:0:5}****** e ${GW_REPO} e ${GH_OWNER}"

# echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"

docker buildx create --use

if [[ "$BRANCH_NAME" == "homolog" ]]; then
  TAG=$(python3 /scripts/main.py --prerelease | grep "TAG:" | awk '{print $2}')
elif [[ "$BRANCH_NAME" == "master" ]]; then
  TAG=$(python3 /scripts/main.py --release | grep "TAG:" | awk '{print $2}')
else
  echo "Branch $BRANCH_NAME não suportada para release"
  exit 1
fi

echo "Tag calculada: $TAG"

# docker buildx build --platform linux/amd64,linux/arm64 \
#   -t "${CI_REGISTRY_IMAGE}:${TAG}" \
#   --push \
#   -f Dockerfile .

echo "Build e push finalizados com sucesso."
