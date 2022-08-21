### This is a basic checkout API server built with FastAPI and MySQL. <br/>
You can:
- add/remove products to cart
- checkout items 
- view you orders

Not implemented functionalities:
- Login/Logout, (that is, no user session)
- Payment service
- Create new users
<br/>

# Prerequisites
python, Docker
<br/>

# Setup
```
# Start virtual environment for Python
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

# Start MySQL
docker-compose up

```

# Start Command

`python -m uvicorn app.app`<br/>
or for dev environment, run:<br/>
`python -m uvicorn app.app --reload`

## Connection to MySQL
`mysql -h 127.0.0.1 -P 3307 -u root -p` <br/>
(password is root for easy testing, DO NOT store sensitive data)
<br/><br/>

# API Documents
Utilizes OpenAPI, you can also run the APIs from below url.<br/>
`localhost:8000/docs#`