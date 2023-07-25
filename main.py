import logging
from src.server import Server

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s][%(filename)s] %(message)s',
                    datefmt='%b/%d/%Y-%H:%M:%S')
logger = logging.getLogger(__name__)


def info():
    logger.info("AntaresViewer 2023@Suto-Commune")


if __name__ == "__main__":
    info()
    server = Server()
    server.launcher()
