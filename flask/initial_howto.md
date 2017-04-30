# HOW TO DO STUFF
  0. Make sure you have the necessary things
  1. Add the raspberry pi to Ansible
  2. Run Ansible to configure the raspberry pi
  3. Add a new Celery task
  4. Add a new interface for I/O
     1.  add a task to send messages to an interface
     2.  add a periodic task to check for new messages
  5. Add a new Flask endpoint
  6. Confirm that the software is running
     1. Confirm that webserver is running
     2. Confirm that celery tasks are running
     3. Confirm that logs are being collected
  
## One note

In many of the commands below, linux forms of slashes will be used for file names. We assume you are savvy enough to translate into your local machine's system.

## Basic setup

A raspberry pi is a small ( 4 inch by 3 inch ) Linux computer with video output, sound output, ethernet, USB, flash storage. The version we are using ( Pi 3 ) also has Wifi and Bluetooth.

It's better to use a fresh install of your Raspberry Pi operating system, we're then going to install a set of system packages via Ansible.

Please see the file raspberry.md in the root directory to get your RPi up to the starting point we'll use.

You will need a computer, typically some form of laptop or PC. That computer run Ansible, which is a system for managing remote systems. This is called the "local computer" in the scripts below.

## A quick note about IP addresses and names

The following discussion talks about IP addresses. However, your network may use multicast DNS ( my pi is `pi3.citrusleaf.local` when it is at work), or you may decide to edit your `/etc/hosts` file to map the name to an address.
If you want to do this and know what you're doing, power to you.


## HOW USE ANSIBLE ON YOUR WORKSTATION TO CONFIGURE A RASBERRY-PI

1. Ansible needs to be installed on your local computer. If your workstation is running Ubuntu, one needs to
    ```bash
    sudo apt-get install ansible
    ```
    if you are using a different OS, please look at [the documentation]( http://docs.ansible.com/ansible/intro_installation.html#installing-the-control-machine)

    With a Mac, it is common to use `brew` to install packages like ansible.
    ```bash
    brew install ansible
    ```

2. If you are using your RPi with a monitor and keyboard, ensure that your raspberry-pi is running an ssh server, which is should do after the basic setup steps. On the raspberry pi do
    ```bash
    sudo service ssh status | grep [r]unning
    ```
    you should get back a like that looks like:
    ```bash
    Active: active (running) since $DATESTAMP; $DAYCOUNT days $HOURCOUNTh ago
    ```
    if you don't, try running
    ```bash
    sudo service ssh start
    ```
    and check the ssh status again when it is complete.

3. Find the IP address for your Raspberry pi. 
   It will be the output of
    ```bash
    ifconfig eth0 | grep 'inet addr:' | awk -F'[: ]+' '{print $4}'

4. Make sure the hosts in  `ansible\hosts` file in the repo match the hosts you want to control
	The `ansible\hosts` file should have the names of the hosts you wish to control.
	The checked in version should be the names of the hosts we are using on the production system.
	Therefore, you may need to comment out ( prepend with `#` ) the production hosts, and add the
	host you are using on your network.

## HOW TO USE ANSIBLE ON A RASPBERRY PI TO CONFIGURE THAT RASPBERRYPI

1. Install pip and Ansible. Starting with the system default version of Python, you can get ansible by:
```bash
sudo easy_install pip
sudo pip install ansible
```

2. Cd into the `ansible` directory in the project and run

```bash
ansible-playbook -i "localhost," -c local setup_hostfile.yml
ansible-playbook package_installs.yml
```

## HOW TO RUN ANSIBLE TO CONFIGURE A RPI

1. Make sure you have a public key generated. You probably do, which is if you `ls ~/.ssh` you will see an `id_rsa.pub`.
	If you don't have a public key, use these instructions to create one, but you don't have to add your public
	key to your github account ( although you should! )
	[Here's a link from github to help set up the keys!](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)<br><br>

2. Add your public keys to the PI so all other commands will succeed, using ansible.
	From your local computers's MagnusFlora project folder, run
   ```bash
   pushd ansible
   ansible-playbook manage_authorized_keys.yml
   ```
   this will ask for the password for the ```pi``` user on the raspberry pi

   ```bash
   ansible-playbook package_installs.yml
   popd
   ```
   this should NOT ask for your password.

3. Set up the entire set of applications
	Todo:
   ```bash
   ansible-playbook web_flower_install.yml
   ```
   this will install, configure and start the flask application and supervisor jobs which manage celery. Still in progress right now.
   
   
## HOW TO MAKE A CELERY TASK
1. Install required packages
	If you have run the Ansible tasks, this should be complete. If this hasn't worked yet, while in the root project dircectory do
   ```bash
   sudo apt-get install redis
   sudo pip install -r flask/requirements.txt
   ```
1. Configure your application
<br>copy the ```app``` portion of ```flask\dummy_task.py``` into your new python file.
1. Write a function which carries out a task
   * can take an object as an argument, but should not be defined on a class
   * can return values, if needed
   * can call other tasks
1. Add the ```@app.task``` decorator to the function<br>
		you probably don't need to add arguments, to the decorator but can

1. Run the celery worker locally
   ```bash
   celery -A $MODULE_NAME worker -B --loglevel=INFO
   ```
   where $MODULE_NAME is 'dummy_task' for the tasks defined in dummy_task.py
		
1. Add the command to start workers to a Supervisor job
   * currently: Edit or add a file in the /etc/supervisor/conf.d directory
   * soon: 
      * Edit or add a file in the ```ansible/files/flask``` directory
      * run ```ansible-playbook -i hosts celery_tasks.yml```
## Group tasks related to I/O with a specific device types into modules
TODO

## Add a Flask endpoint to interact with I/O tasks
TODO

## Confirm software is running as expected
todo
