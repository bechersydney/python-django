===== set up new project ====
pip install virtualenv
virtualenv env
note: find the folder contains the env then there were you can activate your virtual env
env\scripts\activate
note: if error in activating run terminal as admin then run this command
{{

''Set-ExecutionPolicy RemoteSigned -Scope LocalMachine''
}}
pip install django
django-admin startproject projectname
cd to projectname
python manage.py run server
note: drag env folder inside projectfolder

==== creating app =====

python manage.py startapp appname
note: do not forget to add the new app in installed apps in settings.py

==== when creating templates please do not forget to add in templates in settings.py
==== when creating static file please do not forget to add in settings
{{
    '''
    STATIC_FILES_DIRS = [
    BASE_DIR / 'static'
    ]
    '''
}}



========WORKING WITH DATABASE AND MODELS===========
python manage.py migrate
after creating model in models.py make sure to run migration
{{
    '''
    python manage.py makemigrations
    python manage.py migrate
    '''
}}
create super users in terminal
{{
    '''
    python manage.py createsuperuser
    '''
}}
to see your created model you need to register to the admin.py(please see admin.py)

==== working on api
-make sure your environment is activated
-pip install djangorestframework
-if some issue in installation use this command
{{
    '''
    python -m pip install djangorestframework
    '''
}}
== to enable front end to access api install this cors header
{{
    '''

    '''
}}


