#!/bin/bash
VAULT_VERSION="1.0.0"
sudo apt-get install -y unzip curl jq
echo "Determining Consul version to install ..."
CHECKPOINT_URL="https://checkpoint-api.hashicorp.com/v1/check"
if [ -z "$CONSUL_DEMO_VERSION" ]; then
    CONSUL_DEMO_VERSION=$(curl -s "${CHECKPOINT_URL}"/consul | jq .current_version | tr -d '"')
fi
echo "Fetching Consul version ${CONSUL_DEMO_VERSION} ..."
curl -s https://releases.hashicorp.com/consul/${CONSUL_DEMO_VERSION}/consul_${CONSUL_DEMO_VERSION}_linux_amd64.zip -o consul.zip
unzip -f consul.zip
chmod +x consul
rm consul.zip
# Vault
echo "Fetching Vault version: $VAULT_VERSION"
curl -s https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip  -o vault.zip
unzip -f vault.zip
chmod +x vault
rm vault.zip