from flask import Blueprint, request, jsonify
from modules.common.gestor_carrera import gestor_carrera

carreras_bp = Blueprint('routes_carreras', __name__)

@carreras_bp.route('/carreras', methods=['GET'])
def obtener_carreras():
    carreras = gestor_carrera().consultar_carreras()
    carreras_data = [carrera.serialize() for carrera in carreras]
    return jsonify({"Exito": True, "MensajePorFallo": None, "Resultado": carreras_data})

