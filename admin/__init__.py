from flask_admin import Admin

admin = Admin()

def init_app(app):
  admin.name = 'Fraldário PMVC'
  admin.template_mode = 'bootstrap4'
  admin.init_app(app)