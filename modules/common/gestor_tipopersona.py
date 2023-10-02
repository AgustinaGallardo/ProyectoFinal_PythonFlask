from modules.common.gestor_comun import ResponseMessage
from modules.models.entities import TipoPersona

class GestorTiposPersona(ResponseMessage):
    def __init__(self):
        super().__init__() 

    def crear_tipo_persona(self, nombre):
        # Crea un nuevo tipo de persona
        nuevo_tipo_persona = TipoPersona(nombre=nombre)

        # Guarda el nuevo tipo de persona en la base de datos
        resultado = nuevo_tipo_persona.guardar()  # Suponiendo que tienes un método guardar() en tu entidad TipoPersona

        # Maneja errores y devuelve un mensaje de éxito o fallo
        if resultado["Exito"]:
            self.Exito = True
            self.Resultado = "Tipo de persona creado con éxito."
        else:
            self.Exito = False
            self.MensajePorFallo = "No se pudo crear el tipo de persona."

    def editar_tipo_persona(self, tipo_persona_id, nombre):
        # Busca el tipo de persona existente por su ID
        tipo_persona_existente = TipoPersona.query.get(tipo_persona_id)

        if tipo_persona_existente:
            # Edita el nombre del tipo de persona
            tipo_persona_existente.nombre = nombre

            # Guarda los cambios en la base de datos
            resultado = tipo_persona_existente.guardar()  # Suponiendo que tienes un método guardar() en tu entidad TipoPersona

            # Maneja errores y devuelve un mensaje de éxito o fallo
            if resultado["Exito"]:
                self.Exito = True
                self.Resultado = "Tipo de persona editado con éxito."
            else:
                self.Exito = False
                self.MensajePorFallo = "No se pudo editar el tipo de persona."
        else:
            self.Exito = False
            self.MensajePorFallo = "El tipo de persona no existe."

    def eliminar_tipo_persona(self, tipo_persona_id):
        # Busca el tipo de persona existente por su ID
        tipo_persona_existente = TipoPersona.query.get(tipo_persona_id)

        if tipo_persona_existente:
            # Elimina el tipo de persona de la base de datos
            resultado = tipo_persona_existente.borrar()  # Suponiendo que tienes un método borrar() en tu entidad TipoPersona

            # Maneja errores y devuelve un mensaje de éxito o fallo
            if resultado["Exito"]:
                self.Exito = True
                self.Resultado = "Tipo de persona eliminado con éxito."
            else:
                self.Exito = False
                self.MensajePorFallo = "No se pudo eliminar el tipo de persona."
        else:
            self.Exito = False
            self.MensajePorFallo = "El tipo de persona no existe."

    def consultar_tipos_persona(self):
        # Realiza una consulta para obtener todos los tipos de persona
        tipos_persona = TipoPersona.query.all()

        # Devuelve una lista de tipos de persona o un mensaje si no hay tipos
        if tipos_persona:
            tipos = [tipo.nombre for tipo in tipos_persona]
            return tipos
        else:
            self.Exito = False
            self.MensajePorFallo = "No se encontraron tipos de persona."
            return []
        

    def obtener_todo(self):
        return TipoPersona.obtener_todo()