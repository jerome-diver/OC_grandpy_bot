"""Test Flask views.py project module and his routes provide templates"""

from flask_testing import TestCase
from flask import url_for, render_template, Markup
from _pytest.monkeypatch import MonkeyPatch
import pytest

from project.models import BotSpeach


@pytest.fixture(scope="class")
def monkeypatch_for_class(request):
    """I use monkeypatch self fixture variable
    for class test methods API"""

    request.cls._monkeypatch = MonkeyPatch()


@pytest.mark.usefixtures("monkeypatch_for_class")
class TestViews(TestCase):
    """Test views API class"""

    render_templates = False
    BOT = BotSpeach()

    def create_app(self):
        """Test app for TESTING with Flask_testing TestCase mixin"""

        from project.views import app
        app.config['TESTING'] = True
        return app

    def analyze(type, *args):
        """mock return a str for what ever need"""

        return str

    def analyze_ok(self):
        """mock return "OK" for what ever need"""

        return 'OK'

    def find_something(self):
        """mock Analyzer.find_something for one thing found"""

        return 1

    def find_many_things(self):
        """mock Analyzer.find_something for find many things"""

        return 2

    def find_nothing(self):
        """mock Analyzer.find_something for find nothing back"""

        return 0

    def test_index_template(self):
        """test render index and / template"""

        response = self.client.get("/")
        assert response.status_code == 200
        self.assert_template_used('index.html')

    def test_submit(self):
        """test render json after post http request
        from ajax call form submit
        and mock Analyzer class methods"""

        from uuid import uuid4
        from project.analyzer import Analyzer
        self._monkeypatch.setattr(Analyzer, "find_something",
                                  self.find_many_things)
        self._monkeypatch.setattr(Analyzer, "title", self.analyze_ok())
        self._monkeypatch.setattr(Analyzer, "answer", self.analyze_ok())
        self._monkeypatch.setattr(Analyzer, "ask", self.analyze('null'))
        # get a response from POST on /submit url
        response = self.client.post( url_for("submit"),
                                     data={'question': 'try',
                                           'type': 'question',
                                           'index': 0})
        self.assertEqual(response.json,  dict(question='try',
                                              answer='OK',
                                              found=2,
                                              messages='',
                                              title='OK'))
        self.assert_template_used('messages.html')
        self.assert_context('alert', 'alert-success')
        """ TEST AJAX call request.form['type'] = 'answer'
            and find something
        """
        self._monkeypatch.setattr(Analyzer, "find_something", self.find_something)
        self._monkeypatch.setattr(Analyzer, "resume", self.analyze_ok())
        self._monkeypatch.setattr(Analyzer, "latitude", self.analyze_ok())
        self._monkeypatch.setattr(Analyzer, "longitude", self.analyze_ok())
        self._monkeypatch.setattr(Analyzer, "address", self.analyze_ok())
        response = self.client.post( url_for("submit"),
                                     data={'question': 'try',
                                           'type': 'answer',
                                           'index': str(uuid4())})
        self.assertEqual(response.json, dict(question='try',
                                             answer='OK',
                                             found=1,
                                             messages='',
                                             title='OK',
                                             address='OK',
                                             latitude='OK',
                                             longitude='OK',
                                             map_id='OK',
                                             resume='OK'))
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
        self._monkeypatch.setattr(Analyzer, "find_something", self.find_nothing)
        response = self.client.post( url_for("submit"),
                                     data={'question': 'nothing found',
                                           'type': 'question',
                                           'index': 0})
        result = TestViews.BOT.answer("last", 'nothing')
        self.assertEqual(response.json, dict(answer=False,
                                             found=0,
                                             messages='',
                                             result=result))
        self.assert_template_used('messages.html')
        self.assert_context('alert', 'alert-warning')

    def test_map_coordinates(self):
        """Test render json data with map_id, latitude, longitude and
        address linked with coordinates for GoogleMap object for AJAX
        call"""

        def analyze_ok(self):
            """Mock function for Analyze methods"""

            return 'OK'

        from project.analyzer import Analyzer
        self._monkeypatch.setattr(Analyzer, "map_id", analyze_ok(0))
        self._monkeypatch.setattr(Analyzer, "latitude", analyze_ok(0))
        self._monkeypatch.setattr(Analyzer, "longitude", analyze_ok(0))
        self._monkeypatch.setattr(Analyzer, "address", analyze_ok(0))

        response = self.client.get( url_for("map_coordinates") )
        self.assertEqual(response.json, dict(address='OK',
                                             latitude='OK',
                                             longitude='OK',
                                             map_id='OK'))

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
