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
            
            elif carrera_type == 'obtener_universidades':
                universidades = gestor_carrera().consultar_universidades()
                universidades_data = [universidad.serialize() for universidad in universidades]
                return {"Exito": True, "MensajePorFallo": None, "Resultado": universidades_data}, 200

            # elif carrera_type == 'obtener_facultades':
            #     facultades = gestor_carrera().consultar_facultades()
            #     facultades_data = [facultad.serialize() for facultad in facultades]
            #     return {"Exito": True, "MensajePorFallo": None, "Resultado": facultades_data}, 200
            
            else:
                return {"Exito": False, "MensajePorFallo": "Recurso no definido", "Resultado": None}, 400
            
        @jwt_or_login_required()
        def post(self, carrera_type=None):
            if not carrera_type:
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

            if (carrera_type == 'obtener_facultades'):
                data = request.get_json() 
                universidad = data.get('universidad')
                if not universidad:
                    return {"Exito":False,"MensajePorFallo":"Debe indicar el universidad","Resultado":None}, 400
                facultads = gestor_carrera().consultar_facultades(universidad=universidad)
                facultads_data = [facultad.serialize() for facultad in facultads]
                return {"Exito":True,"MensajePorFallo":None,"Resultado":facultads_data}, 200
            elif (carrera_type ==  'obtener_campus'):
                data = request.get_json() 
                universidad = data.get('universidad')
                facultad = data.get('facultad')
                if not universidad or not facultad:
                    return {"Exito":False,"MensajePorFallo":"Debe indicar el universidad y facultad","Resultado":None}, 400
                campuses = gestor_carrera().consultar_campus(universidad=universidad, facultad=facultad)
                campuses_data = [campus.serialize() for campus in campuses]
                return {"Exito":True,"MensajePorFallo":None,"Resultado":campuses_data}, 200
            elif (carrera_type == 'obtener_programas'):
                data = request.get_json() 
                universidad = data.get('universidad')
                facultad = data.get('facultad')
                campus = data.get('campus')
                if not universidad or not facultad or not campus:
                    return {"Exito":False,"MensajePorFallo":"Debe indicar el universidad, facultad y campus","Resultado":None}, 400
                programas = gestor_carrera().consultar_programas(universidad=universidad, facultad=facultad, campus=campus)
                programas_data = [programa.serialize() for programa in programas]
                return {"Exito":True,"MensajePorFallo":None,"Resultado":programas_data}, 200
            else:
                return {"Exito":False,"MensajePorFallo":"Recurso no definido","Resultado":None}, 400


        @jwt_or_login_required()
        def put(self, carrera_id):
                args = request.get_json()
                resultado = gestor_carrera().editar_carrera(carrera_id, **args)            
                if resultado.Exito:  # Accede al atributo Exito sin corchetes
                    carrera = resultado.Resultado  # Accede al atributo Resultado
                    carrera_data = carrera.serialize()
                    carrera_data["programa"] = carrera.programa.nombre
                    carrera_data["facultad"] = carrera.facultad.nombre
                    carrera_data["universidad"] = carrera.universidad.nombre
                    carrera_data["campus"] = carrera.campus.nombre
                    return {"Exito": resultado.Exito, "MensajePorFallo": resultado.MensajePorFallo, "Resultado": carrera_data}, 200
                else:
                    return {"Exito": resultado.Exito, "MensajePorFallo": resultado.MensajePorFallo, "Resultado": None}, 400


