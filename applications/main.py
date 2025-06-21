from flask import Flask
from flask_cors import CORS
from applications.data_collector.src.main.data_collector import db, create_app
from applications.data_analyzer.src.main.data_analyzer import register_routes
from applications.frontend.src.main.app import init_dash_app

server = create_app(testing=False)
CORS(server)

# Register flask api routes
register_routes(server)

# Attach dash app to shared server
dash_app = init_dash_app(server)

if __name__ == "__main__":
    server.run(debug=True, host="0.0.0.0", port=5050)