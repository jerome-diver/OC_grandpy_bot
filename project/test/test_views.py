"""Test Flask views.py project module and his routes provide templates"""

from flask_testing import TestCase
from flask import json, url_for


class TestViews(TestCase):
    """Test views module"""

    render_templates = False

    def create_app(self):
        """Test app"""

        from project.views import app
        app.config['TESTING'] = True
        return app

    def test_index_template(self):
        """test render index and / template"""

        response = self.client.get("/")
        assert response.status_code == 200
        self.assert_template_used('index.html')

    def test_submit(self):
        """test render json after post http request
        from ajax call form submit"""

        tests = [
            dict(assert_k="answer",
                 assert_v='',
                 assert_t=False,
                 data=dict([('question', 'pizza')])),
            dict(assert_k="ERROR",
                 assert_v='missing question',
                 assert_t=True,
                 data=dict([('question','')]))]
        for req in tests:
            response = self.client.post(
                url_for("question"),
                data=req["data"])
            assert response.status_code == 200
            assert response.json[req["assert_k"]] == req["assert_v"] \
                if req["assert_t"] \
                else response.json[req["assert_k"]] != req["assert_v"]

    def test_map_coordinates(self):
        """Test render json data with map_id, latitude, longitude and
        address linked with coorinates for GoogleMap object for AJAX
        call"""

        pass

    def user_said(self):
        """Test render html template 'user_said.html' with question,
        time, localtime for AJAX call"""

        pass

    def test_bot_said(self):
        """Test render html template 'bot_said.html' with map_id, answer,
        localtime, time from AJAX call"""

        pass
