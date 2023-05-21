import os

SECRET_KEY = "MkwEdUaC-lEEo0ePBxd35ZYeM47LjxUzd1YPWflnz3U0iO7op70bBxNb-1fL7CDzjoI"

CSVFOLDER = "CSV/"

ADMINISTRATEUR_USERNAME = "Administrateur"
ADMINISTRATEUR_PASSWORD = "TIZXSs7eDrfDn47OMrwnX1USyHt3Z1sxTcWnZaKR8NXiUr0"

MAIL_USERNAME = "adm.clubinfomathlposada@gmail.com"
MAIL_PASSWORD = "8N28g2QbAOyI9G5iv1E_FVN55wwpA5xsRpyHZ9NFtHdc_t4"

# Database initialization
if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

staticurl = os.path.join(os.path.dirname(__file__), 'CarteApp/static')
if not os.path.exists(os.path.join(staticurl, CSVFOLDER)):
    os.makedirs(os.path.join(staticurl, CSVFOLDER))