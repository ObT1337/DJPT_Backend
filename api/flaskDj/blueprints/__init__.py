def register_all_blueprints(app):
    from flaskDj.config import Config
    for bp in Config.BLUEPRINTS:
        app.register_blueprint(bp.bp)