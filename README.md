# RDManager
## About
RustDesk "address book" for Free and Self-Hosted users
This program is just a simple id/password database, allowing you to organize the terminals by customer organization

## Install
- Execute the following commands:
```
$ git clone https://github.com/rdxdt/rdmanager.git
cd rdmanager
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```
- Now edit config.py with your database settings
- Execute the following commands to create the database 
```
$ flask shell
>>> from rdmanager import db
>>> import bestmanager.models
>>> db.create_all()
>>> exit()
```
If everything is correct no error will come from this last step.
- Now create a service unit to automatically start the gunicorn server that will serve our application
For systemd distros: create the file /etc/systemd/system/rdmanager.service
```
[Unit]
Description= RDManager Application
[Service]
WorkingDirectory=/path/to/rdmanager
User=REPLACE_WITH_YOUR_USER
ExecStart=/path/to/rdmanager/.venv/bin/gunicorn --bind=0.0.0.0 -w 3 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
Now execute
```
# systemctl daemon-reload
# systemctl enable rdmanager
# systemctl start rdmanager
```
It is not a good idea to leave Gunicorn facing the internet, so configure a reverse proxy and firewall rules accordingly.

## Todo
- Page to create the first user of the system 
- Test the application
- API for possible integration
- Use dotenv instead of hardcoding configurations on config.py