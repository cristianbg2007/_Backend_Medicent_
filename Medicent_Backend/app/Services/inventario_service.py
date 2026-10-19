from datetime import date
from app.database.database import db
from app.models.stock_disponible import StockDisponible
from app.models.medicamento import Medicamento

class InventarioService:
    @staticmethod
    def obtener_inventario_paciente(id_paciente):
        return StockDisponible.query.all()

    @staticmethod
    def recargar_stock(id_paciente, id_medicamento, cantidad, fecha_vencimiento=None):
        med = Medicamento.query.get(id_medicamento)
        
        stock_item = None
        if med and getattr(med, 'stock_disponible', None):
            stock_item = med.stock_disponible
        else:
            stock_item = StockDisponible.query.get(id_medicamento)

        if not stock_item:
            stock_item = StockDisponible(
                fechaActualizacion=date.today(),
                cantidadFrascos=1,
                cantidadPastillas=int(cantidad)
            )
            db.session.add(stock_item)
            if med:
                med.stock_disponible = stock_item
        else:
            stock_item.cantidadPastillas = (stock_item.cantidadPastillas or 0) + int(cantidad)
            stock_item.fechaActualizacion = date.today()

        db.session.commit()
        return stock_item