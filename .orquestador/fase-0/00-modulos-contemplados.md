---
version: 1.0.0
estado: activo
dueño: C
fecha: 2026-07-01
proyecto: Sistema de Gestión de Urgencias y Triaje — Posta Médica Rural
---

# Módulos contemplados — mapa de alcance

> Este documento es de referencia y planificación. No es un fase-0.
> Cada módulo listado aquí requiere su propio `fase-0/{modulo}.md`
> con discovery real antes de habilitar Fase 1. Este archivo se
> actualiza cuando cambia el alcance del proyecto, no cuando avanza
> la construcción (eso vive en `00-indice.md`).

## 1. registro-pacientes

**Estado:** ✅ fase-0 congelada
**Problema:** Registrar y vincular Usuarios (cuenta + teléfono
oficial) con Pacientes (quienes reciben atención), incluyendo
vínculo de tutela para menores/dependientes.
**Actor principal:** Enfermero (alta) · Médico (lectura)
**Dependencias:** Ninguna — es la base del dominio.

## 2. triaje

**Estado:** ✅ fase-0 congelada
**Problema:** Registro manual de síntomas y signos vitales
(peso, talla, presión, síntomas) con asignación manual de nivel de
atención (crítico/moderado/leve), buscando al paciente por DNI.
**Actor principal:** Enfermero (crea) · Médico (lectura)
**Dependencias:** `registro-pacientes` (búsqueda por DNI).

## 3. historial-clinico

**Estado:** ⬜ fase-0 pendiente
**Problema:** Consolidar el historial de visitas, triajes y
urgencias de cada Paciente, y sostener el catálogo de síntomas
comunes que alimenta sugerencias (incluida IA generativa a futuro).
**Actor principal:** Médico y Enfermero (lectura) · Sistema (agregación)
**Dependencias:** `registro-pacientes`, `triaje`.
**Nota abierta:** el componente de "base de datos de síntomas
comunes mediante historias médicas" es analítico, no transaccional
simple — su alcance exacto (¿reporte estático? ¿motor de sugerencia
con IA?) se define en su propio fase-0, no aquí.

## 4. bot-ivr-urgencias

**Estado:** ⬜ fase-0 pendiente
**Problema:** Registrar una urgencia médica mediante una sola
llamada telefónica, sin depender de internet del lado del paciente
(voz vía Whisper local como plan A, DTMF como respaldo de
confiabilidad). Debe resolver "¿a qué paciente representa este
teléfono?" antes de registrar, dado el modelo Usuario/Paciente/tutela.
**Actor principal:** Usuario que llama (titular o tutor) · Sistema (bot)
**Dependencias:** `registro-pacientes` (resolución de paciente por
teléfono), `triaje` (comparte concepto de nivel de atención — glosario
a alinear).
**Decisión ya tomada (00-arquitectura-y-calidad.md §1-2):** entra
como Adapter sobre `RegistrarUrgenciaPort`; flujo de estados resuelto
vía Application Service, sin patrón State Machine dedicado.

## 5. dashboard-enfermero

**Estado:** ⬜ fase-0 pendiente
**Problema:** Cola de control de nuevos registros (llamadas y
triajes) filtrable por nivel de atención (crítico/leve/moderado).
**Actor principal:** Enfermero
**Dependencias:** `triaje`, `bot-ivr-urgencias`.
**Nota abierta:** PENDIENTE de sincronización online/offline ya
declarado en `00-arquitectura-y-calidad.md` §4 — se resuelve en el
fase-0 de este módulo antes de que B empiece la pieza.

## 6. dashboard-medico

**Estado:** ⬜ fase-0 pendiente
**Problema:** Visualización de casos críticos/moderados para
monitoreo, notificación de llegada al enfermero, visualización de
registro de llamadas y triajes, y coordinación directa con el
enfermero presente en la posta.
**Actor principal:** Médico
**Dependencias:** `triaje`, `bot-ivr-urgencias`, `notificaciones`.
**Nota abierta:** mismo PENDIENTE de sincronización online/offline
que `dashboard-enfermero`.

## 7. notificaciones

**Estado:** ⬜ fase-0 pendiente
**Problema:** Puerto de notificación por nivel de prioridad hacia
el Médico cuando un triaje o urgencia lo amerita, y canal de
coordinación Médico↔Enfermero.
**Actor principal:** Sistema (emisor) · Médico y Enfermero (receptores)
**Dependencias:** `triaje`, `bot-ivr-urgencias`.
**Nota:** ya referenciado como puerto (`NotificacionPort`) desde el
MUST de `triaje` — este módulo formaliza su propio fase-0 cuando se
necesite más que notificación simple (ej. coordinación bidireccional).

---

## Resumen de dependencias (orden sugerido, no obligatorio salvo 1→2)

```

1. registro-pacientes (base — obligatorio primero)
2. triaje (obligatorio segundo — consume DNI)
3. bot-ivr-urgencias ┐
4. historial-clinico ├─ orden libre entre sí, todos dependen de 1 y 2
5. notificaciones ┘
6. dashboard-enfermero (depende de 3, 4, 5 en distinto grado)
7. dashboard-medico (depende de 3, 4, 5, 6 en distinto grado)

```

## Cierre

Este documento no se "congela" como un fase-0 — se actualiza cada
vez que el alcance del proyecto cambia. Su única regla de
integridad: ningún módulo aquí puede tener su fase-0 real
contradiciendo lo descrito en esta sección sin que esta sección se
actualice también.
