from app.database.database import db
from app.models.toma import Toma

class Adherencia(db.Model):
    __tablename__ = 'adherencia'

    idAdherencia = db.Column(db.Integer, primary_key=True)
    fechaGeneracion = db.Column(db.Date, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    
    idPaciente = db.Column(db.Integer, db.ForeignKey('paciente.idPaciente'), nullable=False)

    def to_dict(self):
        pct = float(self.porcentaje)
        obs = "Adherencia adecuada" if pct >= 80 else "Adherencia irregular, requiere seguimiento"
        fecha_str = str(self.fechaGeneracion) if self.fechaGeneracion else ""
        
        # Conteo dinámico real basado en la tabla de tomas
        total_tomas = Toma.query.count()
        total_programadas = total_tomas if total_tomas > 0 else 0
        total_realizadas = int(round((pct / 100.0) * total_programadas)) if total_programadas > 0 else 0

        return {
            "idAdherencia": self.idAdherencia,
            "idPaciente": self.idPaciente,
            "idTratamiento": 1,
            "fechaGeneracion": fecha_str,
            "periodoInicio": fecha_str,
            "periodoFin": fecha_str,
            "totalProgramadas": total_programadas,
            "totalRealizadas": total_realizadas,
            "porcentaje": pct,
            "observaciones": obs
        }