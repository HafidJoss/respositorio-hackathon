import { Usuario, Paciente, UsuarioPaciente, Triaje } from '../types';

const API_BASE = '/api';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
  });

  if (!response.ok) {
    let errorMessage = `HTTP error! Status: ${response.status}`;
    try {
      const errorData = await response.json();
      if (errorData?.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      // Ignorar fallo al parsear JSON de error
    }
    throw new Error(errorMessage);
  }

  return response.json() as Promise<T>;
}

export const api = {
  // --- Módulo registro-pacientes ---
  
  /**
   * Registra un nuevo usuario en el sistema.
   * POST /usuarios
   */
  crearUsuario: (dni: string, telefono: string): Promise<Usuario> => {
    return request<Usuario>('/usuarios', {
      method: 'POST',
      body: JSON.stringify({ dni, telefono }),
    });
  },

  /**
   * Obtiene la información de un usuario específico.
   * GET /usuarios/{usuario_id}
   */
  obtenerUsuario: (usuarioId: string): Promise<Usuario> => {
    return request<Usuario>(`/usuarios/${usuarioId}`);
  },

  /**
   * Registra un nuevo paciente (o lo vincula si ya existe su DNI).
   * POST /pacientes
   */
  registrarPaciente: (params: {
    dni: string;
    nombres: string;
    apellidos: string;
    edad: number;
    jurisdiccion_sis: string;
    usuario_id: string;
    tipo_relacion: string;
  }): Promise<Paciente & { ya_existia: boolean }> => {
    return request<Paciente & { ya_existia: boolean }>('/pacientes', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  },

  /**
   * Busca un paciente por su DNI. Retorna 404 si no existe.
   * GET /pacientes?dni={dni}
   */
  buscarPacientePorDni: (dni: string): Promise<Paciente> => {
    return request<Paciente>(`/pacientes?dni=${encodeURIComponent(dni)}`);
  },

  /**
   * Vincula un paciente existente a otro usuario.
   * POST /usuarios/{usuario_id}/pacientes
   */
  vincularPacienteExistente: (
    usuarioId: string,
    pacienteId: string,
    tipoRelacion: string
  ): Promise<UsuarioPaciente> => {
    return request<UsuarioPaciente>(`/usuarios/${usuarioId}/pacientes`, {
      method: 'POST',
      body: JSON.stringify({ paciente_id: pacienteId, tipo_relacion: tipoRelacion }),
    });
  },

  /**
   * Lista todos los pacientes vinculados a un usuario.
   * GET /usuarios/{usuario_id}/pacientes
   */
  listarPacientesDeUsuario: (usuarioId: string): Promise<UsuarioPaciente[]> => {
    return request<UsuarioPaciente[]>(`/usuarios/${usuarioId}/pacientes`);
  },

  // --- Módulo triaje ---

  /**
   * Registra un nuevo triaje para un paciente.
   * POST /triajes
   */
  registrarTriaje: (params: {
    paciente_id: string;
    nombres: string;
    apellidos: string;
    dni: string;
    edad: number;
    peso: number;
    talla: number;
    presion_arterial: string;
    sintomas: string[];
    nivel_atencion: string;
  }): Promise<Triaje> => {
    return request<Triaje>('/triajes', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  },

  /**
   * Obtiene un registro de triaje por su ID.
   * GET /triajes/{triaje_id}
   */
  obtenerTriaje: (triajeId: string): Promise<Triaje> => {
    return request<Triaje>(`/triajes/${triajeId}`);
  },

  /**
   * Lista el historial de triajes de un paciente específico.
   * GET /pacientes/{paciente_id}/triajes
   */
  listarTriajesDePaciente: (pacienteId: string): Promise<Triaje[]> => {
    return request<Triaje[]>(`/pacientes/${pacienteId}/triajes`);
  },

  /**
   * Obtiene el catálogo estático de síntomas comunes.
   * GET /sintomas-comunes
   */
  listarSintomasComunes: (): Promise<string[]> => {
    return request<string[]>('/sintomas-comunes');
  },
};
