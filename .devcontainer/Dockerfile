# Base image
FROM mcr.microsoft.com/azureml/base:intelmpi2018.3-ubuntu16.04

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Non-root user with sudo access
ARG USERNAME=default
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Conda
ARG CONDA_ENV_NAME=default
ARG CONDA_DBX_NAME=dbx

# Install apt deps
# hadolint ignore=DL3004
RUN apt-get update \
  && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
  #
  # More apt deps
  && apt-get install -y --no-install-recommends \
  sudo \
  curl \
  vim \
  fuse \
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/* \
  #
  # Install docker binary
  && curl -L https://download.docker.com/linux/static/stable/x86_64/docker-19.03.9.tgz | tar xvz docker/docker \
  && cp docker/docker /usr/local/bin \
  && rm -R docker \
  #
  # Azure CLI
  && curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash \
  #
  # Hadolint
  && wget -O /bin/hadolint \
  https://github.com/hadolint/hadolint/releases/download/v1.19.0/hadolint-Linux-x86_64 \
  && chmod +x /bin/hadolint \
  #
  # Pin conda environment
  #
  && conda install conda=4.9.2 \
  # Create DBX conda environment
  && conda create -n $CONDA_DBX_NAME -c conda-forge \
  python=3.7.7 \
  pip=20.2.4 \
  ipykernel=5.3.4 \
  openjdk=8.0.265 \
  notebook=6.3.0 \
  && conda run -n $CONDA_DBX_NAME \
  pip install --disable-pip-version-check --no-cache-dir databricks-connect==7.3.* \
  #
  # Add Jupyter kernels
  && conda run -n $CONDA_DBX_NAME python -m ipykernel install --name $CONDA_DBX_NAME \
  #
  # Create a non-root user to use if preferred
  && groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  #
  # Accept dbx agreement
  && echo '{}' > /home/$USERNAME/.databricks-connect

# Setup default environment
COPY environment.yaml /tmp/environment.yaml
RUN conda env create -f /tmp/environment.yaml \
  && rm /tmp/environment.yaml \
  && conda run -n $CONDA_ENV_NAME python -m ipykernel install --name $CONDA_ENV_NAME \
  && chown default /opt/miniconda/envs/default

# Init conda for non-root user
USER $USERNAME
RUN conda init bash \
  && conda config --set auto_activate_base false \
  && echo "conda activate $CONDA_ENV_NAME" >> ~/.bashrc

# Set working directory
WORKDIR /home/$USERNAME

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog