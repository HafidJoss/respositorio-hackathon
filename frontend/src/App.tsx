import { useState } from 'react'
import Login from './pages/Login'
import EnfermeroCola from './pages/EnfermeroCola'
import RegistroPaciente from './pages/RegistroPaciente'
import NuevoTriaje from './pages/NuevoTriaje'
import PanelMedico from './pages/PanelMedico'
import { Paciente } from './types'

export type Page = 'login' | 'enfermero-cola' | 'enfermero-registro-paciente' | 'enfermero-nuevo-triaje' | 'medico-monitoreo'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('login')
  const [userDni, setUserDni] = useState('')
  const [userNombre, setUserNombre] = useState('')
  const [selectedPaciente, setSelectedPaciente] = useState<Paciente | null>(null)

  const handleLogin = (selectedRole: 'doctor' | 'nurse', dni: string, nombre: string) => {
    setUserDni(dni)
    setUserNombre(nombre)
    setCurrentPage(selectedRole === 'nurse' ? 'enfermero-cola' : 'medico-monitoreo')
  }

  const handleLogout = () => {
    setCurrentPage('login')
    setUserDni('')
    setUserNombre('')
    setSelectedPaciente(null)
  }

  const handleSelectPaciente = (paciente: Paciente) => {
    setSelectedPaciente(paciente)
    setCurrentPage('enfermero-nuevo-triaje')
  }

  return (
    <div className="min-h-screen bg-background text-on-surface">
      {currentPage === 'login' && (
        <Login onLogin={handleLogin} />
      )}
      {currentPage === 'enfermero-cola' && (
        <EnfermeroCola 
          onLogout={handleLogout} 
          userDni={userDni}
          onNavigateToRegister={() => setCurrentPage('enfermero-registro-paciente')}
        />
      )}
      {currentPage === 'enfermero-registro-paciente' && (
        <RegistroPaciente 
          onBack={() => setCurrentPage('enfermero-cola')}
          onSuccess={handleSelectPaciente}
        />
      )}
      {currentPage === 'enfermero-nuevo-triaje' && selectedPaciente && (
        <NuevoTriaje
          paciente={selectedPaciente}
          onBack={() => setCurrentPage('enfermero-cola')}
          onSuccess={() => {
            setSelectedPaciente(null)
            setCurrentPage('enfermero-cola')
          }}
        />
      )}
      {currentPage === 'medico-monitoreo' && (
        <PanelMedico userNombre={userNombre} onLogout={handleLogout} />
      )}
    </div>
  )
}

export default App
