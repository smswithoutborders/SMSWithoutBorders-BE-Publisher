import pytest
import os

phoneNumber = "+237123456789"
userId = "dead3662-5f78-11ed-b8e7-6d06c3aaf3c6"
password = "dummy_password"

from SwobBackendPublisher import Lib, MySQL

@pytest.fixture
def connection():
    """
    """
    db = MySQL.connector(
        database=os.environ["MYSQL_DATABASE"],
        user=os.environ["MYSQL_USER"],
        host=os.environ["MYSQL_HOST"],
        password=os.environ["MYSQL_PASSWORD"]
    )

    SBPLib = Lib(db=db)
    return SBPLib

@pytest.mark.parametrize('platform_name',["gmail", "twitter", "telegram"])
def test_get_grant_from_platform_name(connection, platform_name):
    """
    """
    result = connection.get_grant_from_platform_name(
        phone_number=phoneNumber,
        platform_name=platform_name
    )

    assert isinstance(result, (dict, list))
    print("is %s" % type(result))

    if isinstance(result, dict):
        assert "token" in result
        assert isinstance(result["token"], dict)
        assert "uniqueId" in result
        assert isinstance(result["uniqueId"], str)
        assert "username" in result
        assert isinstance(result["username"], str)
        assert "phoneNumber_hash" in result
        assert isinstance(result["phoneNumber_hash"], str)

def test_get_userid_from_phonenumber(connection):
    """
    """
    result = connection.get_userid_from_phonenumber(
        phone_number=phoneNumber
    )

    assert isinstance(result, dict)
    assert "user_id" in result
    assert result["user_id"] == userId
    assert isinstance(result["user_id"], str)

@pytest.mark.parametrize('platform_letter', ['t','T','g'])
def test_get_platform_name_from_letter(connection, platform_letter):
    """
    """
    expected = None

    if platform_letter == "t":
        expected = "twitter"
    elif platform_letter == "T":
        expected = "telegram"
    elif platform_letter == "g":
        expected = "gmail"

    result = connection.get_platform_name_from_letter(
        platform_letter=platform_letter
    )

    assert isinstance(result, dict)
    assert "platform_name" in result
    assert result["platform_name"] == expected
    assert isinstance(result["platform_name"], str)

def test_get_user_platforms_from_id(connection):
    """
    """
    result = connection.get_user_platforms_from_id(
        user_id=userId
    )

    assert isinstance(result, dict)
    assert "unsaved_platforms" in result
    assert "saved_platforms" in result
    assert isinstance(result["unsaved_platforms"], list)
    assert isinstance(result["saved_platforms"], list)

def test_get_phone_number_hash_from_id(connection):
    """
    """
    result = connection.get_phone_number_hash_from_id(
        user_id=userId,
        password=password
    )

    assert isinstance(result, dict)
    assert "phoneNumber_hash" in result
    assert isinstance(result["phoneNumber_hash"], str)