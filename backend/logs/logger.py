import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/atx.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("ATX")

def log(message):
    logger.info(message)
    print(message)
    