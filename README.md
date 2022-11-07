<img src="https://github.com/smswithoutborders/SMSWithoutBorders-Resources/raw/master/multimedia/img/swob_logo_icon.png" align="right" width="350px"/>

# SMSWithoutBorders-BE-Publisher

SMSWithoutBorders Backend Publisher library

## Installation

Please make sure you have Python 3.7 or newer (python --version).

### Create a Virtual Environments

```
python3 -m venv venv
. venv/bin/activate
```

### PyPI

```bash
pip install --upgrade pip wheel
pip install git+https://github.com/smswithoutborders/SMSWithoutBorders-BE-Publisher.git#egg=SwobBackendPublisher
```

## Usage

### decrypt

```python
from SwobBackendPublisher import MySQL, Lib

MYSQL_HOST="my-host"
MYSQL_USER="my-username"
MYSQL_PASSWORD="my-root-password"
MYSQL_DATABASE="my-database"

# Connect to a MySQL database
db = MySQL.connector(
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST
    )

# Initialize SwobBackendPublisher Lib
SBPLib = Lib(db=db)

result = SBPLib.decrypt(phone_number="+xxxxxxxxxxxx", platform_name="gmail")

print(result)
```

result

```json
{ "username": "", "token": {} }
```

### whoami

```python
from SwobBackendPublisher import MySQL, Lib

MYSQL_HOST="my-host"
MYSQL_USER="my-username"
MYSQL_PASSWORD="my-root-password"
MYSQL_DATABASE="my-database"

# Connect to a MySQL database
db = MySQL.connector(
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST
    )

# Initialize SwobBackendPublisher Lib
SBPLib = Lib(db=db)

result = SBPLib.whoami(phone_number="+xxxxxxxxxxxx")

print(result)
```

result

```json
{ "user_id": "" }
```

## Licensing

This project is licensed under the [GNU General Public License v3.0](LICENSE).
