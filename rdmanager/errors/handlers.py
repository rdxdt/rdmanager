from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('error.html',errorcode='404',errormessage='Not found.'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('error.html',errorcode='403',errormessage='Forbidden.'), 403

@errors.app_errorhandler(405)
def error_405(error):
    return render_template('error.html',errorcode='405',errormessage='Request not supported'), 405


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('error.html',errorcode='500',errormessage='Internal error.'), 500