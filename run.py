"""
Vitesse Control Center

Main entry point.
"""

from src.vcc.logger import get_logger
from src.vcc.tasks import ApplicationTask


def main():

    logger = get_logger()

    logger.info("===================================")
    logger.info("Vitesse Control Center")
    logger.info("===================================")

    ApplicationTask().execute()

    logger.info("")
    logger.info("Done.")


if __name__ == "__main__":
    main()