Django project template with Vagrant and Ansible 
================================================

Starting new project  
--------------------
1. Switch to directory with projects;
2. `django-admin.py startproject --template=https://bitbucket.org/grialexey/django-project-template/get/master.zip --name=Vagrantfile,README.md,vars.yml project_name`  
3. Create repository


Starting development
--------------------
0. Don't forget to install vagrant plugins:  
   `vagrant plugin install vagrant-cachier`  
   `vagrant plugin install vagrant-vbguest`  
   And download VBoxGuestAdditions.iso for your version of VirtualBox
1. Switch to project's directory
2. `vagrant up`
3. Uncomment line in Vagrantfile: 
   `config.vm.synced_folder ".", "/var/webapps/{{ project_name }}/code", owner: "{{ project_name }}", group: "{{ project_name }}"`
4. `vagrant reload`
5. `ansible-playbook deployment/deploy.yml -i deployment/hosts/development`
6. `vagrant ssh`
7. `sudo su -l {{ project_name }}`
8. `/var/webapps/{{ project_name }}/virtualenv/bin/python /var/webapps/{{ project_name }}/code/manage.py createsuperuser`
9. `/var/webapps/{{ project_name }}/virtualenv/bin/pip freeze > /var/webapps/{{ project_name }}/code/requirements.txt`
10. `/var/webapps/{{ project_name }}/virtualenv/bin/python /var/webapps/{{ project_name }}/code/manage.py runserver 0.0.0.0:8001`
11. localhost:8002
12. Install static files libs (from local, not from server):
    `cd /var/webapps/{{ project_name }}/code/{{ project_name }}/static/frontend`  
    `npm install`  
    `bower install`

Useful commands
---------------
`vagrant ssh`  
`sudo su -l {{ project_name }}`  
`/var/webapps/{{ project_name }}/virtualenv/bin/python /var/webapps/{{ project_name }}/code/manage.py createsuperuser`  
`/var/webapps/{{ project_name }}/virtualenv/bin/python /var/webapps/{{ project_name }}/code/manage.py shell`  
`/var/webapps/{{ project_name }}/virtualenv/bin/python /var/webapps/{{ project_name }}/code/manage.py runserver 0.0.0.0:8001`  

`/var/webapps/{{ project_name }}/virtualenv/bin/pip install <package>`  
`/var/webapps/{{ project_name }}/virtualenv/bin/pip freeze > /var/webapps/{{ project_name }}/code/requirements.txt`

Passwords crypt
---------------
`>>> openssl passwd -salt salty -1 mypass`


Initial remote server setup
---------------------------
1. Edit deployment/vars.yml file
2. Add files:
   `credentials/production/super_user_name`  
   `credentials/production/super_user_password`  
   `credentials/production/super_user_password_crypted`  
   `credentials/production/project_user_password`  
   `credentials/production/project_user_password_crypted`  
   `credentials/production/ssh_port`  
   `hosts/production`
3. create deployment/hosts/initial  
4. create deployment/hosts/production  
5. generate ssh key in deployment/files/ssh/ dir:  
6. `ssh-keygen -t rsa -C "grialexey@gmail.com"`  
7. add public key in BitBucket repository  
8. `ansible-playbook deployment/initial.yml -i deployment/hosts/initial --ask-pass -c paramiko`  
9. `ansible-playbook deployment/provision.yml -i deployment/hosts/production -K`  
10. `ansible-playbook deployment/upgrade.yml -i deployment/hosts/production -K`  
11. bug with postgres  
    solve by login by ssh and reinstall postgres:  
12. `sudo apt-get remove --purge postgresql-9.1`  
13. `sudo apt-get install postgresql-9.1`  
14. `ansible-playbook deployment/deploy.yml -i deployment/hosts/production -K`


Production deploy
-----------------
`ansible-playbook deployment/deploy.yml -i deployment/hosts/production -K`
