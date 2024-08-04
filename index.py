from flask import Flask
from src.routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    app.register_blueprint(main_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
