from apiflask import APIFlask
from dotenv import load_dotenv
from api.extensions import *
from .auth.controllers import auth
from .customer.controllers import customer
from .rental.controllers import rental
from .report.controllers import report
from .vehicle.controllers import vehicle
from api.config import config_dict
from os import getenv

# Load environment variables
load_dotenv()


def create_app():
    # Create the application instance
    app = APIFlask(__name__, title="v-rental API", version="1.0.0")

    # Adding application configurations
    app.config.from_object(config_dict[getenv("FLASK_ENV")])

    # Adding application extensions
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(customer)
    app.register_blueprint(rental)
    app.register_blueprint(report)
    app.register_blueprint(vehicle)

    return app
