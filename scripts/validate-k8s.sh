#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-k8s}"
K8S_VERSION="${K8S_VERSION:-1.31.0}"

echo "Discovering YAML manifests under: ${ROOT} (excluding kustomization.yaml)..."

FILES=""
while IFS= read -r f; do
  FILES="${FILES}"$'\n'"${f}"
done < <(
  find "${ROOT}" -type f \( -name "*.yml" -o -name "*.yaml" \) \
    ! -name "kustomization.yml" ! -name "kustomization.yaml" \
    -print
)

if [ -z "${FILES//$'\n'/}" ]; then
  echo "No Kubernetes YAML files found under: ${ROOT}"
  exit 0
fi

echo "Validating manifests with kubeconform (k8s version: ${K8S_VERSION})..."

kubeconform \
  -kubernetes-version "${K8S_VERSION}" \
  -strict \
  -ignore-missing-schemas \
  -schema-location default \
  -schema-location "https://raw.githubusercontent.com/yannh/kubernetes-json-schema/master/{{.NormalizedKubernetesVersion}}-standalone-strict/{{.ResourceKind}}.json" \
  -schema-location "https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json" \
  -schema-location "https://raw.githubusercontent.com/karuppiah7890/kubernetes-crd-schema/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json" \
  $(printf "%s\n" "${FILES}" | sed '/^$/d')
