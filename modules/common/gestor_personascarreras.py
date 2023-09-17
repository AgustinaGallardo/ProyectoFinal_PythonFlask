from modules.common.gestor_comun import ResponseMessage
from modules.models.entities import personasCarreras,TipoPersona,Carrera,Facultad,Campus,Programa,Universidad,db

class Gestor_Personas_Carreras(ResponseMessage):
    def __init__(self):
        super().__init__()

    def agregar_persona_a_carrera(self, persona_id, carrera_id, tipo_id):
        # Realiza validaciones si es necesario
        # Asegúrate de que la persona, carrera y tipo existan

        # Crea una nueva entrada en la tabla personasCarreras
        nueva_relacion = personasCarreras(persona_id=persona_id, carrera_id=carrera_id, tipo_id=tipo_id)

        # Guarda la nueva relación en la base de datos
        resultado = nueva_relacion.guardar()  # Suponiendo que tienes un método guardar() en tu entidad personasCarreras

        # Maneja errores y devuelve un mensaje de éxito o fallo
        if resultado["Exito"]:
            self.Exito = True
            self.Resultado = "La persona ha sido agregada a la carrera."
        else:
            self.Exito = False
            self.MensajePorFallo = "No se pudo agregar a la persona a la carrera."

    def eliminar_persona_de_carrera(self, persona_id, carrera_id):
        # Realiza validaciones si es necesario
        # Asegúrate de que la relación entre persona y carrera exista

        # Busca la relación existente en la tabla personasCarreras
        relacion_existente = personasCarreras.query.filter_by(persona_id=persona_id, carrera_id=carrera_id).first()

        if relacion_existente:
            # Elimina la entrada en la tabla personasCarreras
            resultado_borrar = relacion_existente.borrar()  # Suponiendo que tienes un método borrar() en tu entidad personasCarreras

            # Maneja errores y devuelve un mensaje de éxito o fallo
            if resultado_borrar["Exito"]:
                self.Exito = True
                self.Resultado = "La persona ha sido eliminada de la carrera."
            else:
                self.Exito = False
                self.MensajePorFallo = "No se pudo eliminar a la persona de la carrera."
        else:
            self.Exito = False
            self.MensajePorFallo = "La relación persona-carrera no existe."

    def consultar_carreras_de_persona(self, persona_id, tipo_id):
        # Realiza una consulta en la tabla personasCarreras para encontrar carreras relacionadas con la persona y el tipo
        relaciones = personasCarreras.query.filter_by(persona_id=persona_id, tipo_id=tipo_id).all()

        # Devuelve una lista de carreras o un mensaje si no hay carreras
        if relaciones:
            carreras = [relacion.carrera for relacion in relaciones]
            return carreras
        else:
            self.Exito = False
            self.MensajePorFallo = "No se encontraron carreras para esta persona y tipo."
            return []

    def consultar_personas_en_carrera(self, carrera_id, tipo_id):
        # Realiza una consulta en la tabla personasCarreras para encontrar personas relacionadas con la carrera y el tipo
        relaciones = personasCarreras.query.filter_by(carrera_id=carrera_id, tipo_id=tipo_id).all()

        # Devuelve una lista de personas o un mensaje si no hay personas
        if relaciones:
            personas = [relacion.persona for relacion in relaciones]
            return personas
        else:
            self.Exito = False
            self.MensajePorFallo = "No se encontraron personas para esta carrera y tipo."
            return []

            