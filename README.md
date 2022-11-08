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
$ pip install git+https://github.com/smswithoutborders/SMSWithoutBorders-BE-Publisher.git#egg=SwobBackendPublisher
```

## Usage

### decrypt

```python
from SwobBackendPublisher import MySQL, Lib
from SwobBackendPublisher.exceptions import (
    PlatformDoesNotExist,
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

    result = SBPLib.decrypt(phone_number="+xxxxxxxxxxxx", platform_name="gmail")

    print(result)

except (UserDoesNotExist, DuplicateUsersExist, PlatformDoesNotExist, InvalidDataError) as error:
    # Handle exception ...

except Exception as error:
    # Handle exception here ...
```

result

```json
{ "username": "", "token": {} }
```

### whoami

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

    result = SBPLib.whoami(phone_number="+xxxxxxxxxxxx")

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

### whichplatform

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

    result = SBPLib.whichplatform(platform_letter="x")

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

### myplatforms

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

    result = SBPLib.myplatforms(user_id="xxxxxxxxxxxxxx")

    print(result)

except Exception as error:
    # Handle exception here ...
```

result

```json
{ "unsaved_platforms": [], "saved_platforms": [] }
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
