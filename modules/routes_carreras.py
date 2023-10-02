from flask import Blueprint, render_template,flash, request, redirect, url_for
from flask_login import login_required
from modules.common.gestor_carrera import gestor_carrera
from flask import Blueprint
from modules.auth import csrf


carreras_bp = Blueprint('routes_carreras', __name__)

@carreras_bp.route('/carreras', methods=['GET'])
@login_required
def obtener_lista_paginada():
    page = request.args.get('page', default=1, type=int)
    programa = request.args.get('programa', default="", type=str)
    universidad = request.args.get('universidad', default="", type=str)
    facultad = request.args.get('facultad', default="", type=str)
    campus = request.args.get('campus', default="", type=str)
    filtros = {
        'programa': programa,
        'universidad': universidad,
        'facultad': facultad,
        'campus':campus
    }
    carreras, total_paginas = gestor_carrera().obtener_pagina(page, **filtros)
    return render_template('carreras/carreras.html',carreras=carreras, total_paginas=total_paginas, csrf=csrf, filtros=filtros)