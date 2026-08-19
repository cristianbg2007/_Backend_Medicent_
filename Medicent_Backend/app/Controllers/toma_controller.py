from flask import request, jsonify
from app.models.toma import Toma
from app.database.database import db
from datetime import datetime, date

class TomaController:

    @staticmethod
    def crear_toma():
        data = request.get_json()
        try:
            nueva_toma = Toma(
                fecha=date.fromisoformat(data.get('fecha')),
                hora=datetime.strptime(data.get('hora'), '%H:%M').time(),
                dosis=data.get('dosis'),
                nota=data.get('nota', ''),
                estado=data.get('estado', 'tomado'),
                idMedicamento=data.get('idMedicamento'),
                idPaciente=data.get('idPaciente')
            )
            db.session.add(nueva_toma)
            db.session.commit()
            return jsonify({"message": "Toma registrada exitosamente"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 400

    @staticmethod
    def get_tomas():
        fecha = request.args.get('fecha')
        if fecha:
            tomas = Toma.query.filter_by(fecha=date.fromisoformat(fecha)).all()
        else:
            tomas = Toma.query.all()

        return jsonify([
            {
                "id": t.idToma,
                "fecha": str(t.fecha),
                "hora": str(t.hora),
                "dosis": t.dosis,
                "nota": t.nota,
                "estado": t.estado,
                "medicamento": t.medicamento.nombre if t.medicamento else '',
                "via": t.medicamento.idViaAdministracion if t.medicamento else ''
            }
            for t in tomas
        ]), 200