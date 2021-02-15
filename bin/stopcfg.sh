#!/bin/bash
remote_host=$1

ssh $remote_host /bin/bash << 'EOF'
az login
az config set extension.use_dynamic_install=yes_without_prompt
echo '00 20 * * * az ml computetarget computeinstance stop --name $remote_host > /tmp/azstop.log 2>&1' > /tmp/azureuser
sudo mv /tmp/azureuser /var/spool/cron/crontabs/azureuser
sudo service cron reload
EOF