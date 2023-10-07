from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.common.gestor_universidades import gestor_universidades
from modules.common.gestor_carreras_personas import gestor_carreras_personas
from modules.common.gestor_generos import gestor_generos
from modules.common.gestor_comun import exportar
from flask import Blueprint
from modules.auth import csrf


universidades_bp = Blueprint('routes_universidades', __name__)

@universidades_bp.route('/universidades', methods=['GET'])
@login_required
def obtener_lista_paginada():
    page = request.args.get('page', default=1, type=int)
    nombre = request.args.get('nombre', default="", type=str)
    filtros = {
        'nombre': nombre
    }
    universidades, total_paginas = gestor_universidades().obtener_pagina(page, **filtros)
    return render_template('universidades/universidades.html', universidades=universidades, total_paginas=total_paginas,  csrf=csrf, filtros=filtros)



@universidades_bp.route('/universidades/<int:universidad_id>', methods=['POST'])
@login_required
def crear_editar_eliminar_universidad(universidad_id):
    formulario_data = request.form.to_dict()

    if formulario_data['accion'] == 'eliminar_modal': #ENTRA POR ACA CUANDO QUEREMOS MODIFICAR UNA UNIVERSIDAD
        
        resultado=gestor_universidades().eliminar(universidad_id)
        if resultado["Exito"]:
            flash('Universidad eliminada correctamente', 'success')
        else:
            flash('Error al eliminar universidad', 'success')
        return redirect(url_for('routes_universidades.obtener_lista_paginada'))
    
    if formulario_data['accion'] == 'editar_modal':

        # formulario_data = request.form.to_dict()
        print(universidad_id)
        resultado=gestor_universidades().editar(universidad_id, **formulario_data) 
        if resultado["Exito"]:
            flash('Universidad actualizada correctamente', 'success')
        else:
            flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_universidades.obtener_lista_paginada'))
    
    if formulario_data['accion'] == 'agregar_modal':

        # formulario_data = request.form.to_dict()
        # print(universidad_id)
        resultado=gestor_universidades().crear(**formulario_data) 
        if resultado["Exito"]:
            flash('Universidad creada correctamente', 'success')
        else:
            flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_universidades.obtener_lista_paginada'))


@universidades_bp.route('/universidades/generar_excel', methods=['GET', 'POST'])
@login_required
def generar_excel():
    nombre = request.args.get('nombre', default="", type=str)
    filtros = {
        'nombre': nombre
    }
    universidades=gestor_universidades().obtener_todo_por_filtro(**filtros)
    universidades_data=[]
    
    if(len(universidades) > 0): #valida que exista al menos un registro, sino se rompe
        for universidad in universidades:
            pd={}
            pd["Nombre"] = universidad.nombre
            universidades_data.append(pd)

        return exportar.exportar_excel(universidades_data)
    return redirect(url_for('routes_universidades.obtener_lista_paginada'))
