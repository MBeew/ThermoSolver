# This code initializes a Flask application and runs it in debug mode.
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

