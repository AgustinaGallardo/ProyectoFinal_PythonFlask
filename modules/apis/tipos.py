from flask_restful import Resource
from modules.auth import jwt_or_login_required
from modules.common.gestor_tipopersona import GestorTiposPersona

class TiposResource(Resource):
	@jwt_or_login_required()
	def get(self):
		tipos = GestorTiposPersona().obtener_todo()
		tipos_data = [tipo.serialize() for tipo in tipos]
		return {"Exito":True,"MensajePorFallo":None,"Resultado":tipos_data}, 200