from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.common.gestor_personascarreras import gestor_personascarreras
from modules.common.gestor_generos import gestor_generos
from flask import Blueprint
from modules.auth import csrf

personascarreras_bp = Blueprint('routes_personascarreras', __name__)

@personascarreras_bp.route('/personascarreras', methods=['GET'])
@login_required
def obtener_lista_paginada():
    page = request.args.get('page', default=1, type=int)
    nombre = request.args.get('nombre', default="", type=str)
    apellido = request.args.get('apellido', default="", type=str)
    universidad = request.args.get('universidad', default="", type=str)
    facultad = request.args.get('facultad', default="", type=str)
    filtros = {
        'nombre': nombre,
        'apellido': apellido,
        'universidad': universidad,
        'facultad': facultad,
    }
    personas, total_paginas = gestor_personascarreras().obtener_pagina(page, **filtros)
    return render_template('personascarreras/personascarreras.html', personas=personas, total_paginas=total_paginas, csrf=csrf, filtros=filtros)

@personascarreras_bp.route('/personascarreras/<int:personacarreras_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_personacarreras(personacarreras_id):
    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        resultado=gestor_personascarreras().editar(personacarreras_id, **formulario_data)
        if resultado["Exito"]:
            flash('Persona carrera actualizada correctamente', 'success')
            return redirect(url_for('routes_personascarreras.obtener_lista_paginada'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')

    resultado=gestor_personascarreras().obtener(personacarreras_id)
    if resultado["Exito"]:
        persona=resultado["Resultado"]
        return render_template('personascarreras/editar_personacarrera.html', persona=persona, csrf=csrf)
    else:
        flash(resultado["MensajePorFallo"], 'warning')
        return redirect(url_for('routes_personascarreras.obtener_lista_paginada'))
    
@personascarreras_bp.route('/personascarreras/<int:personacarreras_id>', methods=['POST'])
@login_required
def eliminar_personacarrera(personacarreras_id):
    resultado=gestor_personascarreras().eliminar(personacarreras_id)
    if resultado["Exito"]:
        flash('Persona Carrera eliminada correctamente', 'success')
    else:
        flash('Error al eliminar persona carrera', 'success')
    return redirect(url_for('routes_personascarreras.obtener_lista_paginada'))

@personascarreras_bp.route('/personascarreras/crear', methods=['GET', 'POST'])
@login_required
def crear_personacarrera():
    formulario_data = {} 
    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        resultado=gestor_personascarreras().crear(**formulario_data)
        if resultado["Exito"]:
            flash('Persona carrera creada correctamente', 'success')
            return redirect(url_for('routes_personascarreras.obtener_lista_paginada'))
        else:
            flash(resultado["MensajePorFallo"], 'warning')
    return render_template('personascarreras/crear_personacarrera.html', formulario_data=formulario_data, csrf=csrf)

