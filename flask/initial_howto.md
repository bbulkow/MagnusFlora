# HOW TO DO STUFF
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
  




## HOW TO ADD A RASBERRY-PI TO ANSIBLE
1. Ansible needs to be installed on your local computer. If your workstation is running Ubuntu, one needs to
    ```bash
    sudo apt-get install ansible
    ```
    if you are using a different OS, please look at [the documentation]( http://docs.ansible.com/ansible/intro_installation.html#installing-the-control-machine)
2. Ensure that your raspberry-pi is running an ssh server. On the raspberry pi do
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
4. Add the Raspberry pi's ip address to the end of the ```ansible\hosts``` file in the repo
5. If you're working on a solo machine, you're done. If you're adding a new node to the project, commit your change and push to github!

## HOW TO RUN ANSIBLE TO CONFIGURE A RPI


1. If you haven't already, add your public key to the ```ansible\authorized_keys``` directory.<br>[Here's a link from github to help set up the keys!](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)<br><br>
2. From your workstation's  root project folder, run
   ```bash
   pushd ansible
   ansible-playbook -i hosts manage_authorized_keys.yml
   ```
   this will ask for the password for the ```pi``` user on the raspberry pi
   ```bash
   ansible-playbook -i hosts package_installs.yml
   popd
   ```
   this should NOT ask for your password.
3. TODO:
   ```bash
   ansible-playbook -i hosts web_flower_install.yml
   ```
   this will install, configure and start the flask application and supervisor jobs which manage celery. Still in progress right now.
   
   
## HOW TO MAKE A CELERY TASK
1. Install required packages
<br>If you have run the Ansible tasks, this should be complete. If this hasn't worked yet, while in the root project dircectory do
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
