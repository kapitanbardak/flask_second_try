from flask import jsonify


def init_routes(app):
    @app.route("/api", methods=["GET"])
    def get_api_base_url():
        return jsonify({
            "msg": "todos api is up",
            "success": True,
            "data": None
        }), 200

    @app.route('/')
    def hello_world():
        return 'Hello World!'
