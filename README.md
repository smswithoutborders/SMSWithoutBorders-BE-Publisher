<img src="https://github.com/smswithoutborders/SMSWithoutBorders-Resources/raw/master/multimedia/img/swob_logo_icon.png" align="right" width="350px"/>

# SMSWithoutBorders-BE-Publisher

SMSWithoutBorders Backend Publisher library

## Installation

Please make sure you have Python 3.7 or newer (python --version).

### Create a Virtual Environments

```bash
$ python3 -m venv venv
$ . venv/bin/activate
```

### PyPI

```bash
$ pip install --upgrade pip wheel
$ pip install "git+https://github.com/smswithoutborders/SMSWithoutBorders-BE-Publisher.git@main#egg=SwobBackendPublisher"
```

Install upgrades

```bash
$ pip install --force-reinstall "git+https://github.com/smswithoutborders/SMSWithoutBorders-BE-Publisher.git@main#egg=SwobBackendPublisher"
```

### From source

```bash
$ git clone https://github.com/smswithoutborders/SMSWithoutBorders-BE-Publisher.git
$ cd SMSWithoutBorders-BE-Publisher
$ python3 setup.py install
```

## Usage

### Table of Content

---

1. [get_grant_from_platform_name](#get_grant_from_platform_name)
2. [get_userid_from_phonenumber](#get_userid_from_phonenumber)
3. [get_platform_name_from_letter](#get_platform_name_from_letter)
4. [get_user_platforms_from_id](#get_user_platforms_from_id)
5. [get_phone_number_hash_from_id](#get_phone_number_hash_from_id)

---

### get_grant_from_platform_name

```python
from SwobBackendPublisher import MySQL, Lib
from SwobBackendPublisher.exceptions import (
    UserDoesNotExist,
    DuplicateUsersExist,
    InvalidDataError
)

MYSQL_HOST="my-host"
MYSQL_USER="my-username"
MYSQL_PASSWORD="my-root-password"
MYSQL_DATABASE="my-database"

try:
    # Connect to a MySQL database
    db = MySQL.connector(
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST
        )

    # Initialize SwobBackendPublisher Lib
    SBPLib = Lib(db=db)

    result = SBPLib.get_grant_from_platform_name(phone_number="+xxxxxxxxxxxx", platform_name="gmail")

    print(result)

except (UserDoesNotExist, DuplicateUsersExist, InvalidDataError) as error:
    # Handle exception ...

except Exception as error:
    # Handle exception here ...
```

result

```json
{ "username": "", "token": {}, "uniqueId": "", "phoneNumber_hash": "" }
```

### get_userid_from_phonenumber

```python
from SwobBackendPublisher import MySQL, Lib
from SwobBackendPublisher.exceptions import UserDoesNotExist, DuplicateUsersExist

MYSQL_HOST="my-host"
MYSQL_USER="my-username"
MYSQL_PASSWORD="my-root-password"
MYSQL_DATABASE="my-database"

try:
    # Connect to a MySQL database
    db = MySQL.connector(
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST
        )

    # Initialize SwobBackendPublisher Lib
    SBPLib = Lib(db=db)

    result = SBPLib.get_userid_from_phonenumber(phone_number="+xxxxxxxxxxxx")

    print(result)

except (UserDoesNotExist, DuplicateUsersExist) as error:
    # Handle exception ...

except Exception as error:
    # Handle exception here ...
```

result

```json
{ "user_id": "" }
```

### get_platform_name_from_letter

```python
from SwobBackendPublisher import MySQL, Lib
from SwobBackendPublisher.exceptions import PlatformDoesNotExist

MYSQL_HOST="my-host"
MYSQL_USER="my-username"
MYSQL_PASSWORD="my-root-password"
MYSQL_DATABASE="my-database"

try:
    # Connect to a MySQL database
    db = MySQL.connector(
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST
        )

    # Initialize SwobBackendPublisher Lib
    SBPLib = Lib(db=db)

    result = SBPLib.get_platform_name_from_letter(platform_letter="x")

    print(result)

except PlatformDoesNotExist as error:
    # Handle exception ...

except Exception as error:
    # Handle exception here ...
```

result

```json
{ "platform_name": "" }
```

### get_user_platforms_from_id

```python
from SwobBackendPublisher import MySQL, Lib

MYSQL_HOST="my-host"
MYSQL_USER="my-username"
MYSQL_PASSWORD="my-root-password"
MYSQL_DATABASE="my-database"

try:
    # Connect to a MySQL database
    db = MySQL.connector(
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST
        )

    # Initialize SwobBackendPublisher Lib
    SBPLib = Lib(db=db)

    result = SBPLib.get_user_platforms_from_id(user_id="xxxxxxxxxxxxxx")

    print(result)

except Exception as error:
    # Handle exception here ...
```

result

```json
{ "unsaved_platforms": [], "saved_platforms": [] }
```

### get_phone_number_hash_from_id

```python
from SwobBackendPublisher import MySQL, Lib
from SwobBackendPublisher.exceptions import UserDoesNotExist, DuplicateUsersExist

MYSQL_HOST="my-host"
MYSQL_USER="my-username"
MYSQL_PASSWORD="my-root-password"
MYSQL_DATABASE="my-database"

try:
    # Connect to a MySQL database
    db = MySQL.connector(
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            host=MYSQL_HOST
        )

    # Initialize SwobBackendPublisher Lib
    SBPLib = Lib(db=db)

    result = SBPLib.get_phone_number_hash_from_id(user_id="xxxxxxxxxxxxxx", password="password")

    print(result)

except (UserDoesNotExist, DuplicateUsersExist) as error:
    # Handle exception ...

except Exception as error:
    # Handle exception here ...
```

result

```json
{ "phoneNumber_hash": "" }
```

## Exceptions

- **PlatformDoesNotExist**: Exception raised when Platform is not Found.

  _return:_ String

- **UserDoesNotExist**: Exception raised when User is not Found.

  _return:_ String

- **DuplicateUsersExist**: Exception raised when Duplicate Users Exist.

  _return:_ String

- **InvalidDataError**: Exception raised when data mismatch the required format during decryption.

  _return:_ String

## Licensing

This project is licensed under the [GNU General Public License v3.0](LICENSE).
