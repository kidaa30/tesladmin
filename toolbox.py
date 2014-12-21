#!/usr/bin/env python

import sys, os, glob, getpass, shutil
from tinymk import *

try:
    import django
    assert django.VERSION[:2] == (1, 7)
except:
    sys.exit('You need to install Django 1.7')

python = sys.executable
db = 'db.sqlite3'

def check():
    if not os.path.exists('db.sqlite3'):
        sys.exit('You need to run %s init first' % sys.argv[0])

@task()
def init():
    if os.path.exists('db.sqlite3'):
        sys.exit('You already ran %s init!? Delete %s to reinitialize' % (python,
                                                                          db))
    try:
        os.mkdir('static')
    except:
        pass
    run('%s manage.py makemigrations' % python)
    run('%s manage.py migrate' % python)
    run('%s manage.py createsuperuser --username=admin' % python)
    run('nikola init static')
    orig = os.getcwd()
    os.chdir(os.path.join(orig, 'static'))
    try:
        run('nikola build')
    finally:
        os.chdir(orig)
    assert os.path.exists(db), 'ACK!! TIME WENT BACKWARDS AND YOUR HDD EXPLODED!!'

@task()
def change_password():
    check()
    run('%s manage.py changepassword admin' % python)

@task()
def update():
    check()
    if need_to_update(db, glob.glob('manager/*.py')+glob.glob('tesladmin/*.py')):
        run('%s manage.py makemigrations' % python)
        run('%s manage.py migrate' % python)
        # make sure the db gets touched so this won't run indefinitely
        os.utime(db, None)

@task()
def serve():
    check()
    qinvoke('update')
    run('%s manage.py runserver' % python)

@task()
def clean():
    check()
    choice = None
    while choice not in ('y', 'n'):
        choice = (raw_input if sys.version_info.major == 2 else input)\
                 ('Are you sure? (y/N) ').lower()
    if choice == 'n': return
    for f in glob.glob('manager/*.pyc'): os.remove(f)
    for f in glob.glob('tesladmin/*.pyc'): os.remove(f)
    os.remove(db)
    shutil.rmtree('static')

main(default='serve')
