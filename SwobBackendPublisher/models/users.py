import logging

from peewee import DatabaseError

from SwobBackendPublisher.schemas.users import Users
from SwobBackendPublisher.schemas.usersinfo import UsersInfos

from SwobBackendPublisher.security.data import Data

from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import InternalServerError

UserObject = ()
UserPlatformObject= ()

logger = logging.getLogger(__name__)

class UserModel:
    def __init__(self) -> None:
        """
        """
        self.Users = Users
        self.UsersInfos = UsersInfos
        self.Data = Data

    def find(self, phone_number: str = None, user_id: str = None) -> UserObject:
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
                    logger.error("Invalid Phone number")
                    raise Unauthorized()

                # check for duplicate user
                if len(userinfos) > 1:
                    logger.error("Duplicate verified users found: %s" % phone_number_hash)
                    raise Conflict()

                logger.info("- Successfully found verified user: %s" % phone_number_hash)
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
                    logger.error("Invalid User Id")
                    raise Unauthorized()

                # check for duplicate user
                if len(userinfos) > 1:
                    logger.error("Duplicate verified users found: %s" % user_id)
                    raise Conflict()

                logger.info("- Successfully found verified user: %s" % user_id)

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
                    logger.error("Invalid User Id")
                    raise Unauthorized()

                # check for duplicate user
                if len(user) > 1:
                    logger.error("Duplicate verified users found: %s" % user_id)
                    raise Conflict()

                return {
                    "userinfo": userinfos[0],
                    "createdAt": user[0]["createdAt"],
                    "last_login": user[0]["last_login"]
                }

        except DatabaseError as err:
            logger.error("Failed finding user check logs")
            raise InternalServerError(err)