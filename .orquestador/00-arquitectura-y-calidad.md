---
version: 0.1.0
estado: borrador
dueño: C
fecha: [fecha]
congelada: false
regla: Se decide UNA VEZ por proyecto, antes del primer fase-0/{modulo}.md.
  Todo módulo hereda esto sin redecidir. Cambiarlo después requiere
  ADR explícito (ver §5) — no se reabre por conveniencia puntual.
---

# Arquitectura y calidad — decisión de proyecto

## 1. Arquitectura general

**Decisión por defecto (recomendada, basada en experiencia real
validada — cámbiala solo con justificación explícita en §5):**

    Monolito modular + núcleo hexagonal en módulos críticos
    (dominio / puertos / adaptadores separados).

**Por qué es el default:** menor complejidad operativa para un
equipo de 3, mejor testabilidad, evita el costo de coordinación
de microservicios sin necesidad real de escalado independiente.
No se adopta arquitectura distribuida sin una necesidad medida
de desacoplamiento — no por moda ni por anticipación especulativa.

**Marca la decisión real de este proyecto:**

- [ ] Monolito modular + hexagonal (default)
- [ ] Otra: ******\_\_\_****** — **justificación obligatoria si no es el default:**
      [qué problema real resuelve la alternativa que el default no resuelve]

## 2. Patrones de diseño permitidos

| Patrón                         | Uso permitido para                                             |
| ------------------------------ | -------------------------------------------------------------- |
| Repository                     | Persistencia — abstrae la fuente de datos del dominio          |
| Adapter                        | Infraestructura externa (APIs terceros, colas, notificaciones) |
| DTO / Mapper                   | Contratos de entrada/salida entre capas                        |
| Application Service / Use Case | Encapsular reglas de negocio ejecutables                       |

**Regla vinculante:** ningún patrón fuera de esta lista se introduce
sin registrar antes, en este mismo archivo, qué problema real resuelve
y qué trade-off se acepta. Un patrón sin esa nota es criterio fallido
en `avance-backend.md` — no es "buena práctica", es deuda de gobierno.

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
escriba el primer modelo — nunca al revés. Un modelo de datos escrito
directamente en código sin pasar por fase-0 es criterio fallido.

    □ SQL/NoSQL justificado por caso de uso real de ese módulo,
      no por preferencia — la justificación vive en fase-0/{modulo}.md
    □ Migraciones como código versionado — 0 cambios de esquema
      manuales directos en base de datos, en ningún ambiente
    □ Persistencia entra como adaptador (Repository) — el dominio
      no depende de la tecnología de almacenamiento concreta
    □ Seeds con datos sintéticos (Faker o equivalente) — 0 datos
      reales de producción en fixtures de prueba, sin excepción

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

