from flask import render_template, session
from flask import Blueprint
import requests
from access_token import access_token

holy_timeline = Blueprint('holyTimeline', __name__, template_folder='templates')

@holy_timeline.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@holy_timeline.route('/holy-timeline', methods=['POST', 'GET'])
def holy_timeline_function():

    report_code = session['reportCode']
    source_id = session['sourceId']
    start_time = session['bossStartTime']
    end_time = session['bossEndTime']
    total_time = session['totalTime']
    encounter_id = session['bossEncounterId']
    boss_difficulty = session['bossDifficulty']
    boss_name = session['bossName']
    player_name = session['playerName']
    player_type = session['playerType']
    player_spec = session['playerSpec']

    url = "https://www.warcraftlogs.com/api/v2/client"

    payload = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\tgraph(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tsourceID: "+source_id+"\\n\\t\\t\\t\\tencounterID: "+encounter_id + \
        "\\n\\t\\t\\t\\tdataType: Casts\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers).json()

    holy_shock = 6600
    holy_light = 2200
    flash_of_light = 1500
    crusader_strike = 5300
    hammer_of_wrath = 6600

    name_list = []
    timestamp_list = []

    holy_shock_start_time_list = []
    holy_shock_end_time_list = []

    holy_light_start_time_list = []
    holy_light_end_time_list = []

    flash_of_light_start_time_list = []
    flash_of_light_end_time_list = []

    crusader_strike_start_time_list = []
    crusader_strike_end_time_list = []

    hammer_of_wrath_start_time_list = []
    hammer_of_wrath_end_time_list = []

    for timeline in response['data']['reportData']['report']['graph']['data']['series'][0]['events']:
        names = timeline[0]['ability']['name']
        timestamps = timeline[0]['timestamp']
        timestamp_result = int(timestamps) - int(start_time)
        name_list.append(names)
        timestamp_list.append(timestamp_result)

    for abilities in response['data']['reportData']['report']['graph']['data']['series'][0]['events']:
        if 'Holy Shock' in abilities[0]['ability']['name']:
            holy_shock_timestamps = abilities[0]['timestamp']
            holy_shock_timestamps_result = (int(holy_shock_timestamps) - int(start_time))
            holy_shock_end_timestamp = (int(holy_shock_timestamps) - int(start_time)) + holy_shock
            holy_shock_start_time_list.append(holy_shock_timestamps_result)
            holy_shock_end_time_list.append(holy_shock_end_timestamp)
        if 'Holy Light' in abilities[0]['ability']['name']:
            holy_light_timestamps = abilities[0]['timestamp']
            holy_light_timestamps_result = (int(holy_light_timestamps) - int(start_time))
            holy_light_end_timestamp = (int(holy_light_timestamps) - int(start_time)) + holy_light
            holy_light_start_time_list.append(holy_light_timestamps_result)
            holy_light_end_time_list.append(holy_light_end_timestamp)
        if 'Flash of Light' in abilities[0]['ability']['name']:
            flash_of_light_timestamps = abilities[0]['timestamp']
            flash_of_light_timestamps_result = (int(flash_of_light_timestamps) - int(start_time))
            flash_of_light_end_timestamp = (int(flash_of_light_timestamps) - int(start_time)) + flash_of_light
            flash_of_light_start_time_list.append(flash_of_light_timestamps_result)
            flash_of_light_end_time_list.append(flash_of_light_end_timestamp)
        if 'Crusader Strike' in abilities[0]['ability']['name']:
            crusader_strike_timestamps = abilities[0]['timestamp']
            crusader_strike_timestamps_result = (int(crusader_strike_timestamps) - int(start_time))
            crusader_strike_end_timestamp = (int(crusader_strike_timestamps) -
                            int(start_time)) + crusader_strike
            crusader_strike_start_time_list.append(crusader_strike_timestamps_result)
            crusader_strike_end_time_list.append(crusader_strike_end_timestamp)
        if 'Hammer of Wrath' in abilities[0]['ability']['name']:
            hammer_of_wrath_timestamps = abilities[0]['timestamp']
            hammer_of_wrath_timestamps_result = (int(hammer_of_wrath_timestamps) - int(start_time))
            hammer_of_wrath_end_timestamp = (int(hammer_of_wrath_timestamps) -
                             int(start_time)) + hammer_of_wrath
            hammer_of_wrath_start_time_list.append(hammer_of_wrath_timestamps_result)
            hammer_of_wrath_end_time_list.append(hammer_of_wrath_end_timestamp)

    return render_template('holy/holy_timeline.html', name_list=name_list, timestamp_list=timestamp_list, holy_shock_start_time_list=holy_shock_start_time_list, 
                           holy_shock_end_time_list=holy_shock_end_time_list,holy_light_start_time_list=holy_light_start_time_list, 
                           holy_light_end_time_list=holy_light_end_time_list,boss_difficulty=boss_difficulty,boss_name=boss_name,player_name=player_name,
                           player_type=player_type,player_spec=player_spec,flash_of_light_start_time_list=flash_of_light_start_time_list,
                           flash_of_light_end_time_list=flash_of_light_end_time_list,crusader_strike_start_time_list=crusader_strike_start_time_list,
                           crusader_strike_end_time_list=crusader_strike_end_time_list,hammer_of_wrath_start_time_list=hammer_of_wrath_start_time_list,
                           hammer_of_wrath_end_time_list=hammer_of_wrath_end_time_list, zip=zip)