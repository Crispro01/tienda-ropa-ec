"""
Pruebas automatizadas de la aplicación TiendaRopaEC.
Estas pruebas las ejecuta GitHub Actions antes de desplegar a Azure.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import create_app
from extensions import db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page_carga(client):
    """La página principal debe responder con código 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_contiene_titulo(client):
    """La página principal debe mostrar el nombre de la tienda."""
    response = client.get("/")
    assert "CSP".encode() in response.data


def test_endpoint_salud_responde_ok(client):
    """El endpoint de salud confirma que la app y la base de datos están conectadas."""
    response = client.get("/salud")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_producto_inexistente_devuelve_404(client):
    """Pedir un producto que no existe debe devolver 404, no un error 500."""
    response = client.get("/producto/99999")
    assert response.status_code == 404
