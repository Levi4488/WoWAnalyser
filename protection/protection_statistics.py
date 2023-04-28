from flask import render_template, session
from flask import Blueprint
import requests
from access_token import access_token

protection_statistics = Blueprint(
    'protectionStatistics', __name__, template_folder='templates')

@protection_statistics.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@protection_statistics.route('/protection-statistics', methods=['POST', 'GET'])
def protection_statistics_function():

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

    payload1 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\tgraph(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID:"+source_id + \
        "\\n\\t\\t\\t\\tdataType: DamageDone\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload2 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\tgraph(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID:"+source_id + \
        "\\n\\t\\t\\t\\tdataType: Healing\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload3 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\tgraph(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID:"+source_id + \
        "\\n\\t\\t\\t\\tdataType: DamageTaken\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload4 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID: "+source_id + \
        "\\n\\t\\t\\t\\tdataType: DamageTaken\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload5 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID: "+source_id + \
        "\\n\\t\\t\\t\\tdataType: Casts\\n\\t\\t\\t\\tviewBy: Ability\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }

    response1 = requests.request(
        "POST", url, data=payload1, headers=headers).json()
    response2 = requests.request(
        "POST", url, data=payload2, headers=headers).json()
    response3 = requests.request(
        "POST", url, data=payload3, headers=headers).json()
    response4 = requests.request(
        "POST", url, data=payload4, headers=headers).json()
    response5 = requests.request(
        "POST", url, data=payload5, headers=headers).json()
    
    # DPS
    total_damage = 0
    damage_data = response1['data']['reportData']['report']['graph']['data']['series'][0]
    if 'total' in response1['data']['reportData']['report']['graph']['data']['series'][0]:
        total_damage = response1['data']['reportData']['report']['graph']['data']['series'][0]['total']
    damage_graph = damage_data['data']
    damage_length = len(damage_data['data'])

    # Calculating DPS
    damage_per_second = total_damage / total_time * 1000
    damage_per_second = round(damage_per_second)

    # HPS
    total_heals = 0
    heals_data = response2['data']['reportData']['report']['graph']['data']['series'][0]
    if 'total' in response2['data']['reportData']['report']['graph']['data']['series'][0]:
        total_heals = response2['data']['reportData']['report']['graph']['data']['series'][0]['total']
    heals_graph = heals_data['data']
    heals_length = len(heals_data['data'])

    # Calculating HPS
    heals_per_second = total_heals / total_time * 1000
    heals_per_second = round(heals_per_second)

    # DTPS
    total_dtps = 0
    dtps_data = response3['data']['reportData']['report']['graph']['data']['series'][0]
    if 'total' in response3['data']['reportData']['report']['graph']['data']['series'][0]:
        total_dtps = response3['data']['reportData']['report']['graph']['data']['series'][0]['total']
    dtps_graph = dtps_data['data']
    dtps_length = len(dtps_data['data'])

    # Calculating DTPS
    damage_taken_per_second = total_dtps / total_time * 1000
    damage_taken_per_second = round(damage_taken_per_second)

    # Getting Active Time and Percentage
    active_time = response4['data']['reportData']['report']['table']['data']['entries'][0]['activeTime']
    active_time_percent = ((active_time / total_time) * 100)
    active_time_percent = round(active_time_percent,2)

    # Total Damage Reduced
    total_damage_reduced = response4['data']['reportData']['report']['table']['data']['entries'][0]['totalReduced']

    # Blocked Damage
    blocked_damage = response4['data']['reportData']['report']['table']['data']['entries'][0]['blocked']

    # Theck-Meloree Index
    theck_meloree_index = response4['data']['reportData']['report']['table']['data']['entries'][0]['tmi']
    theck_meloree_index = round(theck_meloree_index)

    consecration_casts = 0
    shield_of_the_righteous_casts = 0
    judgment_casts = 0
    blessed_hammer_casts = 0
    hammer_of_wrath_casts = 0
    lay_on_hands_casts = 0
    word_of_glory_casts = 0
    ardent_defender_casts = 0
    guardian_of_ancient_kings_casts = 0
    divine_shield_casts = 0
    avengers_shield_casts = 0
    avenging_wrath_casts = 0
    divine_toll_casts = 0

    for casts in response5['data']['reportData']['report']['table']['data']['entries']:
        if 'Consecration' in casts['name']:
            consecration_casts = casts['total']
        if 'Shield of the Righteous' in casts['name']:
            shield_of_the_righteous_casts = casts['total']
        if 'Judgment' in casts['name']:
            judgment_casts = casts['total']
        if 'Blessed Hammer' in casts['name']:
            blessed_hammer_casts = casts['total']
        if 'Hammer of Wrath' in casts['name']:
            hammer_of_wrath_casts = casts['total']
        if 'Lay on Hands' in casts['name']:
            lay_on_hands_casts = casts['total']
        if 'Word of Glory' in casts['name']:
            word_of_glory_casts = casts['total']
        if 'Ardent Defender' in casts['name']:
            ardent_defender_casts = casts['total']
        if 'Guardian of Ancient Kings' in casts['name']:
            guardian_of_ancient_kings_casts = casts['total']
        if 'Divine Shield' in casts['name']:
            divine_shield_casts = casts['total']
        if "Avenger's Shield" in casts['name']:
            avengers_shield_casts = casts['total']
        if 'Avenging Wrath' in casts['name'] and casts['guid'] == 31884:
            avenging_wrath_casts = casts['total']
        if 'Divine Toll' in casts['name']:
            divine_toll_casts = casts['total']

    # Cooldowns
    consecration = 3900
    blessed_hammer = 5300
    lay_on_hands = 600000
    ardent_defender = 84000
    guardian_of_ancient_kings = 300000
    divine_shield = 300000
    avengers_shield = 13000
    avenging_wrath = 120000
    judgment = 5300
    hammer_of_wrath = 6600
    divine_toll = 60000

    hammer_of_wrath_potential_casts = total_time / hammer_of_wrath
    hammer_of_wrath_potential_casts = round(hammer_of_wrath_potential_casts)

    avenging_wrath_potential_casts = total_time / avenging_wrath
    avenging_wrath_potential_casts = round(avenging_wrath_potential_casts)

    divine_shield_potential_casts = total_time / divine_shield
    divine_shield_potential_casts = round(divine_shield_potential_casts)

    guardian_of_ancient_kings_potential_casts = total_time / guardian_of_ancient_kings
    guardian_of_ancient_kings_potential_casts = round(guardian_of_ancient_kings_potential_casts)

    ardent_defender_potential_casts = total_time / ardent_defender
    ardent_defender_potential_casts = round(ardent_defender_potential_casts)

    consecration_potential_casts = total_time / consecration
    consecration_potential_casts = round(consecration_potential_casts)

    blessed_hammer_potential_casts = total_time / blessed_hammer
    blessed_hammer_potential_casts = round(blessed_hammer_potential_casts)

    lay_on_hands_potential_casts = total_time / lay_on_hands
    lay_on_hands_potential_casts = round(lay_on_hands_potential_casts)

    avengers_shield_potential_casts = total_time / avengers_shield
    avengers_shield_potential_casts = round(avengers_shield_potential_casts)

    judgment_potential_casts = total_time / judgment
    judgment_potential_casts = round(judgment_potential_casts)

    divine_toll_potential_casts = total_time / divine_toll
    divine_toll_potential_casts = round(divine_toll_potential_casts)

    if hammer_of_wrath_potential_casts < 1:
        hammer_of_wrath_potential_casts = 1
    if avenging_wrath_potential_casts < 1:
        avenging_wrath_potential_casts = 1
    if divine_shield_potential_casts < 1:
        divine_shield_potential_casts = 1
    if guardian_of_ancient_kings_potential_casts < 1:
        guardian_of_ancient_kings_potential_casts = 1
    if ardent_defender_potential_casts < 1:
        ardent_defender_potential_casts = 1
    if consecration_potential_casts < 1:
        consecration_potential_casts = 1
    if blessed_hammer_potential_casts < 1:
        blessed_hammer_potential_casts = 1
    if lay_on_hands_potential_casts < 1:
        lay_on_hands_potential_casts = 1
    if avengers_shield_potential_casts < 1:
        avengers_shield_potential_casts = 1
    if judgment_potential_casts < 1:
        judgment_potential_casts = 1
    if divine_toll_potential_casts < 1:
        divine_toll_potential_casts = 1

    # Total Holy Power generation
    total_holy_power = judgment_casts + blessed_hammer_casts + hammer_of_wrath_casts

    # Calculating Holy Power Per Minute
    holy_power_per_min = total_holy_power / total_time * 60000
    holy_power_per_min = round(holy_power_per_min)

    # Total Holy Power spent
    shield_of_the_righteous_holy_power_spent = shield_of_the_righteous_casts * 3
    word_of_glory_holy_power_spent = word_of_glory_casts * 3
    holy_power_casts = shield_of_the_righteous_casts + word_of_glory_casts
    holy_power_spent = shield_of_the_righteous_holy_power_spent + word_of_glory_holy_power_spent

    # Holy Power wasted
    holy_power_wasted = total_holy_power - holy_power_spent
    holy_power_wasted_percent = holy_power_spent / total_holy_power * 100
    
    if holy_power_wasted < 0:
        holy_power_wasted = 0
    if holy_power_wasted_percent < 0:
        holy_power_wasted_percent = 0

    # Holy gen per ability percent
    judgment_holy_power_percent = judgment_casts / total_holy_power * 100
    judgment_holy_power_percent = round(judgment_holy_power_percent,2)
    blessed_hammer_holy_power_percent = blessed_hammer_casts / total_holy_power * 100
    blessed_hammer_holy_power_percent = round(blessed_hammer_holy_power_percent,2)
    hammer_of_wrath_holy_power_percent = hammer_of_wrath_casts / total_holy_power * 100
    hammer_of_wrath_holy_power_percent = round(hammer_of_wrath_holy_power_percent,2)

    # Consecration
    consecration_efficiency = consecration_casts / consecration_potential_casts * 100
    consecration_efficiency = round(consecration_efficiency,2)
    
    # Blessed Hammer
    blessed_hammer_efficiency = blessed_hammer_casts / blessed_hammer_potential_casts * 100
    blessed_hammer_efficiency = round(blessed_hammer_efficiency,2)
    
    # Lay on Hands
    lay_on_hands_efficiency = lay_on_hands_casts / lay_on_hands_potential_casts * 100
    lay_on_hands_efficiency = round(lay_on_hands_efficiency,2)
    
    # Avengers Shield
    avengers_shield_efficiency = avengers_shield_casts / avengers_shield_potential_casts * 100
    avengers_shield_efficiency = round(avengers_shield_efficiency,2)
    
    # Avenging Wrath
    avenging_wrath_efficiency = avenging_wrath_casts / avenging_wrath_potential_casts * 100
    avenging_wrath_efficiency = round(avenging_wrath_efficiency,2)
    
    # Judgment
    judgment_efficiency = judgment_casts / judgment_potential_casts * 100
    judgment_efficiency = round(judgment_efficiency,2)
    
    # Hammer of Wrath
    hammer_of_wrath_efficiency = hammer_of_wrath_casts / hammer_of_wrath_potential_casts * 100
    hammer_of_wrath_efficiency = round(hammer_of_wrath_efficiency,2)
    
    # Divine Toll
    divine_toll_efficiency = divine_toll_casts / divine_toll_potential_casts * 100
    divine_toll_efficiency = round(divine_toll_efficiency,2)
    
    # Ardent Defender
    ardent_defender_efficiency = ardent_defender_casts / ardent_defender_potential_casts * 100
    ardent_defender_efficiency = round(ardent_defender_efficiency,2)
    
    # Guardian of Ancient Kings
    guardian_of_ancient_kings_efficiency = guardian_of_ancient_kings_casts / guardian_of_ancient_kings_potential_casts * 100
    guardian_of_ancient_kings_efficiency = round(guardian_of_ancient_kings_efficiency,2)
    
    # Divine Shield
    divine_shield_efficiency = divine_shield_casts / divine_shield_potential_casts * 100
    divine_shield_efficiency = round(divine_shield_efficiency,2)
    
    # CPM
    word_of_glory_cpm = word_of_glory_casts / total_time * 60000
    word_of_glory_cpm = round(word_of_glory_cpm,2)
    ardent_defender_cpm = ardent_defender_casts / total_time * 60000
    ardent_defender_cpm = round(ardent_defender_cpm,2)
    guardian_of_ancient_kings_cpm = guardian_of_ancient_kings_casts / total_time * 60000
    guardian_of_ancient_kings_cpm = round(guardian_of_ancient_kings_cpm,2)
    divine_shield_cpm = divine_shield_casts / total_time * 60000
    divine_shield_cpm = round(divine_shield_cpm,2)
    consecration_cpm = consecration_casts / total_time * 60000
    consecration_cpm = round(consecration_cpm,2)
    blessed_hammer_cpm = blessed_hammer_casts / total_time * 60000
    blessed_hammer_cpm = round(blessed_hammer_cpm,2)
    lay_on_hands_cpm = lay_on_hands_casts / total_time * 60000
    lay_on_hands_cpm = round(lay_on_hands_cpm,2)
    shield_of_the_righteous_cpm = shield_of_the_righteous_casts / total_time * 60000
    shield_of_the_righteous_cpm = round(shield_of_the_righteous_cpm,2)
    avengers_shield_cpm = avengers_shield_casts / total_time * 60000
    avengers_shield_cpm = round(avengers_shield_cpm,2)
    avenging_wrath_cpm = avenging_wrath_casts / total_time * 60000
    avenging_wrath_cpm = round(avenging_wrath_cpm,2)
    judgment_cpm = judgment_casts / total_time * 60000
    judgment_cpm = round(judgment_cpm,2)
    hammer_of_wrath_cpm = hammer_of_wrath_casts / total_time * 60000
    hammer_of_wrath_cpm = round(hammer_of_wrath_cpm,2)
    divine_toll_cpm = divine_toll_casts / total_time * 60000
    divine_toll_cpm = round(divine_toll_cpm,2)

    return render_template('protection/protection_statistics.html', damage_per_second=damage_per_second, heals_per_second=heals_per_second, damage_taken_per_second=damage_taken_per_second,
                           damage_graph=damage_graph, damage_length=damage_length, heals_graph=heals_graph, heals_length=heals_length, dtps_graph=dtps_graph, dtps_length=dtps_length,
                           total_holy_power=total_holy_power,holy_power_wasted=holy_power_wasted,holy_power_spent=holy_power_spent,shield_of_the_righteous_casts=shield_of_the_righteous_casts,shield_of_the_righteous_cpm=shield_of_the_righteous_cpm,
                           holy_power_per_min=holy_power_per_min,consecration_casts=consecration_casts,consecration_potential_casts=consecration_potential_casts,consecration_efficiency=consecration_efficiency,consecration_cpm=consecration_cpm,
                           blessed_hammer_cpm=blessed_hammer_cpm,blessed_hammer_casts=blessed_hammer_casts,blessed_hammer_potential_casts=blessed_hammer_potential_casts,blessed_hammer_efficiency=blessed_hammer_efficiency,
                           lay_on_hands_cpm=lay_on_hands_cpm,lay_on_hands_casts=lay_on_hands_casts,lay_on_hands_potential_casts=lay_on_hands_potential_casts,lay_on_hands_efficiency=lay_on_hands_efficiency,word_of_glory_cpm=word_of_glory_cpm,
                           word_of_glory_casts=word_of_glory_casts,ardent_defender_cpm=ardent_defender_cpm,ardent_defender_casts=ardent_defender_casts,ardent_defender_potential_casts=ardent_defender_potential_casts,
                           ardent_defender_efficiency=ardent_defender_efficiency,guardian_of_ancient_kings_cpm=guardian_of_ancient_kings_cpm,guardian_of_ancient_kings_casts=guardian_of_ancient_kings_casts,
                           guardian_of_ancient_kings_potential_casts=guardian_of_ancient_kings_potential_casts,guardian_of_ancient_kings_efficiency=guardian_of_ancient_kings_efficiency,divine_shield_cpm=divine_shield_cpm,
                           divine_shield_casts=divine_shield_casts,divine_shield_potential_casts=divine_shield_potential_casts,divine_shield_efficiency=divine_shield_efficiency,boss_difficulty=boss_difficulty,boss_name=boss_name,
                           player_name=player_name,player_type=player_type,player_spec=player_spec,shield_of_the_righteous_holy_power_spent=shield_of_the_righteous_holy_power_spent,word_of_glory_holy_power_spent=word_of_glory_holy_power_spent,
                           holy_power_casts=holy_power_casts,avengers_shield_casts=avengers_shield_casts,avengers_shield_potential_casts=avengers_shield_potential_casts,avengers_shield_cpm=avengers_shield_cpm,
                           avengers_shield_efficiency=avengers_shield_efficiency,avenging_wrath_casts=avenging_wrath_casts,avenging_wrath_potential_casts=avenging_wrath_potential_casts,avenging_wrath_cpm=avenging_wrath_cpm,
                           avenging_wrath_efficiency=avenging_wrath_efficiency,judgment_casts=judgment_casts,judgment_potential_casts=judgment_potential_casts,judgment_cpm=judgment_cpm,judgment_efficiency=judgment_efficiency,
                           hammer_of_wrath_casts=hammer_of_wrath_casts,hammer_of_wrath_potential_casts=hammer_of_wrath_potential_casts,hammer_of_wrath_cpm=hammer_of_wrath_cpm,hammer_of_wrath_efficiency=hammer_of_wrath_efficiency,
                           divine_toll_casts=divine_toll_casts,divine_toll_potential_casts=divine_toll_potential_casts,divine_toll_cpm=divine_toll_cpm,divine_toll_efficiency=divine_toll_efficiency,
                           judgment_holy_power_percent=judgment_holy_power_percent,blessed_hammer_holy_power_percent=blessed_hammer_holy_power_percent,hammer_of_wrath_holy_power_percent=hammer_of_wrath_holy_power_percent,
                           active_time_percent=active_time_percent,total_damage_reduced=total_damage_reduced,blocked_damage=blocked_damage,theck_meloree_index=theck_meloree_index)
