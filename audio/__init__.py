from flask import Flask, render_template, request, send_from_directory

from sassutils.wsgi import SassMiddleware


def create_app():
    app = Flask(__name__, static_url_path="/static")
    # app.config.from_object(config_class)

    app.wsgi_app = SassMiddleware(
        app.wsgi_app, {"audio": ("static/sass", "static/css", "/static/css")}
    )

    @app.route("/", methods=["GET"])
    def root():
        return render_template(
            "layout.html",
            title="Sample Title",
        )

    # serve files for robots
    # @app.route("/sitemap.xml")
    @app.route("/robots.txt")
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])

    return app
