# Gestión de Eventos - Configuración de base de datos remota

Este proyecto usa Django y puede conectarse a un servidor PostgreSQL remoto en la red local.

## Requisitos
- La base de datos PostgreSQL corre en la máquina Fedora.
- Las laptops cliente están conectadas por cable y switch al mismo segmento de red.
- La IP del servidor debe ser accesible desde las laptops.

## Configuración de `settings.py`
El proyecto ya está preparado para usar variables de entorno. En `gestion_eventos/gestion_eventos/settings.py` el bloque `DATABASES` usa:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'eventos_db'),
        'USER': os.environ.get('DB_USER', 'admin_eventos'),
        'PASSWORD': os.environ.get('DB_PASS', 'admin200A'),
        'HOST': os.environ.get('DB_HOST', '172.16.118.221'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## Pasos para la laptop cliente (Windows o Linux)
1. Crear y activar el entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate    # Windows
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
pip install psycopg2-binary
```

3. Exportar las variables de entorno para la conexión a PostgreSQL:

### Linux / Fedora
```bash
export DB_HOST=172.16.118.221
export DB_NAME=eventos_db
export DB_USER=admin_eventos
export DB_PASS='admin200A'
export DB_PORT=5432
```

### Windows PowerShell
```powershell
$env:DB_HOST = '172.16.118.221'
$env:DB_NAME = 'eventos_db'
$env:DB_USER = 'admin_eventos'
$env:DB_PASS = 'admin200A'
$env:DB_PORT = '5432'
```

4. Ejecutar migraciones y crear superusuario si aún no existe:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Levantar el servidor de desarrollo:

```bash
python manage.py runserver 0.0.0.0:8000
```

6. Abrir en el navegador de la laptop cliente:

```text
http://127.0.0.1:8000/
```

## Notas para Fedora (servidor PostgreSQL)
- `listen_addresses = '*'` en `postgresql.conf`
- Agregar la red cliente en `pg_hba.conf`, por ejemplo:

```text
host all all 172.16.0.0/16 md5
```

- Abrir el puerto 5432:

```bash
sudo firewall-cmd --add-port=5432/tcp --permanent
sudo firewall-cmd --reload
```

- El usuario y base de datos recomendados son:
  - `admin_eventos`
  - `eventos_db`
  - `admin200A`

## Problemas comunes
- Si la laptop cliente no puede conectarse, prueba:
  - `ping 172.16.118.221`
  - `psql -h 172.16.118.221 -U admin_eventos -d eventos_db -W`

- Asegúrate de que todas las máquinas estén en la misma subred del switch.

---

Si quieres, también puedo ayudarte a generar un script pequeño para configurar el `venv` y las variables de entorno automáticamente en la laptop de tu compañero.