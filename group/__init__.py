from sheep.api.statics import static_files
from flask import Flask
from config import *

app = Flask(__name__)
app.debug = True
app.config.update(
    SQLALCHEMY_DATABASE_URI = DATABASE_URI,
    SQLALCHEMY_POOL_SIZE = 1000
)

app.jinja_env.filters['s_files'] = static_files
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

from views import *
from models import *

init_db(app)
