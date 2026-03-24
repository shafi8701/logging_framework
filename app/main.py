import uuid
import time
import traceback
from logging_framework import get_request_logger
from logging_framework.log_context import LogContext, set_context, add_to_context

def run_test():
    # -------------------------------
    # Generate unique request ID
    # -------------------------------
    request_id = str(uuid.uuid4())
    print(f"Run ID: {request_id}")

    # -------------------------------
    # Initialize context and logger
    # -------------------------------
    ctx = LogContext(request_id)
    set_context(ctx)  # optional if using global context
    logger = get_request_logger(request_id, ctx)

    # -------------------------------
    # Add initial context info
    # -------------------------------
    add_to_context(request_id, "query", "Test Query")
    add_to_context(request_id, "query_length", 1)
    logger.info("Context initialized")

    # -------------------------------
    # Processing loop (simulate work)
    # -------------------------------
    try:
        for i in range(10):
            logger.info("Processing record", extra={"iteration": i})

            # Simulate an occasional exception
            if i % 5 == 0 and i != 0:
                try:
                    1 / 0
                except Exception:
                    logger.exception("Test exception occurred")

            time.sleep(0.01)

        logger.warning("Processing completed successfully")

    except Exception as e:
        # Catch any unexpected error
        logger.exception(f"Unexpected error: {str(e)}")
        add_to_context(request_id, "error", str(e))
        add_to_context(request_id, "error_trace", traceback.format_exc())

    finally:
        # -------------------------------
        # Always generate summary log
        # -------------------------------
        summary_data = ctx.summary()
        logger.summary(
            "RAG Summary",
            extra={
                "component": "evaluation",
                **summary_data
            }
        )
        print("Summary logged")


if __name__ == "__main__":
    run_test()