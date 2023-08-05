import os
import requests
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor


def _callback(future):
    """Default callback function."""
    pass


class EvaRequests(object):
    """Asynchronous HTTP Client for Python."""

    def __init__(self, max_workers=os.cpu_count()*2, max_retries=3):
        """Initializes a New HTTP Client.

        :param max_workers: The maximum number of threads that can be used to
            execute the given calls.
        :param max_retries: The maximum number of retries each connection
            should attempt. Note, this applies only to failed DNS lookups, socket
            connections and connection timeouts, never to requests where data has
            made it to the server. By default, Requests does not retry failed
            connections. If you need granular control over the conditions under
            which we retry a request, import urllib3's ``Retry`` class and pass
            that instead.   
        """
        self.s = requests.Session()
        self.s.mount('http', HTTPAdapter(max_retries=max_retries))
        self.pool = ThreadPoolExecutor(max_workers=max_workers)

    def get(self, callback=_callback, *args, **kwargs):
        """Sends a GET request.

        :param callback: Attaches a callable that will be called when the request finishes.
        :param \*args: Optional arguments that ``request`` takes.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        self.pool.submit(self.s.get, *args, **kwargs)\
            .add_done_callback(callback)

    def options(self, callback=_callback, *args, **kwargs):
        """Sends a OPTIONS request.

        :param callback: Attaches a callable that will be called when the request finishes.
        :param \*args: Optional arguments that ``request`` takes.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        self.pool.submit(self.s.options, *args, **kwargs)\
            .add_done_callback(callback)

    def head(self, callback=_callback, *args, **kwargs):
        """Sends a HEAD request.

        :param callback: Attaches a callable that will be called when the request finishes.
        :param \*args: Optional arguments that ``request`` takes.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        self.pool.submit(self.s.head, *args, **kwargs)\
            .add_done_callback(callback)

    def post(self, callback=_callback, *args, **kwargs):
        """Sends a POST request.

        :param callback: Attaches a callable that will be called when the request finishes.
        :param \*args: Optional arguments that ``request`` takes.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        self.pool.submit(self.s.post, *args, **kwargs)\
            .add_done_callback(callback)

    def put(self, callback=_callback, *args, **kwargs):
        """Sends a PUT request.

        :param callback: Attaches a callable that will be called when the request finishes.
        :param \*args: Optional arguments that ``request`` takes.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        self.pool.submit(self.s.put, *args, **kwargs)\
            .add_done_callback(callback)

    def patch(self, callback=_callback, *args, **kwargs):
        """Sends a PATCH request.

        :param callback: Attaches a callable that will be called when the request finishes.
        :param \*args: Optional arguments that ``request`` takes.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        self.pool.submit(self.s.patch, *args, **kwargs)\
            .add_done_callback(callback)

    def delete(self, callback=_callback, *args, **kwargs):
        """Sends a DELETE request.

        :param callback: Attaches a callable that will be called when the request finishes.
        :param \*args: Optional arguments that ``request`` takes.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        """

        self.pool.submit(self.s.delete, *args, **kwargs)\
            .add_done_callback(callback)


r = EvaRequests()
