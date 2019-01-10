# Sysmonitor

Undergoing heavy development.

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
Copy `config.sample.json` to `config.json` and adjust accordingly.

If using MySQL docker container from above, replace `username` in `config.json` with `root` and set the password accordingly.
