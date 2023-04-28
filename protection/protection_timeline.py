from flask import render_template, session
from flask import Blueprint
import requests
from access_token import access_token

protection_timeline = Blueprint('protectionTimeline', __name__, template_folder='templates')

@protection_timeline.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@protection_timeline.route('/protection-timeline', methods=['POST', 'GET'])
def protection_timeline_function():

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

    judgment = 5300
    avengers_shield = 13000
    consecration = 3900
    hammer_of_wrath = 6600
    shield_of_the_righteous = 6000

    name_list = []
    timestamp_list = []

    judgment_start_time_list = []
    judgment_end_time_list = []
    avengers_shield_start_time_list = []
    avengers_shield_end_time_list = []
    consecration_start_time_list = []
    consecration_end_time_list = []
    hammer_of_wrath_start_time_list = []
    hammer_of_wrath_end_time_list = []
    shield_of_the_righteous_start_time_list = []
    shield_of_the_righteous_end_time_list = []

    for timeline in response['data']['reportData']['report']['graph']['data']['series'][0]['events']:
        names = timeline[0]['ability']['name']
        timestamps = timeline[0]['timestamp']
        timestamps_result = int(timestamps) - int(start_time)
        name_list.append(names)
        timestamp_list.append(timestamps_result)

    for abilities in response['data']['reportData']['report']['graph']['data']['series'][0]['events']:
        if 'Judgment' in abilities[0]['ability']['name']:
            judgment_timestamps = abilities[0]['timestamp']
            judgment_timestamps_result = (int(judgment_timestamps) - int(start_time))
            judgment_end_timestamp = (int(judgment_timestamps) - int(start_time)) + judgment
            judgment_start_time_list.append(judgment_timestamps_result)
            judgment_end_time_list.append(judgment_end_timestamp)
        if "Avenger's Shield" in abilities[0]['ability']['name']:
            avengers_shield_timestamps = abilities[0]['timestamp']
            avengers_shield_timestamps_result = (int(avengers_shield_timestamps) - int(start_time))
            avengers_shield_end_timestamp = (int(avengers_shield_timestamps) -
                              int(start_time)) + avengers_shield
            avengers_shield_start_time_list.append(avengers_shield_timestamps_result)
            avengers_shield_end_time_list.append(avengers_shield_end_timestamp)
        if 'Consecration' in abilities[0]['ability']['name']:
            consecration_timestamps = abilities[0]['timestamp']
            consecration_timestamps_result = (int(consecration_timestamps) - int(start_time))
            consecration_end_timestamp = (int(consecration_timestamps) -
                             int(start_time)) + consecration
            consecration_start_time_list.append(consecration_timestamps_result)
            consecration_end_time_list.append(consecration_end_timestamp)
        if 'Hammer of Wrath' in abilities[0]['ability']['name']:
            hammer_of_wrath_timestamps = abilities[0]['timestamp']
            hammer_of_wrath_timestamps_result = (int(hammer_of_wrath_timestamps) - int(start_time))
            hammer_of_wrath_end_timestamp = (int(hammer_of_wrath_timestamps) -
                             int(start_time)) + hammer_of_wrath
            hammer_of_wrath_start_time_list.append(hammer_of_wrath_timestamps_result)
            hammer_of_wrath_end_time_list.append(hammer_of_wrath_end_timestamp)
        if 'Shield of the Righteous' in abilities[0]['ability']['name']:
            shield_of_the_righteous_timestamps = abilities[0]['timestamp']
            shield_of_the_righteous_timestamps_result = (int(shield_of_the_righteous_timestamps) - int(start_time))
            shield_of_the_righteous_end_timestamp = (int(shield_of_the_righteous_timestamps) -
                             int(start_time)) + shield_of_the_righteous
            shield_of_the_righteous_start_time_list.append(shield_of_the_righteous_timestamps_result)
            shield_of_the_righteous_end_time_list.append(shield_of_the_righteous_end_timestamp)

    return render_template('protection/protection_timeline.html', name_list=name_list, timestamp_list=timestamp_list, judgment_start_time_list=judgment_start_time_list, 
                           judgment_end_time_list=judgment_end_time_list, avengers_shield_start_time_list=avengers_shield_start_time_list, avengers_shield_end_time_list=avengers_shield_end_time_list, 
                           consecration_start_time_list=consecration_start_time_list, consecration_end_time_list=consecration_end_time_list, boss_difficulty=boss_difficulty,
                           boss_name=boss_name,player_name=player_name,player_type=player_type,player_spec=player_spec, hammer_of_wrath_start_time_list=hammer_of_wrath_start_time_list,
                           hammer_of_wrath_end_time_list=hammer_of_wrath_end_time_list,shield_of_the_righteous_start_time_list=shield_of_the_righteous_start_time_list,
                           shield_of_the_righteous_end_time_list=shield_of_the_righteous_end_time_list, zip=zip)