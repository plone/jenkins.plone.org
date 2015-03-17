Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.ssh.insert_key = false

  config.vm.define "master", primary: true do |master|
    master.vm.network :forwarded_port, guest: 80, host: 8080

    master.vm.provision "ansible" do |ansible|
      ansible.inventory_path = "inventory.txt"
      ansible.playbook = "jenkins_local.yml"
      ansible.limit = "master"
    end
  end

  config.vm.define "node" do |node|
    node.vm.provision "ansible" do |ansible|
      ansible.inventory_path = "inventory.txt"
      ansible.playbook = "jenkins_local.yml"
      ansible.limit = "node"
    end
  end

end
