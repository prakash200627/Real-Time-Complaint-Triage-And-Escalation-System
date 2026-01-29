import os
from app import create_app

config_object = os.getenv("FLASK_CONFIG", "config.DevelopmentConfig")
app = create_app(config_object=config_object)

if __name__ == "__main__":
    app.run(debug=True)
