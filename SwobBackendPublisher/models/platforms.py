import logging

from peewee import DatabaseError

from SwobBackendPublisher.schemas.platforms import Platforms
from SwobBackendPublisher.exceptions import PlatformDoesNotExist

logger = logging.getLogger(__name__)

class PlatformModel:
    def __init__(self) -> None:
        self.Platforms = Platforms

    def find(self, platform_name: str = None, platform_id: str = None, platform_letter: str = None) -> object:
        """
        """
        if platform_id:
            try:
                logger.debug("Finding platform by id '%s' ..." % platform_id)

                platform = self.Platforms.get(self.Platforms.id == platform_id)

                logger.debug("- Successfully found platform with ID '%s'" % platform_id)

                return platform

            except self.Platforms.DoesNotExist:
                reason = "Platform with ID '%s' not found" % platform_id
                logger.error(reason)
                raise PlatformDoesNotExist(reason)

            except DatabaseError as error:
                raise error

        elif platform_name:
            try:
                logger.debug("Finding platform by name '%s' ..." % platform_name)

                platform = self.Platforms.get(self.Platforms.name == platform_name)

                logger.debug("- Successfully found platform with Name '%s'" % platform_name)

                return platform

            except self.Platforms.DoesNotExist:
                reason = "Platform with Name '%s' not found" % platform_name
                logger.error(reason)
                raise PlatformDoesNotExist(reason)

            except DatabaseError as error:
                raise error
        
        elif platform_letter:
            try:
                logger.debug("Finding platform by letter '%s' ..." % platform_letter)

                platforms = (
                    self.Platforms.select()
                )

                result = None

                for platform in platforms:
                    if platform.letter == platform_letter:
                        result = platform

                if result:
                    logger.debug("- Successfully found platform with Letter '%s'" % platform_letter)
                    return result
                
                else:
                    reason = "Platform with letter '%s' not found" % platform_letter
                    logger.error(reason)
                    raise PlatformDoesNotExist(reason)

            except DatabaseError as error:
                raise error