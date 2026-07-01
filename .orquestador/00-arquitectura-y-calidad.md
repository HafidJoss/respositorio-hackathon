---
version: 1.1.0
estado: congelada
dueño: C
fecha: 2026-07-01
congelada: true
regla: Se decide UNA VEZ por proyecto, antes del primer fase-0/{modulo}.md.
  Todo módulo hereda esto sin redecidir. Cambiarlo después requiere
  ADR explícito (ver §5) — no se reabre por conveniencia puntual.
  (§4.1 diccionario de datos se agregó en v1.1.0 sin reabrir §1/§2)
proyecto: Sistema de Gestión de Urgencias y Triaje — Posta Médica Rural
---

# Arquitectura y calidad — decisión de proyecto

## 1. Arquitectura general

**Decisión de este proyecto:**

    Monolito modular + núcleo hexagonal en módulos críticos
    (dominio / puertos / adaptadores separados).

- [x] Monolito modular + hexagonal (default)
- [ ] Otra: ******\_\_******

**Justificación:**

Equipo reducido, sin necesidad medida de escalado independiente entre
módulos. Los siete módulos identificados (`registro-pacientes`,
`historial-clinico`, `bot-ivr-urgencias`, `triaje`,
`dashboard-enfermero`, `dashboard-medico`, `notificaciones`) comparten
un dominio central (`Usuario`, `Paciente`, `Triaje`, `Urgencia`) que en
una arquitectura distribuida exigiría sincronización entre servicios
sin beneficio real medido.

El núcleo hexagonal es la pieza no negociable: el dominio (`Paciente`,
`Triaje`, `Urgencia`) no debe conocer el origen técnico de un registro
ni de una sugerencia. Tres fuentes externas entran exclusivamente como
**adaptadores de infraestructura**, nunca como lógica de dominio:

| Fuente externa                                     | Puerto de dominio       |
| -------------------------------------------------- | ----------------------- |
| Llamada telefónica (IVR: voz/Whisper local o DTMF) | `RegistrarUrgenciaPort` |
| Registro manual (dashboard enfermero)              | `RegistrarUrgenciaPort` |
| Sugerencia de síntomas vía IA generativa           | `SugeridorSintomasPort` |

Esto garantiza que una urgencia registrada por llamada, por triaje
manual o por dashboard pasa por el mismo caso de uso de dominio — no
hay tres implementaciones paralelas de "registrar urgencia".

## 2. Patrones de diseño permitidos

| Patrón                         | Uso permitido para                                                                                                    |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| Repository                     | Persistencia — abstrae la fuente de datos del dominio                                                                 |
| Adapter                        | Infraestructura externa: IVR (voz/DTMF), IA generativa (sugerencia de síntomas), notificaciones                       |
| DTO / Mapper                   | Contratos de entrada/salida entre capas                                                                               |
| Application Service / Use Case | Encapsular reglas de negocio ejecutables, incluido el flujo de estados de la llamada IVR (`GestionarLlamadaUrgencia`) |

**Decisión sobre flujo de estados del IVR:** no se introduce un patrón
"State Machine" dedicado. El estado de la llamada (usuario
identificado → paciente seleccionado si hay más de uno asociado →
dato de urgencia capturado → confirmación → cierre) se modela como
datos (`sesion_llamada.estado_actual`) gestionados por un Application
Service existente en la lista. Se reabre esta decisión vía ADR-lite
(§5) solo si el árbol de decisión de la llamada crece más allá de un
flujo lineal de ~5 pasos (ej. triaje completo por voz).

No se contemplan microservicios, CQRS ni Event Sourcing salvo que §1
haya sido reabierto con ADR explícito.

## 3. Código limpio — reglas ejecutables (aplican a A y B)

    □ Funciones ≤ 20 líneas — excepción documentada por PR si hay
      coordinación legítima entre módulos, nunca por mezcla de lógica
    □ Nombres significativos — 0 abreviaturas ambiguas, 0 sinónimos
      fuera del glosario canónico de cada fase-0/{modulo}.md
    □ 0 comentarios redundantes o decorativos — comentario solo para
      decisión, restricción o intención no evidente en el código
    □ Bajo acoplamiento / alta cohesión — verificado por el criterio
      DIP existente en avance-backend.md (0 imports infra→domain)
    □ Manejo de errores estructurado — nunca print()/console.log()/
      exit() suelto; códigos de error + contexto + recuperación
      graceful

Estas 5 líneas se agregan como fila fija en `avance-backend.md` y
`avance-frontend.md` de cada módulo — no se repiten aquí por módulo,
se referencian.

## 4. Gestión de datos

**Regla de orden:** el ERD (o modelo de datos equivalente) se define
en el **contrato esqueleto de fase-0/{modulo}.md** antes de que A
escriba el primer modelo — nunca al revés. **Excepción declarada:**
las entidades centrales compartidas por más de un módulo (`Usuario`,
`Paciente`, `usuario_paciente`) se definen aquí, en §4.1, precisamente
porque pertenecen a más de un fase-0 y no deben redefinirse en cada uno.

**Modelo central de dominio:**

- `Usuario` — quien tiene cuenta y teléfono oficial en el sistema.
  No es necesariamente el paciente.
- `Paciente` — quien recibe la atención médica; tiene historial
  clínico propio, vinculado a jurisdicción SIS.
- `usuario_paciente` (tabla intermedia, N:M) — relación entre quien
  gestiona/llama y quien es atendido.

### 4.1 Diccionario de datos — entidades centrales

**Usuario**

| Campo            | Tipo      | Obligatorio | Único | Restricciones / notas                                                       |
| ---------------- | --------- | ----------- | ----- | --------------------------------------------------------------------------- |
| `id`             | UUID      | sí          | sí    | PK, autogenerado                                                            |
| `dni`            | string(8) | sí          | sí    | Solo dígitos, exactamente 8 caracteres (formato Perú)                       |
| `telefono`       | string    | sí          | sí    | Formato +51 9XXXXXXXX; es el canal de identificación en `bot-ivr-urgencias` |
| `fecha_registro` | timestamp | sí          | no    | Autogenerado al crear, nunca editable                                       |

**Paciente**

| Campo              | Tipo      | Obligatorio | Único | Restricciones / notas                                                                                                                                                                                                                                                                                      |
| ------------------ | --------- | ----------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`               | UUID      | sí          | sí    | PK, autogenerado                                                                                                                                                                                                                                                                                           |
| `dni`              | string(8) | sí          | sí    | Solo dígitos, exactamente 8; búsqueda principal reutilizada por `triaje` y `bot-ivr-urgencias`                                                                                                                                                                                                             |
| `nombres`          | string    | sí          | no    | —                                                                                                                                                                                                                                                                                                          |
| `apellidos`        | string    | sí          | no    | —                                                                                                                                                                                                                                                                                                          |
| `edad`             | integer   | sí          | no    | **PENDIENTE de decisión:** almacenar `edad` directa envejece el dato con el tiempo; alternativa es `fecha_nacimiento` calculando edad en tiempo de consulta. Se mantiene `edad` por ahora porque así se declaró en fase-0 de `registro-pacientes` y `triaje`; se reabre si esto causa inconsistencia real. |
| `jurisdiccion_sis` | string    | sí          | no    | Referencia a dirección/correspondencia de jurisdicción bajo seguro SIS                                                                                                                                                                                                                                     |
| `fecha_registro`   | timestamp | sí          | no    | Autogenerado al crear                                                                                                                                                                                                                                                                                      |

**usuario_paciente**

| Campo               | Tipo                    | Obligatorio | Único                                    | Restricciones / notas                                                                                  |
| ------------------- | ----------------------- | ----------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `id`                | UUID                    | sí          | sí                                       | PK, autogenerado                                                                                       |
| `usuario_id`        | UUID (FK → Usuario.id)  | sí          | no                                       | —                                                                                                      |
| `paciente_id`       | UUID (FK → Paciente.id) | sí          | no                                       | —                                                                                                      |
| `tipo_relacion`     | enum                    | sí          | no                                       | Valores permitidos: `titular`, `madre`, `padre`, `tutor_legal`, `otro` — 0 valores fuera de este enum  |
| `vigente`           | boolean                 | sí          | no                                       | Default `true`; pasa a `false` en baja de tutela (flujo aún PENDIENTE en fase-0 de registro-pacientes) |
| `fecha_vinculacion` | timestamp               | sí          | no                                       | Autogenerado al crear el vínculo                                                                       |
| —                   | —                       | —           | (usuario_id, paciente_id, tipo_relacion) | Restricción compuesta: no se permite duplicar exactamente el mismo vínculo activo                      |

**Regla de gobierno de este diccionario:** ningún campo se agrega,
elimina o cambia de tipo en estas 3 entidades sin actualizar esta
sección — un modelo de código que se desvíe de esta tabla es
criterio fallido en `avance-backend.md`, igual que un ERD no definido.

    □ SQL/NoSQL justificado por caso de uso real de ese módulo,
      no por preferencia — la justificación vive en fase-0/{modulo}.md
    □ Migraciones como código versionado — 0 cambios de esquema
      manuales directos en base de datos, en ningún ambiente
    □ Persistencia entra como adaptador (Repository) — el dominio
      no depende de la tecnología de almacenamiento concreta
    □ Seeds con datos sintéticos (Faker o equivalente) — 0 datos
      reales de producción en fixtures de prueba, sin excepción

**PENDIENTE:** estrategia de sincronización online/offline (cola
local + resolución de conflictos al reconectar) para
`dashboard-enfermero` y `dashboard-medico` — no bloquea Fase 1 de
ningún módulo; se resuelve en el `fase-0` de cada dashboard antes de
que B empiece esa pieza específica.

## 5. Registro de reapertura (ADR-lite)

> Solo se llena si §1 o §2 se reabren después de congelados.

| Fecha | Qué se reabrió | Alternativas consideradas | Decisión | Consecuencias aceptadas |
| ----- | -------------- | ------------------------- | -------- | ----------------------- |

---

## Cierre

Las 4 secciones tienen decisión explícita marcada — ninguna casilla
"Otra: \_\_\_" sin su justificación llena.

    estado: congelada
    congelada: true
