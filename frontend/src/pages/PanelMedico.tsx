import React, { useState } from 'react'
import { api } from '../services/api'
import { Triaje } from '../types'

interface PacienteCola {
  id: string;
  paciente: string;
  dni: string;
  edad: number;
  cama: string;
  nivel: 'critico' | 'moderado' | 'leve';
  vitales: { label: string; valor: string }[];
}

interface Atencion extends PacienteCola {
  atendidoEn: string;
}

// Datos de demostración: no existe todavía un backend de vitales/alertas en tiempo real
// (módulo dashboard-medico sin fase-0, ver .orquestador/ledger-dependencias.md DEP-006).
// El DNI 33344455 corresponde a un paciente real sembrado en la base — permite probar
// "Ver Historial Clínico" contra datos reales; el otro DNI es ficticio a propósito.
const COLA_INICIAL: PacienteCola[] = [
  {
    id: '1',
    paciente: 'Pérez, Juan Camilo',
    dni: '40201199',
    edad: 58,
    cama: 'Cama 402 - UCI 2',
    nivel: 'critico',
    vitales: [
      { label: 'FC (BPM)', valor: '142' },
      { label: 'SpO2', valor: '88%' },
    ],
  },
  {
    id: '2',
    paciente: 'Huaman, Rosa',
    dni: '33344455',
    edad: 45,
    cama: 'Cama 118 - Urgencias',
    nivel: 'moderado',
    vitales: [
      { label: 'Presión', valor: '130/85' },
      { label: 'Temp', valor: '38.4°C' },
    ],
  },
]

const FEED_DEMO = [
  { titulo: 'Ingreso de Laboratorio', detalle: 'Resultados de gasometría listos para Rodríguez, Alberto (Cama 202).', tiempo: 'Ahora' },
  { titulo: 'Cambio de Turno', detalle: 'Enfermera S. Valdivia inició monitoreo en Sector C.', tiempo: 'Hace 12 min' },
  { titulo: 'Alerta Descartada', detalle: 'Sensor de Cama 104 recalibrado por técnico.', tiempo: 'Hace 28 min' },
]

const NIVEL_ESTILOS: Record<string, string> = {
  critico: 'bg-error-container text-on-error-container',
  moderado: 'bg-amber-100 text-amber-800',
  leve: 'bg-secondary-container text-on-secondary-container',
}

interface PanelMedicoProps {
  userNombre: string;
  onLogout: () => void;
}

const PanelMedico: React.FC<PanelMedicoProps> = ({ userNombre, onLogout }) => {
  const [tab, setTab] = useState<'alertas' | 'feed' | 'historial' | 'chat'>('alertas')

  // Cola activa y "Mi Historial de Atenciones" — estado local, movimiento instantáneo sin recarga.
  const [cola, setCola] = useState<PacienteCola[]>(COLA_INICIAL)
  const [atenciones, setAtenciones] = useState<Atencion[]>([])
  const [pacienteEnAtencion, setPacienteEnAtencion] = useState<PacienteCola | null>(null)

  const [dniBusqueda, setDniBusqueda] = useState('')
  const [buscando, setBuscando] = useState(false)
  const [errorBusqueda, setErrorBusqueda] = useState('')
  const [pacienteEncontrado, setPacienteEncontrado] = useState<{ id: string; nombres: string; apellidos: string } | null>(null)
  const [triajes, setTriajes] = useState<Triaje[] | null>(null)

  const buscarHistorialPorDni = async (dni: string) => {
    if (!/^\d{8}$/.test(dni)) {
      setErrorBusqueda('El DNI debe contener exactamente 8 dígitos.')
      return
    }
    setBuscando(true)
    setErrorBusqueda('')
    setTriajes(null)
    setPacienteEncontrado(null)
    try {
      const paciente = await api.buscarPacientePorDni(dni)
      setPacienteEncontrado(paciente)
      const historial = await api.listarTriajesDePaciente(paciente.id)
      setTriajes(historial)
    } catch (err: any) {
      setErrorBusqueda(err.message || 'No se encontró un paciente con ese DNI.')
    } finally {
      setBuscando(false)
    }
  }

  const handleBuscarHistorial = (e: React.FormEvent) => {
    e.preventDefault()
    buscarHistorialPorDni(dniBusqueda)
  }

  const handleVerHistorialClinico = (dni: string) => {
    setPacienteEnAtencion(null)
    setDniBusqueda(dni)
    setTab('historial')
    buscarHistorialPorDni(dni)
  }

  const handleMarcarAtendido = (paciente: PacienteCola) => {
    setCola(prev => prev.filter(p => p.id !== paciente.id))
    setAtenciones(prev => [{ ...paciente, atendidoEn: new Date().toLocaleString() }, ...prev])
    setPacienteEnAtencion(null)
  }

  return (
    <div className="bg-background text-on-surface font-body-lg antialiased min-h-screen pb-20">
      {/* TopAppBar */}
      <header className="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-4 h-16 bg-white border-b border-surface-container-highest">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-[24px]">monitor_heart</span>
          <h1 className="text-lg font-bold text-primary">Panel Médico</h1>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-on-surface-variant hidden sm:inline">{userNombre}</span>
          <button
            onClick={onLogout}
            className="flex items-center gap-1 px-4 py-2 rounded-full border border-outline text-on-surface-variant font-semibold hover:bg-surface-container-high transition-colors text-xs"
          >
            <span className="material-symbols-outlined text-[16px]">logout</span>
            Cerrar Sesión
          </button>
        </div>
      </header>

      <main className="pt-20 px-4 max-w-2xl mx-auto">
        {tab === 'alertas' && (
          <section className="space-y-8">
            <div>
              <h2 className="text-sm font-bold text-error uppercase tracking-wider mb-3 flex items-center gap-1">
                <span className="material-symbols-outlined text-[18px]">warning</span>
                Alertas Prioritarias ({cola.length})
                <span className="text-xs font-normal text-on-surface-variant normal-case ml-2">(datos de demostración)</span>
              </h2>
              {cola.length === 0 ? (
                <p className="text-sm text-on-surface-variant">No hay pacientes en cola. Todos fueron atendidos.</p>
              ) : (
                <div className="space-y-3">
                  {cola.map(p => (
                    <div key={p.id} className="bg-white border border-error rounded-xl p-4 clinical-shadow">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <p className="font-bold text-on-surface">{p.paciente}</p>
                          <p className="text-xs text-on-surface-variant">{p.cama}</p>
                        </div>
                        <span className={`text-xs font-bold px-2 py-1 rounded-full ${NIVEL_ESTILOS[p.nivel]}`}>
                          {p.nivel.toUpperCase()}
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 my-3">
                        {p.vitales.map(d => (
                          <div key={d.label} className="bg-surface-container rounded-lg p-2 text-center">
                            <p className="text-xs text-on-surface-variant">{d.label}</p>
                            <p className="text-lg font-bold text-error">{d.valor}</p>
                          </div>
                        ))}
                      </div>
                      <button
                        onClick={() => setPacienteEnAtencion(p)}
                        className="w-full bg-primary text-white font-semibold py-2 rounded-lg hover:bg-primary-container transition-colors text-sm"
                      >
                        Atender
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Mi Historial de Atenciones — pacientes marcados como atendidos en esta sesión */}
            <div>
              <h2 className="text-sm font-bold text-on-surface-variant uppercase tracking-wider mb-3 flex items-center gap-1">
                <span className="material-symbols-outlined text-[18px]">task_alt</span>
                Mi Historial de Atenciones ({atenciones.length})
              </h2>
              {atenciones.length === 0 ? (
                <p className="text-sm text-on-surface-variant">Aún no atendiste a ningún paciente en esta sesión.</p>
              ) : (
                <div className="space-y-2">
                  {atenciones.map(a => (
                    <div key={a.id} className="bg-surface-container-low border border-outline-variant rounded-xl p-3 flex justify-between items-center">
                      <div>
                        <p className="font-semibold text-sm text-on-surface">{a.paciente}</p>
                        <p className="text-xs text-on-surface-variant">DNI {a.dni} · Atendido: {a.atendidoEn}</p>
                      </div>
                      <button
                        onClick={() => handleVerHistorialClinico(a.dni)}
                        className="text-xs text-primary font-semibold hover:underline whitespace-nowrap ml-2"
                      >
                        Ver Historial
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>
        )}

        {tab === 'feed' && (
          <section>
            <h2 className="text-sm font-bold text-on-surface-variant uppercase tracking-wider mb-3">
              Feed en Tiempo Real <span className="text-xs font-normal normal-case ml-2">(datos de demostración)</span>
            </h2>
            <div className="space-y-3">
              {FEED_DEMO.map((item, i) => (
                <div key={i} className="bg-white border border-outline-variant rounded-xl p-4 clinical-shadow flex justify-between items-start">
                  <div>
                    <p className="font-semibold text-on-surface text-sm">{item.titulo}</p>
                    <p className="text-xs text-on-surface-variant mt-1">{item.detalle}</p>
                  </div>
                  <span className="text-xs text-outline whitespace-nowrap ml-2">{item.tiempo}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {tab === 'historial' && (
          <section>
            <h2 className="text-sm font-bold text-on-surface-variant uppercase tracking-wider mb-3">
              Historial de Paciente
            </h2>
            <form onSubmit={handleBuscarHistorial} className="flex gap-2 mb-4">
              <input
                type="text"
                maxLength={8}
                value={dniBusqueda}
                onChange={(e) => setDniBusqueda(e.target.value.replace(/\D/g, ''))}
                placeholder="Buscar por DNI del paciente..."
                className="flex-1 px-4 py-2 border border-outline-variant rounded-lg outline-none focus:ring-2 focus:ring-primary focus:border-primary text-sm"
              />
              <button
                type="submit"
                disabled={buscando}
                className="bg-primary text-white font-semibold px-4 rounded-lg hover:bg-primary-container transition-colors text-sm disabled:opacity-60"
              >
                {buscando ? '...' : 'Buscar'}
              </button>
            </form>

            {errorBusqueda && <p className="text-sm text-error font-semibold mb-3">{errorBusqueda}</p>}

            {pacienteEncontrado && (
              <p className="text-sm text-on-surface-variant mb-3">
                Paciente: <span className="font-semibold text-on-surface">{pacienteEncontrado.nombres} {pacienteEncontrado.apellidos}</span>
              </p>
            )}

            {triajes && triajes.length === 0 && (
              <p className="text-sm text-on-surface-variant">Este paciente no tiene triajes registrados.</p>
            )}

            {triajes && triajes.length > 0 && (
              <div className="space-y-3">
                {triajes.map(t => (
                  <div key={t.id} className="bg-white border border-outline-variant rounded-xl p-4 clinical-shadow">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-xs text-on-surface-variant">
                        {new Date(t.fecha_registro).toLocaleString()}
                      </span>
                      <span className={`text-xs font-bold px-2 py-1 rounded-full ${NIVEL_ESTILOS[t.nivel_atencion]}`}>
                        {t.nivel_atencion.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-on-surface"><strong>PA:</strong> {t.presion_arterial}</p>
                    <p className="text-sm text-on-surface"><strong>Síntomas:</strong> {t.sintomas.join(', ')}</p>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {tab === 'chat' && (
          <section className="text-center py-16">
            <span className="material-symbols-outlined text-[48px] text-outline">chat</span>
            <p className="text-on-surface-variant mt-2">Chat entre médicos — próximamente.</p>
          </section>
        )}
      </main>

      {/* Bottom Nav */}
      <nav className="fixed bottom-0 left-0 w-full bg-white border-t border-surface-container-highest flex justify-around items-center h-16 z-50">
        {([
          { id: 'alertas', icon: 'notifications', label: 'Alertas' },
          { id: 'feed', icon: 'dynamic_feed', label: 'Feed' },
          { id: 'historial', icon: 'history', label: 'Historial' },
          { id: 'chat', icon: 'chat', label: 'Chat' },
        ] as const).map(item => (
          <button
            key={item.id}
            onClick={() => setTab(item.id)}
            className={`flex flex-col items-center gap-0.5 text-xs font-semibold transition-colors ${
              tab === item.id ? 'text-primary' : 'text-on-surface-variant'
            }`}
          >
            <span className="material-symbols-outlined text-[22px]">{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      {/* Vista de Atención (modal) */}
      {pacienteEnAtencion && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/40" onClick={() => setPacienteEnAtencion(null)}>
          <div
            className="bg-white rounded-xl clinical-shadow w-full max-w-sm p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-lg font-bold text-primary">Vista de Atención</h3>
              <button onClick={() => setPacienteEnAtencion(null)} className="text-on-surface-variant hover:text-primary">
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <div className="bg-surface-container-low rounded-lg p-3 mb-4 text-sm space-y-1">
              <p className="font-bold text-on-surface">{pacienteEnAtencion.paciente}</p>
              <p><strong className="text-on-surface-variant">DNI:</strong> {pacienteEnAtencion.dni}</p>
              <p><strong className="text-on-surface-variant">Edad:</strong> {pacienteEnAtencion.edad} años</p>
              <div className="grid grid-cols-2 gap-2 mt-2">
                {pacienteEnAtencion.vitales.map(d => (
                  <div key={d.label} className="bg-white rounded-lg p-2 text-center border border-outline-variant">
                    <p className="text-xs text-on-surface-variant">{d.label}</p>
                    <p className="text-sm font-bold text-error">{d.valor}</p>
                  </div>
                ))}
              </div>
            </div>

            <button
              onClick={() => handleVerHistorialClinico(pacienteEnAtencion.dni)}
              className="w-full border border-primary text-primary font-semibold py-2 rounded-lg hover:bg-primary/5 transition-colors text-sm mb-4 flex items-center justify-center gap-2"
            >
              <span className="material-symbols-outlined text-[18px]">history</span>
              Ver Historial Clínico
            </button>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                onChange={(e) => {
                  if (e.target.checked) handleMarcarAtendido(pacienteEnAtencion)
                }}
                className="w-5 h-5 text-primary border-outline-variant rounded focus:ring-primary"
              />
              <span className="text-sm font-semibold text-on-surface">Marcar como Atendido</span>
            </label>
          </div>
        </div>
      )}
    </div>
  )
}

export default PanelMedico
