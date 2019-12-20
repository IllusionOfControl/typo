from flask import render_template


def forbidden(error):
    return render_template("errors/403.html", error=error.description), 403


def page_not_found(error):
    return render_template('errors/404.html', error=error.description), 404


def general_error(error):
    return render_template("errors/502.html", error=error.description), 502