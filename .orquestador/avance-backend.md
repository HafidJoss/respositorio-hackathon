---
version: 0.1.0
estado: borrador
modulo: [nombre del módulo]
dueño: C
fecha: [fecha]
congelada: false
habilita: avance-backend.md · avance-frontend.md (sección de este módulo)
---

# Fase 0 — {módulo}

## Problema en una frase

[...]

## Actores/roles del sistema

[lista — determina RBAC y bloques de aislamiento en avance-frontend.md]

## MUST del módulo (no SHOULD, no COULD — eso se descarta acá, no se posterga sin marcar)

- [ ]
- [ ]

## Glosario canónico

> Solo términos donde la ambigüedad ya causó o puede causar error real.
> No es un diccionario completo.

| Término | Significa | Sinónimo prohibido en dominio |
| ------- | --------- | ----------------------------- |

## Contrato esqueleto

> Punto de partida — A lo completa a OpenAPI real durante Fase 1.
> Esto solo evita que A y B inventen nombres de entidad distintos.

| Entidad | Endpoints mínimos | Notas |
| ------- | ----------------- | ----- |

## Pantallas mínimas + principios UX

- Pantallas: [...]
- Principio 1: [nombre] → [qué implica concretamente]
- Estado vacío: [regla general, una línea]
- Estado de carga: [regla general, una línea]
- Estado de error: [regla general, una línea]

## Seguridad baseline — lista negativa

- [ ] [lo que NINGÚN rol puede hacer — lo mínimo que rompería confianza si se olvida]

## Pendientes explícitos

> Todo lo que no se sabe todavía se declara aquí, nunca se deja
> vacío sin marcar. Un vacío es ambigüedad; un PENDIENTE es una
> decisión consciente de diferir, y no bloquea el cierre de Fase 0.

- PENDIENTE: [...] — no bloquea Fase 1

---

## Cierre de Fase 0

Las 6 secciones anteriores están llenas o tienen su PENDIENTE
declarado explícitamente. Ninguna casilla queda con "[...]" sin
resolver ni sin marcar.

    estado: congelada
    congelada: true
    fecha_congelamiento: [fecha]

