import uuid
import time
from logging_framework import get_request_logger


#Context class allows to store context parameters when a call is made... Later you can summary in the end as single log line...
from logging_framework.log_context import LogContext, set_context, get_context, add_to_context

def run_test():

    try:

        request_id = str(uuid.uuid4())
        logger = get_request_logger(request_id)
        """
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
        """

        logger.info("Creating the Log Context Object")

        ctx = LogContext(request_id)

        logger.info("Setting context object")

        set_context(ctx)

        logger.info("Adding context object")

        add_to_context("query", "Test Query")
        add_to_context("query_length", 1)

            
        ctx = get_context()
        if ctx is not None:
            summary_data = ctx.summary()
            logger.debug(
                "RAG Summary",
                extra={
                    "component": "evaluation",
                    **summary_data
                }
            )
    
    except Exception as e:
        logger.exception("Unhandled error in run_test(): %s", e)


if __name__ == "__main__":
    run_test()