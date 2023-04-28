from flask import render_template
from flask import Blueprint

work_in_progress = Blueprint('workInProgress',__name__, template_folder='templates')

@work_in_progress.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@work_in_progress.route('/work-in-progress')
def work_in_progress_function():

    return render_template('work_in_progress.html')