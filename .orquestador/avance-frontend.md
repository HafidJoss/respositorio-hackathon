---
version: 0.1.0
estado: activo
dueño: B
alcance_sesion_actual: [módulo/pieza + carpeta exacta]
---
# Avance — Frontend

> Fuente de criterios por pieza: `fase-0/{modulo}.md` congelada +
> `contratos/openapi.json` (consumido, nunca editado a mano).
> Archivo autogobernado — A nunca lo edita.

## Pieza: {pantalla/dashboard}

| Bloque | Criterio | Verificación |
|---|---|---|
| Fidelidad | Contenido obligatorio de fase-0 presente, nada de más ni de menos | comparar contra fase-0 §pantallas |
| Aislamiento de rol | 0 componentes cruzados entre roles del sistema | comparación de árboles de componentes |
| Capacidades = autorizaciones | Toda acción visible tiene su rol autorizado en fase-0/contrato | cruce exacto |
| Principio Cero | Pieza muestra ≥1 registro real de la API — nunca fixture hardcodeado | smoke visual + inspección de red |
| No-duplicación transversal | Patrones de error/carga/vacío/confirmación: un solo componente reutilizado, no uno por pantalla | grep de estructura repetida |

**Estado de la pieza:** ⬜ pendiente / 🔵 en progreso / ✅ cerrada

## Regla de corrección automática

PRIMERO: ¿el criterio depende de algo registrado en ledger-dependencias.md?
SÍ → 0 intentos, detención inmediata, bloqueo LOCAL a esta pieza —
seguir con otras piezas independientes
NO → ciclo normal de 3 intentos (igual que backend)

## No regresión — regla reforzada
Al modificar cualquier componente TRANSVERSAL (no una pieza
individual) → reverificar TODAS las piezas ya cerradas, no solo
la que motivó el cambio. Este es el tipo de regresión más caro —
nunca se salta, aunque parezca lento.

## Formato de detención
PIEZA: {nombre}
CRITERIO FALLIDO: {...}
TIPO: {fidelidad | aislamiento-de-rol | principio-cero | transversal | dependencia-bloqueante}
VALOR OBTENIDO / ESPERADO: {...}
BLOQUEO: {local — sigo con otras piezas | no aplica global en este archivo}
QUÉ NECESITA EL HUMANO: {...}

## Log de avance
| Fecha | Pieza | Estado | Evidencia |
|---|---|---|---|