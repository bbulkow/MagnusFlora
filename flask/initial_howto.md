HOW TO MAKE A CELERY TASK
    INSTALL CELERY
		install redis - already done via ansible on the pis
		celery[redis] - already done via pip on the pis

    CONFIGURE YOUR APP
		use dummy_task.py as a template

    WRITE A FUNCTION
		can take an object as an argument, but should not be defined on a class
		determine if you need to make a return

    ADD THE DECORATOR
		probably don't need to add arguments, but can

	HOW TO RUN A CELERY WORKER LOCALLY
		make as specific of a command as possible
			find the name of the actual executable
		number of wokers
		

	HOW TO START WORKERS WITH A SUPERVISOR JOB
		add a file to the /etc/supervisor/conf.d directory
		celery_task_template.conf

	ADD SUPERVISOR JOB TO ANSIBLE to start the workers on boot




+_+_+_+_+_+_+_+_+_+_
HOW TO RUN ANSIBLE
	generate public key if you don't have one
	ADD public key to file
	have somebody run the key distribution job, or add it manually
	ssh-add your key to /home/pi/.ssh/authorized_keys, if required

	Host file
	  Host Groups
	running locally
