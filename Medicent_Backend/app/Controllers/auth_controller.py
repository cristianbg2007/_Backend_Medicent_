from flask import request, jsonify
from flask_jwt_extended import create_access_token # <-- 1. IMPORTAMOS LA FUNCIÓN DEL TOKEN
from app.database.database import db, bcrypt
from app.models.usuario import Usuario

class AuthController:

    @staticmethod
    def register():
        try:
            data = request.get_json()

            # 1. Validar campos obligatorios básicos
            required_fields = ['nombre', 'apellido', 'documento', 'correo', 'telefono', 'fechaNacimiento', 'password', 'idTipoDocumento']
            for field in required_fields:
                if not data or field not in data:
                    return jsonify({"error": f"El campo '{field}' es obligatorio."}), 400

            # 2. Verificar si el usuario ya existe por correo o documento
            existing_user = Usuario.query.filter(
                (Usuario.correo == data['correo']) | (Usuario.documento == data['documento'])
            ).first()

            if existing_user:
                return jsonify({"error": "El correo electrónico o el número de documento ya están registrados."}), 400

            # 3. Cifrar la contraseña
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

            # 4. Crear la instancia del nuevo usuario
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

            # 5. Guardar en la base de datos
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
                
                # 2. CREAMOS EL TOKEN (La llave de seguridad)
                token_seguridad = create_access_token(identity=str(usuario.idUsuario))
                
                return jsonify({
                    "message": "Inicio de sesión exitoso",
                    "access_token": token_seguridad, # <-- 3. LO ENVIAMOS A FLUTTER
                    "usuario": {
                        "id": usuario.idUsuario,
                        "correo": usuario.correo,
                        "nombre": usuario.nombre
                    }
                }), 200
            else:
                return jsonify({"error": "Credenciales inválidas"}), 401

        except Exception as e:
            return jsonify({"error": f"Ocurrió un error en el servidor: {str(e)}"}), 500