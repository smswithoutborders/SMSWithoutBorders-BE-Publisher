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

    def __init__(self, db) -> None:
        """
        """
        self.__configure(db)

    def decrypt(self, phone_number: str, platform_name: str) -> dict:
        """
        """
        from SwobBackendPublisher.models.grants import GrantModel
        from SwobBackendPublisher.models.platforms import PlatformModel
        from SwobBackendPublisher.models.users import UserModel

        try:
            User = UserModel()
            Grant = GrantModel()
            Platform = PlatformModel()
        
            user = User.find(phone_number=phone_number)
            platform = Platform.find(platform_name=platform_name)
            
            try:
                grant = Grant.find(user_id=user["userId"], platform_id=platform.id)
                d_grant = Grant.decrypt(platform_name=platform.name, grant=grant, refresh=True)
            except GrantDoesNotExist:
                d_grant = []

            return d_grant
        
        except (
            UserDoesNotExist, 
            DuplicateUsersExist,
            PlatformDoesNotExist,
            InvalidDataError
            ) as error:
            raise error from None
                    
        except Exception as error:
            logger.exception(error)
            raise error

    def whoami(self, phone_number: str) -> dict:
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

    def whichplatform(self, platform_letter: str) -> dict:
        """
        """
        from SwobBackendPublisher.models.platforms import PlatformModel

        try:
            Platform = PlatformModel()

            platform = Platform.find(platform_letter=platform_letter)

            return {
                "platform_name": platform.name
            }

        except PlatformDoesNotExist as error:
            raise error from None

        except Exception as error:
            logger.exception(error)
            raise error

    def myplatforms(self, user_id: str) -> dict:
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