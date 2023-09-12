# practico-pil2023
 
 
 - Gestión de Dependencias - 
Para ejecutar el proyecto y asegurarse de que las dependencias están correctamente instaladas,
Sigue los siguientes pasos:

Crea un entorno virtual utilizando el siguiente comando
(asegúrate de estar en la raíz del proyecto):

# python3 -m venv virtual-env
(En Linux,Mac, usa python3 en lugar de python).
# python -m venv virtual-env
(En Windows, usa python en lugar de python3).

Activa el entorno virtual con el siguiente comando:

# source virtual-env/bin/activate
(En Linux,Mac,, utiliza virtual-env\Scripts\activate).
# virtual-env\Scripts\activate
(En Windows, utiliza virtual-env\Scripts\activate).

Al activar el entorno virtual, todas las dependencias instaladas estarán disponibles 
para tu proyecto.
Instala las dependencias del proyecto desde el archivo requirements.txt con el siguiente comando:

 # pip install -r requirements.txt

Este comando instalará todas las dependencias especificadas en el archivo requirements.txt, 
asegurándose de que tu proyecto tenga acceso a las versiones adecuadas de las bibliotecas
necesarias.
Con estos pasos, habrás configurado tu entorno virtual y 
tendrás todas las dependencias instaladas, listo para ejecutar y trabajar en tu proyecto. 
Recuerda mantener tu entorno virtual activo mientras trabajas en el proyecto para asegurarte 
de que estás utilizando las dependencias correctas. Si necesitas agregar o actualizar 
dependencias, asegúrate de hacerlo en el archivo requirements.txt y luego vuelve a instalarlas
con el comando pip install -r requirements.txt.

 
Paso 1: Crear el archivo .env
Dentro de la carpeta, crea un nuevo archivo llamado .env ( el nombre comienza con un punto para que sea un archivo oculto).
Paso 2: Agregar variables de entorno al archivo .env
Paso 3: Configurar .gitignore
 Crea o edita un archivo llamado .gitignore. Este archivo se utiliza para especificar qué archivos y carpetas no deben incluirse en el control de versiones de Git.
Dentro del archivo .gitignore,  agregar una línea para ignorar el archivo .env.
Si quieren desactivar el viertual env 
deactivate  # Para salir del entorno virtual actual
rm -r /ruta/a/tu/virtualenv  # Elimina el entorno virtual
