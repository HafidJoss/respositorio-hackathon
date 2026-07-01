# Cómo levantar el sistema (backend)

Estado actual: **registro-pacientes** y **triaje** están construidos y
cerrados en `.orquestador/avance-backend.md`. Los otros 5 módulos
del proyecto están bloqueados por falta de fase-0 congelada (ver
`.orquestador/ledger-dependencias.md`) — no existen todavía.

## Requisitos

- Python 3.11+ (probado en 3.14)
- Docker + Docker Compose (para PostgreSQL)

## 1. Instalar dependencias

```bash
cd src/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## 2. Levantar PostgreSQL

```bash
docker compose up -d
```

Esto levanta Postgres en `localhost:55432` (usuario `posta`,
password `posta`, base `posta_urgencias`).

## 3. Aplicar migraciones

```bash
alembic upgrade head
```

## 4. (Opcional) Sembrar catálogo de síntomas comunes

El catálogo (`GET /sintomas-comunes`) se alimenta manualmente, no por
API. Para tener datos de partida en desarrollo:

```bash
python3 -c "
from app.core.database import SessionLocal
from app.modules.triaje.infrastructure.repositories import sembrar_catalogo_si_vacio
db = SessionLocal()
sembrar_catalogo_si_vacio(db, ['fiebre', 'tos', 'dolor de cabeza', 'dolor abdominal',
    'dolor de pecho', 'dificultad para respirar', 'mareo', 'nausea', 'vomito',
    'diarrea', 'debilidad', 'sangrado', 'convulsiones', 'perdida de conciencia'])
db.close()
"
```

Ya está sembrado en la base de datos de desarrollo actual — este paso
solo hace falta si se recrea la base desde cero.

## 5. Levantar la API

```bash
uvicorn app.main:app --reload
```

La API queda en `http://localhost:8000`.

- Documentación interactiva (Swagger): `http://localhost:8000/docs`
- Documentación (ReDoc): `http://localhost:8000/redoc`
- Contrato OpenAPI versionado (el que consume el frontend): `contratos/openapi.json`
  — se regenera desde código, nunca se edita a mano.
- Healthcheck: `GET /health` → `{"estado": "ok"}`

## 6. Correr los tests (opcional, requiere una segunda base de datos)

```bash
docker exec <contenedor_postgres> psql -U posta -d posta_urgencias -c "CREATE DATABASE posta_test;"
DATABASE_URL="postgresql+psycopg://posta:posta@localhost:55432/posta_test" alembic upgrade head
pytest --cov=app.modules --cov-branch
```

---

# Endpoints listos para el frontend

Todas las respuestas de error tienen el mismo formato:
`{"detail": "<mensaje>"}`, con el código HTTP correspondiente:

- `400` — dato inválido (formato de DNI, teléfono, nivel de atención, signos vitales, etc.)
- `404` — recurso no encontrado (usuario, paciente o triaje inexistente)
- `409` — conflicto (usuario duplicado, vínculo ya existente)

## Módulo `registro-pacientes`

### Crear usuario
`POST /usuarios`

```json
// body
{ "dni": "12345678", "telefono": "+51 987654321" }
```
```json
// 201
{ "id": "uuid", "dni": "12345678", "telefono": "+51 987654321", "fecha_registro": "2026-07-01T16:00:00Z" }
```
Errores: `400` (dni no son 8 dígitos, teléfono no matchea `+51 9XXXXXXXX`), `409` (dni o teléfono ya registrado).

### Obtener usuario
`GET /usuarios/{usuario_id}` → `200` `UsuarioResponse` · `404` si no existe.

### Registrar paciente (crea o vincula, nunca duplica)
`POST /pacientes`

```json
// body
{
  "dni": "87654321",
  "nombres": "Ana",
  "apellidos": "Quispe",
  "edad": 34,
  "jurisdiccion_sis": "Ayacucho",
  "usuario_id": "uuid del usuario que gestiona/es titular",
  "tipo_relacion": "titular | madre | padre | tutor_legal | otro"
}
```
```json
// 201 — paciente nuevo
{ "id": "uuid", "dni": "87654321", "nombres": "Ana", "apellidos": "Quispe",
  "edad": 34, "jurisdiccion_sis": "Ayacucho", "fecha_registro": "...",
  "ya_existia": false }
```
Si el DNI **ya existe**, no se duplica: se crea el vínculo con el
`usuario_id` enviado y la respuesta vuelve con `"ya_existia": true` y
los datos del paciente ya existente (el frontend debe mostrar esto
como "paciente ya registrado, se vinculó a tu cuenta", no como error).
Errores: `400` (dni/edad inválidos, `tipo_relacion` fuera del enum),
`404` (usuario_id no existe), `409` (ese usuario ya tenía ese mismo
`tipo_relacion` vigente con ese paciente).

### Buscar paciente por DNI
`GET /pacientes?dni=87654321` → `200` `PacienteResponse` · `404` si no existe
(el frontend debe ofrecer ir a "registrar paciente" en ese caso).

### Vincular paciente existente a otro usuario (ej. segundo tutor)
`POST /usuarios/{usuario_id}/pacientes`

```json
// body
{ "paciente_id": "uuid", "tipo_relacion": "tutor_legal" }
```
`201` → `VinculoResponse`. Errores: `404` (usuario o paciente no
existen), `409` (vínculo duplicado).

### Listar pacientes vinculados a un usuario
`GET /usuarios/{usuario_id}/pacientes` → `200` lista de `VinculoResponse`.

## Módulo `triaje`

### Registrar triaje
`POST /triajes` — requiere que `paciente_id` ya exista (se obtiene
antes vía `GET /pacientes?dni=...`); este endpoint nunca crea pacientes.

```json
// body
{
  "paciente_id": "uuid",
  "nombres": "Ana", "apellidos": "Quispe", "dni": "87654321", "edad": 34,
  "peso": 60.5, "talla": 1.6,
  "presion_arterial": "140/95",
  "sintomas": ["fiebre", "dolor de cabeza"],
  "nivel_atencion": "critico | moderado | leve"
}
```
`201` → `TriajeResponse`. Si el nivel es `critico` o `moderado`, el
backend dispara notificación hacia el médico (best-effort: si falla,
el triaje igual queda guardado). Errores: `400` (presión con formato
inválido, peso/talla ≤ 0, `nivel_atencion` vacío o fuera del enum),
`404` (`paciente_id` no existe — dirigir al frontend a
registro-pacientes).

### Obtener triaje
`GET /triajes/{triaje_id}` → `200` `TriajeResponse` · `404` si no existe.

### Listar triajes de un paciente (historial)
`GET /pacientes/{paciente_id}/triajes` → `200` lista de `TriajeResponse` ·
`404` si el paciente no existe.

### Catálogo de síntomas comunes (solo lectura)
`GET /sintomas-comunes` → `200` lista de strings, para poblar el
selector de síntomas en el formulario de triaje.
