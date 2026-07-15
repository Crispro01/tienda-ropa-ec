# TiendaRopaEC

Aplicación web de tienda de ropa, desarrollada para el Proyecto Final de Cloud Computing.
Desplegada en Azure App Service, conectada a una base de datos PostgreSQL (Azure Database
for PostgreSQL Flexible Server), con un pipeline de integración y despliegue continuo
mediante GitHub Actions.

## Stack tecnológico

- **Backend:** Python 3.12 + Flask
- **ORM:** Flask-SQLAlchemy
- **Base de datos:** PostgreSQL (Azure Database for PostgreSQL Flexible Server)
- **Servidor de aplicación:** Gunicorn
- **Hosting:** Azure App Service (Linux, Python 3.12)
- **CI/CD:** GitHub Actions

## Cómo correr el proyecto en local (WSL/Ubuntu)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edita .env y coloca tu cadena de conexión real a PostgreSQL

export $(cat .env | xargs)
python app.py
```

La app queda disponible en `http://localhost:8000`.

## Cómo correr las pruebas

```bash
pytest tests/ -v
```

## Estructura del proyecto

```
tienda-ropa-ec/
├── app.py                  # Aplicación Flask principal
├── extensions.py           # Instancia de SQLAlchemy (evita imports circulares)
├── models.py                # Modelo Producto
├── startup.sh                # Comando de arranque para Azure App Service
├── requirements.txt          # Dependencias del proyecto
├── templates/                # Vistas HTML
├── static/                    # CSS
├── tests/                     # Pruebas automatizadas (pytest)
└── .github/workflows/         # Pipeline CI/CD
```

## Variables de entorno / Secretos usados en GitHub Actions

| Secreto | Descripción |
|---|---|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL, usada para correr las pruebas |
| `AZURE_WEBAPP_PUBLISH_PROFILE` | Perfil de publicación del App Service, usado para el deploy |

Ninguna credencial está escrita directamente en el código; todas se inyectan como
GitHub Secrets en tiempo de ejecución del pipeline.
