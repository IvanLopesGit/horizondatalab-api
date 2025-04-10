from flask import Flask

from config import Config
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)  # Carrega a variável do config
app.register_blueprint(routes)

if __name__ == "__main__":  # só pra testar
    app.run(debug=True)
