import time
import logging

# You can configure this logger as needed
logger = logging.getLogger(__name__)

class RequestTimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # ========= BEFORE VIEW LOGIC (pre-processing) =========
        start_time = time.time()

        # Process the request
        response = self.get_response(request)

        # ========= AFTER VIEW LOGIC (post-processing) =========
        end_time = time.time()
        duration = end_time - start_time

        logger.info(f"{request.method} {request.get_full_path()} took {duration:.3f} seconds")

        # Optional: add the duration to the response header
        response["X-Response-Time"] = f"{duration:.3f}s"

        return response
