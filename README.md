# Newspaper Agency Project

Django project for managing newspapers and redactors.

### Check it out!

[Deployed to Render](https://newspaper-agency-9ve2.onrender.com/)

````
Test user
login: admin
password: xgaEv^kHyhhbguAS
````

## Installation

Python3 must be already installed

```shell
git clone https://github.com/nyanplague/newspaper-agency
cd newspaper-agency
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
python manage.py migrate
python manage.py manage.py loaddata newspaper_agency_db_data.json
python manage.py runserver
```

## Features
* Authentication for Redactor/User
* Content management
* Managing redactors and topics
* Commenting newspapers

## DB structure
![Db structure](db_structure.png)

