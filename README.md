# Myblog
Minimal social website made with flask 

## Run Locally

Clone the project

```bash
    git clone https://github.com/vaisakh23/Myblog.git
```

Create a virtual environment

```bash
    python3 -m venv venv
```
Activate virtual environment
```bash
    source venv/bin/activate
```
Install dependencies

```bash
    pip install -r requirements.txt
```

Export environment

```bash
    export DATABASE_URI = "<your-database-url>"
    export SECRET_KEY = "<your-secret-key>"
    export MAIL_SERVER = "<mail-sever-name>"
    export MAIL_PORT = "<mail-server-port>"  
    export MAIL_USERNAME = "<your-email>"
    export MAIL_PASSWORD = "<your-password>"
    export ADMIN = "<admin-email>"
```

Setup Database

```bash
    flask db init
    flask db migrate -m "<optional-message>"
    flask db upgrade
  
```
Run the Server
```bash
    flask run
```
