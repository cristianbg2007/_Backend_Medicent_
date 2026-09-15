from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.database.database import db, bcrypt
from app.models.usuario import Usuario

# IMPORTANTE: Asegúrate de que esta importación exista en tu proyecto, 
# ya que tu compañero la usó para validar los roles.
from app.services.auth_service import AuthService 

class AuthController:

    @staticmethod
    def register():
        try:
            data = request.get_json()

            required_fields = ['nombre', 'apellido', 'documento', 'correo', 'telefono', 'fechaNacimiento', 'password', 'idTipoDocumento']
            for field in required_fields:
                if not data or field not in data:
                    return jsonify({"error": f"El campo '{field}' es obligatorio."}), 400

            existing_user = Usuario.query.filter(
                (Usuario.correo == data['correo']) | (Usuario.documento == data['documento'])
            ).first()

            # --- AQUÍ ESTÁ LA PARTE DE TU CÓDIGO (HEAD) ---
            if existing_user:
                return jsonify({"error": "El correo electrónico o el número de documento ya están registrados."}), 400

            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            nuevo_usuario = Usuario(
                nombre=data['nombre'],
                apellido=data['apellido'],
                documento=data['documento'],
                correo=data['correo'],
                telefono=data['telefono'],
                fechaNacimiento=data['fechaNacimiento'],
                password=hashed_password,
                idTipoDocumento=data['idTipoDocumento']
            )

            db.session.add(nuevo_usuario)
            db.session.commit()

            return jsonify({
                "message": "Usuario registrado exitosamente",
                "usuario": {
                    "id": nuevo_usuario.idUsuario,
                    "correo": nuevo_usuario.correo,
                    "nombre": nuevo_usuario.nombre
                }
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Ocurrió un error en el servidor: {str(e)}"}), 500

    @staticmethod
    def login():
        try:
            data = request.get_json()
            
            if not data or 'correo' not in data or 'password' not in data:
                return jsonify({"error": "Se requiere correo y contraseña"}), 400

            usuario = Usuario.query.filter_by(correo=data['correo']).first()

            if usuario and bcrypt.check_password_hash(usuario.password, data['password']):
                
                # --- AQUÍ ESTÁ EL CÓDIGO DE TU COMPAÑERO (INCOMING) ---
                es_admin = AuthService.es_admin(usuario)
                rol = "admin" if es_admin else "usuario"

                token = create_access_token(
                    identity=str(usuario.idUsuario),
                    additional_claims={
                        "nombre": usuario.nombre,
                        "apellido": usuario.apellido,
                        "rol": rol                    
                    }
                )

                # Combinamos ambas respuestas para que el código de tu compañero 
                # funcione, pero sin romper nuestra app de Flutter
                return jsonify({
                    "message": "Inicio de sesión exitoso",
                    "access_token": token,  # Para que funcione en Flutter
                    "accessToken": token,   # Para que le funcione a tu compañero
                    "usuario": {            # Nuestro objeto en Flutter
                        "id": usuario.idUsuario,
                        "correo": usuario.correo,
                        "nombre": usuario.nombre,
                        "apellido": usuario.apellido,
                        "rol": rol
                    },
                    "user": {               # El objeto de tu compañero
                        "id": usuario.idUsuario,
                        "nombre": usuario.nombre,
                        "apellido": usuario.apellido,
                        "correo": usuario.correo,
                        "rol": rol                    
                    }
                }), 200
            else:
                return jsonify({"error": "Credenciales inválidas"}), 401

        except Exception as e:
            return jsonify({"error": f"Ocurrió un error en el servidor: {str(e)}"}), 500