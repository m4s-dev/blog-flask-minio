# Nombre del Proyecto

Breve descripción del proyecto.

## Configuración inicial

### 1. Clonar el repositorio

```bash
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_DIRECTORIO_DEL_REPOSITORIO]
```

### 2. Configurar variables de entorno

Para configurar las variables de entorno necesarias para el proyecto, primero copia el archivo .env.example a un nuevo archivo llamado .env:

```bash
cp .env.example .env
```
Luego, edita el archivo .env con tus valores para las variables de entorno:

```bash
SECRET_KEY=secret-key
MINIO_ROOT_USER=m4s-admin
MINIO_ROOT_PASSWORD=m4s-admin
MINIO_VOLUMES="/mnt/data"
MINIO_SERVER_PORT=9000
MINIO_HOST=minio
MINIO_BUCKET=static-bucket
MINIO_ENDPOINT=${MINIO_HOST}:${MINIO_SERVER_PORT}
```

Nota: No compartas el archivo .env ni incluyas valores reales en el archivo .env.example. El archivo .env contiene información sensible y no debe ser comprometido en el repositorio.