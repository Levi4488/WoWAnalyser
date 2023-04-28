from flask import abort, render_template, request, url_for, redirect, session
from flask import Blueprint
import requests
import time
from access_token import access_token

boss_selection = Blueprint('bossSelection', __name__, template_folder='templates')

@boss_selection.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@boss_selection.route('/boss-selection', methods=['POST', 'GET'])
def boss_selection_function():

    report_code = session['reportCode']

    url = "https://www.warcraftlogs.com/api/v2/client"

    payload = "{\"query\":\"{\\n\\treportData{\\n\\t\\treport(code:\\\""+report_code + \
        "\\\"){\\n\\t\\t\\tfights(killType:Encounters){name,encounterID,difficulty,startTime,endTime,kill,averageItemLevel}\\n\\t\\t}\\n\\t}\\n}\\n\\n\\n\\n\"}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers).json()

    time_list = []

    for timeData in response['data']['reportData']['report']['fights']:
        start_time = timeData['startTime']
        end_time = timeData['endTime']
        total_time = end_time - start_time
        time_seconds = total_time / 1000
        convert_seconds = time.gmtime(time_seconds)
        formatted_time = time.strftime("%M:%S", convert_seconds)
        time_list.append(formatted_time)

    boss_name_list = []
    boss_encounter_id_list = []
    boss_difficulty_list = []
    boss_start_time_list = []
    boss_end_time_list = []
    boss_kill_list = []
    average_item_level_list = []

    for boss in response['data']['reportData']['report']['fights']:
        boss_name = boss['name']
        boss_encounter_id = boss['encounterID']
        boss_difficulty = boss['difficulty']
        boss_start_time = boss['startTime']
        boss_end_time = boss['endTime']
        boss_kill = boss['kill']
        average_item_level = boss['averageItemLevel']
        average_item_level = round(average_item_level)
        if boss_difficulty == 3:
            difficulty_name = "Normal"
        elif boss_difficulty == 4:
            difficulty_name = "Heroic"
        elif boss_difficulty == 5:
            difficulty_name = "Mythic"
        boss_name_list.append(boss_name)
        boss_encounter_id_list.append(boss_encounter_id)
        boss_difficulty_list.append(difficulty_name)
        boss_start_time_list.append(boss_start_time)
        boss_end_time_list.append(boss_end_time)
        boss_kill_list.append(boss_kill)
        average_item_level_list.append(average_item_level)

    if request.method == 'POST':
        session['bossName'] = request.form['bossName']
        session['bossEncounterId'] = request.form['bossEncounterId']
        session['bossDifficulty'] = request.form['bossDifficulty']
        session['bossStartTime'] = request.form['bossStartTime']
        session['bossEndTime'] = request.form['bossEndTime']
        session['time'] = request.form['time']
        session['averageItemLevel'] = request.form['averageItemLevel']
        return redirect(url_for('playerSelection.player_selection_function'))

    if response['data']['reportData']['report'] is None:
        abort(500)

    return render_template('boss_selection.html', time_list=time_list, boss_name_list=boss_name_list, 
                           boss_encounter_id_list=boss_encounter_id_list, boss_difficulty_list=boss_difficulty_list, 
                           boss_start_time_list=boss_start_time_list, boss_end_time_list=boss_end_time_list, 
                           boss_kill_list=boss_kill_list, average_item_level_list=average_item_level_list, zip=zip)