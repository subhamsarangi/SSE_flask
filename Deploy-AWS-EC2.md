## make EC2 instance create key pair(login). Add security group rule with port 5000.

### Give permission to the downloaded key file
`chmod 400 ec2-key.pem`

## log into the ec2 instance
`ssh -i "ec2-key.pem" ubuntu@<your-instance-hostname>`

something like `ssh -i "your-key.pem" username@ec2-12-34-56-78.ap-south-1.compute.amazonaws.com`


### update ubuntu and install pip
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip -y
```

### create a new user
`sudo adduser subadmin`

### give them admin privileges
`sudo usermod -aG sudo subadmin`

## log into the newly created account
`su — subadmin`

### Create a .ssh directory in the subadmin home directory
`mkdir .ssh`

### Change its permissions (only the owner can read, write, or open the directory) 
`chmod 700 .ssh`

### Create a file named authorized_keys in the .ssh directory
`touch .ssh/authorized_keys`

### change its permissions to 600 (only the owner can read or write to the file)
`chmod 600 .ssh/authorized_keys`

### Open the authorized_keys file
`sudo nano .ssh/authorized_keys`

### open another terminal and generate a public key for the newly created account
`ssh-keygen -y -f ec2-key.pem`

### copy the value into the authorized_keys file

## Now the new account can log into EC2 directly
`ssh -i “ec2.pem” lyle@<your-instance-hostname>`


[LINK](https://medium.com/@lyle-okoth/how-to-deploy-a-production-grade-flask-application-to-an-aws-ec2-instance-using-github-actions-fabc8c16f8db)