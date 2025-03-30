from backend.auth import auth
from backend.dashboard import dashboard
from backend.home import home
from backend.categories import categories
from backend.services import services
from backend.packages import packages
from backend.general import general
from backend.customer import customer
from backend.professional import professional
from backend.admin import admin

def register_apis(app):
    # Register all blueprints here
    app.register_blueprint(home)

    # Register all blueprints here
    app.register_blueprint(auth, url_prefix='/auth')

    # Register the dashboard routes with URL prefix
    app.register_blueprint(dashboard, url_prefix='/dashboard')

    # Register the general routes with URL prefix
    app.register_blueprint(general, url_prefix='/api')

    # Register the customer routes with URL prefix
    app.register_blueprint(customer, url_prefix='/api')

    # Register the professional routes with URL prefix
    app.register_blueprint(professional, url_prefix='/api')

    # Register the admin routes with URL prefix
    app.register_blueprint(admin, url_prefix='/api')

    # Register the services routes with URL prefix
    app.register_blueprint(categories, url_prefix='/api')

    # Register the services routes with URL prefix
    app.register_blueprint(services, url_prefix='/api')

    # Register the packages routes with URL prefix
    app.register_blueprint(packages, url_prefix='/api')
