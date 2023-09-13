from flask_restful import Resource
from flask import request
from modules.auth import jwt_or_login_required
from modules.common.gestor_carrera import gestor_carrera

class CarrerasResource(Resource):    
    @jwt_or_login_required()
    def get(self, carrera_type=None):
        if not carrera_type:
            data = request.get_json()
            facultad = data.get('facultad')
            universidad = data.get('universidad')
            campus = data.get('campus')
            programa = data.get('programa')

            carreras = gestor_carrera().consultar_carreras(
                facultad=facultad,
                universidad=universidad,
                campus=campus,
                programa=programa)

            carreras_data = []
            for carrera in carreras:
                cd = carrera.serialize()
                cd["facultad"] = carrera.facultad.nombre
                cd["universidad"] = carrera.universidad.nombre
                cd["campus"] = carrera.campus.nombre
                cd["programa"] = carrera.programa.nombre
                carreras_data.append(cd)

            return {"Exito": True, "MensajePorFallo": None, "Resultado": carreras_data}, 200

        elif carrera_type == 'obtener_facultades':
            facultades = gestor_carrera().consultar_facultades()
            facultades_data = [facultad.serialize() for facultad in facultades]
            return {"Exito": True, "MensajePorFallo": None, "Resultado": facultades_data}, 200
        else:
            return {"Exito": False, "MensajePorFallo": "Recurso no definido", "Resultado": None}, 400
        
"""
    @CarrerasResource.route('/carreras', methods=['POST'])
    @login_required
    def crear_carrera(self):
        data = request.form  # Cambiado a request.form para obtener datos de formulario

        carrera_type = data.get('carrera_type')

        if carrera_type == 'crear_carrera':
            # Obtener los datos del formulario
            facultad = data.get('facultad')
            universidad = data.get('universidad')
            campus = data.get('campus')
            programa = data.get('programa')

            # Lógica para crear la carrera utilizando tu gestor de carreras
            resultado = gestor_carrera().crear_carrera(
                programa=programa,
                facultad=facultad,
                universidad=universidad,
                campus=campus               
            )

        if resultado["Exito"]:
            flash('Carrera creada correctamente', 'success')
                # Asegúrate de tener un método para redireccionar después de crear la carrera
            return redirect(url_for('nombre_de_ruta_redireccion'))  # Reemplaza 'nombre_de_ruta_redireccion' por la ruta adecuada
        else:
            flash(resultado["MensajePorFallo"], 'warning')
                # Asegúrate de tener un método para redireccionar en caso de error
            return redirect(url_for('nombre_de_ruta_error'))  # Reemplaza 'nombre_de_ruta_error' por la ruta adecuada
        else:
            return {"Exito": False, "MensajePorFallo": "Recurso no definido", "Resultado": None}, 400   """