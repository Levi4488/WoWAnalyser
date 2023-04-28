from flask import render_template, session
from flask import Blueprint
import requests
from access_token import access_token

protection_overview = Blueprint(
    'protectionOverview', __name__, template_folder='templates')


@protection_overview.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500


@protection_overview.route('/protection-overview', methods=['POST', 'GET'])
def protection_overview_function():

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
        "\\n\\t\\t\\t\\tdataType: DamageTaken\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload3 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID: "+source_id + \
        "\\n\\t\\t\\t\\tdataType: Casts\\n\\t\\t\\t\\tviewBy: Ability\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload4 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID: "+source_id + \
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
    active_time_percent = active_time / total_time * 100
    active_time_percent = round(active_time_percent,2)

    word_of_glory_casts = 0
    judgment_casts = 0
    avengers_shield_casts = 0
    blessed_hammer_casts = 0
    ardent_defender_casts = 0
    guardian_of_ancient_kings_casts = 0
    lay_on_hands_casts = 0
    divine_shield_casts = 0

    for casts in response3['data']['reportData']['report']['table']['data']['entries']:
        if 'Word of Glory' in casts['name']:
            word_of_glory_casts = casts['total']
        if 'Judgment' in casts['name']:
            judgment_casts = casts['total']
        if "Avenger's Shield" in casts['name']:
            avengers_shield_casts = casts['total']
        if 'Blessed Hammer' in casts['name']:
            blessed_hammer_casts = casts['total']
        if 'Ardent Defender' in casts['name']:
            ardent_defender_casts = casts['total']
        if 'Guardian of Ancient Kings' in casts['name']:
            guardian_of_ancient_kings_casts = casts['total']
        if 'Lay on Hands' in casts['name']:
            lay_on_hands_casts = casts['total']
        if 'Divine Shield' in casts['name']:
            divine_shield_casts = casts['total']

    
    food_buff = False
    flask_used = False

    # Getting buff data
    for auras in response4['data']['reportData']['report']['table']['data']['auras']:
        if 'Well Fed' in auras['name']:
            food_buff = True
        if 'Phial' in auras['name']:
            flask_used = True

    judgment = 5300
    avengers_shield = 13000
    blessed_hammer = 5300
    ardent_defender = 84000
    guardian_of_ancient_kings = 300000
    lay_on_hands = 600000
    divine_shield = 300000

    lay_on_hands_potential_casts = total_time / lay_on_hands
    lay_on_hands_potential_casts = round(lay_on_hands_potential_casts)

    divine_shield_potential_casts = total_time / divine_shield
    divine_shield_potential_casts = round(divine_shield_potential_casts)

    guardian_of_ancient_kings_potential_casts = total_time / guardian_of_ancient_kings
    guardian_of_ancient_kings_potential_casts = round(guardian_of_ancient_kings_potential_casts)

    ardent_defender_potential_casts = total_time / ardent_defender
    ardent_defender_potential_casts = round(ardent_defender_potential_casts)

    blessed_hammer_potential_casts = total_time / blessed_hammer
    blessed_hammer_potential_casts = round(blessed_hammer_potential_casts)

    avengers_shield_potential_casts = total_time / avengers_shield
    avengers_shield_potential_casts = round(avengers_shield_potential_casts)

    judgment_potential_casts = total_time / judgment
    judgment_potential_casts = round(judgment_potential_casts)

    if lay_on_hands_potential_casts < 1:
        lay_on_hands_potential_casts = 1
    if divine_shield_potential_casts < 1:
        divine_shield_potential_casts = 1
    if guardian_of_ancient_kings_potential_casts < 1:
        guardian_of_ancient_kings_potential_casts = 1
    if ardent_defender_potential_casts < 1:
        ardent_defender_potential_casts = 1
    if blessed_hammer_potential_casts < 1:
        blessed_hammer_potential_casts = 1
    if avengers_shield_potential_casts < 1:
        avengers_shield_potential_casts = 1
    if judgment_potential_casts < 1:
        judgment_potential_casts = 1

    # Ability efficiency
    
    judgment_efficiency = judgment_casts / judgment_potential_casts * 100
    judgment_efficiency = round(judgment_efficiency,2)
    
    avengers_shield_efficiency = avengers_shield_casts / avengers_shield_potential_casts * 100
    avengers_shield_efficiency = round(avengers_shield_efficiency,2)
    
    blessed_hammer_efficiency = blessed_hammer_casts / blessed_hammer_potential_casts * 100
    blessed_hammer_efficiency = round(blessed_hammer_efficiency,2)
    
    ardent_defender_efficiency = ardent_defender_casts / ardent_defender_potential_casts * 100
    ardent_defender_efficiency = round(ardent_defender_efficiency,2)
    
    guardian_of_ancient_kings_efficiency = guardian_of_ancient_kings_casts / guardian_of_ancient_kings_potential_casts * 100
    guardian_of_ancient_kings_efficiency = round(guardian_of_ancient_kings_efficiency,2)
    
    divine_shield_efficiency = divine_shield_casts / divine_shield_potential_casts * 100
    divine_shield_efficiency = round(divine_shield_efficiency,2)
    
    lay_on_hands_efficiency = lay_on_hands_casts / lay_on_hands_potential_casts * 100
    lay_on_hands_efficiency = round(lay_on_hands_efficiency,2)
    
    # Cooldown efficiency
    damage_abilities_efficiency = ((judgment_efficiency + avengers_shield_efficiency + blessed_hammer_efficiency) / 3)
    damage_abilities_efficiency = round(damage_abilities_efficiency,2)

    # How prepared the player was
    prepared_percent = ((enchant_tally + enhanced_tally) / 9) * 100
    prepared_percent = round(prepared_percent,2)

    return render_template('protection/protection_overview.html', player_name=player_name, player_type=player_type, boss_name=boss_name, player_spec=player_spec, boss_difficulty=boss_difficulty,
                           weapon_enchant=weapon_enchant, chest_enchant=chest_enchant,ring1_enchant=ring1_enchant, ring2_enchant=ring2_enchant, cloak_enchant=cloak_enchant, 
                           enchant_tally=enchant_tally, player_itemlvl=player_itemlvl,active_time_percent=active_time_percent, player_potion_use=player_potion_use, player_healthstone_use=player_healthstone_use, 
                           word_of_glory_casts=word_of_glory_casts, judgment_efficiency=judgment_efficiency, judgment_casts=judgment_casts, judgment_potential_casts=judgment_potential_casts,avengers_shield_efficiency=avengers_shield_efficiency, 
                           blessed_hammer_efficiency=blessed_hammer_efficiency,ardent_defender_efficiency=ardent_defender_efficiency, ardent_defender_casts=ardent_defender_casts, ardent_defender_potential_casts=ardent_defender_potential_casts,
                           guardian_of_ancient_kings_efficiency=guardian_of_ancient_kings_efficiency, guardian_of_ancient_kings_casts=guardian_of_ancient_kings_casts, guardian_of_ancient_kings_potential_casts=guardian_of_ancient_kings_potential_casts,
                           lay_on_hands_efficiency=lay_on_hands_efficiency, lay_on_hands_casts=lay_on_hands_casts, lay_on_hands_potential_casts=lay_on_hands_potential_casts,divine_shield_efficiency=divine_shield_efficiency, 
                           divine_shield_casts=divine_shield_casts, divine_shield_potential_casts=divine_shield_potential_casts,damage_abilities_efficiency=damage_abilities_efficiency, prepared_percent=prepared_percent,
                           weapon_enhanced=weapon_enhanced,legguards_enchant=legguards_enchant, boots_enchant=boots_enchant, wristguards_enchant=wristguards_enchant, enhanced_tally=enhanced_tally, 
                           food_buff=food_buff, flask_used=flask_used)
