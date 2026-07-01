import React, { useState } from 'react'

interface LoginProps {
  onLogin: (role: 'doctor' | 'nurse', dni: string) => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [role, setRole] = useState<'doctor' | 'nurse'>('doctor')
  const [dni, setDni] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validación básica de DNI (8 dígitos según .orquestador)
    const dniRegex = /^\d{8}$/
    if (!dniRegex.test(dni)) {
      setError('El DNI debe contener exactamente 8 dígitos.')
      return
    }

    if (!password) {
      setError('Por favor ingrese su contraseña.')
      return
    }

    setError('')
    onLogin(role, dni)
  }

  return (
    <main className="w-full min-h-screen flex flex-col items-center justify-center p-4 relative overflow-hidden bg-surface text-on-surface">
      {/* Elementos Decorativos de Fondo */}
      <div className="absolute top-0 left-0 w-full h-full opacity-5 pointer-events-none overflow-hidden">
        <div className="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-primary blur-3xl"></div>
        <div className="absolute -bottom-24 -right-24 w-96 h-96 rounded-full bg-accent-gold blur-3xl"></div>
      </div>

      <div className="w-full max-w-md z-10">
        {/* Header / Brand */}
        <header className="flex flex-col items-center mb-6">
          <div className="w-16 h-16 bg-primary-container rounded-xl flex items-center justify-center mb-4 clinical-shadow">
            <span className="material-symbols-outlined text-[40px] text-white filled">monitor_heart</span>
          </div>
          <h1 className="font-semibold text-2xl text-primary text-center">
            Centro de Monitoreo Médico
          </h1>
        </header>

        {/* Tarjeta de Login */}
        <div className="bg-surface-container-lowest border border-outline-variant p-6 rounded-xl clinical-shadow">
          <div className="mb-6 text-center">
            <h2 className="text-xl md:text-2xl font-bold text-on-surface">
              Bienvenido al Portal Clínico
            </h2>
            <p className="text-sm text-on-surface-variant mt-1">
              Ingrese sus credenciales para acceder al sistema
            </p>
          </div>

          <form className="space-y-4" onSubmit={handleSubmit}>
            {/* Selección de Rol */}
            <div className="space-y-1">
              <label className="text-sm font-semibold text-on-surface-variant ml-1">
                Tipo de Usuario
              </label>
              <div className="grid grid-cols-2 p-1 bg-surface-container rounded-lg gap-1 border border-outline-variant">
                <button
                  type="button"
                  onClick={() => setRole('doctor')}
                  className={`transition-soft text-sm font-semibold py-2 rounded-lg flex items-center justify-center gap-2 ${
                    role === 'doctor'
                      ? 'bg-white text-primary clinical-shadow border border-accent-gold'
                      : 'text-on-surface-variant hover:bg-surface-container-high'
                  }`}
                >
                  <span className="material-symbols-outlined text-[18px]">medical_services</span>
                  Soy Médico
                </button>
                <button
                  type="button"
                  onClick={() => setRole('nurse')}
                  className={`transition-soft text-sm font-semibold py-2 rounded-lg flex items-center justify-center gap-2 ${
                    role === 'nurse'
                      ? 'bg-white text-primary clinical-shadow border border-accent-gold'
                      : 'text-on-surface-variant hover:bg-surface-container-high'
                  }`}
                >
                  <span className="material-symbols-outlined text-[18px]">person_play</span>
                  Soy Enfermero
                </button>
              </div>
            </div>

            {/* DNI / Usuario */}
            <div className="space-y-1">
              <label className="text-sm font-semibold text-on-surface-variant ml-1" htmlFor="dni">
                DNI / Usuario
              </label>
              <div className="relative group">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline group-focus-within:text-primary transition-colors">
                  badge
                </span>
                <input
                  id="dni"
                  type="text"
                  maxLength={8}
                  value={dni}
                  onChange={(e) => setDni(e.target.value.replace(/\D/g, ''))}
                  placeholder="Ej: 12345678"
                  className="w-full pl-10 pr-4 py-3 bg-white border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary focus:border-primary text-sm outline-none transition-soft"
                />
              </div>
            </div>

            {/* Contraseña */}
            <div className="space-y-1">
              <div className="flex justify-between items-center px-1">
                <label className="text-sm font-semibold text-on-surface-variant" htmlFor="password">
                  Contraseña
                </label>
                <a className="text-xs text-primary hover:underline" href="#">
                  ¿Olvidó su clave?
                </a>
              </div>
              <div className="relative group">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline group-focus-within:text-primary transition-colors">
                  lock
                </span>
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-12 py-3 bg-white border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary focus:border-primary text-sm outline-none transition-soft"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-outline hover:text-on-surface transition-colors"
                >
                  <span className="material-symbols-outlined">
                    {showPassword ? 'visibility_off' : 'visibility'}
                  </span>
                </button>
              </div>
            </div>

            {/* Mensaje de Error */}
            {error && (
              <p className="text-xs text-error font-semibold px-1">
                {error}
              </p>
            )}

            {/* Mantener sesión iniciada */}
            <div className="flex items-center px-1">
              <input
                id="remember"
                type="checkbox"
                className="w-4 h-4 text-primary border-outline-variant rounded focus:ring-primary"
              />
              <label
                className="ml-2 text-sm text-on-surface-variant cursor-pointer select-none"
                htmlFor="remember"
              >
                Mantener sesión iniciada
              </label>
            </div>

            {/* Botón de Enviar */}
            <button
              type="submit"
              className="w-full bg-primary hover:bg-primary-container text-white hover:text-white font-semibold py-4 rounded-lg flex items-center justify-center gap-2 clinical-shadow transition-soft active:scale-[0.98]"
            >
              Iniciar Sesión
              <span className="material-symbols-outlined">login</span>
            </button>
          </form>
        </div>

        {/* Footer Help */}
        <footer className="mt-6 flex flex-col items-center gap-2">
          <p className="text-xs text-outline text-center">
            © 2024 Centro de Monitoreo Médico. Todos los derechos reservados.
          </p>
          <div className="flex gap-4">
            <a className="text-xs text-on-surface-variant hover:text-primary transition-colors" href="#">
              Soporte Técnico
            </a>
            <span className="text-outline-variant">|</span>
            <a className="text-xs text-on-surface-variant hover:text-primary transition-colors" href="#">
              Política de Privacidad
            </a>
          </div>
        </footer>
      </div>

      {/* Ilustración de Fondo */}
      <div className="hidden lg:block fixed left-12 bottom-12 w-48 h-48 opacity-20 pointer-events-none">
        <div
          className="w-full h-full bg-contain bg-no-repeat bg-center"
          style={{
            backgroundImage: `url('https://lh3.googleusercontent.com/aida-public/AB6AXuBG56UvPbdOv-fb5lgYt0NNdgJgG6Gkr4PpZ8pQrjzxU5pz3CVwBH0ABOp_L1jBA02m5j_KWDl0293_uiJaTY2BWIIIT3_DNVUCcebMbzaANao-E15dc-yNFdhevhhLZ1LWoVWdqNS2C89Yi-AGgq8kZaV-HLoiMSz0N4x4Tml32XVYY8-IMwfLTUhOXIYCgwO2W5pIidMk-S3aK7VNlOOeR1FHFqW-eAID3MG3w08mNO_ftI93cIiQ-KneVbkuGeFylm1Ma9Ra5Aw')`
          }}
        ></div>
      </div>
    </main>
  )
}

export default Login
