import logging
import json

from peewee import DatabaseError

from SwobBackendPublisher.schemas.wallets import Wallets
from SwobBackendPublisher.security.data import Data

from SwobBackendPublisher.exceptions import GrantDoesNotExist

logger = logging.getLogger(__name__)

class GrantModel:
    def __init__(self) -> None:
        self.Wallets = Wallets
        self.Data = Data

    def decrypt(self, platform_name: str, grant, refresh: bool = False) -> dict:
        """
        """
        platformName = platform_name.lower()

        logger.debug("decrypting %s grant ..." % platformName)

        data = self.Data()

        iv = grant.iv
        username = data.decrypt(data=grant.username, iv=iv)
        token = data.decrypt(data=grant.token, iv=iv)
        uniqueId = data.decrypt(data=grant.uniqueId, iv=iv)

        decrypted_grant = {
            "username":json.loads(username) if username else username,
            "token":json.loads(token),
            "uniqueId":json.loads(uniqueId)
        }

        logger.info("- Successfully decrypted %s grant" % platformName)

        return decrypted_grant
        
    def find(self, user_id: str, platform_id: int) -> object:
        """
        """
        try:
            logger.debug("Finding grant user_id:%s, platform_id:%d ..." % (user_id, platform_id))

            grant = self.Wallets.get(self.Wallets.userId == user_id, self.Wallets.platformId == platform_id)

            logger.info("- Successfully found grant")

            return grant

        except self.Wallets.DoesNotExist:
            reason = "Grant for user_id:%s, platform_id:%d not found" % (user_id, platform_id)
            logger.error(reason)
            raise GrantDoesNotExist(reason)

        except DatabaseError as error:
            raise error