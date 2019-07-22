"""Test Flask views.py project module and his routes provide templates"""

from flask_testing import TestCase


class TestViews(TestCase):
    """Test views module"""

    render_templates = False

    def create_app(selfself):
        """Test app"""

        from project.views import app
        app.config['TESTING'] = True
        return app

    def test_index_template(self):
        """test render index and / template"""

        response = self.client.get("/")
        assert response.status_code == 200
        self.assert_template_used('index.html')
