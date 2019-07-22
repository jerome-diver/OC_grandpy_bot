"""Package Modules Initialize"""

from . import views
from . import models

from .views import app
models.db.init_app(app)


@app.cli.command("init_stopwords")
def init_stopwords():
    """Flask command to initialize database"""

    models.init_stopwords()
