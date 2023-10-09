from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Facultad,Universidad,Campus,Programa,Carrera, db
from config import registros_por_pagina
from sqlalchemy.exc import IntegrityError



class gestor_carrera(ResponseMessage):

	def __init__(self):
		super().__init__()
	
	campos_obligatorios = {
		'universidad': 'La universidad es obligatoria',
		'facultad': 'La facultad es obligatoria',
		'campus': 'El campus es obligatorio',
		'programa': 'El programa es obligatorio',
	}

	def _validar_campos_obligatorios(self, kwargs):
		for campo, mensaje in self.campos_obligatorios.items():
			if campo not in kwargs or kwargs[campo]=='':
				self.Exito = False
				self.MensajePorFallo = mensaje
				return False
		return True
		

	def obtener_pagina(self, pagina, **kwargs):
		query = Carrera.query.filter(Carrera.activo==True).order_by(Carrera.id)
		if 'facultad' in kwargs:
			query = query.join(Facultad).filter(Facultad.activo==True).filter(Facultad.nombre.ilike(f"%{kwargs['facultad']}%"))
		if 'universidad' in kwargs:
			query = query.join(Universidad).filter(Universidad.activo==True).filter(Universidad.nombre.ilike(f"%{kwargs['universidad']}%"))
		if 'campus' in kwargs:
			query = query.join(Campus).filter(Campus.activo==True).filter(Campus.nombre.ilike(f"%{kwargs['campus']}%"))
		if 'programa' in kwargs:
			query = query.join(Programa).filter(Programa.activo==True).filter(Programa.nombre.ilike(f"%{kwargs['programa']}%"))
			
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
	




	def crear(self, **kwargs):

		if not self._validar_campos_obligatorios(kwargs):
			return self.obtenerResultado()
		

		facultad=Facultad.crear_y_obtener(nombre=kwargs['facultad'])
		print("facultad en kwargs:")
		print(kwargs['facultad'])
		print("facultad resultado .crear_y_obtener:")
		print(facultad)

		universidad=Universidad.crear_y_obtener(nombre=kwargs['universidad'])
		campus=Campus.crear_y_obtener(nombre=kwargs['campus'])
		programa=Programa.crear_y_obtener(nombre=kwargs['programa'])		
				
		nueva_carrera = Carrera( programa=programa, facultad=facultad, universidad=universidad, campus=campus )	
		resultado_crear=nueva_carrera.guardar()
		self.Resultado=resultado_crear["Resultado"]
		self.Exito=resultado_crear["Exito"]
		self.MensajePorFallo=resultado_crear["MensajePorFallo"]
		return self.obtenerResultado()
	



	def obtener_todo(self):
		return Carrera.obtener_todo()
	
	def consultar_universidades(self, **kwargs):
		universidades = (
			db.session.query(Universidad).filter(Universidad.activo==True)
			.distinct()
			.join(Carrera)
			.all()
		)
		return universidades
	
    #Funciones para selects relacionados
	def consultar_facultades(self, **kwargs):
		facultades = (
			db.session.query(Facultad).filter(Facultad.activo==True)
			.distinct()
			.join(Carrera)
	 		.join(Universidad)
			.filter(Universidad.nombre == kwargs["universidad"])
			.all()
		)
		return facultades
	

	def consultar_campus(self, **kwargs):
			campus = (
				db.session.query(Campus).filter(Campus.activo==True)
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
			db.session.query(Programa).filter(Programa.activo==True)
			.distinct()
			.join(Carrera)
			.join(Universidad)
			.join(Facultad)
			.join(Campus)
			.filter(Universidad.nombre == kwargs["universidad"], Facultad.nombre == kwargs["facultad"], Campus.nombre == kwargs["campus"])
			.all()
		)
		return programas
    #Funciones para selects relacionados




    #Funciones para selects NO relacionados


	def consultar_universidades_noRelacionadas(self, **kwargs):
		universidades = (
			db.session.query(Universidad).filter(Universidad.activo==True)
			.distinct()
			# .join(Carrera)
			.all()
		)
		return universidades

	def consultar_facultades_noRelacionadas(self):
		facultades = (
			db.session.query(Facultad).filter(Facultad.activo==True)
			.distinct()
			# .join(Carrera)
	 		# .join(Universidad)
			.all()
		)
		return facultades
	

	def consultar_campus_noRelacionadas(self):
			campus = (
				db.session.query(Campus).filter(Campus.activo==True)
				.distinct()
				# .join(Carrera)
				# .join(Universidad)
				# .join(Facultad)
				.all()
			)
			return campus
	
	
	def consultar_programas_noRelacionadas(self):
		programas = (
			db.session.query(Programa).filter(Programa.activo==True)
			.distinct()
			# .join(Carrera)
			# .join(Universidad)
			# .join(Facultad)
			# .join(Campus)
			.all()
		)
		return programas

	#Funciones para selects NO relacionados






	def editar_carrera(self, id, **kwargs):
			# Busca la carrera por su ID
			carrera = Carrera.query.get(id)

			if carrera==None:
				self.Exito = False
				self.MensajePorFallo = "La carrera no existe"
				return self.obtenerResultado()
			

			# Validaciones
			for campo, mensaje in self.campos_obligatorios.items():
				if campo in kwargs and kwargs[campo]=='':
					self.Exito = False
					self.MensajePorFallo = mensaje
					return self.obtenerResultado()
				
			universidad=carrera.universidad
			facultad=carrera.facultad
			campus=carrera.campus
			programa=carrera.programa

			if 'universidad' in kwargs:
				universidad=Universidad.crear_y_obtener(nombre=kwargs['universidad'])
			if 'facultad' in kwargs:
				facultad=Facultad.crear_y_obtener(nombre=kwargs['facultad'])
			if 'campus' in kwargs:
				campus=Campus.crear_y_obtener(nombre=kwargs['campus'])
			if 'programa' in kwargs:
				programa=Programa.crear_y_obtener(nombre=kwargs['programa'])


			carrera.universidad=universidad
			carrera.facultad=facultad
			carrera.campus=campus
			carrera.programa=programa

			resultado_guardar=carrera.guardar()
			self.Exito=resultado_guardar["Exito"]
			self.MensajePorFallo=resultado_guardar["MensajePorFallo"]

			return self.obtenerResultado()
	
			
# def editar(self, id, **kwargs):
# 		persona = Persona.query.get(id)

# 		if persona==None:
# 			self.Exito = False
# 			self.MensajePorFallo = "La persona no existe"
# 			return self.obtenerResultado()
		
# 		#Validaciones
# 		for campo, mensaje in self.campos_obligatorios.items():
# 			if campo in kwargs and kwargs[campo]=='':
# 				self.Exito = False
# 				self.MensajePorFallo = mensaje
# 				return self.obtenerResultado()
			

# 		pais=persona.lugar.pais
# 		provincia=persona.lugar.provincia
# 		ciudad=persona.lugar.ciudad
# 		barrio=persona.lugar.barrio

# 		if 'pais' in kwargs:
# 			pais=Pais.crear_y_obtener(nombre=kwargs['pais'])
# 		if 'provincia' in kwargs:
# 			provincia=Provincia.crear_y_obtener(nombre=kwargs['provincia'])
# 		if 'ciudad' in kwargs:
# 			ciudad=Ciudad.crear_y_obtener(nombre=kwargs['ciudad'])
# 		if 'barrio' in kwargs:
# 			barrio=Barrio.crear_y_obtener(nombre=kwargs['barrio'])
# 		lugar=Lugar.crear_y_obtener(pais=pais,provincia=provincia,ciudad=ciudad, barrio=barrio)

# 		genero=persona.genero
# 		if 'genero' in kwargs:
# 			genero=Genero.crear_y_obtener(nombre=kwargs['genero'])

# 		if 'nombre' in kwargs:
# 			persona.nombre=kwargs['nombre']
		
# 		if 'apellido' in kwargs:
# 			persona.apellido=kwargs['apellido']

# 		if 'personal_id' in kwargs:
# 			persona.personal_id=kwargs['personal_id']

# 		persona.genero=genero
# 		persona.lugar=lugar

# 		resultado_guardar=persona.guardar()
# 		self.Exito=resultado_guardar["Exito"]
# 		self.MensajePorFallo=resultado_guardar["MensajePorFallo"]

# 		return self.obtenerResultado()


































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
			query = query.join(Facultad).filter(Facultad.activo==True).filter(Facultad.nombre.ilike(f"%{kwargs['facultad']}%"))
		if 'universidad' in kwargs:
			query = query.join(Universidad).filter(Universidad.activo==True).filter(Universidad.nombre.ilike(f"%{kwargs['universidad']}%"))
		if 'campus' in kwargs:
			query = query.join(Campus).filter(Campus.activo==True).filter(Campus.nombre.ilike(f"%{kwargs['campus']}%"))
		if 'programa' in kwargs:
			query = query.join(Programa).filter(Programa.activo==True).filter(Programa.nombre.ilike(f"%{kwargs['programa']}%"))
			
		return query.all()
		
	
	def obtener(self, id):
		carrera = Carrera.query.get(id)
		if carrera==None:
			self.Exito = False
			self.MensajePorFallo = "La carrera no existe"
			return self.obtenerResultado()
		self.Resultado = carrera
		return self.obtenerResultado()


	