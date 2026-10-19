from app.database.database import db

class StockDisponible(db.Model):
    __tablename__ = 'stock_disponible'

    idStock = db.Column(db.Integer, primary_key=True)
    fechaActualizacion = db.Column(db.Date, nullable=False)
    cantidadFrascos = db.Column(db.Integer, nullable=False, default=0)
    cantidadPastillas = db.Column(db.Integer, nullable=False, default=0)

    medicamentos = db.relationship('Medicamento', backref='stock_disponible', lazy=True)

    def to_dict(self):
        id_med = self.idStock
        nombre_med = f"Medicamento #{self.idStock}"

        if self.medicamentos and len(self.medicamentos) > 0:
            med = self.medicamentos[0]
            id_med = getattr(med, 'idMedicamento', self.idStock)
            # Intenta leer nombreMedicamento o nombre según esté definido en Medicamento
            nombre_med = getattr(med, 'nombreMedicamento', None) or getattr(med, 'nombre', f"Medicamento #{id_med}")

        return {
            "id_inventario": self.idStock,
            "id_paciente": 1,
            "id_medicamento": id_med,
            "nombre_medicamento": nombre_med,
            "cantidad_actual": self.cantidadPastillas,
            "fecha_vencimiento_lote": str(self.fechaActualizacion) if self.fechaActualizacion else None,
            "alerta_stock_minimo": 5,
            "es_bajo_stock": self.cantidadPastillas <= 5
        }