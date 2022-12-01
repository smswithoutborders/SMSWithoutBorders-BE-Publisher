import logging

from SwobBackendPublisher.exceptions import (
    PlatformDoesNotExist,
    UserDoesNotExist,
    DuplicateUsersExist,
    GrantDoesNotExist,
    InvalidDataError
)

logger = logging.getLogger(__name__)

class Lib:
    
    DB = None

    @classmethod
    def __configure(cls, db):
        """
        """
        cls.DB = db

    def __init__(self, db = None) -> None:
        """
        """
        self.__configure(db)

    def get_grant_from_platform_name(self, phone_number: str, platform_name: str) -> dict or list:
        """
        """
        from SwobBackendPublisher.models.grants import GrantModel
        from SwobBackendPublisher.models.users import UserModel
        from SwobBackendPublisher.security.data import Data

        try:
            User = UserModel()
            Grant = GrantModel()
            data = Data()
        
            user = User.find(phone_number=phone_number)

            try:
                grant = Grant.find(user_id=user["userId"], platform_id=platform_name.lower())
                d_grant = Grant.decrypt(grant=grant)
                d_grant["phoneNumber_hash"] = data.hash(phone_number)
            except GrantDoesNotExist:
                d_grant = []

            return d_grant
        
        except (
            UserDoesNotExist, 
            DuplicateUsersExist,
            InvalidDataError
            ) as error:
            raise error from None
                    
        except Exception as error:
            logger.exception(error)
            raise error

        finally:
            self.DB.close()

    def get_userid_from_phonenumber(self, phone_number: str) -> dict:
        """
        """
        from SwobBackendPublisher.models.users import UserModel

        try:
            User = UserModel()

            user = User.find(phone_number=phone_number)

            return {
                "user_id": user["userId"]
            }

        except (UserDoesNotExist, DuplicateUsersExist) as error:
            raise error from None

        except Exception as error:
            logger.exception(error)
            raise error

        finally:
            self.DB.close()

    def get_platform_name_from_letter(self, platform_letter: str) -> dict:
        """
        """
        from SwobThirdPartyPlatforms import ImportPlatform, available_platforms

        try:
            for platform in available_platforms:
                Platform = ImportPlatform(platform_name = platform)
                platform_info = Platform.info

                if platform_letter == platform_info["letter"]:
                    return {
                        "platform_name": platform_info["name"]
                    }
                else:
                    continue
                
            reason = "Platform letter '%s' not found" % platform_letter
            raise PlatformDoesNotExist(reason)

        except PlatformDoesNotExist as error:
            raise error from None

        except Exception as error:
            logger.exception(error)
            raise error

    def get_user_platforms_from_id(self, user_id: str) -> dict:
        """
        """
        from SwobBackendPublisher.models.users import UserModel

        try:
            User = UserModel()

            result = User.find_platform(user_id=user_id)

            return result

        except Exception as error:
            logger.exception(error)
            raise error

        finally:
            self.DB.close()

    def get_phone_number_hash_from_id(self, user_id: str, password: str) -> dict:
        """
        """
        from SwobBackendPublisher.models.users import UserModel

        try:
            User = UserModel()

            phoneNumber_hash = User.verify(password=password, user_id=user_id)

            return {
                "phoneNumber_hash": phoneNumber_hash
            }

        except (UserDoesNotExist, DuplicateUsersExist) as error:
            raise error from None

        except Exception as error:
            logger.exception(error)
            raise error

        finally:
            self.DB.close()

    def hasher(self, data: str, salt: str = None) -> dict:
        """
        """
        from SwobBackendPublisher.security.data import Data

        crypto = Data()

        try:
            result = crypto.hash(data=data, salt=salt)

            return result

        except Exception as error:
            logger.exception(error)
            raise error