from flask import render_template


def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(_error):
        return (
            render_template(
                "errors/404.html",
                meta_title="Страница не найдена — НОВА",
                meta_description="Запрошенной страницы нет на сайте НОВА.",
                canonical=None,
            ),
            404,
        )

    @app.errorhandler(500)
    def server_error(_error):
        return render_template("errors/500.html"), 500
