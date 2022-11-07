import logging
import json

from peewee import JOIN, DatabaseError

from SwobBackendPublisher.schemas.users import Users
from SwobBackendPublisher.schemas.usersinfo import UsersInfos
from SwobBackendPublisher.schemas.wallets import Wallets
from SwobBackendPublisher.schemas.platforms import Platforms

from SwobBackendPublisher.security.data import Data

from SwobBackendPublisher.exceptions import UserDoesNotExist, DuplicateUsersExist

logger = logging.getLogger(__name__)

class UserModel:
    def __init__(self) -> None:
        """
        """
        self.Users = Users
        self.UsersInfos = UsersInfos
        self.Wallets = Wallets
        self.Platforms = Platforms
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
                
                return userinfos[0]

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
            user_platforms = {
                "unsaved_platforms": [],
                "saved_platforms": []
            }

            logger.debug("Fetching unsaved platforms for %s ..." % user_id)
            
            t2 = (
                self.Wallets.alias("t2").select()
                .where(
                    self.Wallets.alias("t2").userId == user_id
                )
            )

            unsaved_platforms = (
                self.Platforms.select()
                .join(t2, JOIN.LEFT_OUTER, on=(t2.c.platformId == self.Platforms.id))
                .where(
                    t2.c.platformId == None
                )
                .dicts()
            )

            for row in unsaved_platforms:
                result = {
                    "name": row["name"].lower(),
                    "description": json.loads(row["description"]),
                    "logo": row["logo"],
                    "initialization_url": f"/platforms/{row['name']}/protocols/{json.loads(row['protocols'])[0]}",
                    "type": row["type"],
                    "letter": row["letter"]
                }

                user_platforms["unsaved_platforms"].append(result)

            logger.debug("Fetching saved platforms for %s ..." % user_id)

            saved_wallet_platform = (
                self.Wallets.select()
                .where(
                    self.Wallets.userId == user_id
                )
                .dicts()
            )

            for row in saved_wallet_platform:
                saved_platforms = (
                    self.Platforms.select()
                    .where(
                        self.Platforms.id == row["platformId"]
                    )
                    .dicts()
                )

                result = {
                    "name": saved_platforms[0]["name"].lower(),
                    "description": json.loads(saved_platforms[0]["description"]),
                    "logo": saved_platforms[0]["logo"],
                    "initialization_url": f"/platforms/{saved_platforms[0]['name']}/protocols/{json.loads(saved_platforms[0]['protocols'])[0]}",
                    "type": saved_platforms[0]["type"],
                    "letter": saved_platforms[0]["letter"]
                }

                user_platforms["saved_platforms"].append(result)

            logger.info("- Successfully Fetched users platforms")
            return user_platforms

        except DatabaseError as error:
            raise error