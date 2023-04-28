from operator import length_hint
from flask import render_template, request, url_for, redirect, session
from flask import Blueprint

import requests

from access_token import access_token

player_selection = Blueprint(
    'playerSelection', __name__, template_folder='templates')


@player_selection.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500


@player_selection.route('/player-selection', methods=['POST', 'GET'])
def player_selection_function():

    report_code = session['reportCode']
    start_time = session['bossStartTime']
    end_time = session['bossEndTime']
    encounter_id = session['bossEncounterId']
    boss_name = session['bossName']
    boss_difficulty = session['bossDifficulty']
    time = session['time']
    average_item_level = session['averageItemLevel']

    total_time = (int(end_time) - int(start_time))
    session['totalTime'] = total_time

    url = "https://www.warcraftlogs.com/api/v2/client"

    payload = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\tplayerDetails(startTime: "+start_time+", endTime: "+end_time+", encounterID: "+encounter_id+")\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers).json()


    name_list = []
    id_list = []
    type_list = []
    spec_list = []
    item_level_list = []
    potion_use_list = []
    healthstone_use_list = []

    for healers in response['data']['reportData']['report']['playerDetails']['data']['playerDetails']['healers']:
        healer_name = healers['name']
        healer_id = healers['id']
        healer_type = healers['type']
        healer_spec = healers['specs'][0]['spec']
        healer_itemlv = healers['maxItemLevel']
        healer_potion_use = healers['potionUse']
        healer_healthstone_use = healers['healthstoneUse']
        name_list.append(healer_name)
        id_list.append(healer_id)
        type_list.append(healer_type)
        spec_list.append(healer_spec)
        item_level_list.append(healer_itemlv)
        potion_use_list.append(healer_potion_use)
        healthstone_use_list.append(healer_healthstone_use)

    for dps in response['data']['reportData']['report']['playerDetails']['data']['playerDetails']['dps']:
        dps_name = dps['name']
        dps_id = dps['id']
        dps_type = dps['type']
        dps_spec = dps['specs'][0]['spec']
        dps_itemlv = dps['maxItemLevel']
        dps_potion_use = dps['potionUse']
        dps_healthstone_use = dps['healthstoneUse']
        name_list.append(dps_name)
        id_list.append(dps_id)
        type_list.append(dps_type)
        spec_list.append(dps_spec)
        item_level_list.append(dps_itemlv)
        potion_use_list.append(dps_potion_use)
        healthstone_use_list.append(dps_healthstone_use)

    for tank in response['data']['reportData']['report']['playerDetails']['data']['playerDetails']['tanks']:
        tank_name = tank['name']
        tank_id = tank['id']
        tank_type = tank['type']
        tank_spec = tank['specs'][0]['spec']
        tank_itemlv = tank['maxItemLevel']
        tank_potion_use = tank['potionUse']
        tank_healthstone_use = tank['healthstoneUse']
        name_list.append(tank_name)
        id_list.append(tank_id)
        type_list.append(tank_type)
        spec_list.append(tank_spec)
        item_level_list.append(tank_itemlv)
        potion_use_list.append(tank_potion_use)
        healthstone_use_list.append(tank_healthstone_use)

    healer_tally = len(response['data']['reportData']['report']['playerDetails']['data']['playerDetails']['healers'])
    dps_tally = len(response['data']['reportData']['report']['playerDetails']['data']['playerDetails']['dps'])
    tank_tally = len(response['data']['reportData']['report']['playerDetails']['data']['playerDetails']['tanks'])

    if request.method == 'POST':
        session['sourceId'] = request.form['sourceId']
        session['playerName'] = request.form['playerName']
        session['playerType'] = request.form['playerType']
        session['playerSpec'] = request.form['playerSpec']
        session['playerItemLevel'] = request.form['playerItemLevel']
        session['playerPotionUse'] = request.form['playerPotionUse']
        session['playerHealthstoneUse'] = request.form['playerHealthstoneUse']
        if session['playerSpec'] == "Retribution" and session['playerType'] == "Paladin":
            return redirect(url_for('retributionOverview.retribution_overview_function'))
        if session['playerSpec'] == "Protection" and session['playerType'] == "Paladin":
            return redirect(url_for('protectionOverview.protection_overview_function'))
        if session['playerSpec'] == "Holy" and session['playerType'] == "Paladin":
            return redirect(url_for('holyOverview.holy_overview_function'))
        return redirect(url_for('workInProgress.work_in_progress_function'))

    return render_template('player_selection.html', boss_name=boss_name, tank_tally=tank_tally, healer_tally=healer_tally, dps_tally=dps_tally, 
                           boss_difficulty=boss_difficulty, name_list=name_list, id_list=id_list, type_list=type_list,
                           spec_list=spec_list, item_level_list=item_level_list, potion_use_list=potion_use_list, healthstone_use_list=healthstone_use_list,
                           time=time, average_item_level=average_item_level,zip=zip)
