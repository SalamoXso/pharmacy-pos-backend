from app import create_app
from config import Config  # Explicit import

app = create_app(Config)  # Pass Config explicitly

if __name__ == "__main__":
    app.run(debug=True)
