import logging

from peewee import DatabaseError

from SwobBackendPublisher.schemas.users import Users
from SwobBackendPublisher.schemas.usersinfo import UsersInfos
from SwobBackendPublisher.schemas.wallets import Wallets

from SwobBackendPublisher.security.data import Data
from SwobBackendPublisher.exceptions import UserDoesNotExist, DuplicateUsersExist

from SwobThirdPartyPlatforms import ImportPlatform, available_platforms

logger = logging.getLogger(__name__)

class UserModel:
    def __init__(self) -> None:
        """
        """
        self.Users = Users
        self.UsersInfos = UsersInfos
        self.Wallets = Wallets
        self.Data = Data

    def find(self, phone_number: str = None, user_id: str = None) -> object:
        """
        """
        try:
            data = self.Data()

            if phone_number:
                phone_number_hash = data.hash(phone_number)

                logger.debug("finding user: %s" % phone_number_hash)

                userinfos = (
                    self.UsersInfos.select()
                    .where(
                        self.UsersInfos.full_phone_number == phone_number_hash,
                        self.UsersInfos.status == "verified"
                    )
                    .dicts()
                )

                # check for no user
                if len(userinfos) < 1:
                    reason = "Invalid Phone Number: %s" % phone_number_hash
                    logger.error(reason)
                    raise UserDoesNotExist(reason)

                # check for duplicate user
                if len(userinfos) > 1:
                    reason = "Duplicate users found with Phone Number: %s" % phone_number_hash
                    logger.error(reason)
                    raise DuplicateUsersExist(reason)

                logger.info("- Successfully found user with Phone Number: %s" % phone_number_hash)

                userId = userinfos[0]["userId"]
                alias = data.decrypt(data=userinfos[0]["name"])

                return {
                    "userId": userId,
                    "alias": alias
                }

            elif user_id:
                logger.debug("finding user: %s" % user_id)

                userinfos = (
                    self.UsersInfos.select()
                    .where(
                        self.UsersInfos.userId == user_id,
                        self.UsersInfos.status == "verified"
                    )
                    .dicts()
                )

                # check for no user
                if len(userinfos) < 1:
                    reason = "Invalid UserId: %s" % user_id
                    logger.error(reason)
                    raise UserDoesNotExist(reason)

                # check for duplicate user
                if len(userinfos) > 1:
                    reason = "Duplicate users found with UserId: %s" % user_id
                    logger.error(reason)
                    raise DuplicateUsersExist(reason)

                logger.info("- Successfully found user with ID: %s" % user_id)

                user = (
                    self.Users.select(
                        self.Users.createdAt,
                        self.Users.last_login
                    )
                    .where(
                        self.Users.id == userinfos[0]["userId"]
                    )
                    .dicts()
                )

                 # check for no user
                if len(user) < 1:
                    reason = "Invalid UserId: %s" % userinfos[0]["userId"]
                    logger.error(reason)
                    raise UserDoesNotExist(reason)

                # check for duplicate user
                if len(user) > 1:
                    reason = "Duplicate users found with UserId: %s" % userinfos[0]["userId"]
                    logger.error(reason)
                    raise DuplicateUsersExist(reason)

                return {
                    "userinfo": userinfos[0],
                    "createdAt": user[0]["createdAt"],
                    "last_login": user[0]["last_login"]
                }

        except DatabaseError as error:
            raise error

    def find_platform(self, user_id: str) -> object:
        """
        """
        try:
            saved_platforms = []

            user_platforms = {
                "unsaved_platforms": [],
                "saved_platforms": []
            }

            logger.debug("Fetching saved platforms for %s ..." % user_id)

            saved_wallet_platform = (
                self.Wallets.select()
                .where(
                    self.Wallets.userId == user_id
                )
                .dicts()
            )

            for row in saved_wallet_platform:
                saved_platforms.append(row["platformId"])

                Platform = ImportPlatform(platform_name = row["platformId"])
                platform_info = Platform.info

                result = {
                    "name": platform_info["name"].lower(),
                    "description": platform_info["description"],
                    "logo": platform_info["logo"],
                    "initialization_url": f"/platforms/{platform_info['name']}/protocols/{platform_info['protocols'][0]}",
                    "type": platform_info["type"],
                    "letter": platform_info["letter"]
                }

                user_platforms["saved_platforms"].append(result)

            logger.debug("Fetching unsaved platforms for %s ..." % user_id)
            
            for platform in available_platforms:
                if platform not in saved_platforms:
                    Platform = ImportPlatform(platform_name = platform)
                    platform_info = Platform.info

                    result = {
                        "name": platform_info["name"].lower(),
                        "description": platform_info["description"],
                        "logo": platform_info["logo"],
                        "initialization_url": f"/platforms/{platform_info['name']}/protocols/{platform_info['protocols'][0]}",
                        "type": platform_info["type"],
                        "letter": platform_info["letter"]
                    }

                    user_platforms["unsaved_platforms"].append(result)
        
            logger.info("- Successfully Fetched users platforms")

            return user_platforms

        except DatabaseError as error:
            raise error

    def verify(self, password: str, user_id: str = None) -> str:
        """
        """
        try:
            data = self.Data()
            password_hash = data.hash(password)

            logger.debug("Verifying user: %s" % user_id)

            userinfos = (
                self.UsersInfos.select()
                .where(
                    self.UsersInfos.userId == user_id,
                    self.UsersInfos.status == "verified"
                )
                .dicts()
            )

            # check for no user
            if len(userinfos) < 1:
                reason = "Invalid User Id: '%s'" % user_id
                logger.error(reason)
                raise UserDoesNotExist(reason)

            # check for duplicate user
            if len(userinfos) > 1:
                reason = "Duplicate users found with UserId: %s" % user_id
                logger.error(reason)
                raise DuplicateUsersExist(reason)

            logger.debug("Verifying Password for User with ID: %s" % user_id)

            users = (
                self.Users.select()
                .where(
                    self.Users.id == userinfos[0]["userId"],
                    self.Users.password == password_hash
                )
                .dicts()
            )

            # check for no user
            if len(users) < 1:
                reason = "Invalid password for users with UserId: %s" % userinfos[0]["userId"]
                logger.error(reason)
                raise UserDoesNotExist(reason)

            # check for duplicate user
            if len(users) > 1:
                reason = "Duplicate users found with UserId: %s" % userinfos[0]["userId"]
                logger.error(reason)
                raise DuplicateUsersExist(reason)

            logger.info("- Successfully found User with UserID: %s" % userinfos[0]["userId"])

            return str(userinfos[0]["full_phone_number"])

        except DatabaseError as error:
            raise error