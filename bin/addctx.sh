#!/bin/bash
remote_host=$1
ip_address=$2

# add SSH configuration
touch ~/.ssh/config
grep "Host $remote_host" ~/.ssh/config >> /dev/null
if [ $? -eq 1 ]; then
cat << EOF >> ~/.ssh/config
Host $remote_host
  HostName $ip_address
  User azureuser
  Port 50000
  ForwardAgent true
EOF
fi

# add docker context
docker context inspect "$remote_host" > /dev/null 2>&1
if [ $? -eq 1 ]; then
  docker context create "$remote_host" --docker host="ssh://$remote_host"
fi