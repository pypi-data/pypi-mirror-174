import time
from google.api_core.exceptions import ServiceUnavailable


def retry_decorator(retries: int = 5, backoff_in_seconds: int = 1):
    ''' Decorator to retry a function on a 503 ServiceUnavailable exception

    This retry decorator uses exponential back off with a default value of 5 retries
    and 1 second for backoff

    Args:
        func (function): the function we wish to use the retry strategy on
        retries (int): optional paramter with the number of retries for the client call
        backoff_in_seconds (int): optional parameter the number of seconds to wait initially

    Returns:
        function: the wrapped function
    '''

    def rd(func):

        def retry(*args, **kwargs):
            for x in range(0, retries):
                try:
                    returned_value = func(*args, **kwargs)
                    break
                except ServiceUnavailable:
                    # exponential backoff
                    sleep = (backoff_in_seconds * 2**x)
                    time.sleep(sleep)

            return returned_value

        return retry

    return rd
