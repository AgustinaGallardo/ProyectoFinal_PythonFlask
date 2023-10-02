from flask_restful import Resource
from flask import request
from modules.auth import jwt_or_login_required
from modules.common.gestor_carrera import gestor_carrera

class CarrerasResource(Resource):    
        @jwt_or_login_required()
        def get(self, carrera_id=None):
            if carrera_id is None:
                data = request.get_json()
                pagina = data.get('pagina')
                filtros = data.get('filtros', {})
                carreras, total_paginas = gestor_carrera().obtener_pagina(pagina, **filtros)
                carreras_data = []
                for carrera in carreras:
                    cd = carrera.serialize()
                    cd["facultad"] = carrera.facultad.nombre
                    cd["universidad"] = carrera.universidad.nombre
                    cd["campus"] = carrera.campus.nombre
                    cd["programa"] = carrera.programa.nombre
                    carreras_data.append(cd)

                return {"Exito": True, "MensajePorFallo": None, "Resultado": carreras_data, "TotalPaginas":total_paginas}, 200
            '''else:
                resultado = gestor_carrera().obtener(carrera_id)
                if resultado["Exito"]:
                    carrera=resultado["Resultado"]
                    carrera_data=carrera.serialize()
                    carrera_data["birthdate"]=carrera.birthdate.isoformat()
                    carrera_data["pais"]=carrera.lugar.pais.nombre
                    carrera_data["provincia"]=carrera.lugar.provincia.nombre
                    carrera_data["ciudad"]=carrera.lugar.ciudad.nombre
                    carrera_data["barrio"]=carrera.lugar.barrio.nombre
                    return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":persona_data}, 200
                else:
                    return {"Exito":resultado["Exito"],"MensajePorFallo":resultado["MensajePorFallo"],"Resultado":None}, 400
                    '''
            
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
