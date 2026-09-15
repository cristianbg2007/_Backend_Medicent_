from datetime import date, time
from app import create_app
from app.database.database import db, bcrypt  # <-- Agregamos bcrypt aquí
from app.models.usuario import Usuario
from app.models.administrador import Administrador
from app.models.tipo_documento import TipoDocumento
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
        
        # --- 1. Crear tablas faltantes (Tu código) ---
        db.create_all()

        # --- 2. Crear Tipo de Documento (Código de tu compañero) ---
        tipo_cc = TipoDocumento.query.filter_by(nombre='Cédula de Ciudadanía').first()
        if tipo_cc is None:
            tipo_cc = TipoDocumento(nombre='Cédula de Ciudadanía')
            db.session.add(tipo_cc)
            db.session.commit()
            print("📁 Tipo de documento creado.")

        # --- 3. Crear el usuario Admin (Código de tu compañero) ---
        admin_existente = Usuario.query.filter_by(correo='adminmedicent@gmail.com').first()
        if admin_existente is None:
            admin_usuario = Usuario(
                nombre='Admin',
                apellido='Medicent',
                documento='123456789',
                correo='adminmedicent@gmail.com',
                telefono='3001234567',
                fechaNacimiento=date(2000, 1, 1),
                password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                idTipoDocumento=tipo_cc.idTipoDocumento
            )
            db.session.add(admin_usuario)
            db.session.commit()
            print("👤 Usuario Admin creado exitosamente.")
        else:
            admin_usuario = admin_existente
            print("ℹ️ El usuario Admin ya existe.")

        # --- 4. Asignar Rol Administrador (Código de tu compañero) ---
        admin_rol = Administrador.query.filter_by(idUsuario=admin_usuario.idUsuario).first()
        if admin_rol is None:
            nuevo_admin = Administrador(
                nombre='Admin',
                apellido='Medicent',
                correo='adminmedicent@gmail.com',
                telefono='3001234567',
                idUsuario=admin_usuario.idUsuario
            )
            db.session.add(nuevo_admin)
            db.session.commit()
            print("🔑 Rol de Administrador asignado correctamente.")
        else:
            print("ℹ️ El rol de Administrador ya estaba asignado.")

        # --- 5. Crear el Paciente vinculado (Tu código adaptado) ---
        # Ahora usamos directamente el ID del admin que tu compañero creó arriba
        paciente = Paciente.query.filter_by(idUsuario=admin_usuario.idUsuario).first()
        if not paciente:
            paciente = Paciente(
                estatura=1.75,
                peso=70.5,
                tipoSangre=TipoSangreEnum.A_POSITIVO,
                dieta="Balanceada",
                idUsuario=admin_usuario.idUsuario
            )
            db.session.add(paciente)
            db.session.commit()
            print("❤️ Paciente de prueba creado y vinculado al usuario admin.")
        else:
            print(f"ℹ️ El paciente ya existe (ID: {paciente.idPaciente}), reutilizándolo...")

        # --- 6. Crear catálogos médicos (Tu código) ---
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

        # --- 7. Crear Tratamiento (Tu código) ---
        tratamiento = Tratamiento.query.filter_by(idPaciente=paciente.idPaciente).first()
        if not tratamiento:
            tratamiento = Tratamiento(
                fechaInicio=date(2026, 1, 1),
                fechaFin=date(2027, 12, 31),
                idPaciente=paciente.idPaciente
            )
            db.session.add(tratamiento)
            db.session.commit()
            print(f"💊 Tratamiento creado (ID: {tratamiento.idTratamiento}).")
        else:
            print(f"ℹ️ El tratamiento ya existe (ID: {tratamiento.idTratamiento}), reutilizándolo...")

        # --- 8. Crear Medicamento (Tu código) ---
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
            print("🧪 Medicamento de prueba creado con éxito.")
        else:
            print("ℹ️ El medicamento ya existe, omitiendo creación...")

        # --- 9. Crear Biomarcador (Tu código) ---
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
            print("📊 Biomarcador de prueba creado con éxito.")
        else:
            print("ℹ️ El biomarcador ya existe, omitiendo creación...")

if __name__ == "__main__":
    run_seed()