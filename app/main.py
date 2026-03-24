# main.py
import uuid
import time
import traceback

#These two files must be imported to each file where this needs to be used in downstream... files...
from logging_framework import get_request_logger
from logging_framework.log_context import LogContext, set_context, add_to_context

def run_test():
<<<<<<< HEAD
    
    #This is unique for each user request...
    #Request ID must be passed to downstream flows...
    request_id = str(uuid.uuid4())

    #Creating the context object so that info can be appended as needed in the flow... 
    ctx = LogContext(request_id)
    set_context(request_id, ctx)

    #Pass logger object to downstream flows...
    logger = get_request_logger(request_id, ctx)

    # Add context
    add_to_context(request_id, "query", "Test Query")
    add_to_context(request_id, "query_length", 1)
=======
    # Initialize context for this request
    ctx = LogContext()
    ctx.set_request_id(str(uuid.uuid4()))
    set_context(ctx)

    logger = get_request_logger()  # no args needed

    add_to_context("query", "Test Query")
    add_to_context("query_length", 1)
>>>>>>> 2fa9051 (Version 1)

    try:
        for i in range(10):
            logger.info("Processing record", extra={"iteration": i})
            if i % 5 == 0 and i != 0:
                try:
                    1 / 0
                except Exception:
                    logger.exception("Test exception occurred")
            time.sleep(0.01)

        logger.warning("Processing completed successfully")

    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        add_to_context("error", str(e))
        add_to_context("error_trace", traceback.format_exc())

    finally:
<<<<<<< HEAD
        summary_data = ctx.summary()
        logger.summary(
            "RAG Summary",
            extra={
                "component": "evaluation",
                **summary_data
            }
        )
=======
        logger.summary("RAG Summary", extra={"component": "evaluation"})
        print("Summary logged")
>>>>>>> 2fa9051 (Version 1)

if __name__ == "__main__":
    run_test()
