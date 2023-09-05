# Docker-Django-Base

This is a template for a Django Project that will run in a Docker environment

Guidance on how to build for both local development and production (Amazon AWS EC2) below.

## Deploying Locally

### Step 1. Clone repo

```bash
git clone git@github.com:rtreharne/docker-django-base.git
```

If you need to configure your ssh key then read <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account" target="_blank">this</a>.

Also, for testing locally:
```bash
cp env.sample .env
```

### Step 2 - Install Docker

Linux (Ubbuntu 22.04):

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04

Windows:

https://statswork.wiki/docker-for-windows/install-windows-home/f

### Step 3 - Build image and run in container locally

```bash
docker-compose build app
```

```bash
docker-compose up
```
To check open up http://127.0.0.1:8000/

### Step 4 - Create a superuser
```bash
docker-compose run --user root --rm app sh -c "python manage.py createsuperuser"
```
Run `docker-compose up app` again to re-start local server.

### Step 5 - Configure application

Watch this video on how to configure application for first use:

https://liverpool.instructuremedia.com/embed/f4c28100-c6ab-4e3a-8bc6-38d0229e2015

Here is the Canvas Community Guide on how to manage/create API tokens:

https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89

### Step 5 - Run scheduler

```bash
docker-compose run -d --rm app sh -c "celery -A app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"
```


## Deploying to AWS EC2 

### Step 1. Clone Repo

Clone this repo and push to new GitHub repository.

Create a new AWS EC2 instance.

For guidance on configuring ssh keys and security groups for the app please refer to: https://youtu.be/mScd-Pc_pX0?t=7311

SSH into your instance using
```bash
ssh ec2-user@<Public IPv4 DNS Address>
```

Install git
```bash
sudo yum install git
```

Install docker
```bash
sudo amazon-linux-extras install docker -y
```

Enable Docker and start
```bash
sudo systemctl enable docker.service && sudo systemctl start docker.service
```

Add user to group
```bash
sudo usermod -aG docker ec2-user
```

Install Docker-Compose
(https://docs.docker.com/compose/install/other/)
```bash
sudo curl -SL https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
```

Apply executable permissions
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

Logout of server using `exit` and ssh back in. You need to do this to make sure the group permissions are applied.

Setup Github deploy key (assuming public repository). Create public key. Press enter when prompted for file save and don't set passphrase.

```bash
ssh-keygen -t ed25519 -b 4096
```

```bash
cat ~/.ssh/id_ed25519.pub
```

Go to your GitHub repo's Settings/Deploy keys. Create a new deploy key and copy contents of .pub file to "Key" box. Don't allow write access.


Clone the repo using the SSH URL.
```bash
git clone git@github.com:rtreharne/django-docker-compose-deployment.git
```

cd into the project directory.

Create your .env file.
```bash
cp env.sample .env
```

vi into the file and set your env parameters. Make sure they're different from those in env.sample. You can generate a Django secret key using https://djecrety.ir/

Make sure you set `ALLOWED_HOSTS` to the IPv4 URL.

Build and deploy.


```bash
docker-compose -f docker-compose-deploy.yml build
```

Create admin superuser
```bash
docker-compose -f docker-compose-deploy.yml run --user root --rm app sh -c "python manage.py createsuperuser"
```

Start the container (use -d flag at end to run in background).
```bash
docker-compose -f docker-compose-deploy.yml up -d
```

Start the scheduler
```bash
docker-compose run -d --rm app sh -c "celery -A app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"
```

If you want to stop the container.
```bash
docker-compose -f docker-compose-deploy.yml down
```

In case you want to force stop ALL containers:
```bash
docker stop $(docker ps -a -q)
```

In case you want to force stop and remove all containers (warning, will remove db):
```bash
docker rm $(docker ps -a -q)
```




