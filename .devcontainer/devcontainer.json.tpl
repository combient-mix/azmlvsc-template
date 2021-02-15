{
  "name": "devcontainer",
  "dockerFile": "../Dockerfile",
  "remoteUser": "default",
  // Uncomment when running on Azure instance
  // "workspaceFolder": "/code/path/to/workspace",
  // "workspaceMount": "source=/home/azureuser/cloudfiles/code,target=/code,type=bind,consistency=default",
  "extensions": [
    "ms-azuretools.vscode-docker",
    "ms-python.python",
    "ms-toolsai.jupyter",
    "exiasr.hadolint",
	  "timonwong.shellcheck",
  ],
  "mounts": [
    "source=/var/run/docker.sock,target=/var/run/docker.sock,type=bind,consistency=default",
  ]
}