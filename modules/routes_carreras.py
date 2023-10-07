from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.common.gestor_carrera import gestor_carrera
from modules.common.gestor_comun import exportar
from flask import Blueprint
from modules.auth import csrf
from modules.models.entities import Facultad,Universidad,Campus,Programa,Carrera

carreras_bp = Blueprint('routes_carreras', __name__)

@carreras_bp.route('/carreras', methods=['GET'])
@login_required
def obtener_lista_paginada():
    page = request.args.get('page', default=1, type=int)
    programa = request.args.get('programa', default="", type=str)
    facultad = request.args.get('facultad', default="", type=str)
    campus = request.args.get('campus', default="", type=str)
    universidad = request.args.get('universidad', default="", type=str)
    filtros = {
        'programa': programa,
        'facultad': facultad,
        'campus': campus,
        'universidad': universidad
    }
    carreras, total_paginas = gestor_carrera().obtener_pagina(page, **filtros)
    return render_template('carreras/carreras.html',carreras=carreras, total_paginas=total_paginas, csrf=csrf, filtros=filtros)

@carreras_bp.route('/carreras/crear', methods=['GET', 'POST'])
@login_required
def crear_carrera():
    formulario_data = {}
    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        resultado=gestor_carrera().crear(**formulario_data)
        if resultado["Exito"]:
            flash('carrera creada correctamente', 'success')
            return redirect(url_for('routes_carreras.obtener_lista_paginada'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')
    return render_template('carreras/crear_carrera.html', formulario_data=formulario_data, csrf=csrf)
        
    #     # Obtener los valores de facultad, universidad, campus y programa
    #     facultad = Facultad.query.filter_by(nombre=formulario_data.get('facultad')).first()
    #     universidad = Universidad.query.filter_by(nombre=formulario_data.get('universidad')).first()
    #     campus = Campus.query.filter_by(nombre=formulario_data.get('campus')).first()
    #     programa = Programa.query.filter_by(nombre=formulario_data.get('programa')).first()

    #     # Verificar si alguno de los valores es None
    #     if facultad is None or universidad is None or campus is None or programa is None:
    #         flash('Error: Asegúrate de seleccionar valores válidos para facultad, universidad, campus y programa.', 'warning')
    #     else:
    #         resultado = gestor_carrera().crear(
    #             facultad=facultad,
    #             universidad=universidad,
    #             campus=campus,
    #             programa=programa
    #         )

    #         if resultado["Exito"]:
    #             flash('Carrera creada correctamente', 'success')
    #             return redirect(url_for('routes_carreras.obtener_lista_paginada'))
    #         else:
    #             flash(resultado["MensajePorFallo"], 'warning')

    # return render_template('carreras/crear_carrera.html', formulario_data=formulario_data, csrf=csrf)


# @personas_bp.route('/personas/crear', methods=['GET', 'POST'])
# @login_required
# def crear_persona():
#     formulario_data = {} 
#     if request.method == 'POST':
#         formulario_data = request.form.to_dict()
#         resultado=gestor_personas().crear(**formulario_data)
#         if resultado["Exito"]:
#             flash('Persona creada correctamente', 'success')
#             return redirect(url_for('routes_personas.obtener_lista_paginada'))
#         else:
#             flash(resultado["MensajePorFallo"], 'warning')
#     return render_template('personas/crear_persona.html', formulario_data=formulario_data, csrf=csrf)




#@carreras_bp.route('/carreras/editar/', methods=['GET', 'POST'])
@carreras_bp.route('/carreras/editar/<int:carrera_id>', methods=['GET', 'POST'])
@login_required
def editar_carrera(carrera_id):
    # carrera = gestor_carrera().obtener_por_id(carrera_id)

    # if carrera is None:
    #     flash('Carrera no encontrada', 'danger')
    #     return redirect(url_for('routes_carreras.obtener_lista_paginada'))

    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        resultado=gestor_carrera().editar_carrera(carrera_id, **formulario_data)
        if resultado["Exito"]:
            flash('Carrera actualizada correctamente', 'success')
            return redirect(url_for('routes_carreras.obtener_lista_paginada'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')

        # # Realiza las actualizaciones necesarias en la carrera con los datos del formulario
        # carrera.facultad = Facultad.query.filter_by(nombre=formulario_data.get('facultad')).first()
        # carrera.universidad = Universidad.query.filter_by(nombre=formulario_data.get('universidad')).first()
        # carrera.campus = Campus.query.filter_by(nombre=formulario_data.get('campus')).first()
        # carrera.programa = Programa.query.filter_by(nombre=formulario_data.get('programa')).first()

        # if None in (carrera.facultad, carrera.universidad, carrera.campus, carrera.programa):
        #     flash('Error: Asegúrate de seleccionar valores válidos para facultad, universidad, campus y programa.', 'warning')
        # else:
        #     # Realiza la actualización en la base de datos
        #     resultado = gestor_carrera().editar_carrera(carrera)

        #     if resultado.Exito:
        #         flash('Carrera editada correctamente', 'success')
        #         return redirect(url_for('routes_carreras.obtener_lista_paginada'))
        #     else:
        #         flash(resultado.MensajePorFallo, 'warning')


    resultado=gestor_carrera().obtener(carrera_id)

    if resultado["Exito"]:
        carrera=resultado["Resultado"]
        return render_template('carreras/editar_carrera.html', carrera=carrera, csrf=csrf)
    else:
        flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_carreras.obtener_lista_paginada'))



# def editar_persona():

#     if request.method == 'POST':
#         formulario_data = request.form.to_dict()
#         #prueba
#         # print(formulario_data)
#         if formulario_data['accion'] == 'editar_persona': #ENTRA POR ACA CUANDO QUEREMOS MODIFICAR UNA PERSONA SELECCIONADA
#             # print("VENGO A EDITAR PERSONA COMUN")
#             resultado=gestor_personas().editar(persona_id, **formulario_data)
#             if resultado["Exito"]:
#                 flash('Persona actualizada correctamente', 'success')
#                 return redirect(url_for('routes_personas.obtener_lista_paginada'))
#             else:
#                 flash(resultado["MensajePorFallo"], 'warning')
#         if formulario_data['accion'] == 'crear_carrera_persona': #ENTRA POR ACA CUANDO QUEREMOS AGREGAR UNA NUEVA RELACION CARRERA-PERSONA
#             # print("VENGO A CARRERA-PERSONA")
#             resultado=gestor_carreras_personas().crear(**formulario_data)
#             if resultado["Exito"]:
#                 flash('Carrera-Persona creada correctamente', 'success')
#                 # return redirect(url_for('routes_personas.obtener_lista_paginada'))
#             else:
#                 flash(resultado["MensajePorFallo"], 'warning')



       
#         if formulario_data['accion'] == 'eliminar_modal':
#                     print("VENGO A eliminar CARRERA-PERSONA")
#                     print(carrera_id)
                    
#                     resultado=gestor_carreras_personas().eliminar(carrera_id)
#                     if resultado["Exito"]:
#                         flash('Carrera de persona eliminada correctamente', 'success')
#                     else:
#                         flash('Error al eliminar carrera de persona', 'success')
#                     # return redirect(url_for('routes_personas.obtener_lista_paginada'))
#                     return redirect(url_for('routes_personas.editar_persona', persona_id=persona_id))


#                     # def eliminar_carrera_persona(carrera_id):
#                     # resultado=gestor_carreras_personas().eliminar(carrera_id)
#                     # if resultado["Exito"]:
#                     #     flash('Carrera de persona eliminada correctamente', 'success')
#                     # else:
#                     #     flash('Error al eliminar carrera de persona', 'success')
#                     # return redirect(url_for('routes_personas.obtener_lista_paginada'))

     

#     resultado=gestor_personas().obtener(persona_id)

#     if resultado["Exito"]:
#         persona=resultado["Resultado"]
#         carreras, total_paginas = gestor_carreras_personas().obtener_pagina(page, **filtros) #persona_id
#         return render_template('personas/editar_persona.html', persona=persona,  total_paginas=total_paginas, carreras=carreras, csrf=csrf, filtros=filtros) #agregar  total_paginas=total_paginas, filtros=filtros #AGREGADO POR MI
#     else:
#         flash(resultado["MensajePorFallo"], 'warning')
#         return redirect(url_for('routes_personas.obtener_lista_paginada'))  


























@carreras_bp.route('/carreras/<int:carrera_id>', methods=['POST'])
@login_required
def eliminar_carrera(carrera_id):
    resultado=gestor_carrera().eliminar(carrera_id)
    if resultado["Exito"]:
        flash('Carrera eliminada correctamente', 'success')
    else:
        flash('Error al eliminar carrera', 'success')
    return redirect(url_for('routes_carreras.obtener_lista_paginada'))


@carreras_bp.route('/carreras/generar_excel', methods=['GET', 'POST'])
@login_required
def generar_excel():
    programa = request.args.get('programa', default="", type=str)
    facultad = request.args.get('facultad', default="", type=str)
    campus = request.args.get('campus', default="", type=str)
    universidad = request.args.get('universidad', default="", type=str)
    filtros = {
        'programa': programa,
        'facultad': facultad,
        'campus': campus,
        'universidad': universidad
    }
    carreras=gestor_carrera().obtener_todo_por_filtro(**filtros)
    carreras_data=[]
    if(len(carreras) > 0): #valida que exista al menos un registro, sino se rompe
        print('me meti a len(carreas) >0')
        for carrera in carreras:
            pd={}
            pd["Programa"] = carrera.programa.nombre
            pd["Facultad"] = carrera.facultad.nombre
            pd["Universidad"] = carrera.universidad.nombre
            pd["Campus"] = carrera.campus.nombre
            carreras_data.append(pd)

        return exportar.exportar_excel(carreras_data)
    return redirect(url_for('routes_carreras.obtener_lista_paginada'))
