from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Facultad,Universidad,Campus,Programa,Carrera, db
from config import registros_por_pagina

class gestor_carrera(ResponseMessage):

	def __init__(self):
		super().__init__()


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
	
	def crear(self, **kwargs):
		
		facultad=Facultad.crear_y_obtener(nombre=kwargs['facultad'])
		universidad=Universidad.crear_y_obtener(nombre=kwargs['universidad'])
		campus=Campus.crear_y_obtener(nombre=kwargs['campus'])
		programa=Programa.crear_y_obtener(nombre=kwargs['programa'])		
		
		facultad = kwargs['facultad']
		universidad = kwargs['universidad']
		campus = kwargs['campus']
		programa = kwargs['programa']		
		nueva_carrera = Carrera(facultad=facultad, universidad=universidad, campus=campus, programa=programa)	
		resultado_crear=nueva_carrera.guardar()
		self.Resultado=resultado_crear["Resultado"]
		self.Exito=resultado_crear["Exito"]
		self.MensajePorFallo=resultado_crear["MensajePorFallo"]
		return self.obtenerResultado()

	def obtener_todo(self):
		return Carrera.obtener_todo()
	

	def consultar_facultades(self, **kwargs):
		facultades = (
			db.session.query(Facultad)
			.distinct()
			.all()
		)
		return facultades

	def consultar_universidades(self, **kwargs):
		universidades = (
			db.session.query(Universidad)
			.distinct()
			.all()
		)
		return universidades

	def consultar_programas(self, **kwargs):
		programas = (
			db.session.query(Programa)
			.distinct()
			.all()
		)
		return programas

	def consultar_campus(self, **kwargs):
		campus = (
			db.session.query(Campus)
			.distinct()
			.all()
		)
		return campus

			
