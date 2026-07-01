export interface Usuario {
  id: string; // UUID
  dni: string; // exactamente 8 dígitos
  telefono: string; // formato +51 9XXXXXXXX
  fecha_registro: string;
}

export type RolPersonal = 'medico' | 'enfermero';

export interface Personal {
  id: string; // UUID
  dni: string; // exactamente 8 dígitos
  nombre: string;
  rol: RolPersonal;
  fecha_registro: string;
}

export interface Paciente {
  id: string; // UUID
  dni: string; // exactamente 8 dígitos
  nombres: string;
  apellidos: string;
  edad: number;
  jurisdiccion_sis: string;
  fecha_registro: string;
}

export type TipoRelacion = 'titular' | 'madre' | 'padre' | 'tutor_legal' | 'otro';

export interface UsuarioPaciente {
  id: string; // UUID
  usuario_id: string;
  paciente_id: string;
  tipo_relacion: TipoRelacion;
  vigente: boolean;
  fecha_vinculacion: string;
}

export type NivelAtencion = 'critico' | 'moderado' | 'leve';

export interface Triaje {
  id: string; // UUID
  paciente_id: string;
  peso: number;
  talla: number;
  presion_arterial: string;
  sintomas: string[];
  nivel_atencion: NivelAtencion;
  fecha_registro: string;
}

export interface SintomaComun {
  id: string;
  nombre: string;
}
