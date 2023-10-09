from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.common.gestor_personas import gestor_personas
from modules.common.gestor_generos import gestor_generos
from modules.common.gestor_comun import exportar
from modules.common.gestor_carreras_personas import gestor_carreras_personas #AGREGADO POR MI
from flask import Blueprint
from modules.auth import csrf


personas_bp = Blueprint('routes_personas', __name__)

@personas_bp.route('/personas', methods=['GET'])
@login_required
def obtener_lista_paginada():
    page = request.args.get('page', default=1, type=int)
    nombre = request.args.get('nombre', default="", type=str)
    apellido = request.args.get('apellido', default="", type=str)
    email = request.args.get('email', default="", type=str)
    filtros = {
        'nombre': nombre,
        'apellido': apellido,
        'email': email
    }
    personas, total_paginas = gestor_personas().obtener_pagina(page, **filtros)
    return render_template('personas/personas.html', personas=personas, total_paginas=total_paginas, csrf=csrf, filtros=filtros)




@personas_bp.route('/personas/editar/', methods=['GET', 'POST'])
@login_required
def editar_persona():
    persona_id = request.args.get('persona_id', type=int)
    page = request.args.get('page', default=1, type=int)
    campus = request.args.get('campus', default="", type=str)
    programa = request.args.get('programa', default="", type=str)
    facultad = request.args.get('facultad', default="", type=str)
    universidad = request.args.get('universidad', default="", type=str)
    filtros = {
        'campus': campus,
        'programa': programa,
        'facultad': facultad,
        'universidad': universidad,
        'persona_id': persona_id
    }
    print(persona_id)
    # formulario_data_get = request.form.to_dict()
    # print(formulario_data_get)

    carrera_id = request.args.get('carrera_id', type=int)
    print(carrera_id)


    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        #prueba
        # print(formulario_data)
        if formulario_data['accion'] == 'editar_persona': #ENTRA POR ACA CUANDO QUEREMOS MODIFICAR UNA PERSONA SELECCIONADA
            # print("VENGO A EDITAR PERSONA COMUN")
            resultado=gestor_personas().editar(persona_id, **formulario_data)
            if resultado["Exito"]:
                flash('Persona actualizada correctamente', 'success')
                return redirect(url_for('routes_personas.obtener_lista_paginada'))
            else:
                flash(resultado["MensajePorFallo"], 'warning')
        if formulario_data['accion'] == 'crear_carrera_persona': #ENTRA POR ACA CUANDO QUEREMOS AGREGAR UNA NUEVA RELACION CARRERA-PERSONA
            # print("VENGO A CARRERA-PERSONA")
            resultado=gestor_carreras_personas().crear(**formulario_data)
            if resultado["Exito"]:
                flash('Carrera-Persona creada correctamente', 'success')
                # return redirect(url_for('routes_personas.obtener_lista_paginada'))
            else:
                flash(resultado["MensajePorFallo"], 'warning')



       
        if formulario_data['accion'] == 'eliminar_modal':
                    print("VENGO A eliminar CARRERA-PERSONA")
                    print(carrera_id)
                    
                    resultado=gestor_carreras_personas().eliminar(carrera_id)
                    if resultado["Exito"]:
                        flash('Carrera de persona eliminada correctamente', 'success')
                    else:
                        flash('Error al eliminar carrera de persona', 'success')
                    # return redirect(url_for('routes_personas.obtener_lista_paginada'))
                    return redirect(url_for('routes_personas.editar_persona', persona_id=persona_id))


                    # def eliminar_carrera_persona(carrera_id):
                    # resultado=gestor_carreras_personas().eliminar(carrera_id)
                    # if resultado["Exito"]:
                    #     flash('Carrera de persona eliminada correctamente', 'success')
                    # else:
                    #     flash('Error al eliminar carrera de persona', 'success')
                    # return redirect(url_for('routes_personas.obtener_lista_paginada'))

     

    resultado=gestor_personas().obtener(persona_id)

    if resultado["Exito"]:
        persona=resultado["Resultado"]
        carreras, total_paginas = gestor_carreras_personas().obtener_pagina(page, **filtros) #persona_id
        return render_template('personas/editar_persona.html', persona=persona,  total_paginas=total_paginas, carreras=carreras, csrf=csrf, filtros=filtros) #agregar  total_paginas=total_paginas, filtros=filtros #AGREGADO POR MI
    else:
        flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_personas.obtener_lista_paginada'))
    










@personas_bp.route('/personas/editarCarreraPersona/', methods=['GET', 'POST'])
@login_required
def editar_carrera_persona():
    carrera_id = request.args.get('carrera_id', type=int)

    if request.method == 'POST':
            formulario_data = request.form.to_dict()

            # if formulario_data['accion'] == 'cargarDatos_editar_carrera_persona':
            #         print("VENGO A editar CARRERA-PERSONA")
            #         # print(formulario_data)
                    
            #         resultado=gestor_carreras_personas().obtener(formulario_data['carrera_id'])
            #         if resultado["Exito"]:
            #             carrerapersona=resultado["Resultado"]
            #             return render_template('personas/editar_persona_carrera.html', carrerapersona=carrerapersona)
            #         else:
            #             flash(resultado["MensajePorFallo"], 'warning')
            #             return redirect(url_for('routes_personas.obtener_lista_paginada'))   
            
            
            if formulario_data['accion'] == 'editar_carrera_persona': #ENTRA POR ACA CUANDO QUEREMOS MODIFICAR UNA CARRERA-PERSONA SELECCIONADA
                resultado=gestor_carreras_personas().editar(carrera_id, **formulario_data)
                if resultado["Exito"]:
                    flash('Carrera de persona actualizada correctamente', 'success')
                    return redirect(url_for('routes_personas.editar_persona', persona_id=formulario_data['persona_id']))
                else:
                    flash(resultado["MensajePorFallo"], 'warning')

    resultado=gestor_carreras_personas().obtener(carrera_id)

    if resultado["Exito"]:
        carrerapersona=resultado["Resultado"]
        return render_template('personas/editar_persona_carrera.html', carrerapersona=carrerapersona)
    else:
        flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_personas.obtener_lista_paginada'))   
    









     
@personas_bp.route('/personas/<int:persona_id>', methods=['POST'])
@login_required
def eliminar_persona(persona_id):
    resultado=gestor_personas().eliminar(persona_id)
    if resultado["Exito"]:
        flash('Persona eliminada correctamente', 'success')
    else:
        flash('Error al eliminar persona', 'success')
    return redirect(url_for('routes_personas.obtener_lista_paginada'))

@personas_bp.route('/personas/crear', methods=['GET', 'POST'])
@login_required
def crear_persona():
    formulario_data = {} 
    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        resultado=gestor_personas().crear(**formulario_data)
        if resultado["Exito"]:
            flash('Persona creada correctamente', 'success')
            return redirect(url_for('routes_personas.obtener_lista_paginada'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')
    return render_template('personas/crear_persona.html', formulario_data=formulario_data, csrf=csrf)


@personas_bp.route('/personas/generar_excel', methods=['GET', 'POST'])
@login_required
def generar_excel():
    nombre = request.args.get('nombre', default="", type=str)
    apellido = request.args.get('apellido', default="", type=str)
    email = request.args.get('email', default="", type=str)
    filtros = {
        'nombre': nombre,
        'apellido': apellido,
        'email': email
    }
    personas=gestor_personas().obtener_todo_por_filtro(**filtros)
    personas_data=[]

    if(len(personas) > 0): #valida que exista al menos un registro, sino se rompe

        for persona in personas:
            pd={}
            pd["Nombre"] = persona.nombre
            pd["Apellido"] = persona.apellido
            pd["email"] = persona.email
            pd["Edad"] = persona.age
            pd["Fecha nacimiento"]=persona.birthdate.strftime('%d/%m/%Y') 
            pd["Genero"]=persona.genero.nombre
            pd["Pais"]=persona.lugar.pais.nombre
            pd["Provincia"]=persona.lugar.provincia.nombre
            pd["Ciudad"]=persona.lugar.ciudad.nombre
            pd["Barrio"]=persona.lugar.barrio.nombre
            personas_data.append(pd)

        return exportar.exportar_excel(personas_data)
    return redirect(url_for('routes_personas.obtener_lista_paginada'))
