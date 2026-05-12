# Prueba Técnica – Analista Metodologías RNF

Gestión de vulnerabilidades CVE catalogadas en CISA y Nuclei.

## Estructura

```
etapa1-python/     # Descarga, enriquecimiento y análisis de CVEs
etapa2-backend/    # API REST con Spring Boot y PostgreSQL
etapa2-frontend/   # Dashboard Angular
etapa3-cobit/      # solución caso práctico
```


## Regenerar datos (Etapa 1)
Para crear la base de información se requieren tener la informacion ejecutando la etapa 1

```bash
pip install -r requirements.txt
```

**`main.py`** — descarga CVEs de CISA KEV y Nuclei, los enriquece con la API de NIST y genera 4 archivos en `output/`:
- `vulnerabilidades.json` — todos los CVEs combinados y enriquecidos
- `cve_vs_cwe.json` — conteo de CVEs únicos por tipo de debilidad (CWE)
- `ranking_cpe.json` — top 50 plataformas más afectadas (vendor:producto)
- `tendencias.json` — conteo mensual y detección estadística de meses pico

```bash
python main.py
```

**`cargar_bd.py`** — lee los 4 archivos de `output/` y pobla el PostgreSQL usado por el backend.

```bash
python cargar_bd.py
```

Se puede correr el proyecto con docker o de manera independiente

## Requisitos

- Docker y Docker Compose
- Python 3.10+ (para regenerar datos)
- Java 17+ y Node 20+ (para desarrollo local sin Docker)

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto antes de correr cualquier cosa. Este archivo lo leen tanto los scripts de Python como Docker Compose:

```
DB_HOST=localhost
DB_PORT=5433
DB_NAME=vulnerabilidades_db
DB_USER=postgres
DB_PASSWORD=[tu_contraseña]
NVD_API_KEY=[api_key_de_nist]  # opcional, aumenta el límite de consultas
```

## Ejecución con Docker

```bash
docker-compose up --build
```

Acceder en `http://localhost:4200`

> El seeder carga los datos automáticamente al levantar los contenedores. Requiere que los archivos `output/*.json` existan (generados con `main.py`).

## Ejecución local (sin Docker)

**1. Base de datos**
Poblar la base con la etapa 1

**2. Backend**
```bash
cd etapa2-backend/etapa2-backend
./mvnw spring-boot:run
```

**3. Frontend**
```bash
cd etapa2-frontend
ng serve --proxy-config proxy.conf.json
```

## Funcionalidades

- **Dashboard** – KPIs de severidad, distribución por fuente y tendencia mensual
- **Vulnerabilidades** – listado paginado con filtros por fuente, severidad y búsqueda por CVE ID
- **CWE Stats** – ranking de debilidades con drill-down a CVEs asociados
- **CPE Ranking** – plataformas más afectadas con drill-down y filtro de severidad
- **CRUD** – crear, editar y eliminar vulnerabilidades
- **Tendencias** – detección estadística de meses pico de explotabilidad (media + σ)
