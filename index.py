from flask import render_template,request,url_for,redirect,session
from flask import Blueprint

index = Blueprint('index',__name__, template_folder='templates')

@index.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@index.route('/')
@index.route('/index', methods=['POST', 'GET'])
def index_function():
    if request.method == 'POST':
        session['reportCode'] = request.form['reportCode']
        return redirect(url_for('bossSelection.boss_selection_function'))
    return render_template('index.html')