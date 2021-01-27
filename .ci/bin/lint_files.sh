#!/bin/bash
set -e
LINT_IMAGE="combientmix/devcontainer-azureml:latest"
CONDA_BIN="/opt/conda/envs/default/bin/"

# Lint Dockerfile
docker run -u default -v $PWD/.hadolint.yaml:/.hadolint.yaml -i $LINT_IMAGE \
  hadolint --config /.hadolint.yaml - < Dockerfile

# Lint YAML files
docker run  -u default -v $PWD:/workdir -w /workdir $LINT_IMAGE \
  $CONDA_BIN/yamllint -c .yamllint.yml -s $(find . -name '*.yml' -or -name '*.yaml')

# Lint sh files
docker run -v $PWD:/workdir -w /workdir $LINT_IMAGE \
  $CONDA_BIN/shellcheck $(find . -name '*.sh')

# Check python files
PY_FILES="$(find . -name '*.py')"
if [ -n "$PY_FILES" ]; then
  docker run -v $PWD:/workdir -w /workdir combientmix/devcontainer-azureml:latest \
    $CONDA_BIN/pylint $PY_FILES
  docker run -v $PWD:/workdir -w /workdir combientmix/devcontainer-azureml:latest \
    $CONDA_BIN/yapf --diff $PY_FILES
fi