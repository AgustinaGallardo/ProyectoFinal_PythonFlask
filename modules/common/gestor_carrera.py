from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Facultad,Universidad,Campus,Programa,Carrera, db

class gestor_carrera(ResponseMessage):
	def __init__(self):
		super().__init__()
		
	def consultar_carreras(self, **kwargs):

		query = db.session.query(Carrera)

		if 'facultad' in kwargs and kwargs["facultad"]:
			query = query.join(Facultad).filter(Facultad.nombre == kwargs["facultad"])
		if 'universidad' in kwargs and kwargs["universidad"]:
			query = query.join(Universidad).filter(Universidad.nombre == kwargs["universidad"])
		if 'campus' in kwargs and kwargs["campus"]:
			query = query.join(Campus).filter(Campus.nombre == kwargs["campus"])
		if 'programa' in kwargs and kwargs["programa"]:
			query = query.join(Programa).filter(Programa.nombre == kwargs["programa"])

		carreras = query.all()

		return carreras