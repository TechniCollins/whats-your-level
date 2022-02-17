## Databse setup


### 1. Install PostgreSQL

    sudo apt update

    sudo apt install postgresql postgresql-contrib


### 2. Create DB

    sudo -i -u postgres psql

    CREATE USER username WITH ENCRYPTED PASSWORD 'password';

    CREATE DATABASE levels OWNER username;


### 3. Configure remote access

    SHOW config_file;

    SHOW hba_file;

    \q

    nano  /etc/postgresql/12/main/postgresql.conf (path to config file)


Set `listen address` to `*` in config file


    nano /etc/postgresql/12/main/pg_hba.conf (path to pg_hba file)


Append to the end of file;

host    all             all              0.0.0.0/0                       md5
host    all             all              ::/0                            md5


    sudo ufw allow 5432


### 4. Restart postgres

    service postgresql restart


## Building the App

### 1. Get Project files

    git clone https://github.com/TechniCollins/whats-your-level.git


### 2. Environment variables

    cd whats-your-level
    
    nano .env

Copy paste the contents of .env.sample and edit accordingly.


### 3. NGINX

    nano nginx/conf/nginx.conf


Copy paste the contents of nginx.conf.sample and replace all occurrences of `yourdomain.com` with your domain.


### 4. Build image and run container
    
    docker-compose up --build -d


### 5. SSH KEYS

    docker-compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d yourdomain.com

    docker-compose down

    nano nginx/conf/nginx.conf


Uncomment the second server block and save file

    docker-compose up --build -d


### 6. Initializing Database

    docker-compose exec web python manage.py migrate

    docker-compose exec web python manage.py loaddata levels music


## Connect to Twitter
    
    docker-compose exec web python manage.py webhooks register --url https://yourdomain.com/api/activity
    
    curl https://yourdomain.com/twitter-auth/?authenticate

Follow the link returned and give the app permissions.
