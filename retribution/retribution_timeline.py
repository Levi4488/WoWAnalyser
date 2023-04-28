from flask import render_template, session
from flask import Blueprint
import requests
from access_token import access_token

retribution_timeline = Blueprint('retributionTimeline', __name__, template_folder='templates')

@retribution_timeline.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@retribution_timeline.route('/retribution-timeline', methods=['POST', 'GET'])
def retribution_timeline_function():

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

    judgment = 7900
    hammer_of_wrath = 6600
    blade_of_justice = 11000
    execution_sentence = 30000
    wake_of_ashes = 30000

    name_list = []
    timestamp_list = []

    judgment_start_time_list = []
    judgment_end_time_list = []

    hammer_of_wrath_start_time_list = []
    hammer_of_wrath_end_time_list = []

    blade_of_justice_start_time_list = []
    blade_of_justice_end_time_list = []

    execution_sentence_start_time_list = []
    execution_sentence_end_time_list = []

    wake_of_ashes_start_time_list = []
    wake_of_ashes_end_time_list = []

    for timeline in response['data']['reportData']['report']['graph']['data']['series'][0]['events']:
        names = timeline[0]['ability']['name']
        timestamps = timeline[0]['timestamp']
        timestamps_result = (int(timestamps) - int(start_time))
        name_list.append(names)
        timestamp_list.append(timestamps_result)

    for abilities in response['data']['reportData']['report']['graph']['data']['series'][0]['events']:
        if 'Judgment' in abilities[0]['ability']['name']:
            judgment_timestamps = abilities[0]['timestamp']
            judgment_timestamps_result = (int(judgment_timestamps) - int(start_time))
            judgment_end_timestamp = (int(judgment_timestamps) - int(start_time)) + judgment
            judgment_start_time_list.append(judgment_timestamps_result)
            judgment_end_time_list.append(judgment_end_timestamp)
        if 'Hammer of Wrath' in abilities[0]['ability']['name']:
            hammer_of_wrath_timestamps = abilities[0]['timestamp']
            hammer_of_wrath_timestamps_result = (int(hammer_of_wrath_timestamps) - int(start_time))
            hammer_of_wrath_end_timestamp = (int(hammer_of_wrath_timestamps) -
                            int(start_time)) + hammer_of_wrath
            hammer_of_wrath_start_time_list.append(hammer_of_wrath_timestamps_result)
            hammer_of_wrath_end_time_list.append(hammer_of_wrath_end_timestamp)
        if 'Blade of Justice' in abilities[0]['ability']['name']:
            blade_of_justice_timestamps = abilities[0]['timestamp']
            blade_of_justice_timestamps_result = (int(blade_of_justice_timestamps) - int(start_time))
            blade_of_justice_end_timestamp = (int(blade_of_justice_timestamps) -
                            int(start_time)) + blade_of_justice
            blade_of_justice_start_time_list.append(blade_of_justice_timestamps_result)
            blade_of_justice_end_time_list.append(blade_of_justice_end_timestamp)
        if 'Execution Sentence' in abilities[0]['ability']['name']:
            execution_sentence_timestamps = abilities[0]['timestamp']
            execution_sentence_timestamps_result = (int(execution_sentence_timestamps) - int(start_time))
            execution_sentence_end_timestamp = (int(execution_sentence_timestamps) -
                            int(start_time)) + execution_sentence
            execution_sentence_start_time_list.append(execution_sentence_timestamps_result)
            execution_sentence_end_time_list.append(execution_sentence_end_timestamp)
        if 'Wake of Ashes' in abilities[0]['ability']['name']:
            wake_of_ashes_timestamps = abilities[0]['timestamp']
            wake_of_ashes_timestamps_result = (int(wake_of_ashes_timestamps) - int(start_time))
            wake_of_ashes_end_timestamp = (int(wake_of_ashes_timestamps) -
                            int(start_time)) + wake_of_ashes
            wake_of_ashes_start_time_list.append(wake_of_ashes_timestamps_result)
            wake_of_ashes_end_time_list.append(wake_of_ashes_end_timestamp)
        

    return render_template('retribution/retribution_timeline.html', name_list=name_list, timestamp_list=timestamp_list, judgment_start_time_list=judgment_start_time_list,
                           judgment_end_time_list=judgment_end_time_list, hammer_of_wrath_start_time_list=hammer_of_wrath_start_time_list, 
                           hammer_of_wrath_end_time_list=hammer_of_wrath_end_time_list,blade_of_justice_start_time_list=blade_of_justice_start_time_list,
                           blade_of_justice_end_time_list=blade_of_justice_end_time_list,execution_sentence_start_time_list=execution_sentence_start_time_list,
                           execution_sentence_end_time_list=execution_sentence_end_time_list,boss_difficulty=boss_difficulty,boss_name=boss_name,player_name=player_name,
                           player_type=player_type,player_spec=player_spec,wake_of_ashes_start_time_list=wake_of_ashes_start_time_list,
                           wake_of_ashes_end_time_list=wake_of_ashes_end_time_list,zip=zip)