from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.common.gestor_programas import gestor_programas
from modules.common.gestor_carreras_personas import gestor_carreras_personas
from modules.common.gestor_generos import gestor_generos
from modules.common.gestor_comun import exportar
from flask import Blueprint
from modules.auth import csrf


programas_bp = Blueprint('routes_programas', __name__)

@programas_bp.route('/programas', methods=['GET'])
@login_required
def obtener_lista_paginada():
    page = request.args.get('page', default=1, type=int)
    nombre = request.args.get('nombre', default="", type=str)
    filtros = {
        'nombre': nombre
    }
    programas, total_paginas = gestor_programas().obtener_pagina(page, **filtros)
    return render_template('programas/programas.html', programas=programas, total_paginas=total_paginas,  csrf=csrf, filtros=filtros)



@programas_bp.route('/programas/<int:programa_id>', methods=['POST'])
@login_required
def crear_editar_eliminar_programa(programa_id):
    formulario_data = request.form.to_dict()

    if formulario_data['accion'] == 'eliminar_modal': #ENTRA POR ACA CUANDO QUEREMOS MODIFICAR UNA UNIVERSIDAD
        
        resultado=gestor_programas().eliminar(programa_id)
        if resultado["Exito"]:
            flash('Programa eliminada correctamente', 'success')
        else:
            flash('Error al eliminar programa', 'success')
        return redirect(url_for('routes_programas.obtener_lista_paginada'))
    
    if formulario_data['accion'] == 'editar_modal':

        # formulario_data = request.form.to_dict()
        print(programa_id)
        resultado=gestor_programas().editar(programa_id, **formulario_data) 
        if resultado["Exito"]:
            flash('Programa actualizada correctamente', 'success')
        else:
            flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_programas.obtener_lista_paginada'))
    
    if formulario_data['accion'] == 'agregar_modal':

        # formulario_data = request.form.to_dict()
        # print(programa_id)
        resultado=gestor_programas().crear(**formulario_data) 
        if resultado["Exito"]:
            flash('Programa creada correctamente', 'success')
        else:
            flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_programas.obtener_lista_paginada'))


@programas_bp.route('/programas/generar_excel', methods=['GET', 'POST'])
@login_required
def generar_excel():
    nombre = request.args.get('nombre', default="", type=str)
    filtros = {
        'nombre': nombre
    }
    programas=gestor_programas().obtener_todo_por_filtro(**filtros)
    programas_data=[]
    for programa in programas:
        pd={}
        pd["Nombre"] = programa.nombre
        programas_data.append(pd)

    return exportar.exportar_excel(programas_data)