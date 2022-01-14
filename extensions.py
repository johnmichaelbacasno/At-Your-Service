from flaskext.mysql import MySQL
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_session import Session

db = MySQL()
bootstrap = Bootstrap()
csrf = CSRFProtect()
session = Session()