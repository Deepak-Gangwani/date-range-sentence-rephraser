from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from routes_date import date_bp
from routes_rephrase import rephrase_bp
from models import db, init_db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    init_db(app)

    app.register_blueprint(date_bp, url_prefix='/api/date')
    app.register_blueprint(rephrase_bp, url_prefix='/api/rephrase')

    @app.get('/')
    def index():
        return jsonify({
            "message": "Flask Flexible APIs — Date Range Generator and Sentence Rephraser",
            "date_endpoint": "/api/date/generate?range=<range_value>",
            "rephrase_endpoint": "/api/rephrase/ (POST)"
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
