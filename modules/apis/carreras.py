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
        
    @jwt_or_login_required()
    def post(self):
        args = request.get_json() 
        resultado = gestor_carrera().crear(**args)
        if resultado["Exito"]:
            carrera = resultado["Resultado"]
            carrera_data = carrera.serialize()
            carrera_data["programa"] = carrera.programa.nombre
            carrera_data["facultad"] = carrera.facultad.nombre
            carrera_data["universidad"] = carrera.universidad.nombre
            carrera_data["campus"] = carrera.campus.nombre
            return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"], "Resultado": carrera_data}, 201
        else:
            return {"Exito": resultado["Exito"], "MensajePorFallo": resultado["MensajePorFallo"], "Resultado": None}, 400


            """
        
    def editar_carrera(self, id, **kwargs):
        
        carrera = Carrera.query.get(id)

        if carrera is None:
            self.Exito = False
            self.MensajePorFallo = "La carrera no existe"
            return self.obtenerResultado()

        if 'programa' in kwargs:
            carrera.programa = Programa.crear_y_obtener(nombre=kwargs['programa'])

        if 'facultad' in kwargs:
            carrera.facultad = Facultad.crear_y_obtener(nombre=kwargs['facultad'])

        if 'universidad' in kwargs:
            carrera.universidad = Universidad.crear_y_obtener(nombre=kwargs['universidad'])

        if 'campus' in kwargs:
            carrera.campus = Campus.crear_y_obtener(nombre=kwargs['campus'])

        resultado_guardar = carrera.guardar()
        self.Exito = resultado_guardar["Exito"]
        self.MensajePorFallo = resultado_guardar["MensajePorFallo"]

        return self.obtenerResultado()    """