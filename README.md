# Sysmonitor

Undergoing heavy development.

### Virtual Environment Setup
```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

### Database Initialisation
```python
from core.db import init_db
init_db()
```

Until a docker compose file is created, you can spin up a local MySQL dev database using:
```
docker run --name mysql -e MYSQL_ROOT_PASSWORD=password -p3306:3306 -d mysql
```

### Configuration
Copy `sample.config.json` to `sysmon.config.json` and adjust accordingly.

If using MySQL docker container from above, replace `username` in `config.json` with `root` and set the password accordingly.

### Creating a User for Development
You'll need to create an initial user to get started with development until the installer is made.

```python
from core.model.user import User
User.add('username', 'Display Name', 'mail@example.com', 'password')
```

### Start the Development UI Server
If working on the Flask UI, the development server can be started with:
```
python3 dev_ui.py
```
