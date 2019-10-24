"""Test Flask views.py project module and his routes provide templates"""

from flask_testing import TestCase
from flask import jsonify, url_for, request
from _pytest.monkeypatch import MonkeyPatch


class TestViews(TestCase):
    """Test views module"""

    render_templates = False

    def setUp(self):
        """At setup time initialization"""

        self._monkeypatch = MonkeyPatch()

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

        def request_question():
            """Mock 'request.form' AJAX's POST called object
            for a question type"""

            return jsonify({
                'question': "Sais-tu où se trouve le Musée du Louvre ?",
                'type': 'question',
                'index': 0 })

        def request_answer():
            """Mock request.form AJAX's post called object
            for an answer type"""

            return jsonify({
                'question': '',
                'type': 'answer',
                'index': 1 })

        # TEST AJAX call request.form['type'] = 'question'
        self._monkeypatch.setattr(request, "form", request_question)

        response = self.client.post( url_for("submit") )
        assert response.status_code == 200
        print(response)

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
