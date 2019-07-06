"""
    kession
    ~~~~~~~~~~~~~

    Adds server session support to your application.
"""

__version__ = '0.3.1'

from .sessions import NullSessionInterface, RedisSessionInterface


class Kession(object):
    """This class is used to add Server-side Session to one or more Quart
    applications.
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """This is used to set up session for your app object.

        :param app: the app object with proper configuration.
        """

        app.session_interface = self._get_interface(app)

    def _get_interface(self, app):
        config = app.config.copy()
        config.setdefault('SESSION_TYPE', 'null')
        config.setdefault('SESSION_PERMANENT', True)
        config.setdefault('SESSION_USE_SIGNER', False)
        config.setdefault('SESSION_KEY_PREFIX', 'session:')
        config.setdefault('SESSION_REDIS', None)

        if config['SESSION_TYPE'] == 'redis':
            session_interface = RedisSessionInterface(
                config['SESSION_REDIS'], config['SESSION_KEY_PREFIX'],
                config['SESSION_USE_SIGNER'], config['SESSION_PERMANENT'])
        else:
            session_interface = NullSessionInterface()

        return session_interface
