import React, { useState } from 'react'

interface PacienteMock {
  id: string;
  nombres: string;
  apellidos: string;
  dni: string;
  nivel: 'critico' | 'moderado' | 'leve';
  tiempoEspera: string;
  motivo: string;
  pa: string;
  fc: number;
  satO2: number;
  temp: number;
}

const INITIAL_PATIENTS: PacienteMock[] = [
  {
    id: '1',
    nombres: 'Carlos',
    apellidos: 'Mendoza',
    dni: '45892104',
    nivel: 'critico',
    tiempoEspera: '0h 45m',
    motivo: 'Dolor torácico opresivo, diaforesis, dificultad respiratoria.',
    pa: '160/95',
    fc: 110,
    satO2: 88,
    temp: 37.2
  },
  {
    id: '2',
    nombres: 'María',
    apellidos: 'Quispe',
    dni: '10293847',
    nivel: 'critico',
    tiempoEspera: '0h 20m',
    motivo: 'Hemorragia activa en miembro inferior derecho, post accidente.',
    pa: '90/60',
    fc: 125,
    satO2: 95,
    temp: 36.5
  },
  {
    id: '3',
    nombres: 'Juan',
    apellidos: 'Perez',
    dni: '74839201',
    nivel: 'moderado',
    tiempoEspera: '1h 15m',
    motivo: 'Dolor abdominal agudo FID, náuseas, fiebre.',
    pa: '120/80',
    fc: 95,
    satO2: 98,
    temp: 38.5
  },
  {
    id: '4',
    nombres: 'Ana',
    apellidos: 'Silva',
    dni: '85940312',
    nivel: 'leve',
    tiempoEspera: '2h 30m',
    motivo: 'Tos seca persistente, rinorrea, malestar general x 3 días.',
    pa: '110/70',
    fc: 78,
    satO2: 99,
    temp: 37.0
  },
  {
    id: '5',
    nombres: 'Lucía',
    apellidos: 'Fernández',
    dni: '71029384',
    nivel: 'moderado',
    tiempoEspera: '0h 55m',
    motivo: 'Cefalea intensa, visión borrosa, presión arterial elevada registrada en casa.',
    pa: '150/90',
    fc: 88,
    satO2: 97,
    temp: 36.8
  },
  {
    id: '6',
    nombres: 'Pedro',
    apellidos: 'Chávez',
    dni: '48392019',
    nivel: 'leve',
    tiempoEspera: '1h 40m',
    motivo: 'Dolor de oído derecho pulsátil de inicio gradual, sin supuración.',
    pa: '115/75',
    fc: 72,
    satO2: 99,
    temp: 37.5
  }
]

interface EnfermeroColaProps {
  onLogout: () => void;
  userDni: string;
}

const EnfermeroCola: React.FC<EnfermeroColaProps> = ({ onLogout }) => {
  const [patients, setPatients] = useState<PacienteMock[]>(INITIAL_PATIENTS)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterNivel, setFilterNivel] = useState<'all' | 'critico' | 'moderado' | 'leve'>('all')

  const filteredPatients = patients.filter(patient => {
    const matchesSearch = 
      patient.nombres.toLowerCase().includes(searchTerm.toLowerCase()) ||
      patient.apellidos.toLowerCase().includes(searchTerm.toLowerCase()) ||
      patient.dni.includes(searchTerm)
    
    const matchesFilter = filterNivel === 'all' || patient.nivel === filterNivel

    return matchesSearch && matchesFilter
  })

  // Estadísticas del listado total
  const countCriticos = patients.filter(p => p.nivel === 'critico').length
  const countModerados = patients.filter(p => p.nivel === 'moderado').length
  const countLeves = patients.filter(p => p.nivel === 'leve').length

  const handleAction = (patientName: string, actionType: string) => {
    alert(`${actionType} para el paciente: ${patientName}`)
  }

  return (
    <div className="bg-background text-on-surface font-body-lg antialiased min-h-screen">
      {/* TopAppBar */}
      <header className="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-4 h-16 bg-white border-b border-surface-container-highest">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-[24px]">clinical_notes</span>
          <h1 className="text-lg font-bold text-primary">Panel de Triaje y Recepción</h1>
        </div>
        <div className="flex items-center gap-4">
          <button 
            onClick={onLogout}
            className="flex items-center gap-1 px-4 py-2 rounded-full border border-outline text-on-surface-variant font-semibold hover:bg-surface-container-high transition-colors text-xs"
          >
            <span className="material-symbols-outlined text-[16px]">logout</span>
            Cerrar Sesión
          </button>
        </div>
      </header>

      {/* NavigationDrawer (Web) */}
      <nav className="hidden lg:flex flex-col h-screen fixed left-0 top-0 pt-20 bg-surface-container-low border-r border-surface-container-highest w-72">
        <div className="px-6 mb-4">
          <h2 className="text-sm font-bold text-primary uppercase tracking-wider">Gestión Hospitalaria</h2>
        </div>
        <ul className="flex flex-col gap-1 px-2">
          <li>
            <button className="w-full flex items-center gap-3 px-4 py-3 bg-secondary-container text-on-secondary-container rounded-full font-semibold transition-all">
              <span className="material-symbols-outlined text-[20px] filled">queue</span>
              Cola de Pacientes
            </button>
          </li>
          <li>
            <button 
              onClick={() => alert("Formulario de Nuevo Triaje en desarrollo")}
              className="w-full flex items-center gap-3 px-4 py-3 text-on-surface-variant font-semibold hover:bg-surface-container-high rounded-full transition-colors text-left"
            >
              <span className="material-symbols-outlined text-[20px]">emergency</span>
              Nuevo Triaje
            </button>
          </li>
          <li>
            <button 
              onClick={() => alert("Historial en desarrollo")}
              className="w-full flex items-center gap-3 px-4 py-3 text-on-surface-variant font-semibold hover:bg-surface-container-high rounded-full transition-colors text-left"
            >
              <span className="material-symbols-outlined text-[20px]">history</span>
              Historial de Pacientes
            </button>
          </li>
        </ul>
      </nav>

      {/* Main Content */}
      <main className="pt-20 pb-20 lg:pl-72 px-4 lg:px-8 min-h-screen">
        <div className="max-w-5xl mx-auto py-6 flex flex-col gap-6">
          {/* Header Section */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-surface-container-highest pb-2">
            <div>
              <h2 className="text-2xl font-bold text-on-surface">Pacientes Pendientes</h2>
              <p className="text-sm text-on-surface-variant mt-1">
                {filteredPatients.length} pacientes filtrados de {patients.length} en sala.
              </p>
            </div>
            <div className="flex gap-2 w-full md:w-auto">
              <div className="relative w-full md:w-64">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[20px]">
                  search
                </span>
                <input
                  type="text"
                  placeholder="Buscar por DNI o Nombre"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-white border border-surface-container-highest rounded-full text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
                />
              </div>
            </div>
          </div>

          {/* Dashboard Overview */}
          <div className="grid grid-cols-3 gap-4">
            <button 
              onClick={() => setFilterNivel(filterNivel === 'critico' ? 'all' : 'critico')}
              className={`border rounded-xl p-4 flex items-center justify-between transition-all ${
                filterNivel === 'critico' 
                  ? 'bg-error-container border-error ring-2 ring-error' 
                  : 'bg-white border-outline-variant hover:bg-surface-container-low'
              }`}
            >
              <div className="text-left">
                <p className="text-xs text-on-surface-variant uppercase tracking-wider font-semibold">Críticos</p>
                <p className="text-2xl text-error font-bold">{countCriticos}</p>
              </div>
              <div className="w-10 h-10 rounded-full bg-error-container flex items-center justify-center">
                <span className="material-symbols-outlined text-on-error-container filled">warning</span>
              </div>
            </button>

            <button 
              onClick={() => setFilterNivel(filterNivel === 'moderado' ? 'all' : 'moderado')}
              className={`border rounded-xl p-4 flex items-center justify-between transition-all ${
                filterNivel === 'moderado' 
                  ? 'bg-orange-100 border-orange-500 ring-2 ring-orange-500' 
                  : 'bg-white border-outline-variant hover:bg-surface-container-low'
              }`}
            >
              <div className="text-left">
                <p className="text-xs text-on-surface-variant uppercase tracking-wider font-semibold">Moderados</p>
                <p className="text-2xl text-orange-600 font-bold">{countModerados}</p>
              </div>
              <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center">
                <span className="material-symbols-outlined text-orange-600">schedule</span>
              </div>
            </button>

            <button 
              onClick={() => setFilterNivel(filterNivel === 'leve' ? 'all' : 'leve')}
              className={`border rounded-xl p-4 flex items-center justify-between transition-all ${
                filterNivel === 'leve' 
                  ? 'bg-green-100 border-green-500 ring-2 ring-green-500' 
                  : 'bg-white border-outline-variant hover:bg-surface-container-low'
              }`}
            >
              <div className="text-left">
                <p className="text-xs text-on-surface-variant uppercase tracking-wider font-semibold">Leves</p>
                <p className="text-2xl text-green-600 font-bold">{countLeves}</p>
              </div>
              <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                <span className="material-symbols-outlined text-green-600 filled">check_circle</span>
              </div>
            </button>
          </div>

          {/* Patient List (Bento Grid) */}
          {filteredPatients.length === 0 ? (
            <div className="bg-white border border-outline-variant rounded-xl p-8 text-center text-on-surface-variant">
              No se encontraron pacientes que coincidan con la búsqueda o filtro.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredPatients.map(patient => {
                const isCritico = patient.nivel === 'critico';
                const isModerado = patient.nivel === 'moderado';
                const indicatorColor = isCritico 
                  ? 'bg-error' 
                  : isModerado 
                    ? 'bg-orange-500' 
                    : 'bg-green-500';

                return (
                  <div 
                    key={patient.id}
                    className="bg-white rounded-xl border border-outline-variant overflow-hidden flex flex-col relative clinical-shadow hover:scale-[1.01] transition-all"
                  >
                    {/* Indicador de Prioridad Lateral */}
                    <div className={`absolute left-0 top-0 bottom-0 w-[6px] ${indicatorColor}`}></div>
                    
                    <div className="p-4 pl-6 flex flex-col h-full gap-3">
                      <div className="flex justify-between items-start">
                        <div className={`flex items-center gap-1 px-2 py-0.5 rounded-full ${
                          isCritico 
                            ? 'bg-error-container text-on-error-container' 
                            : isModerado 
                              ? 'bg-orange-100 text-orange-700' 
                              : 'bg-green-100 text-green-700'
                        }`}>
                          <span className="material-symbols-outlined text-[14px]">
                            {isCritico ? 'local_hospital' : isModerado ? 'warning' : 'check_circle'}
                          </span>
                          <span className="font-bold text-[10px] uppercase">
                            {patient.nivel}
                          </span>
                        </div>
                        <span className={`font-bold text-xs ${isCritico ? 'text-error animate-pulse' : 'text-on-surface-variant'}`}>
                          {patient.tiempoEspera}
                        </span>
                      </div>

                      <div>
                        <h3 className="text-lg font-bold text-on-surface">
                          {patient.nombres} {patient.apellidos}
                        </h3>
                        <p className="text-xs text-on-surface-variant font-semibold">DNI: {patient.dni}</p>
                      </div>

                      <div className="bg-surface-container-low p-3 rounded-lg flex-grow">
                        <p className="text-xs font-bold text-on-surface-variant mb-1">Motivo de consulta</p>
                        <p className="text-sm text-on-surface">{patient.motivo}</p>
                        
                        <div className="grid grid-cols-2 gap-2 mt-3 text-xs">
                          <div><span className="text-on-surface-variant font-semibold">PA:</span> {patient.pa}</div>
                          <div><span className="text-on-surface-variant font-semibold">FC:</span> {patient.fc} lpm</div>
                          <div><span className="text-on-surface-variant font-semibold">SatO2:</span> {patient.satO2}%</div>
                          <div><span className="text-on-surface-variant font-semibold">Temp:</span> {patient.temp}°C</div>
                        </div>
                      </div>

                      {isCritico || isModerado ? (
                        <button 
                          onClick={() => handleAction(`${patient.nombres} ${patient.apellidos}`, 'Llamando atención inmediata')}
                          className="mt-auto w-full bg-primary text-white hover:bg-primary-container hover:text-white font-bold py-2 rounded-full transition-colors flex items-center justify-center gap-1 text-xs"
                        >
                          <span className="material-symbols-outlined text-[18px]">forward</span>
                          Atender Ya
                        </button>
                      ) : (
                        <button 
                          onClick={() => handleAction(`${patient.nombres} ${patient.apellidos}`, 'Llamando paciente')}
                          className="mt-auto w-full bg-transparent border border-primary text-primary hover:bg-surface-container-high font-bold py-2 rounded-full transition-colors flex items-center justify-center gap-1 text-xs"
                        >
                          Llamar Paciente
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </main>

      {/* BottomNavBar (Mobile) */}
      <nav className="lg:hidden fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-2 py-3 bg-white border-t border-surface-container-highest shadow-lg rounded-t-xl">
        <button 
          onClick={() => {
            setFilterNivel('all');
            setSearchTerm('');
          }}
          className="flex flex-col items-center justify-center bg-primary-container text-on-primary-container rounded-full px-4 py-1 scale-95 transition-transform"
        >
          <span className="material-symbols-outlined text-[24px]">view_list</span>
          <span className="text-xs font-semibold">Cola</span>
        </button>
        <button 
          onClick={() => alert("Formulario de Nuevo Triaje en desarrollo")}
          className="flex flex-col items-center justify-center text-on-surface-variant hover:bg-surface-container rounded-full px-4 py-1 transition-colors"
        >
          <span className="material-symbols-outlined text-[24px]">medical_services</span>
          <span className="text-xs font-semibold">Triaje</span>
        </button>
        <button 
          onClick={() => alert("Historial en desarrollo")}
          className="flex flex-col items-center justify-center text-on-surface-variant hover:bg-surface-container rounded-full px-4 py-1 transition-colors"
        >
          <span className="material-symbols-outlined text-[24px]">folder_shared</span>
          <span className="text-xs font-semibold">Historial</span>
        </button>
      </nav>

      {/* Emergency FAB */}
      <button 
        onClick={() => alert("Formulario de Nuevo Triaje en desarrollo")}
        className="fixed bottom-20 right-4 lg:bottom-4 lg:right-8 w-14 h-14 rounded-full bg-primary-container shadow-lg flex items-center justify-center hover:scale-105 transition-transform z-50"
      >
        <span className="material-symbols-outlined text-primary text-[28px] filled">emergency</span>
      </button>
    </div>
  )
}

export default EnfermeroCola
