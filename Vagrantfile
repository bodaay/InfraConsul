# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
echo "Installing dependencies ..."
sudo apt-get update
sudo apt-get install -y unzip curl jq dnsutils
echo "Determining Consul version to install ..."
CHECKPOINT_URL="https://checkpoint-api.hashicorp.com/v1/check"
if [ -z "$CONSUL_DEMO_VERSION" ]; then
    CONSUL_DEMO_VERSION=$(curl -s "${CHECKPOINT_URL}"/consul | jq .current_version | tr -d '"')
fi
echo "Fetching Consul version ${CONSUL_DEMO_VERSION} ..."
cd /tmp/
curl -s https://releases.hashicorp.com/consul/${CONSUL_DEMO_VERSION}/consul_${CONSUL_DEMO_VERSION}_linux_amd64.zip -o consul.zip
echo "Installing Consul version ${CONSUL_DEMO_VERSION} ..."
unzip consul.zip
sudo chmod +x consul
sudo mv consul /usr/bin/consul
sudo mkdir /etc/consul.d
sudo chmod a+w /etc/consul.d
SCRIPT

# Specify a Consul version
CONSUL_DEMO_VERSION = ENV['CONSUL_DEMO_VERSION']

# Specify a custom Vagrant box for the demo
DEMO_BOX_NAME = "ubuntu/bionic64"

# Vagrantfile API/syntax version.
# NB: Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = DEMO_BOX_NAME

  config.vm.define "n1" do |n1|
      n1.vm.hostname = "n1"
    #   n1.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
      n1.vm.network "private_network", ip: "172.20.20.11"
  end

  config.vm.define "n2" do |n2|
      n2.vm.hostname = "n2"
    #   n2.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
      n2.vm.network "private_network", ip: "172.20.20.12"
  end
  
  config.vm.define "n3" do |n3|
      n3.vm.hostname = "n3"
    #   n3.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
      n3.vm.network "private_network", ip: "172.20.20.13"
  end

  config.vm.define "n4" do |n4|
      n4.vm.hostname = "n4"
    #   n4.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
      n4.vm.network "private_network", ip: "172.20.20.14"
  end


  config.vm.define "n5" do |n5|
      n5.vm.hostname = "n5"
    #   n5.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
      n5.vm.network "private_network", ip: "172.20.20.15"
  end

  config.vm.define "n6" do |n6|
    n6.vm.hostname = "n6"
    # n6.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    n6.vm.network "private_network", ip: "172.20.20.16"
  end

  config.vm.define "n7" do |n7|
    n7.vm.hostname = "n7"
    # n7.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    n7.vm.network "private_network", ip: "172.20.20.17"
  end
  
  config.vm.define "n8" do |n8|
    n8.vm.hostname = "n8"
    # n8.vm.provision "shell", inline: $script, env: {'CONSUL_DEMO_VERSION' => CONSUL_DEMO_VERSION}
    n8.vm.network "private_network", ip: "172.20.20.18"
  end
end
