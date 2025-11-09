from app import create_app
from .extensions import init_app
app = create_app()
init_app(app)
print(app)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
