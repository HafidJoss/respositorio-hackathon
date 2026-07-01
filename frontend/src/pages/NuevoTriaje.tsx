import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Paciente, NivelAtencion } from '../types';

interface NuevoTriajeProps {
  paciente: Paciente;
  onBack: () => void;
  onSuccess: () => void;
}

const NuevoTriaje: React.FC<NuevoTriajeProps> = ({ paciente, onBack, onSuccess }) => {
  const [sintomasCatalogo, setSintomasCatalogo] = useState<string[]>([]);
  const [loadingCatalogo, setLoadingCatalogo] = useState(false);
  
  // Datos del Formulario
  const [peso, setPeso] = useState('');
  const [talla, setTalla] = useState('');
  const [presionArterial, setPresionArterial] = useState('');
  const [sintomasSeleccionados, setSintomasSeleccionados] = useState<string[]>([]);
  const [otroSintoma, setOtroSintoma] = useState('');
  const [nivelAtencion, setNivelAtencion] = useState<NivelAtencion | ''>('');
  
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Cargar catálogo de síntomas comunes
  useEffect(() => {
    const fetchSintomas = async () => {
      setLoadingCatalogo(true);
      try {
        const sintomas = await api.listarSintomasComunes();
        setSintomasCatalogo(sintomas);
      } catch (err: any) {
        console.error('Error al cargar catálogo de síntomas', err);
        // Fallback local por si el backend no está iniciado o está vacío
        setSintomasCatalogo([
          'fiebre', 'tos', 'dolor de cabeza', 'dolor abdominal',
          'dolor de pecho', 'dificultad para respirar', 'mareo', 'nausea'
        ]);
      } finally {
        setLoadingCatalogo(false);
      }
    };
    fetchSintomas();
  }, []);

  const toggleSintoma = (sintoma: string) => {
    if (sintomasSeleccionados.includes(sintoma)) {
      setSintomasSeleccionados(sintomasSeleccionados.filter(s => s !== sintoma));
    } else {
      setSintomasSeleccionados([...sintomasSeleccionados, sintoma]);
    }
  };

  const handleAddOtroSintoma = (e: React.FormEvent) => {
    e.preventDefault();
    const cleanSintoma = otroSintoma.trim().toLowerCase();
    if (cleanSintoma && !sintomasSeleccionados.includes(cleanSintoma)) {
      setSintomasSeleccionados([...sintomasSeleccionados, cleanSintoma]);
      setOtroSintoma('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validaciones de negocio (.orquestador)
    if (!peso || parseFloat(peso) <= 0) {
      setError('Por favor ingrese un peso válido (mayor a 0 kg).');
      return;
    }
    if (!talla || parseFloat(talla) <= 0) {
      setError('Por favor ingrese una talla válida (mayor a 0 m).');
      return;
    }
    // Formato de Presión Arterial: ej. "120/80"
    const presionRegex = /^\d{2,3}\/\d{2,3}$/;
    if (!presionRegex.test(presionArterial)) {
      setError('La presión arterial debe tener un formato válido. Ej: 120/80');
      return;
    }
    if (!nivelAtencion) {
      setError('Debe seleccionar manualmente un nivel de urgencia/atención.');
      return;
    }

    setLoading(true);
    try {
      await api.registrarTriaje({
        paciente_id: paciente.id,
        nombres: paciente.nombres,
        apellidos: paciente.apellidos,
        dni: paciente.dni,
        edad: paciente.edad,
        peso: parseFloat(peso),
        talla: parseFloat(talla),
        presion_arterial: presionArterial,
        sintomas: sintomasSeleccionados,
        nivel_atencion: nivelAtencion,
      });

      alert('¡Registro de triaje completado exitosamente!');
      onSuccess();
    } catch (err: any) {
      setError(err.message || 'Error al guardar el triaje.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-on-surface p-4 flex items-center justify-center">
      <div className="w-full max-w-lg bg-surface-container-lowest border border-outline-variant rounded-xl p-6 clinical-shadow relative z-10">
        
        {/* Header */}
        <div className="flex items-center justify-between mb-6 border-b border-surface-container-highest pb-3">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-[28px] filled">medical_services</span>
            <h2 className="text-xl font-bold text-primary">Registrar Nuevo Triaje</h2>
          </div>
          <button 
            onClick={onBack}
            className="text-on-surface-variant hover:text-primary transition-colors flex items-center gap-1 text-sm font-semibold"
          >
            <span className="material-symbols-outlined text-[18px]">arrow_back</span>
            Cancelar
          </button>
        </div>

        {/* Datos del Paciente (Solo Lectura) */}
        <div className="bg-surface-container-low p-4 rounded-xl border border-outline-variant mb-5 flex flex-col gap-1 text-sm">
          <p className="text-xs uppercase tracking-wider text-on-surface-variant font-bold">Paciente Activo</p>
          <h3 className="text-base font-bold text-primary">
            {paciente.nombres} {paciente.apellidos}
          </h3>
          <div className="grid grid-cols-2 gap-2 text-xs text-on-surface-variant mt-1">
            <div><strong className="text-on-surface">DNI:</strong> {paciente.dni}</div>
            <div><strong className="text-on-surface">Edad:</strong> {paciente.edad} años</div>
            <div className="col-span-2"><strong className="text-on-surface">SIS/Jurisdicción:</strong> {paciente.jurisdiccion_sis}</div>
          </div>
        </div>

        {/* Errores */}
        {error && (
          <div className="bg-error-container text-on-error-container p-3 rounded-lg text-sm mb-4 font-semibold">
            {error}
          </div>
        )}

        {/* Formulario */}
        <form onSubmit={handleSubmit} className="space-y-4">
          
          {/* Signos Vitales */}
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="text-xs font-bold text-on-surface-variant" htmlFor="peso">
                Peso (kg)
              </label>
              <input
                id="peso"
                type="number"
                step="0.1"
                min="0"
                value={peso}
                onChange={(e) => setPeso(e.target.value)}
                placeholder="Ej: 70.5"
                className="w-full px-3 py-2 border border-outline-variant rounded-lg outline-none text-sm focus:ring-2 focus:ring-primary focus:border-primary"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-bold text-on-surface-variant" htmlFor="talla">
                Talla (m)
              </label>
              <input
                id="talla"
                type="number"
                step="0.01"
                min="0"
                value={talla}
                onChange={(e) => setTalla(e.target.value)}
                placeholder="Ej: 1.75"
                className="w-full px-3 py-2 border border-outline-variant rounded-lg outline-none text-sm focus:ring-2 focus:ring-primary focus:border-primary"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-on-surface-variant" htmlFor="presion">
              Presión Arterial (PA)
            </label>
            <input
              id="presion"
              type="text"
              value={presionArterial}
              onChange={(e) => setPresionArterial(e.target.value)}
              placeholder="Ej: 120/80"
              className="w-full px-3 py-2 border border-outline-variant rounded-lg outline-none text-sm focus:ring-2 focus:ring-primary focus:border-primary"
            />
          </div>

          {/* Selección de Síntomas */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-on-surface-variant">
              Síntomas del Paciente
            </label>
            {loadingCatalogo ? (
              <p className="text-xs text-outline">Cargando síntomas...</p>
            ) : (
              <div className="flex flex-wrap gap-1.5 max-h-36 overflow-y-auto p-1 bg-surface-container rounded-lg border border-outline-variant">
                {sintomasCatalogo.map((sintoma) => {
                  const selected = sintomasSeleccionados.includes(sintoma);
                  return (
                    <button
                      key={sintoma}
                      type="button"
                      onClick={() => toggleSintoma(sintoma)}
                      className={`px-3 py-1 rounded-full text-xs font-semibold transition-all ${
                        selected 
                          ? 'bg-primary text-white clinical-shadow border border-primary'
                          : 'bg-white text-on-surface-variant border border-outline-variant hover:bg-surface-container-high'
                      }`}
                    >
                      {sintoma}
                    </button>
                  );
                })}
              </div>
            )}

            {/* Agregar Otro Síntoma */}
            <div className="flex gap-2">
              <input
                type="text"
                value={otroSintoma}
                onChange={(e) => setOtroSintoma(e.target.value)}
                placeholder="Añadir otro síntoma..."
                className="flex-grow px-3 py-1.5 border border-outline-variant rounded-lg outline-none text-xs"
              />
              <button
                type="button"
                onClick={handleAddOtroSintoma}
                className="bg-white border border-outline text-on-surface-variant hover:text-primary font-bold px-3 rounded-lg text-xs"
              >
                Agregar
              </button>
            </div>
          </div>

          {/* Nivel de Atención Manual */}
          <div className="space-y-1">
            <label className="text-xs font-bold text-on-surface-variant ml-1">
              Clasificación de Nivel de Atención (Manualmente por Enfermero)
            </label>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => setNivelAtencion('critico')}
                className={`py-2 rounded-lg text-xs font-bold transition-all border ${
                  nivelAtencion === 'critico'
                    ? 'bg-error text-white border-error ring-2 ring-error'
                    : 'bg-white text-error border-error/30 hover:bg-error-container/10'
                }`}
              >
                CRÍTICO (Rojo)
              </button>
              <button
                type="button"
                onClick={() => setNivelAtencion('moderado')}
                className={`py-2 rounded-lg text-xs font-bold transition-all border ${
                  nivelAtencion === 'moderado'
                    ? 'bg-orange-500 text-white border-orange-500 ring-2 ring-orange-500'
                    : 'bg-white text-orange-600 border-orange-200 hover:bg-orange-100/30'
                }`}
              >
                MODERADO (Naranja)
              </button>
              <button
                type="button"
                onClick={() => setNivelAtencion('leve')}
                className={`py-2 rounded-lg text-xs font-bold transition-all border ${
                  nivelAtencion === 'leve'
                    ? 'bg-green-600 text-white border-green-600 ring-2 ring-green-600'
                    : 'bg-white text-green-600 border-green-200 hover:bg-green-100/30'
                }`}
              >
                LEVE (Verde)
              </button>
            </div>
          </div>

          {/* Enviar */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary text-white hover:bg-primary-container font-bold py-3.5 rounded-lg flex items-center justify-center gap-2 clinical-shadow transition-soft active:scale-[0.98] text-sm"
          >
            {loading ? 'Registrando Triaje...' : 'Guardar y Confirmar Registro'}
            <span className="material-symbols-outlined">save_alt</span>
          </button>

        </form>
      </div>
    </div>
  );
};

export default NuevoTriaje;
