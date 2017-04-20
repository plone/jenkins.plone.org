Vagrant.configure("2") do |config|
  config.ssh.insert_key = false

  config.vm.define "master", primary: true do |master|
    master.vm.box = "ubuntu/trusty64"
    master.vm.network :forwarded_port, guest: 80, host: 8080
    master.vm.network "private_network", ip: "192.168.50.2"

    master.vm.provision "ansible" do |ansible|
      ansible.inventory_path = "inventory-local.txt"
      ansible.playbook = "jenkins_local.yml"
      ansible.limit = "master"
    end
  end

  config.vm.define "node" do |node|
    node.vm.box = "bento/ubuntu-16.04"
    node.vm.network "private_network", ip: "192.168.50.10"

    node.vm.provision "ansible" do |ansible|
      ansible.inventory_path = "inventory-local.txt"
      ansible.playbook = "jenkins_local.yml"
      ansible.limit = "node"
    end
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 2
  end

end
