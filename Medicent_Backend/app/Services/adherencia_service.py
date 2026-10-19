from datetime import date
from app.database.database import db
from app.models.adherencia import Adherencia
from app.models.toma import Toma

class AdherenciaService:
    @staticmethod
    def calcular_y_registrar(id_tratamiento, fecha_inicio_str, fecha_fin_str):
        # 1. Consulta tomas registradas para calcular el porcentaje real
        tomas = Toma.query.all()
        if tomas:
            total_programadas = len(tomas)
            total_realizadas = len([t for t in tomas if str(getattr(t, 'estado', '')).lower() == 'tomada'])
            porcentaje = round((total_realizadas / total_programadas) * 100, 2)
        else:
            porcentaje = 100.0

        # 2. Se instancia únicamente con los atributos existentes en la tabla
        reporte = Adherencia(
            idPaciente=1,
            fechaGeneracion=date.today(),
            porcentaje=porcentaje
        )
        db.session.add(reporte)
        db.session.commit()
        return reporte

    @staticmethod
    def obtener_ultimo_reporte(id_paciente):
        return Adherencia.query.filter_by(idPaciente=id_paciente).order_by(Adherencia.idAdherencia.desc()).first()

    @staticmethod
    def obtener_historial_tratamiento(id_tratamiento):
        return Adherencia.query.order_by(Adherencia.idAdherencia.desc()).all()