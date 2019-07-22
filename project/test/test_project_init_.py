"""Pass coverage for test package __ini__.py:
- Flask command init_stopwords
"""

from project import init_stopwords
from project.views import app


def test_init_stop_words():
    """Test of function init_stop_words"""

    runner = app.test_cli_runner()
    result = runner.invoke(init_stopwords)
    assert result.exit_code == 0
    assert result.output == 'INFO :: Database with stop words content ' \
                            'initialized\n'
