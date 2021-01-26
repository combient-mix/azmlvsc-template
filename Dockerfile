# Start from prepackaged devcontainer
FROM combientmix/devcontainer-azureml:latest

# Install pip deps
# RUN conda run -n default \
#   pip install --disable-pip-version-check \
#   pip_dep1==x.y.z \
#   pip_dep2==x.y.z