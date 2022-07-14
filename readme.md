# Personal Blog Portal
## Date of project creation: December 2021
## 1. Description
* Authentification features provided: account activation, register, login, logout, password change
* User can create, update and delete posts wit implemented text editor
* User can modify only his own posts
* Every user can comment all posts, and also can reply to a specific comment
* Every user can like or dislike specific post or he can save it in favorites
* User can create post drafts visible only to him and publish it any time
* User can update profile information, change avatar, change password or delete account
* Dashbord shows all posts sorted by date
* User can display posts by category
* Advanced search functionality with recommendations

## 2. ⚙️ Dev stack
**`Python`**  (v3.8.10)<br />
**`PIP`**  (v21.3.1)<br />
**`Django`**  (v4.0.4)<br />

## 3. Project Setup ##
**install virtual environment**
`sudo pip install virtualenv`

**create virtual environment**
`virtualenv venv`
OR
`virtualenv --python=/usr/bin/python3 venv`

**activate virtual environment**
`source venv/bin/activate`

**install requirements**
`pip install -r requirements.txt`

**django secret key**
* generate django secret key at: https://djecrety.ir/
* paste it in settings.SECRET_KEY

**database info**
* project is configured for PostgreSQL but if you want other databases, configure your settings file and install corresponding database engine
* provide your database credentials in settings.py

**migrate database**
`python manage.py migrate`

**run django server**
`python manage.py runserver`

**registration info**
* account activation or password reset is connected with python console in terminal but you can also provide in settings.py mailtrap or other source credentials to configure your email