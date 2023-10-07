from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.common.gestor_facultades import gestor_facultades
from modules.common.gestor_carreras_personas import gestor_carreras_personas
from modules.common.gestor_generos import gestor_generos
from modules.common.gestor_comun import exportar
from flask import Blueprint
from modules.auth import csrf


facultades_bp = Blueprint('routes_facultades', __name__)

@facultades_bp.route('/facultades', methods=['GET'])
@login_required
def obtener_lista_paginada():
    page = request.args.get('page', default=1, type=int)
    nombre = request.args.get('nombre', default="", type=str)
    filtros = {
        'nombre': nombre
    }
    facultades, total_paginas = gestor_facultades().obtener_pagina(page, **filtros)
    return render_template('facultades/facultades.html', facultades=facultades, total_paginas=total_paginas,  csrf=csrf, filtros=filtros)



@facultades_bp.route('/facultades/<int:facultad_id>', methods=['POST'])
@login_required
def crear_editar_eliminar_facultad(facultad_id):
    formulario_data = request.form.to_dict()

    if formulario_data['accion'] == 'eliminar_modal': #ENTRA POR ACA CUANDO QUEREMOS MODIFICAR UNA UNIVERSIDAD
        
        resultado=gestor_facultades().eliminar(facultad_id)
        if resultado["Exito"]:
            flash('Facultad eliminada correctamente', 'success')
        else:
            flash('Error al eliminar facultad', 'success')
        return redirect(url_for('routes_facultades.obtener_lista_paginada'))
    
    if formulario_data['accion'] == 'editar_modal':

        # formulario_data = request.form.to_dict()
        print(facultad_id)
        resultado=gestor_facultades().editar(facultad_id, **formulario_data) 
        if resultado["Exito"]:
            flash('Facultad actualizada correctamente', 'success')
        else:
            flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_facultades.obtener_lista_paginada'))
    
    if formulario_data['accion'] == 'agregar_modal':

        # formulario_data = request.form.to_dict()
        # print(facultad_id)
        resultado=gestor_facultades().crear(**formulario_data) 
        if resultado["Exito"]:
            flash('Facultad creada correctamente', 'success')
        else:
            flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_facultades.obtener_lista_paginada'))


@facultades_bp.route('/facultades/generar_excel', methods=['GET', 'POST'])
@login_required
def generar_excel():
    nombre = request.args.get('nombre', default="", type=str)
    filtros = {
        'nombre': nombre
    }
    facultades=gestor_facultades().obtener_todo_por_filtro(**filtros)
    facultades_data=[]

    if(len(facultades) > 0): #valida que exista al menos un registro, sino se rompe

        for facultad in facultades:
            pd={}
            pd["Nombre"] = facultad.nombre
            facultades_data.append(pd)

        return exportar.exportar_excel(facultades_data)
    return redirect(url_for('routes_facultades.obtener_lista_paginada'))
