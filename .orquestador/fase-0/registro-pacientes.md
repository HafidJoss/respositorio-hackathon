---
version: 1.0.0
estado: congelada
modulo: registro-pacientes
dueño: C
fecha: 2026-07-01
congelada: true
habilita: avance-backend.md · avance-frontend.md (sección registro-pacientes)
---

# Fase 0 — registro-pacientes

## Problema en una frase

Registrar y vincular Usuarios (quienes tienen cuenta y teléfono
oficial) con Pacientes (quienes reciben atención), incluyendo casos
donde un tercero gestiona la atención de un menor o dependiente, como
base de la que dependen triaje, historial clínico y el bot IVR.

## Actores/roles del sistema

- **Enfermero** — único rol autorizado a crear/editar Usuario, Paciente
  y el vínculo `usuario_paciente`.
- **Médico** — solo lectura sobre este módulo (consulta, no edita).
- **Sistema** — valida unicidad y formato de DNI/teléfono en cada alta.

## MUST del módulo

- [x] Registrar Usuario con DNI y teléfono oficial (ambos obligatorios,
      ambos únicos en el sistema)
- [x] Registrar Paciente con DNI, nombres, apellidos, edad,
      jurisdicción/SIS
- [x] Vincular Usuario↔Paciente vía tabla intermedia con
      `tipo_relacion` (titular / madre / padre / tutor_legal / otro)
      y `vigente`
- [x] Un Usuario puede tener 0..N Pacientes vinculados vigentes; un
      Paciente puede tener 1..N Usuarios vinculados vigentes
- [x] Búsqueda de Paciente por DNI, expuesta como capacidad reutilizable
      (la consumen `triaje` y `bot-ivr-urgencias`, no se reimplementa)
- [x] Si el DNI de un Paciente ya existe, no se duplica: se ofrece
      vincular el Usuario actual al Paciente existente

## Glosario canónico

| Término     | Significa                                                   | Sinónimo prohibido en dominio                         |
| ----------- | ----------------------------------------------------------- | ----------------------------------------------------- |
| Usuario     | Persona con cuenta y teléfono oficial en el sistema         | "paciente" (no intercambiable)                        |
| Paciente    | Persona que recibe atención médica, tiene historial clínico | "usuario", "cliente"                                  |
| Titular     | Usuario que es su propio Paciente (tipo_relacion = titular) | "dueño", "responsable"                                |
| Tutor legal | Usuario que gestiona un Paciente que no es él mismo         | "apoderado", "encargado" (usar siempre "tutor legal") |
| Vigente     | Relación usuario_paciente actualmente válida, no histórica  | "activo"                                              |

## Contrato esqueleto

| Entidad          | Endpoints mínimos                                                | Notas                                                          |
| ---------------- | ---------------------------------------------------------------- | -------------------------------------------------------------- |
| Usuario          | `POST /usuarios` · `GET /usuarios/{id}`                          | DNI y teléfono únicos, validados en dominio no solo en BD      |
| Paciente         | `POST /pacientes` · `GET /pacientes?dni={dni}`                   | Búsqueda por DNI es la capacidad reutilizada por otros módulos |
| usuario_paciente | `POST /usuarios/{id}/pacientes` · `GET /usuarios/{id}/pacientes` | Body incluye `paciente_id`, `tipo_relacion`                    |

## Pantallas mínimas + principios UX

- Pantallas: Alta de Usuario, Alta de Paciente, Vincular Paciente a
  Usuario (con selector de `tipo_relacion`), Buscador de Paciente por DNI
- Principio 1: Búsqueda antes que alta → todo formulario de alta de
  Paciente empieza buscando el DNI primero, para evitar duplicados
- Estado vacío: "Sin resultados para este DNI — ¿desea registrar un
  paciente nuevo?"
- Estado de carga: spinner con bloqueo de doble envío del formulario
- Estado de error: mensaje específico por campo (DNI inválido ≠
  teléfono inválido ≠ duplicado)

## Seguridad baseline — lista negativa

- [ ] Ningún rol puede editar el DNI de un Paciente ya creado sin
      dejar registro de auditoría (evita suplantación silenciosa)
- [ ] Un Usuario no puede autovincularse a un Paciente sin que un
      Enfermero lo registre — la vinculación no es autoservicio
- [ ] Ningún endpoint expone el teléfono de un Usuario a otro Usuario;
      solo Enfermero/Médico lo consultan
- [ ] Ningún Paciente queda sin al menos un Usuario vinculado vigente
      tras el alta — el sistema no permite pacientes huérfanos de contacto

## Pendientes explícitos

- PENDIENTE: mecanismo de verificación de identidad del tutor legal
  más allá del registro presencial por el Enfermero (ej. documento de
  tutela escaneado) — no bloquea Fase 1
- PENDIENTE: proceso de fusión si un Paciente ya existe en el padrón
  SIS de la posta y se re-registra por este sistema — no bloquea Fase 1
- PENDIENTE: qué pasa si un `tipo_relacion` deja de ser `vigente`
  (ej. tutor pierde tutela) — flujo de baja, no bloquea Fase 1

---

## Cierre de Fase 0

Las 6 secciones anteriores están llenas o tienen su PENDIENTE
declarado explícitamente. Ninguna casilla queda con "[...]" sin
resolver ni sin marcar.

    estado: congelada
    congelada: true
    fecha_congelamiento: 2026-07-01
