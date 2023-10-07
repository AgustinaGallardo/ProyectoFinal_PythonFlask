from modules.common.gestor_comun import ResponseMessage, validaciones
from modules.models.entities import Persona, personasCarreras, Carrera, Universidad, Facultad, Campus, Programa, TipoPersona, db
from config import registros_por_pagina
from datetime import datetime
from sqlalchemy import or_

class  gestor_carreras_personas(ResponseMessage):
    def __init__(self):
        super().__init__()

    campos_obligatorios = {
		'universidad': 'La universidad es obligatoria',
		'facultad': 'La facultad es obligatoria',
		'campus': 'El campus es obligatorio',
		'programa': 'El programa es obligatorio',
		'tipo': 'El tipo es obligatorio'
	}

    def _validar_campos_obligatorios(self, kwargs):
        for campo, mensaje in self.campos_obligatorios.items():
            if campo not in kwargs or kwargs[campo]=='':
                self.Exito = False
                self.MensajePorFallo = mensaje
                return False
        return True

    def crear(self, **kwargs):
        if not self._validar_campos_obligatorios(kwargs):
            return self.obtenerResultado()


        tipopersona=TipoPersona.crear_y_obtener(nombre=kwargs['tipo'])
        universidad=Universidad.crear_y_obtener(nombre=kwargs['universidad'])
        facultad=Facultad.crear_y_obtener(nombre=kwargs['facultad'])
        campus=Campus.crear_y_obtener(nombre=kwargs['campus'])
        programa=Programa.crear_y_obtener(nombre=kwargs['programa'])
        carrera=Carrera.crear_y_obtener(universidad=universidad,facultad=facultad,campus=campus, programa=programa)
        persona=Persona.crear_y_obtener(id=kwargs['persona_id'])
        
        nueva_carrera_persona = personasCarreras( persona=persona, carrera=carrera, tipopersona=tipopersona)

        resultado_crear=nueva_carrera_persona.guardar()
        self.Resultado=resultado_crear["Resultado"]
        self.Exito=resultado_crear["Exito"]
        self.MensajePorFallo=resultado_crear["MensajePorFallo"]

        return self.obtenerResultado()




    def editar(self, id, **kwargs):
        if not self._validar_campos_obligatorios(kwargs):
            return self.obtenerResultado()

        personacarrera = personasCarreras.query.get(id)
        print('id de la carrera-persona')
        print(id)

        if personacarrera==None:
            self.Exito = False
            self.MensajePorFallo = "La personacarrera no existe"
            return self.obtenerResultado()
		
			
        persona=personacarrera.persona
        print('PERSONA DEL MODIFICAR')
        print(persona)

        universidad=personacarrera.carrera.universidad
        facultad=personacarrera.carrera.facultad
        campus=personacarrera.carrera.campus
        programa=personacarrera.carrera.programa


        if 'universidad' in kwargs:
            universidad=Universidad.crear_y_obtener(nombre=kwargs['universidad'])
        if 'facultad' in kwargs:
            facultad=Facultad.crear_y_obtener(nombre=kwargs['facultad'])
        if 'campus' in kwargs:
            campus=Campus.crear_y_obtener(nombre=kwargs['campus'])
        if 'programa' in kwargs:
            programa=Programa.crear_y_obtener(nombre=kwargs['programa'])

        carrera=Carrera.crear_y_obtener(universidad=universidad,facultad=facultad,campus=campus, programa=programa)

        tipo=personacarrera.tipopersona

        if 'tipo' in kwargs:
            tipo=TipoPersona.crear_y_obtener(nombre=kwargs['tipo'])


        personacarrera.tipopersona=tipo
        personacarrera.carrera=carrera

        resultado_guardar=personacarrera.guardar()
        self.Exito=resultado_guardar["Exito"]
        self.MensajePorFallo=resultado_guardar["MensajePorFallo"]

        return self.obtenerResultado()



    def eliminar(self, id):
        carrera = personasCarreras.query.get(id)
        if carrera==None:
            self.Exito = False
            self.MensajePorFallo = "La carrera no existe"
            return self.obtenerResultado()
        resultado_borrar=carrera.activar(False)
        self.Exito=resultado_borrar["Exito"]
        self.MensajePorFallo=resultado_borrar["MensajePorFallo"]
        return self.obtenerResultado()
        
    
    #MIO 
    def obtener_carreras_por_persona(persona):
        carreras = (
            db.session.query(personasCarreras)
            .filter(personasCarreras.activo==True)
            .filter(personasCarreras.persona==persona)
            .join(Carrera)
            .join(Universidad)
            .join(Facultad)
            .join(Campus)
            .join(Programa)
            .order_by(Universidad.nombre, Facultad.nombre, Campus.nombre, Programa.nombre).all()
        )
        return carreras
    
    # Obtiene todas las carreras asociadas a una persona, paginada.
    def obtener_pagina(self, pagina, **kwargs):
        query = personasCarreras.query.filter_by(persona_id=kwargs['persona_id']).filter(personasCarreras.activo==True) #traigo solo si la personacarrera esta activa en tabla personascarreras.
        if 'programa' in kwargs:
            query = query.join(Carrera).filter(Carrera.activo==True).join(Programa).filter(Programa.activo==True).filter(Programa.nombre.ilike(f"%{kwargs['programa']}%")) #traigo solo si la carrera relacionada a esta persona tambiene esta activa en tabla Carreras
        if 'facultad' in kwargs:
            query = query.join(Facultad).filter(Facultad.activo==True).filter(Facultad.nombre.ilike(f"%{kwargs['facultad']}%"))
        if 'universidad' in kwargs:
            query = query.join(Universidad).filter(Universidad.activo==True).filter(Universidad.nombre.ilike(f"%{kwargs['universidad']}%"))
        if 'campus' in kwargs:
            query = query.join(Campus).filter(Campus.activo==True).filter(Campus.nombre.ilike(f"%{kwargs['campus']}%"))
        # if 'rol' in kwargs:
        #     query = query.join(TipoPersona).filter(TipoPersona.nombre.ilike(f"%{kwargs['rol']}%"))         
        personacarreras, total_paginas = personasCarreras.obtener_paginado(query, pagina, registros_por_pagina)
        return personacarreras, total_paginas
    
    
    def obtener(self, id):
        carrerapersona = personasCarreras.query.get(id)
        if carrerapersona==None:
            self.Exito = False
            self.MensajePorFallo = "La persona no existe"
            return self.obtenerResultado()
        self.Resultado = carrerapersona
        return self.obtenerResultado()
    

            