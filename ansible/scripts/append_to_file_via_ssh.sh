ssh $1 "if [ ! -d ~/.ssh ]; then mkdir ~/.ssh; fi; echo \"$(cat ~/.ssh/id_rsa.pub)\" >> ~/.ssh/authorized_keys"
