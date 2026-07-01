---
version: 1.0.0
estado: congelada
modulo: triaje
dueño: C
fecha: 2026-07-01
congelada: true
habilita: avance-backend.md · avance-frontend.md (sección triaje)
---
# Fase 0 — triaje

## Problema en una frase
Permitir al Enfermero registrar manualmente un triaje (síntomas y
signos vitales) buscando al Paciente por DNI, y clasificarlo por
nivel de prioridad para que aparezca en `dashboard-enfermero` y, si
corresponde, escale a `dashboard-medico`.

## Actores/roles del sistema
- **Enfermero** — único rol autorizado a crear un registro de triaje
- **Médico** — solo lectura (consulta triajes ya registrados)
- **Sistema** — no calcula nivel de atención en esta versión (ver Pendientes)

## MUST del módulo
- [x] Buscar Paciente por DNI (reutiliza capacidad de `registro-pacientes`,
      no se reimplementa la búsqueda)
- [x] Si el DNI no existe, el Enfermero es dirigido a
      `registro-pacientes` — el triaje no crea pacientes nuevos por su cuenta
- [x] Capturar campos: nombres, apellidos, DNI, edad, peso, talla,
      presión arterial, síntomas (texto libre + selección de comunes)
- [x] Asignar nivel de atención manualmente: crítico / moderado / leve
      — decidido por el Enfermero, el sistema no lo sugiere en esta fase
- [x] Todo triaje queda vinculado al Paciente y visible en su
      historial clínico
- [x] Todo triaje con nivel crítico o moderado dispara notificación
      hacia `dashboard-medico` (vía puerto de notificación, no acoplado
      directo al módulo médico)

## Glosario canónico
| Término | Significa | Sinónimo prohibido en dominio |
|---|---|---|
| Triaje | Registro clínico puntual de síntomas + signos vitales con nivel asignado | "consulta", "atención" |
| Nivel de atención | Clasificación crítico/moderado/leve de un triaje, asignada manualmente por Enfermero | "prioridad", "urgencia" (reservado para el módulo bot-ivr) |
| Síntoma común | Entrada de un catálogo reutilizable de síntomas frecuentes | "diagnóstico" (el triaje no diagnostica) |

## Contrato esqueleto

| Entidad | Endpoints mínimos | Notas |
|---|---|---|
| Triaje | `POST /triajes` · `GET /triajes/{id}` · `GET /pacientes/{id}/triajes` | Requiere `paciente_id` existente, nunca lo crea |
| CatalogoSintomas | `GET /sintomas-comunes` | Solo lectura en esta fase — alimentado manualmente, no por IA aún (eso es `historial-clinico`) |

## Pantallas mínimas + principios UX
- Pantallas: Buscador de Paciente por DNI, Formulario de Triaje,
  Confirmación de registro con nivel asignado
- Principio 1: Nivel de atención siempre visible y editable por el
  Enfermero antes de confirmar — el campo nunca viene precargado
  automáticamente en esta versión
- Estado vacío: "DNI no encontrado — ir a registrar paciente" (enlace directo)
- Estado de carga: bloqueo de doble envío durante el POST del triaje
- Estado de error: distinguir error de validación de campo vs error
  de notificación al médico (el triaje se guarda igual aunque falle
  la notificación — no se pierde el registro clínico por un fallo de red)

## Seguridad baseline — lista negativa
- [ ] El Médico no puede editar un triaje, solo leerlo
- [ ] Ningún triaje se guarda sin `paciente_id` válido — 0 triajes huérfanos
- [ ] El nivel de atención no puede quedar vacío al confirmar el registro
- [ ] Fallo en el envío de notificación al médico nunca revierte ni
      bloquea el guardado del triaje (ver Estado de error arriba)

## Pendientes explícitos
- PENDIENTE: criterio clínico exacto para sugerir nivel de atención
  automáticamente a partir de signos vitales — requiere validación
  con personal médico real, no se define por ingeniería. Mientras
  tanto, el Enfermero asigna manualmente (ver MUST).
- PENDIENTE: origen y gobierno del catálogo de síntomas comunes (quién
  lo edita, con qué fuente) — se resuelve junto con `historial-clinico`
- PENDIENTE: qué pasa si dos Enfermeros intentan triajear al mismo
  Paciente simultáneamente — no bloquea Fase 1

---
## Cierre de Fase 0
Las 6 secciones anteriores están llenas o tienen su PENDIENTE
declarado explícitamente. Ninguna casilla queda con "[...]" sin
resolver ni sin marcar.

    estado: congelada
    congelada: true
    fecha_congelamiento: 2026-07-01
