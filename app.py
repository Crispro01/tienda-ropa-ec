"""
TiendaRopaEC - Aplicación web de tienda de ropa
Proyecto Final - Cloud Computing
Autora: Cristina Soledad Proaño Ullaguari
"""
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from extensions import db


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "clave-de-desarrollo-cambiar-en-produccion")

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

    from models import Producto, Usuario

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

    @app.context_processor
    def inject_usuario():
        """Hace disponible 'usuario_actual' en todas las plantillas."""
        usuario_id = session.get("usuario_id")
        usuario = Usuario.query.get(usuario_id) if usuario_id else None
        return dict(usuario_actual=usuario)

    @app.route("/")
    def home():
        productos = Producto.query.all()
        return render_template("index.html", productos=productos)

    @app.route("/producto/<int:producto_id>")
    def detalle_producto(producto_id):
        producto = Producto.query.get_or_404(producto_id)
        return render_template("producto.html", producto=producto)

    @app.route("/registro", methods=["GET", "POST"])
    def registro():
        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            correo = request.form.get("correo", "").strip().lower()
            telefono = request.form.get("telefono", "").strip()
            password = request.form.get("password", "")

            error = None
            if not nombre or not correo or not password:
                error = "Completa nombre, correo y contraseña."
            elif len(password) < 6:
                error = "La contraseña debe tener al menos 6 caracteres."
            elif Usuario.query.filter_by(correo=correo).first():
                error = "Ese correo ya está registrado."

            if error:
                return render_template("registro.html", error=error, nombre=nombre, correo=correo, telefono=telefono)

            usuario = Usuario(nombre=nombre, correo=correo, telefono=telefono)
            usuario.set_password(password)
            db.session.add(usuario)
            db.session.commit()
            session["usuario_id"] = usuario.id
            return redirect(url_for("perfil"))

        return render_template("registro.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            correo = request.form.get("correo", "").strip().lower()
            password = request.form.get("password", "")
            usuario = Usuario.query.filter_by(correo=correo).first()

            if usuario and usuario.check_password(password):
                session["usuario_id"] = usuario.id
                return redirect(url_for("perfil"))

            return render_template("login.html", error="Correo o contraseña incorrectos.", correo=correo)

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("usuario_id", None)
        return redirect(url_for("home"))

    @app.route("/perfil")
    def perfil():
        usuario_id = session.get("usuario_id")
        if not usuario_id:
            return redirect(url_for("login"))
        usuario = Usuario.query.get(usuario_id)
        return render_template("perfil.html", usuario=usuario)

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
