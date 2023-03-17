# Epic Events: OpenClassRooms-P12
REST API for a small enterprise CRM.

## Installation
### create and enter venv

```
python -m venv env
source env/bin/activate
```

### install dependencies
```
pip install -r requirements.txt
```

### run tests (optional)
```
pytest
```
### create db
Epic Events generates those default credentials: 
* database: ``ocr12``
* user: ``ocr12``
* password: ``ocr12``

You can overwrite those credentials via the environment variables:
* ``OCR_DB_NAME``
* ``OCR_DB_USER``
* ``OCR_DB_PASSWORD``
### initialize db
```
python manage.py migrate
```

By default an admin user is created with credentials:
* username: admin
* password: admin

Three user groups are also created:
* ManagementTeam
* SalesTeam
* SupportTeam

### run the server
```
python manage.py runserver
```

## License
Epic Events OCR-12 is released under the **GNU GPLv3** license.

## Contribution
Please don't.
