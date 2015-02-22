Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network :forwarded_port, guest: 80, host: 8080
  config.ssh.insert_key = false

  config.vm.provision "ansible" do |ansible|
    ansible.inventory_path = "inventory.txt"
    ansible.playbook = "jenkins_local.yml"
    ansible.limit = "local"
  end

end
