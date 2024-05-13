from datetime import timedelta
import os
import logging
from flask import Flask
from flask_mail import Mail
from flask_principal import Principal, identity_loaded, RoleNeed
from flask_swagger_ui import get_swaggerui_blueprint

from Models.models import db
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()
mail = Mail()  # instantiate the mail class


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

logging.basicConfig(level=logging.DEBUG)
my_logger = logging.getLogger(__name__)



def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET')

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )

    app.register_blueprint(swaggerui_blueprint)


    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        role = identity.auth_type[0]
        if role == 'admin':
            identity.provides.add(RoleNeed('admin'))
        else:
            identity.provides.add(RoleNeed('user'))

    app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)  # Set token expiration to 30 minutes

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    jwt = JWTManager(app)

    # configuration of mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'mohammednasser8800@gmail.com'
    app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)
    from routes.product_routes import products
    app.register_blueprint(products, url_prefix='/products')

    from routes.user_routes import user
    app.register_blueprint(user, url_prefix='/user')

    @app.route('/')
    def index():
        return 'welcome'

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
