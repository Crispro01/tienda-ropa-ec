"""
TiendaRopaEC - Aplicación web de tienda de ropa
Proyecto Final - Cloud Computing
Autora: Cristina Soledad Proaño Ullaguari
"""
import os
from flask import Flask, render_template, jsonify
from extensions import db


def create_app():
    app = Flask(__name__)

    # La cadena de conexión viene de una variable de entorno (nunca escrita en el código)
    database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql://usuario:clave@localhost:5432/tienda_ropa"
    )
    # Azure PostgreSQL requiere SSL
    if "sslmode" not in database_url:
        connector = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{connector}sslmode=require"

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from models import Producto

    with app.app_context():
        db.create_all()
        # Si la tabla está vacía, sembramos algunos productos de ejemplo
        if Producto.query.count() == 0:
            productos_demo = [
                Producto(nombre="Camiseta básica", categoria="Camisetas", precio=15.99, stock=40),
                Producto(nombre="Jean slim fit", categoria="Pantalones", precio=32.50, stock=25),
                Producto(nombre="Chompa deportiva", categoria="Chompas", precio=28.00, stock=15),
                Producto(nombre="Vestido casual", categoria="Vestidos", precio=24.99, stock=20),
            ]
            db.session.bulk_save_objects(productos_demo)
            db.session.commit()

    @app.route("/")
    def home():
        productos = Producto.query.all()
        return render_template("index.html", productos=productos)

    @app.route("/producto/<int:producto_id>")
    def detalle_producto(producto_id):
        producto = Producto.query.get_or_404(producto_id)
        return render_template("producto.html", producto=producto)

    @app.route("/salud")
    def salud():
        """Endpoint simple para verificar que la app y la BD responden (usado por el pipeline)."""
        try:
            Producto.query.first()
            return jsonify({"status": "ok", "db": "conectada"}), 200
        except Exception as e:
            return jsonify({"status": "error", "detail": str(e)}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
