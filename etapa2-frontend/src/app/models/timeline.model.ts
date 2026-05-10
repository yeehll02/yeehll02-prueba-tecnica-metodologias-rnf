export interface Timeline {
  conteo_mensual: { [month: string]: number };
  promedio_mensual: number;
  umbral_pico: number;
  meses_pico: string[];
}
