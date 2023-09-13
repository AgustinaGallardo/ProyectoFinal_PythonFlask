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
    
    carreras, total_paginas = gestor_carrera().obtener_pagina(page)

    return render_template('carreras/carreras.html',carreras=carreras, total_paginas=total_paginas, csrf=csrf)