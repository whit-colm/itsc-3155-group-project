# Django server & venv info.

## Activating the venv

Linux / macOS:

```bash
source askserver-venv/bin/activate
```

Windows:

```powershell
myworld\Scripts\activate.bat
```

## Installing dependences:

```
pip install django
pip install djangorestframework
``

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