## Get Project files

    git clone https://github.com/TechniCollins/whats-your-level.git


## Initializing Database

    python manage.py migrate


## Loading Data

This step should be done only on an empty database.

    python manage.py loaddata levels music


## Register Webhook
    
    python manage.py register_webhook https://whatsyourlevel.softlever.com/api/activity
