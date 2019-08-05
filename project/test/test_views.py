"""Test Flask views.py project module and his routes provide templates"""

from flask_testing import TestCase
from flask import json


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

    def test_question_post_json(self):
        """test render json after post http request from ajax call"""

        response = self.client.post(
            "/question",
            data=json.dumps({'question': "pizza"}),
            content_type='application/json', )
        data = json.loads(response.get_data())
        assert response.status_code == 200
