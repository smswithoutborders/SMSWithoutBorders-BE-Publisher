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

    def decrypt(self, grant) -> dict:
        """ """
        logger.debug("decrypting grant ...")

        data = self.Data()

        username = data.decrypt(data=grant.username)
        token = data.decrypt(data=grant.token)
        uniqueId = data.decrypt(data=grant.uniqueId)

        decrypted_grant = {
            "username": username,
            "token": json.loads(token),
            "uniqueId": uniqueId,
        }

        logger.info("- Successfully decrypted grant")

        return decrypted_grant

    def update(self, id: str, token: dict) -> None:
        """ """
        logger.debug("updating grant ...")

        data = self.Data()

        upd_wallet = self.Wallets.update(
            token=data.encrypt(data=json.dumps(token)),
        ).where(self.Wallets.id == id)

        upd_wallet.execute()

        logger.info("- Successfully updated grant")

        return None

    def find(self, user_id: str, platform_id: str) -> object:
        """ """
        try:
            logger.debug(
                "Finding grant user_id:%s, platform_id:%s ...", user_id, platform_id
            )

            grant = self.Wallets.get(
                self.Wallets.userId == user_id, self.Wallets.platformId == platform_id
            )

            logger.info("- Successfully found grant")

            return grant

        except self.Wallets.DoesNotExist:
            reason = f"Grant for user_id:{user_id}, platform_id:{platform_id} not found"
            logger.error(reason)
            raise GrantDoesNotExist(reason)

        except DatabaseError as error:
            raise error
