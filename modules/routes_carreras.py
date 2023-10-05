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
    carreras, total_paginas = gestor_carrera().obtener_pagina(page)
    return render_template('carreras/carreras.html',carreras=carreras, total_paginas=total_paginas, csrf=csrf)

print(obtener_lista_paginada)


@carreras_bp.route('/carreras/crear', methods=['GET', 'POST'])
@login_required
def crear_carrera():
    formulario_data = {}
    if request.method == 'POST':
        formulario_data = request.form.to_dict()
        
        # Obtener los valores de facultad, universidad, campus y programa
        nombre_facultad = formulario_data.get('facultad')
        nombre_universidad = formulario_data.get('universidad')
        nombre_campus = formulario_data.get('campus')
        nombre_programa = formulario_data.get('programa')

        # Verificar si alguno de los valores es None
        if None in [nombre_facultad, nombre_universidad, nombre_campus, nombre_programa]:
            flash('Error: Asegúrate de seleccionar valores válidos para facultad, universidad, campus y programa.', 'warning')
        else:
            facultad = Facultad.query.filter_by(nombre=nombre_facultad).first()
            universidad = Universidad.query.filter_by(nombre=nombre_universidad).first()
            campus = Campus.query.filter_by(nombre=nombre_campus).first()
            programa = Programa.query.filter_by(nombre=nombre_programa).first()

            if facultad is None or universidad is None or campus is None or programa is None:
                flash('Error: Asegúrate de seleccionar valores válidos para facultad, universidad, campus y programa.', 'warning')
            else:
                nueva_carrera = Carrera(facultad=facultad, universidad=universidad, campus=campus, programa=programa)
                resultado = gestor_carrera().crear(facultad=nombre_facultad,
                                                    universidad=nombre_universidad,
                                                    campus=nombre_campus,
                                                    programa=nombre_programa
                                                    )

                if resultado["Exito"]:
                    flash('Carrera creada correctamente', 'success')
                    return redirect(url_for('routes_carreras.obtener_lista_paginada'))
                else:
                    flash(resultado["MensajePorFallo"], 'warning')

    return render_template('carreras/crear_carrera.html', formulario_data=formulario_data, csrf=csrf)


#@carreras_bp.route('/carreras/editar/', methods=['GET', 'POST'])
@carreras_bp.route('/carreras/editar/<int:carrera_id>', methods=['GET', 'POST'])
@login_required
def editar_carrera(carrera_id):
    formulario_data = {}
    carrera = gestor_carrera().obtener_por_id(carrera_id)

    if carrera is None:
        flash('Carrera no encontrada', 'danger')
        return redirect(url_for('routes_carreras.obtener_lista_paginada'))

    if request.method == 'POST':
        formulario_data = request.form.to_dict()

        # Realiza las actualizaciones necesarias en la carrera con los datos del formulario
        carrera.facultad = Facultad.query.filter_by(nombre=formulario_data.get('facultad')).first()
        carrera.universidad = Universidad.query.filter_by(nombre=formulario_data.get('universidad')).first()
        carrera.campus = Campus.query.filter_by(nombre=formulario_data.get('campus')).first()
        carrera.programa = Programa.query.filter_by(nombre=formulario_data.get('programa')).first()

        if None in (carrera.facultad, carrera.universidad, carrera.campus, carrera.programa):
            flash('Error: Asegúrate de seleccionar valores válidos para facultad, universidad, campus y programa.', 'warning')
        else:
            # Realiza la actualización en la base de datos
            resultado = gestor_carrera().editar_carrera(carrera)

            if resultado.Exito:
                flash('Carrera editada correctamente', 'success')
                return redirect(url_for('routes_carreras.obtener_lista_paginada'))
            else:
                flash(resultado.MensajePorFallo, 'warning')

    return render_template('carreras/editar_carrera.html', formulario_data=formulario_data, carrera=carrera, csrf=csrf)


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
    carreras=gestor_carrera().obtener_todo()
    carreras_data=[]
    for carrera in carreras:
        pd={}
        pd["Programa"] = carrera.programa.nombre
        pd["Facultad"] = carrera.facultad.nombre
        pd["Universidad"] = carrera.universidad.nombre
        pd["Campus"] = carrera.campus.nombre
        carreras_data.append(pd)

    return exportar.exportar_excel(carreras_data)