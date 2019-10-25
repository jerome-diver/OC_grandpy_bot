"""Test Flask views.py project module and his routes provide templates"""

from flask_testing import TestCase
from flask import url_for, render_template, Markup
from _pytest.monkeypatch import MonkeyPatch
import pytest


@pytest.fixture(scope="class")
def monkeypatch_for_class(request):
    request.cls._monkeypatch = MonkeyPatch()


@pytest.mark.usefixtures("monkeypatch_for_class")
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
        from ajax call form submit
        and mock Analyzer class methods"""

        def analyze(type, *args):

            return str

        def analyze_ok(self):

            return 'OK'

        def find_something(self):

            return 1

        def find_many_things(self):

            return 2

        def find_nothing(self):

            return 0

        """TEST AJAX call request.form['type'] = 'question'
           and found many things 
        """
        from project.analyzer import Analyzer
        self._monkeypatch.setattr(Analyzer, "find_something",
                                  find_many_things)
        self._monkeypatch.setattr(Analyzer, "title", analyze_ok(0))
        self._monkeypatch.setattr(Analyzer, "answer", analyze_ok(0))
        self._monkeypatch.setattr(Analyzer, "ask", analyze('null'))
        # get a response from POST on /submit url
        response = self.client.post( url_for("submit"),
                                     data={'question': 'try',
                                           'type': 'question',
                                           'index': 0})
        self.assertEqual(response.json, dict(question='try',
                                             answer='OK',
                                             found=2,
                                             messages='',
                                             title='OK'
                                             ))
        self.assert_template_used('messages.html')
        self.assert_context('alert', 'alert-success')
        """ TEST AJAX call request.form['type'] = 'answer'
            and find something
        """
        self._monkeypatch.setattr(Analyzer, "find_something",
                                  find_something)
        self._monkeypatch.setattr(Analyzer, "resume", analyze_ok(0))
        self._monkeypatch.setattr(Analyzer, "map_id", analyze_ok(0))
        self._monkeypatch.setattr(Analyzer, "latitude", analyze_ok(0))
        self._monkeypatch.setattr(Analyzer, "longitude", analyze_ok(0))
        self._monkeypatch.setattr(Analyzer, "address", analyze_ok(0))
        response = self.client.post( url_for("submit"),
                                     data={'question': 'try',
                                           'type': 'answer',
                                           'index': 0})
        self.assertEqual(response.json, dict(question='try',
                                             answer='OK',
                                             found=1,
                                             messages='',
                                             title='OK',
                                             address='OK',
                                             latitude='OK',
                                             longitude='OK',
                                             map_id='OK',
                                             resume='OK'
                                             ))
        self.assert_template_used('messages.html')
        self.assert_context('alert', 'alert-success')
        """ TEST AJAX call request.form['question'] is empty
        """
        response = self.client.post( url_for("submit"),
                                     data={'question': '',
                                           'type': 'question',
                                           'index': 0})
        self.assertEqual(response.json, dict(messages='',
                                             ERROR='missing question'))
        self.assert_template_used('messages.html')
        self.assert_context('alert', 'alert-danger')
        """ TEST AJAX request return nothing found"""
        self._monkeypatch.setattr(Analyzer, "find_something", find_nothing)
        response = self.client.post( url_for("submit"),
                                     data={'question': 'nothing found',
                                           'type': 'question',
                                           'index': 0})
        self.assertEqual(response.json, dict(answer=False,
                                             found=0,
                                             messages=''))
        self.assert_template_used('messages.html')
        self.assert_context('alert', 'alert-warning')



    def test_map_coordinates(self):
        """Test render json data with map_id, latitude, longitude and
        address linked with coorinates for GoogleMap object for AJAX
        call"""

        pass

    def test_user_said(self):
        """Test assert template 'user_said.html',
        assert contextual variables
        and JSON answer"""

        response = self.client.post(url_for("user_said"),
                                    data={'question': 'try',
                                          'time': '10:39:00 PM',
                                          'location': 'Asia/Bangkok'})
        self.assertEqual(response.json, dict(
            question=render_template('user_said.html',
                                     question='try',
                                     time='10:39:00 PM',
                                     location='Asia/Bangkok')))
        self.assert_template_used('user_said.html')
        self.assert_context('question', 'try')
        self.assert_context('time', '10:39:00 PM')
        self.assert_context('location', 'Asia/Bangkok')

    def test_bot_said(self):
        """Test assert template 'bot_said.html',
        assert contextual variables
        and JSON answer"""

        response = self.client.post(url_for("bot_said"),
                                    data={'answer': 'OK',
                                          'time': '10:40:00 PM',
                                          'location': 'Asia/Bangkok',
                                          'mapid': 1})
        self.assertEqual(response.json, dict(
            answer=render_template('bot_said.html',
                                   answer=Markup('OK'),
                                   time='10:40:00 PM',
                                   location='Asia/Bangkok',
                                   map_id=1)))
        self.assert_template_used('bot_said.html')
        self.assert_context('answer', 'OK')
        self.assert_context('time', '10:40:00 PM')
        self.assert_context('location', 'Asia/Bangkok')
        self.assert_context('map_id', 1)
