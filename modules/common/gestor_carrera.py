from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Facultad,Universidad,Campus,Programa,Carrera, db
from config import registros_por_pagina

class gestor_carrera(ResponseMessage):

	def __init__(self):
		super().__init__()


	def obtener_pagina(self, pagina, **kwargs):
		query = Carrera.query
		if 'universidad' in kwargs:
			query = query.filter(Carrera.universidad.ilike(f"%{kwargs['universidad']}%"))
		if 'facultad' in kwargs:
			query = query.filter(Carrera.facultad.ilike(f"%{kwargs['facultad']}%"))
		if 'campus' in kwargs:
			query = query.filter(Carrera.campus.ilike(f"%{kwargs['campus']}%"))
		if 'programa' in kwargs:
			query = query.filter(Carrera.programa.ilike(f"%{kwargs['programa']}%"))
		
		carreras, total_paginas = Carrera.obtener_paginado(query, pagina, registros_por_pagina)
		return carreras, total_paginas
	
		
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
	
	def crear_carrera(self, programa, facultad, universidad, campus):		
		try:
				nueva_carrera = Carrera(
					programa=programa,
					facultad=facultad,
					universidad=universidad,
					campus=campus
				)

				db.session.add(nueva_carrera)
				db.session.commit()

				return {"Exito": True, "MensajePorFallo": None, "Resultado": "Carrera creada exitosamente"}
		except Exception as e:
				
				db.session.rollback()
				return {"Exito": False, "MensajePorFallo": str(e), "Resultado": None}
		
	
	def consultar_facultades(self):
		try:
				facultades = db.session.query(Facultad).all()
				return facultades
		except Exception as e:
				# Manejo de errores en caso de fallo en la consulta
				db.session.rollback()
				raise e
		
