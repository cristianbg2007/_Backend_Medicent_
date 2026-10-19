from flask import Blueprint, request, jsonify
from app.Controllers.auth_controller import AuthController
from app.Controllers.medicamento_controller import MedicamentoController
from app.Controllers.toma_controller import TomaController
from app.Controllers.biomarcador_controller import BiomarcadorController
from app.Controllers.admin_controller import AdminController
from app.Services.inventario_service import InventarioService
from app.Services.adherencia_service import AdherenciaService

auth_bp = Blueprint("auth", __name__)

# ========== AUTENTICACIÓN ==========
auth_bp.route("/login", methods=["POST"])(AuthController.login)
auth_bp.route("/register", methods=["POST"])(AuthController.register)

# ========== MEDICAMENTOS ==========
auth_bp.route("/medicamentos", methods=["GET"])(MedicamentoController.get_medicamentos)
auth_bp.route("/medicamentos", methods=["POST"])(MedicamentoController.crear_medicamento)

# ========== TOMAS ==========
auth_bp.route("/tomas", methods=["GET"])(TomaController.get_tomas)
auth_bp.route("/tomas", methods=["POST"])(TomaController.crear_toma)

# ========== BIOMARCADORES ==========
auth_bp.route("/biomarcadores", methods=["GET"])(BiomarcadorController.get_biomarcadores)
auth_bp.route("/biomarcadores", methods=["POST"])(BiomarcadorController.crear_biomarcador)

# ========== RUTAS DE ADMINISTRADOR ==========
# Usuarios
auth_bp.route("/admin/usuarios", methods=["GET"], endpoint="admin_get_usuarios")(AdminController.get_usuarios)
auth_bp.route("/admin/usuarios/<int:id>", methods=["GET"], endpoint="admin_get_usuario")(AdminController.get_usuario)
auth_bp.route("/admin/usuarios/<int:id>", methods=["PUT"], endpoint="admin_actualizar_usuario")(AdminController.actualizar_usuario)
auth_bp.route("/admin/usuarios/<int:id>", methods=["DELETE"], endpoint="admin_eliminar_usuario")(AdminController.eliminar_usuario)

# Medicamentos
auth_bp.route("/admin/medicamentos", methods=["GET"], endpoint="admin_get_medicamentos")(AdminController.get_medicamentos)
auth_bp.route("/admin/medicamentos/<int:id>", methods=["PUT"], endpoint="admin_actualizar_medicamento")(AdminController.actualizar_medicamento)
auth_bp.route("/admin/medicamentos/<int:id>", methods=["DELETE"], endpoint="admin_eliminar_medicamento")(AdminController.eliminar_medicamento)

# Biomarcadores
auth_bp.route("/admin/biomarcadores", methods=["GET"], endpoint="admin_get_biomarcadores")(AdminController.get_biomarcadores)
auth_bp.route("/admin/biomarcadores/<int:id>", methods=["PUT"], endpoint="admin_actualizar_biomarcador")(AdminController.actualizar_biomarcador)
auth_bp.route("/admin/biomarcadores/<int:id>", methods=["DELETE"], endpoint="admin_eliminar_biomarcador")(AdminController.eliminar_biomarcador)

# ========== INVENTARIO PERSONAL ==========
@auth_bp.route("/inventario/<int:id_paciente>", methods=["GET"])
def get_inventario_paciente(id_paciente):
    try:
        items = InventarioService.obtener_inventario_paciente(id_paciente)
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/inventario/recargar", methods=["POST"])
def recargar_inventario():
    data = request.get_json() or {}
    try:
        id_paciente = data.get("id_paciente")
        id_medicamento = data.get("id_medicamento")
        cantidad = data.get("cantidad")
        fecha_vencimiento = data.get("fecha_vencimiento")

        if not id_paciente or not id_medicamento or not cantidad:
            return jsonify({"error": "Faltan campos obligatorios (id_paciente, id_medicamento, cantidad)"}), 400

        item = InventarioService.recargar_stock(
            id_paciente=id_paciente,
            id_medicamento=id_medicamento,
            cantidad=cantidad,
            fecha_vencimiento=fecha_vencimiento
        )
        return jsonify({
            "message": "Stock recargado exitosamente",
            "inventario": item.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ========== ADHERENCIA ==========
@auth_bp.route("/adherencia/generar", methods=["POST"])
def generar_reporte_adherencia():
    data = request.get_json() or {}
    try:
        id_tratamiento = data.get("idTratamiento")
        fecha_inicio = data.get("fechaInicio")
        fecha_fin = data.get("fechaFin")

        if not id_tratamiento or not fecha_inicio or not fecha_fin:
            return jsonify({"error": "idTratamiento, fechaInicio y fechaFin son requeridos"}), 400

        reporte = AdherenciaService.calcular_y_registrar(
            id_tratamiento=id_tratamiento,
            fecha_inicio_str=fecha_inicio,
            fecha_fin_str=fecha_fin
        )
        return jsonify(reporte.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/adherencia/paciente/<int:id_paciente>/ultimo", methods=["GET"])
def get_ultimo_reporte(id_paciente):
    try:
        reporte = AdherenciaService.obtener_ultimo_reporte(id_paciente)
        if not reporte:
            return jsonify({"message": "Sin reportes registrados"}), 404
        return jsonify(reporte.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/adherencia/tratamiento/<int:id_tratamiento>", methods=["GET"])
def get_historial_tratamiento(id_tratamiento):
    try:
        reportes = AdherenciaService.obtener_historial_tratamiento(id_tratamiento)
        return jsonify([r.to_dict() for r in reportes]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500