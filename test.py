import os

ip_adress = 1
playbook_tmp = "/etc/ansible/scripts/auto_creation_service/templates/windows.txt"
playbook_path = "/etc/ansible/scripts/auto_creation_service/playbook-windows.yml"
copy = "cat '" + playbook_tmp +"' > '" + playbook_path +"'"
os.system(copy)
with open(playbook_path, 'rw') as filer :
    filedata = filer.read()
    filedata = filedata.replace('/IP/', ip_adress)
    file.write(filedata)

