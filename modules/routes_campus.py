from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.common.gestor_campus import gestor_campus
from modules.common.gestor_carreras_personas import gestor_carreras_personas
from modules.common.gestor_generos import gestor_generos
from modules.common.gestor_comun import exportar
from flask import Blueprint
from modules.auth import csrf


campus_bp = Blueprint('routes_campus', __name__)

@campus_bp.route('/campus', methods=['GET'])
@login_required
def obtener_lista_paginada():
    nombre = request.args.get('nombre', default="", type=str)
    page = request.args.get('page', default=1, type=int)
    filtros = {
        'nombre': nombre
    }
    campus, total_paginas = gestor_campus().obtener_pagina(page, **filtros)
    return render_template('campus/campus.html', campus=campus, total_paginas=total_paginas,  csrf=csrf, filtros=filtros)



@campus_bp.route('/campus/<int:campus_id>', methods=['POST'])
@login_required
def crear_editar_eliminar_campus(campus_id):
    formulario_data = request.form.to_dict()

    if formulario_data['accion'] == 'eliminar_modal': #ENTRA POR ACA CUANDO QUEREMOS MODIFICAR UNA UNIVERSIDAD
        
        resultado=gestor_campus().eliminar(campus_id)
        if resultado["Exito"]:
            flash('Campus eliminada correctamente', 'success')
        else:
            flash('Error al eliminar campus', 'success')
        return redirect(url_for('routes_campus.obtener_lista_paginada'))
    
    if formulario_data['accion'] == 'editar_modal':

        # formulario_data = request.form.to_dict()
        print(campus_id)
        resultado=gestor_campus().editar(campus_id, **formulario_data) 
        if resultado["Exito"]:
            flash('Campus actualizada correctamente', 'success')
        else:
            flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_campus.obtener_lista_paginada'))
    
    if formulario_data['accion'] == 'agregar_modal':

        # formulario_data = request.form.to_dict()
        # print(campus_id)
        resultado=gestor_campus().crear(**formulario_data) 
        if resultado["Exito"]:
            flash('Campus creada correctamente', 'success')
        else:
            flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_campus.obtener_lista_paginada'))


@campus_bp.route('/campus/generar_excel', methods=['GET', 'POST'])
@login_required
def generar_excel():
    campus=gestor_campus().obtener_todo()
    campus_data=[]
    for campus in campus:
        pd={}
        pd["Nombre"] = campus.nombre
        campus_data.append(pd)

    return exportar.exportar_excel(campus_data)