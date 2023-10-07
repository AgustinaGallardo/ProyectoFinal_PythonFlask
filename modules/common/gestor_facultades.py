from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, Genero, Pais, Provincia, Ciudad, Barrio, Lugar, Facultad,Carrera, db
from config import registros_por_pagina
from datetime import datetime
from sqlalchemy import or_



class gestor_facultades(ResponseMessage):
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

    def obtener_facultades(self):
        return db.session.query(Facultad).distinct().join(Carrera).all()
    

	
    def obtener_pagina(self, pagina, **kwargs):
        query = Facultad.query.filter(Facultad.activo==True) # Muestra solo facultades activas.
        if 'nombre' in kwargs:
            query = query.filter(Facultad.nombre.ilike(f"%{kwargs['nombre']}%"))

        facultades, total_paginas = Facultad.obtener_paginado(query, pagina, registros_por_pagina)
        return facultades, total_paginas
    
    def obtener_todo_por_filtro(self,**kwargs):
        query = Facultad.query.filter(Facultad.activo==True)
        if 'nombre' in kwargs:
            query = query.filter(Facultad.nombre.ilike(f"%{kwargs['nombre']}%"))
            
        return query.all()


    def eliminar(self, id):
        facultad = Facultad.query.get(id)
        if facultad==None:
            self.Exito = False
            self.MensajePorFallo = "La facultad no existe"
            return self.obtenerResultado()
        resultado_borrar=facultad.activar(False) # Logica dar de baja.
        self.Exito=resultado_borrar["Exito"]
        self.MensajePorFallo=resultado_borrar["MensajePorFallo"]
        return self.obtenerResultado()




    def editar(self, id, **kwargs):
        facultad = Facultad.query.get(id)
        if facultad==None:
            self.Exito = False
            self.MensajePorFallo = "La facultad no existe"
            return self.obtenerResultado()
		
		#Validaciones
        for campo, mensaje in self.campos_obligatorios.items():
            if campo in kwargs and kwargs[campo]=='':
                self.Exito = False
                self.MensajePorFallo = mensaje
                return self.obtenerResultado()
            
        if 'nombre' in kwargs:
            facultad.nombre=kwargs['nombre']
            
        resultado_guardar=facultad.guardar()
        self.Exito=resultado_guardar["Exito"]
        self.MensajePorFallo=resultado_guardar["MensajePorFallo"]

        return self.obtenerResultado()



    def crear(self, **kwargs):
        if not self._validar_campos_obligatorios(kwargs):
            return self.obtenerResultado()
		
        nombre = kwargs['nombre']
		# print("ESTOY EN gestor_personas def crear(self, **kwargs):")
        nueva_facultad = Facultad(nombre=nombre)
	
        resultado_crear=nueva_facultad.guardar()
        self.Resultado=resultado_crear["Resultado"]
        self.Exito=resultado_crear["Exito"]
        self.MensajePorFallo=resultado_crear["MensajePorFallo"]

        return self.obtenerResultado()


    def obtener_todo(self):
        return Facultad.obtener_todo()
	