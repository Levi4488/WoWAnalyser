from flask import render_template, session
from flask import Blueprint
import requests
from access_token import access_token

holy_overview = Blueprint('holyOverview', __name__, template_folder='templates')

@holy_overview.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@holy_overview.route('/holy-overview', methods=['POST', 'GET'])
def holy_overview_function():

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
    player_itemlvl = session['playerItemLevel']
    player_potion_use = session['playerPotionUse']
    player_healthstone_use = session['playerHealthstoneUse']

    url = "https://www.warcraftlogs.com/api/v2/client"

    payload1 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID:"+source_id + \
        "\\n\\t\\t\\t\\tdataType: Summary\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload2 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID: "+source_id + \
        "\\n\\t\\t\\t\\tdataType: Healing\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload3 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID: "+source_id + \
        "\\n\\t\\t\\t\\tdataType: Casts\\n\\t\\t\\t\\tviewBy: Ability\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload4 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: " + \
        end_time+"\\n\\t\\t\\t\\tencounterID: "+encounter_id + \
        "\\n\\t\\t\\t\\tdataType: Buffs\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
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

    # Checking weapons and armor for enchants
    weapon_enchant = False
    weapon_enhanced = False
    chest_enchant = False
    legguards_enchant = False
    boots_enchant = False
    wristguards_enchant = False
    ring1_enchant = False
    ring2_enchant = False
    cloak_enchant = False
    enchant_tally = 0
    enhanced_tally = 0

    for enchants in response1['data']['reportData']['report']['table']['data']['combatantInfo']['gear']:
        if enchants['slot'] == 4:
            if 'permanentEnchant' in enchants:
                chest_enchant = True
                enchant_tally += 1
        if enchants['slot'] == 6:
            if 'permanentEnchant' in enchants:
                legguards_enchant = True
                enchant_tally += 1
        if enchants['slot'] == 7:
            if 'permanentEnchant' in enchants:
                boots_enchant = True
                enchant_tally += 1
        if enchants['slot'] == 8:
            if 'permanentEnchant' in enchants:
                wristguards_enchant = True
                enchant_tally += 1
        if enchants['slot'] == 10:
            if 'permanentEnchant' in enchants:
                ring1_enchant = True
                enchant_tally += 1
        if enchants['slot'] == 11:
            if 'permanentEnchant' in enchants:
                ring2_enchant = True
                enchant_tally += 1
        if enchants['slot'] == 14:
            if 'permanentEnchant' in enchants:
                cloak_enchant = True
                enchant_tally += 1
        if enchants['slot'] == 15:
            if 'permanentEnchant' in enchants:
                weapon_enchant = True
                enchant_tally += 1
            if 'temporaryEnchant' in enchants:
                weapon_enhanced = True
                enhanced_tally += 1

    # Getting Active Time and Percentage
    active_time = response2['data']['reportData']['report']['table']['data']['entries'][0]['activeTime']
    active_time_percent = ((active_time / total_time) * 100)
    active_time_percent = round(active_time_percent,2)

    holy_shock_casts = 0
    avenging_wrath_casts = 0
    lay_on_hands_casts = 0
    
    for casts in response3['data']['reportData']['report']['table']['data']['entries']:
        if 'Holy Shock' in casts['name']:
            holy_shock_casts = casts['total']
        if 'Avenging Wrath' in casts['name']:
            avenging_wrath_casts = casts['total']
        if 'Lay on Hands' in casts['name']:
            lay_on_hands_casts = casts['total']

    beacon_of_light_uptime = 0
    beacon_of_faith_uptime = 0
    food_buff = False
    flask_used = False

    for auras in response4['data']['reportData']['report']['table']['data']['auras']:
        if 'Beacon of Light' in auras['name']:
            beacon_of_light_uptime = auras['totalUptime']
        if 'Beacon of Faith' in auras['name']:
            beacon_of_faith_uptime = auras['totalUptime']
        if 'Well Fed' in auras['name']:
            food_buff = True
        if 'Phial' in auras['name']:
            flask_used = True

    # Cooldowns
    holy_shock = 6600
    avenging_wrath = 120000
    lay_on_hands = 600000
    
    holy_shock_potential_casts = total_time / holy_shock
    holy_shock_potential_casts = round(holy_shock_potential_casts)

    avenging_wrath_potential_casts = total_time / avenging_wrath
    avenging_wrath_potential_casts = round(avenging_wrath_potential_casts)

    lay_on_hands_potential_casts = total_time / lay_on_hands
    lay_on_hands_potential_casts = round(lay_on_hands_potential_casts)

    if holy_shock_potential_casts < 1:
        holy_shock_potential_casts = 1
    if avenging_wrath_potential_casts < 1:
        avenging_wrath_potential_casts = 1
    if lay_on_hands_potential_casts < 1:
        lay_on_hands_potential_casts = 1

    # Beacon Uptime in percent
    beacon_of_light_uptime_percent = beacon_of_light_uptime / total_time * 100
    beacon_of_light_uptime_percent = round(beacon_of_light_uptime_percent,2)
    beacon_of_faith_uptime_percent = beacon_of_faith_uptime / total_time * 100
    beacon_of_faith_uptime_percent = round(beacon_of_faith_uptime_percent,2)

    beacon_efficiency = ((beacon_of_light_uptime_percent + beacon_of_faith_uptime_percent) / 2)
    beacon_efficiency = round(beacon_efficiency,2)

    # Ability efficiency
    holy_shock_efficiency = holy_shock_casts / holy_shock_potential_casts * 100
    holy_shock_efficiency = round(holy_shock_efficiency,2)
    
    avenging_wrath_efficiency = avenging_wrath_casts / avenging_wrath_potential_casts * 100
    avenging_wrath_efficiency = round(avenging_wrath_efficiency,2)
    
    lay_on_hands_efficiency = lay_on_hands_casts / lay_on_hands_potential_casts * 100
    lay_on_hands_efficiency = round(lay_on_hands_efficiency,2)
    
    prepared_percent = ((enchant_tally + enhanced_tally) / 9) * 100
    prepared_percent = round(prepared_percent,2)
    
    return render_template('holy/holy_overview.html', player_name=player_name, player_type=player_type, boss_name=boss_name, player_spec=player_spec, 
                           boss_difficulty=boss_difficulty, weapon_enchant=weapon_enchant, chest_enchant=chest_enchant, ring1_enchant=ring1_enchant, 
                           ring2_enchant=ring2_enchant, cloak_enchant=cloak_enchant, enchant_tally=enchant_tally, player_itemlvl=player_itemlvl,
                           player_potion_use=player_potion_use, player_healthstone_use=player_healthstone_use, holy_shock_efficiency=holy_shock_efficiency,
                           avenging_wrath_efficiency=avenging_wrath_efficiency,beacon_of_light_uptime_percent=beacon_of_light_uptime_percent,
                           beacon_of_faith_uptime_percent=beacon_of_faith_uptime_percent, lay_on_hands_efficiency=lay_on_hands_efficiency,
                           holy_shock_casts=holy_shock_casts,holy_shock_potential_casts=holy_shock_potential_casts, avenging_wrath_casts=avenging_wrath_casts,
                           avenging_wrath_potential_casts=avenging_wrath_potential_casts,lay_on_hands_casts=lay_on_hands_casts, 
                           lay_on_hands_potential_casts=lay_on_hands_potential_casts, prepared_percent=prepared_percent,beacon_efficiency=beacon_efficiency,
                           weapon_enhanced=weapon_enhanced,legguards_enchant=legguards_enchant, boots_enchant=boots_enchant,
                           wristguards_enchant=wristguards_enchant,enhanced_tally=enhanced_tally,food_buff=food_buff,flask_used=flask_used,
                           active_time_percent=active_time_percent)
