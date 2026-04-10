from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO

from config import Config
from routes.health_routes import health_bp
from routes.repo_routes import repo_bp
from routes.chat_routes import chat_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Initialize SocketIO for future real-time features
    socketio = SocketIO(app, cors_allowed_origins="*")
    app.socketio = socketio
    
    # Register blueprints (Routes)
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(repo_bp, url_prefix='/api/repo')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    # Frontend Routes
    @app.route('/')
    def index():
        return render_template('index.html')
        
    @app.route('/repo/<repo_id>')
    def repo_view(repo_id):
        return render_template('repo.html', repo_id=repo_id)

    return app, socketio

app, socketio = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, host="127.0.0.1", port=5000)
