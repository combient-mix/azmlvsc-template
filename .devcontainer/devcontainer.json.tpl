{
  "name": "devcontainer",
  "dockerFile": "Dockerfile",
  "context": "..",
  "remoteUser": "default",
  // Uncomment when running on Azure instance
  // "workspaceFolder": "/code/path/to/workspace",
  // "workspaceMount": "source=/home/azureuser/cloudfiles/code,target=/code,type=bind,consistency=default",
  // "runArgs": [
  //   "--cap-add=SYS_ADMIN",
  //   "--device=/dev/fuse",
  //   "--security-opt=apparmor:unconfined"
  // ],
  "extensions": [
    "ms-azuretools.vscode-docker",
    "ms-python.python",
    "ms-toolsai.jupyter",
    "exiasr.hadolint",
    "yzhang.markdown-all-in-one",
    "ms-mssql.mssql"
  ],
  "mounts": [
    "source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind,consistency=default",
  ],
  "containerEnv": {
    "DATABRICKS_ADDRESS": "",
    "DATABRICKS_API_TOKEN": "",
    "DATABRICKS_CLUSTER_ID": "",
    "DATABRICKS_ORG_ID": "",
    "DATABRICKS_PORT": "15001",
  }
}