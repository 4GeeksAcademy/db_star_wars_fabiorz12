import os
from flask_admin import Admin
from models import db, User, Character, Planet, Favorite  # 👈 importa todos los modelos
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Agregar modelos al panel de administración
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))  # 👈 personajes
    admin.add_view(ModelView(Planet, db.session))     # 👈 planetas
    admin.add_view(ModelView(Favorite, db.session))   # 👈 favoritos