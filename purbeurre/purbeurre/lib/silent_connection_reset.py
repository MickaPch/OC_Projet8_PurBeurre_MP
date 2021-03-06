"""Silent ConnectionResetError: [WinError 10054]"""
# From https://code.djangoproject.com/ticket/21227
import socket
import errno

from django.core.servers.basehttp import ThreadedWSGIServer
from django.test.testcases import QuietWSGIRequestHandler, LiveServerThread


class ConnectionResetErrorSwallowingQuietWSGIRequestHandler(QuietWSGIRequestHandler):
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except socket.error as err:
            if err.errno != errno.WSAECONNRESET:
                raise


class ConnectionResetErrorSwallowingLiveServerThread(LiveServerThread):
    def _create_server(self):
        return ThreadedWSGIServer((self.host, self.port), ConnectionResetErrorSwallowingQuietWSGIRequestHandler, allow_reuse_address=False)
