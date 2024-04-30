# Django server & venv info.

## Activating the venv

Linux / macOS:

```bash
source askserver-venv/bin/activate
```

Windows:

```powershell
askserver-venv\bin\Activate.ps1
```

## Installing dependences:

```bash
pip install django
pip install djangorestframework
pip install django-oauth-toolkit
```

### Pip Problems

If you get an error akin to:

```
Traceback (most recent call last):
  File "/home/user/repos/itsc-3155-group-project/server/askserver-venv/bin/pip3", line 5, in <module>
    from pip._internal.cli.main import main
ModuleNotFoundError: No module named 'pip'
```

then run:

```bash
python3 -m ensurepip --upgrade
```

## Running the server

Assuming your current active directtory is this one:

Linux / macOS:

```bash
python3 ./askserver/manage.py runserver
```

Windows:

```powershell
python .\askserver\manage.py runserver
```