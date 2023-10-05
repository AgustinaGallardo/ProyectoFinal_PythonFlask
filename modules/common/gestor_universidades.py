from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, Genero, Pais, Provincia, Ciudad, Barrio, Lugar, Universidad,Carrera, db
from config import registros_por_pagina
from datetime import datetime
from sqlalchemy import or_



class gestor_universidades(ResponseMessage):
    def __init__(self):
        super().__init__()
		

    campos_obligatorios = {
		'nombre': 'El nombre es obligatorio'
	}

    def _validar_campos_obligatorios(self, kwargs):
        for campo, mensaje in self.campos_obligatorios.items():
            if campo not in kwargs or kwargs[campo]=='':
                self.Exito = False
                self.MensajePorFallo = mensaje
                return False
        return True

    def obtener_universidades(self):
        return db.session.query(Universidad).distinct().join(Carrera).all()
    

	
    def obtener_pagina(self, pagina, **kwargs):
        query = Universidad.query.filter(Universidad.activo==True) # Muestra solo universidades activas.
        if 'nombre' in kwargs:
            query = query.filter(Universidad.nombre.ilike(f"%{kwargs['nombre']}%"))

        universidades, total_paginas = Universidad.obtener_paginado(query, pagina, registros_por_pagina)
        return universidades, total_paginas


    def eliminar(self, id):
        universidad = Universidad.query.get(id)
        if universidad==None:
            self.Exito = False
            self.MensajePorFallo = "La universidad no existe"
            return self.obtenerResultado()
        resultado_borrar=universidad.activar(False) # Logica dar de baja.
        self.Exito=resultado_borrar["Exito"]
        self.MensajePorFallo=resultado_borrar["MensajePorFallo"]
        return self.obtenerResultado()




    def editar(self, id, **kwargs):
        universidad = Universidad.query.get(id)
        if universidad==None:
            self.Exito = False
            self.MensajePorFallo = "La universidad no existe"
            return self.obtenerResultado()
		
		#Validaciones
        for campo, mensaje in self.campos_obligatorios.items():
            if campo in kwargs and kwargs[campo]=='':
                self.Exito = False
                self.MensajePorFallo = mensaje
                return self.obtenerResultado()
            
        if 'nombre' in kwargs:
            universidad.nombre=kwargs['nombre']
            
        resultado_guardar=universidad.guardar()
        self.Exito=resultado_guardar["Exito"]
        self.MensajePorFallo=resultado_guardar["MensajePorFallo"]

        return self.obtenerResultado()



    def crear(self, **kwargs):
        if not self._validar_campos_obligatorios(kwargs):
            return self.obtenerResultado()
		
        nombre = kwargs['nombre']
		# print("ESTOY EN gestor_personas def crear(self, **kwargs):")
        nueva_universidad = Universidad(nombre=nombre)
	
        resultado_crear=nueva_universidad.guardar()
        self.Resultado=resultado_crear["Resultado"]
        self.Exito=resultado_crear["Exito"]
        self.MensajePorFallo=resultado_crear["MensajePorFallo"]

        return self.obtenerResultado()


    def obtener_todo(self):
        return Universidad.obtener_todo()


















	

	# def obtener_facultades(self, **kwargs):
	# 	resultado = (
	# 		db.session.query(Facultad)
	# 		.distinct()
	# 		.join(Carrera)
	# 		.join(Universidad)
	# 		.filter(Universidad.nombre == kwargs["universidad"])
	# 		.all()
	# 	)
	# 	return resultado
	
	# def obtener_campus(self, **kwargs):
	# 	resultado = (
	# 		db.session.query(Campus)
	# 		.distinct()
	# 		.join(Carrera)
	# 		.join(Universidad)
	# 		.join(Facultad)
	# 		.filter(Universidad.nombre == kwargs["universidad"])
	# 		.filter(Facultad.nombre == kwargs["facultad"])
	# 		.all()
	# 	)
	# 	return resultado

	# def obtener_programas(self, **kwargs):
	# 	resultado = (
	# 		db.session.query(Programa)
	# 		.distinct()
	# 		.join(Carrera)
	# 		.join(Universidad)
	# 		.join(Facultad)
	# 		.join(Campus)
	# 		.filter(Universidad.nombre == kwargs["universidad"])
	# 		.filter(Facultad.nombre == kwargs["facultad"])
	# 		.filter(Campus.nombre == kwargs["campus"])
	# 		.all()
	# 	)
	# 	return resultado

	# def obtener_roles(self, **kwargs):
	# 	resultado = (
	# 		db.session.query(TipoPersona).all()
	# 	)
	# 	return resultado
	