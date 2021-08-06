from flask import Flask, render_template, request, send_from_directory

from sassutils.wsgi import SassMiddleware

from .config import setup_configuration


def create_app():
    app = Flask(__name__, static_url_path="/static")
    # app.config.from_object(config_class)

    app.wsgi_app = SassMiddleware(
        app.wsgi_app, {"audio": ("static/sass", "static/css", "/static/css")}
    )

    @app.route("/", methods=["GET"])
    def root():
        ctx = {}
        ctx["title"] = setup_configuration.get("title", "Alan's Audio")
        ctx["year"] = setup_configuration.get("year", "2020")
        ctx["email"] = setup_configuration.get("email")
        ctx["instagram"] = setup_configuration.get("instagram", "http://instagram.com")
        ctx["youtube"] = setup_configuration.get("youtube", "http://youtube.com")
        ctx["google_site_verification"] = setup_configuration.get(
            "google_site_verification"
        )

        return render_template(
            "home.html",
            ctx=ctx,
        )

    # serve files for robots
    # @app.route("/sitemap.xml")
    @app.route("/robots.txt")
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])

    return app
