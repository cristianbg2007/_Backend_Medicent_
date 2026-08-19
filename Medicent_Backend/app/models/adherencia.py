from app.database.database import db

class Adherencia(db.Model):
    __tablename__ = 'adherencia'

    idAdherencia = db.Column(db.Integer, primary_key=True)
    fechaGeneracion = db.Column(db.Date, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)
    
    idPaciente = db.Column(db.Integer, db.ForeignKey('paciente.idPaciente'), nullable=False)