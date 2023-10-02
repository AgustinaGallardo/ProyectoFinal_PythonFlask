from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Facultad,Universidad,Campus,Programa,Carrera, db
from config import registros_por_pagina

class gestor_carrera(ResponseMessage):

	def __init__(self):
		super().__init__()
	
	campos_obligatorios = {
		'facultad': 'La facultad es obligatoria',
		'universidad': 'La universidad es obligatoria',
		'programa': 'El programa es obligatorio',
		'campus': 'El campus es obligatorio',
		
	}
		

	def obtener_pagina(self, pagina, **kwargs):
		query = Carrera.query
		if 'facultad' in kwargs:
			query = query.filter(Carrera.facultad.ilike(f"%{kwargs['facultad']}%"))
		if 'universidad' in kwargs:
			query = query.filter(Carrera.universidad.ilike(f"%{kwargs['universidad']}%"))
		if 'campus' in kwargs:
			query = query.filter(Carrera.campus.ilike(f"%{kwargs['campus']}%"))
		if 'programa' in kwargs:
			query = query.filter(Carrera.programa.ilike(f"%{kwargs['programa']}%"))
			
		carreras, total_paginas = Carrera.obtener_paginado(query, pagina, registros_por_pagina)
		return carreras, total_paginas

		
