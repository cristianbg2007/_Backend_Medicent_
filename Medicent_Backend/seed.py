from datetime import date, time
from app import create_app
from app.database.database import db
from app.models.usuario import Usuario
from app.models.paciente import Paciente, TipoSangreEnum
from app.models.tratamiento import Tratamiento
from app.models.medicamento import Medicamento
from app.models.tipo_medicamento import TipoMedicamento
from app.models.via_administracion import ViaAdministracion
from app.models.stock_disponible import StockDisponible
from app.models.biomarcador import Biomarcador

app = create_app()

def run_seed():
    with app.app_context():
        
        # --- ESTA ES LA LÍNEA AGREGADA ---
        # Fuerza a SQLAlchemy a crear las tablas que falten en MySQL (como 'biomarcador')
        db.create_all()
        # ---------------------------------

        # 1. Verificar que exista al menos un usuario (protegiendo el admin existente)
        usuario = Usuario.query.first()
        if not usuario:
            print(" No se encontró ningún usuario en la base de datos. Por favor crea tu usuario administrador primero.")
            return
        else:
            print(f"Usuario detectado: {usuario.nombre} {usuario.apellido} (ID: {usuario.idUsuario}). ¡Admin protegido!")

        # 2. Verificar o crear el Paciente vinculado a ese usuario
        paciente = Paciente.query.filter_by(idUsuario=usuario.idUsuario).first()
        if not paciente:
            paciente = Paciente(
                estatura=1.75,
                peso=70.5,
                tipoSangre=TipoSangreEnum.A_POSITIVO,
                dieta="Balanceada",
                idUsuario=usuario.idUsuario
            )
            db.session.add(paciente)
            db.session.commit()
            print(" Paciente de prueba creado y vinculado al usuario.")
        else:
            print(f"El paciente ya existe (ID: {paciente.idPaciente}), reutilizándolo...")

        # 3. Verificar o crear catálogos previos (TipoMedicamento, ViaAdministracion, StockDisponible)
        tipo_med = TipoMedicamento.query.first()
        if not tipo_med:
            tipo_med = TipoMedicamento(nombre="Analgésico", descripcion="Medicamentos para el dolor")
            db.session.add(tipo_med)
            db.session.commit()

        via_admin = ViaAdministracion.query.first()
        if not via_admin:
            via_admin = ViaAdministracion(nombre="Oral", descripcion="Administración por vía oral")
            db.session.add(via_admin)
            db.session.commit()

        stock = StockDisponible.query.first()
        if not stock:
            stock = StockDisponible(
                fechaActualizacion=date.today(),
                cantidadFrascos=5,
                cantidadPastillas=50
            )
            db.session.add(stock)
            db.session.commit()

        # 4. Verificar o crear Tratamiento para el paciente
        tratamiento = Tratamiento.query.filter_by(idPaciente=paciente.idPaciente).first()
        if not tratamiento:
            tratamiento = Tratamiento(
                fechaInicio=date(2026, 1, 1),
                fechaFin=date(2027, 12, 31),
                idPaciente=paciente.idPaciente
            )
            db.session.add(tratamiento)
            db.session.commit()
            print(f"Tratamiento creado (ID: {tratamiento.idTratamiento}).")
        else:
            print(f"ℹEl tratamiento ya existe (ID: {tratamiento.idTratamiento}), reutilizándolo...")

        # 5. Verificar o crear Medicamento de prueba
        medicamento = Medicamento.query.filter_by(idTratamiento=tratamiento.idTratamiento).first()
        if not medicamento:
            medicamento = Medicamento(
                nombre="Paracetamol",
                concentracion=500.0,
                frecuenciaDiaria=2,
                fechaVencimiento=date(2027, 12, 31),
                idTratamiento=tratamiento.idTratamiento,
                idTipoMedicamento=tipo_med.idTipoMedicamento,
                idViaAdministracion=via_admin.idViaAdministracion,
                idStock=stock.idStock
            )
            db.session.add(medicamento)
            db.session.commit()
            print("Medicamento de prueba creado con éxito.")
        else:
            print("El medicamento ya existe, omitiendo creación...")

        # 6. Verificar o crear Biomarcador de prueba
        biomarcador = Biomarcador.query.filter_by(idPaciente=paciente.idPaciente).first()
        if not biomarcador:
            biomarcador = Biomarcador(
                tipo="Presión",
                nombre="Presión Arterial",
                valor=120.0,
                unidad="mmHg",
                fecha=date(2026, 9, 7),
                hora=time(8, 0),
                estado="bueno",
                notas="Control matutino automático",
                idPaciente=paciente.idPaciente
            )
            db.session.add(biomarcador)
            db.session.commit()
            print(" Biomarcador de prueba creado con éxito.")
        else:
            print(" El biomarcador ya existe, omitiendo creación...")

if __name__ == "__main__":
    run_seed()