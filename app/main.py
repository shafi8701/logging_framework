import uuid
import time
from logging_framework import get_request_logger

def run_test():
    logger = get_request_logger(str(uuid.uuid4()))

    for i in range(200):
        logger.info(
            "Processing record",
            extra={"iteration": i, "test": "rotation"}
        )

        if i % 50 == 0:
            try:
                1 / 0
            except Exception:
                logger.exception("Test exception")

        time.sleep(0.01)

    logger.warning("Test completed")


if __name__ == "__main__":
    run_test()