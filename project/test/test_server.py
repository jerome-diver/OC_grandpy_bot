"""Test Flask server operational ability"""

from flask_testing import LiveServerTestCase
from urllib.request import urlopen


class TestServer(LiveServerTestCase):
    """Test Flask server WSGI operational"""

    def create_app(self):
        """Test app"""

        from project.views import app
        app.config.from_object('config.TestingConfig')
        return app

    def test_up_and_running(self):
        """Server is up and running"""

        response = urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)
