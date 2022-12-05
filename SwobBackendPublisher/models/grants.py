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

    def decrypt(self, grant, refresh: bool = False) -> dict:
        """
        """
        logger.debug("decrypting grant ...")

        data = self.Data()

        iv = grant.iv
        username = data.decrypt(data=grant.username, iv=iv)
        token = data.decrypt(data=grant.token, iv=iv)
        uniqueId = data.decrypt(data=grant.uniqueId, iv=iv)

        decrypted_grant = {
            "username":username,
            "token":json.loads(token),
            "uniqueId":uniqueId
        }

        logger.info("- Successfully decrypted grant")

        return decrypted_grant
        
    def find(self, user_id: str, platform_id: str) -> object:
        """
        """
        try:
            logger.debug("Finding grant user_id:%s, platform_id:%s ..." % (user_id, platform_id))

            grant = self.Wallets.get(self.Wallets.userId == user_id, self.Wallets.platformId == platform_id)

            logger.info("- Successfully found grant")

            return grant

        except self.Wallets.DoesNotExist:
            reason = "Grant for user_id:%s, platform_id:%s not found" % (user_id, platform_id)
            logger.error(reason)
            raise GrantDoesNotExist(reason)

        except DatabaseError as error:
            raise error