from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Facultad,Universidad,Campus,Programa,Carrera, db
from config import registros_por_pagina
from sqlalchemy.exc import IntegrityError



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
		query = Carrera.query.filter(Carrera.activo==True)
		if 'facultad' in kwargs:
			query = query.join(Facultad).filter(Facultad.nombre.ilike(f"%{kwargs['facultad']}%"))
		if 'universidad' in kwargs:
			query = query.join(Universidad).filter(Universidad.nombre.ilike(f"%{kwargs['universidad']}%"))
		if 'campus' in kwargs:
			query = query.join(Campus).filter(Campus.nombre.ilike(f"%{kwargs['campus']}%"))
		if 'programa' in kwargs:
			query = query.join(Programa).filter(Programa.nombre.ilike(f"%{kwargs['programa']}%"))
			
		carreras, total_paginas = Carrera.obtener_paginado(query, pagina, registros_por_pagina)
		return carreras, total_paginas
		
		
	def crear(self, **kwargs):
			facultad_nombre = kwargs.get('facultad')
			universidad_nombre = kwargs.get('universidad')
			campus_nombre = kwargs.get('campus')
			programa_nombre = kwargs.get('programa')

			facultad = Facultad.crear_y_obtener(nombre=facultad_nombre)
			universidad = Universidad.crear_y_obtener(nombre=universidad_nombre)
			campus = Campus.crear_y_obtener(nombre=campus_nombre)
			programa = Programa.crear_y_obtener(nombre=programa_nombre)

			nueva_carrera = Carrera(facultad=facultad, universidad=universidad, campus=campus, programa=programa)
			resultado_crear = nueva_carrera.guardar()
			
			self.Resultado = resultado_crear["Resultado"]
			self.Exito = resultado_crear["Exito"]
			self.MensajePorFallo = resultado_crear["MensajePorFallo"]		
				
			return self.obtenerResultado()
	
	def consultar_carreras(self, **kwargs):
		query = db.session.query(Carrera) 

		if 'universidad' in kwargs and kwargs["universidad"]:
			query = query.join(Universidad).filter(Universidad.nombre == kwargs["universidad"])
		if 'facultad' in kwargs and kwargs["facultad"]:
			query = query.join(Facultad).filter(Facultad.nombre == kwargs["facultad"])
		if 'campus' in kwargs and kwargs["campus"]:
			query = query.join(Campus).filter(Campus.nombre == kwargs["campus"])
		if 'programa' in kwargs and kwargs["programa"]:
			query = query.join(Programa).filter(Programa.nombre == kwargs["programa"])

		carreras = query.all()

		return carreras
		

	def obtener_todo(self):
		return Carrera.obtener_todo()
	
	def consultar_universidades(self, **kwargs):
		universidades = (
			db.session.query(Universidad)
			.distinct()
			.join(Carrera)
			.all()
		)
		return universidades
	

	def consultar_facultades(self, **kwargs):
		facultades = (
			db.session.query(Facultad)
			.distinct()
			.join(Carrera)
	 		.join(Universidad)
			.filter(Universidad.nombre == kwargs["universidad"])
			.all()
		)
		return facultades
	

	def consultar_campus(self, **kwargs):
			campus = (
				db.session.query(Campus)
				.distinct()
				.join(Carrera)
				.join(Universidad)
				.join(Facultad)
				.filter(Universidad.nombre == kwargs["universidad"], Facultad.nombre == kwargs["facultad"])
				.all()
			)
			return campus
	
	
	def consultar_programas(self, **kwargs):
		programas = (
			db.session.query(Programa)
			.distinct()
			.join(Carrera)
			.join(Universidad)
			.join(Facultad)
			.join(Campus)
			.filter(Universidad.nombre == kwargs["universidad"], Facultad.nombre == kwargs["facultad"], Campus.nombre == kwargs["campus"])
			.all()
		)
		return programas





	def editar_carrera(self, carrera_id, **kwargs):
			# Busca la carrera por su ID
			carrera = Carrera.query.get(carrera_id)

			if not carrera:
				# Si no se encuentra la carrera, devuelve un mensaje de error
				return ResponseMessage(
					Resultado=None,
					Exito=False,
					MensajePorFallo='La carrera no fue encontrada.'
				)
			
			
	

			
# Actualiza los campos de la carrera con los valores proporcionados
			if 'facultad' in kwargs:
				carrera.facultad = kwargs['facultad']
			if 'universidad' in kwargs:
				carrera.universidad = kwargs['universidad']
			if 'campus' in kwargs:
				carrera.campus = kwargs['campus']
			if 'programa' in kwargs:
				carrera.programa = kwargs['programa']

			
			# Guarda los cambios en la base de datos
			resultado_actualizar = carrera.guardar()

			# Devuelve el resultado de la operación
			return ResponseMessage(
				Resultado=resultado_actualizar["Resultado"],
				Exito=resultado_actualizar["Exito"],
				MensajePorFallo=resultado_actualizar["MensajePorFallo"]
			)
	
			




	def eliminar(self, id):
		carrera = Carrera.query.get(id)
		if carrera==None:
			self.Exito = False
			self.MensajePorFallo = "La carrera no existe"
			return self.obtenerResultado()
		resultado_borrar=carrera.activar(False) 
		self.Exito=resultado_borrar["Exito"]
		self.MensajePorFallo=resultado_borrar["MensajePorFallo"]
		return self.obtenerResultado()

	def obtener_todo_por_filtro(self,**kwargs):
		query = Carrera.query.filter(Carrera.activo==True)
		if 'facultad' in kwargs:
			query = query.join(Facultad).filter(Facultad.nombre.ilike(f"%{kwargs['facultad']}%"))
		if 'universidad' in kwargs:
			query = query.join(Universidad).filter(Universidad.nombre.ilike(f"%{kwargs['universidad']}%"))
		if 'campus' in kwargs:
			query = query.join(Campus).filter(Campus.nombre.ilike(f"%{kwargs['campus']}%"))
		if 'programa' in kwargs:
			query = query.join(Programa).filter(Programa.nombre.ilike(f"%{kwargs['programa']}%"))
			
		return query.all()
		
	
	def obtener_por_id(self, carrera_id):
        # Busca la carrera por su ID
            carrera = Carrera.query.get(carrera_id)

            if not carrera:
                # Si no se encuentra la carrera, devuelve None
                return None

            # Si se encuentra la carrera, devuelve el objeto de carrera
            return carrera


	