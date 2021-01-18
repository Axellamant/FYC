from configparser import ConfigParser
import os
import random
from getpass import getpass
import time


#def mac_generator() :
#    mac = [ 0x00, 0x24, 0x81,
#    random.randint(0x00, 0x7f),
#    random.randint(0x00, 0xff),
#    random.randint(0x00, 0xff) ]
#    mac_adress = ':'.join(map(lambda x: "%02x" % x, mac))
#    return(mac_adress)


def network_conf_linux(ip_adress):
    conf_tmp = "/etc/ansible/scripts/auto_creation_service/confs/network/network_template.txt"
    conf_path = "/etc/ansible/scripts/auto_creation_service/confs/network/network_template.tmp"
    copy = "cat '" + conf_tmp +"' > '" + conf_path +"'"
    os.system(copy) 
    with open(conf_path, 'r') as filer :
        filedata = filer.read()
        filedata = filedata.replace('/IP/', ip_adress)
    with open(conf_path, 'w') as file:    
        file.write(filedata)




def network_conf_windows(ip_adress):
    playbook_tmp = "/etc/ansible/scripts/auto_creation_service/templates/windows.txt"
    playbook_path = "/etc/ansible/scripts/auto_creation_service/playbook-windows.yml"
    copy = "cat '" + playbook_tmp +"' > '" + playbook_path +"'"
    os.system(copy)
    with open(playbook_path, 'r') as filer :
        filedata = filer.read()
        filedata = filedata.replace('/IP/', ip_adress)
    with open(playbook_path, 'w') as file:
        file.write(filedata)


config = ConfigParser()
config.read('vm_to_create.properties')
to_create = config['VM']['conf'].split(',')

print("Initialisation ...")
time.sleep(2)
print("Ouverture du fichier de conf ...")
time.sleep(1)

path_dyn_template = "/etc/ansible/scripts/auto_creation_service/templates/create_vm_from_template.txt"
path_creation = "/etc/ansible/scripts/auto_creation_service/templates/create_vm_from_template.yml"
print("Mot de passe de l'utilisateur (admin_ansible@vsphere.local):")
password = getpass()
for vms in to_create:
    name = vms.split(':')[0].strip()
    temp = vms.split(':')[1].strip()
    ip = vms.split(':')[2].strip()
    if temp == "centos7":
        template = "template-centos7"
        network_conf_linux(ip)
    if temp == "windows10":
        template = "template-win10"
        network_conf_windows(ip)
    cmd = "cat '" + path_dyn_template +"' > '" + path_creation +"'"
    os.system(cmd)
    with open(path_creation, 'r') as filer :
        filedata = filer.read()
    filedata = filedata.replace('/PASSWORD/', password)
    filedata = filedata.replace('/NAME/', name)
    filedata = filedata.replace('/TEMPLATE/', template)
    with open(path_creation, 'w') as file:
        file.write(filedata)
    print("Creation de la VM " + name + "...")
    time.sleep(1)
    print("Lancement du playbook Ansible ...")
    time.sleep(0.5)
    cmd2 = "ansible-playbook " + path_creation
    os.system(cmd2)
    print("Démarrage de la VM ...")
    time.sleep(30)
    services = vms.split(':')[3].strip()
    if services == "windows":
        print("Démarrage des services ...")
        time.sleep(160)
        cmd3 = "ansible-playbook playbook-" + services + ".yml --ask-vault-pass"
    if services == "linux-web":
        cmd3 = "ansible-playbook playbook-" + services + ".yml"
    print("Installation/Configuration des services ...")
    os.system(cmd3) 









