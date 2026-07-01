import { useState } from 'react'
import Login from './pages/Login'
import EnfermeroCola from './pages/EnfermeroCola'

export type Page = 'login' | 'enfermero-cola' | 'enfermero-nuevo-triaje' | 'medico-monitoreo'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('login')
  const [role, setRole] = useState<'doctor' | 'nurse'>('doctor')
  const [userDni, setUserDni] = useState('')

  const handleLogin = (selectedRole: 'doctor' | 'nurse', dni: string) => {
    setRole(selectedRole)
    setUserDni(dni)
    if (selectedRole === 'nurse') {
      setCurrentPage('enfermero-cola')
    } else {
      // Por ahora redirige a login hasta tener la vista de médico, o podemos mostrar una alerta
      alert(`Sesión iniciada como Médico (DNI: ${dni}). La vista móvil de médico estará disponible pronto.`)
      setCurrentPage('login')
    }
  }

  const handleLogout = () => {
    setCurrentPage('login')
    setUserDni('')
  }

  return (
    <div className="min-h-screen bg-background text-on-surface">
      {currentPage === 'login' && (
        <Login onLogin={handleLogin} />
      )}
      {currentPage === 'enfermero-cola' && (
        <EnfermeroCola onLogout={handleLogout} userDni={userDni} />
      )}
    </div>
  )
}

export default App
