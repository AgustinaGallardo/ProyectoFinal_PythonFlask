import os
from flask import Flask
from flask_restful import Api
from modules.auth import auth_bp, login_manager
from modules.routes import routes_bp, page_not_found
from modules.routes_personas import personas_bp
from modules.routes_universidades import universidades_bp
from modules.routes_facultades import facultades_bp
from modules.routes_campus import campus_bp
from modules.routes_programas import programas_bp
from modules.routes_carreras import carreras_bp
from modules.apis.personas import PersonasResource
from modules.apis.carreras import CarrerasResource
from modules.apis.lugares import LugaresResource
from modules.apis.generos import GenerosResource
from modules.apis.carreras import CarrerasResource
from modules.apis.tipos import TiposResource
from modules.apis.carreras_noRelacionadas import CarrerasNoRelacionadasResource


from modules.models.base import db 
from config import db_connector, db_user, db_password, db_ip_address, db_name
from flask_jwt_extended import JWTManager
from modules.auth import csrf
from modules.models.entities import User

def create_app():
	app = Flask(__name__)
	app.secret_key = os.urandom(24)
	app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_connector}://{db_user}:{db_password}@{db_ip_address}/{db_name}"

	db.init_app(app)
	#api=Api(app)
	api=Api(app,decorators=[csrf.exempt])
	csrf.init_app(app)
	jwt = JWTManager(app)
	login_manager.init_app(app)
	
	with app.app_context():
		db.create_all()
		usuario=User(username=os.getenv("DEFAULT_USER"), password=os.getenv("DEFAULT_PASSWORD"))
		usuario.guardar()

	app.register_blueprint(auth_bp)
	app.register_blueprint(routes_bp)
	app.register_blueprint(personas_bp)
	app.register_blueprint(universidades_bp)
	app.register_blueprint(facultades_bp)
	app.register_blueprint(campus_bp)
	app.register_blueprint(programas_bp)
	app.register_blueprint(carreras_bp) 
	app.register_blueprint(carreras_bp, url_prefix='/carreras', name='carreras_blueprint')
	app.register_error_handler(404, page_not_found)
	api.add_resource(PersonasResource, '/api/personas', '/api/personas/<int:persona_id>')
	api.add_resource(LugaresResource, '/api/lugares', '/api/lugares/<string:lugar_type>')
	api.add_resource(GenerosResource, '/api/generos')
	api.add_resource(CarrerasResource, '/api/carreras', '/api/carreras/<string:carrera_type>')
	api.add_resource(TiposResource, '/api/tipos')
	api.add_resource(CarrerasNoRelacionadasResource, '/api/carrerasnorelac', '/api/carrerasnorelac/<string:carrera_type>')





	return app