from datetime import timedelta
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt import JWT

from api_livros import blueprint as api
#from controllers.Auth import authenticate, identity


#Carrega o arquivo dotenv
load_dotenv()


app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = 'variante-do-Raul'
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Penaro'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=12)
#jwt = JWT(app, authenticate, identity)

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host = 'localhost', port = '5000', debug = True, load_dotenv = True)