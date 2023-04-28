from flask import render_template, session
from flask import Blueprint
import requests
from access_token import access_token

retribution_overview = Blueprint('retributionOverview', __name__, template_folder='templates')

@retribution_overview.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@retribution_overview.route('/retribution-overview', methods=['POST', 'GET'])
def retribution_overview_function():

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
                "\\n\\t\\t\\t\\tdataType: DamageDone\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload3 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
                "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID: "+source_id + \
                "\\n\\t\\t\\t\\tdataType: Buffs\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload4 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(startTime:"+start_time + \
                ",endTime:"+end_time+",encounterID:"+encounter_id + \
                ",dataType:Casts,viewBy:Ability,sourceID:"+source_id+")\\n\\t\\t}\\n\\t}\\n}\\n\"}"
        
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
    
    food_buff = False
    flask_used = False
    blessing_of_dawn_uptime = 0
    blessing_of_dusk_uptime = 0

    # Getting buff data
    for auras in response3['data']['reportData']['report']['table']['data']['auras']:
        if 'Well Fed' in auras['name']:
            food_buff = True
        if 'Phial' in auras['name']:
            flask_used = True
        if 'Blessing of Dawn' in auras['name']:
            blessing_of_dawn_uptime = auras['totalUptime']
        if 'Blessing of Dusk' in auras['name']:
            blessing_of_dusk_uptime = auras['totalUptime']

    shield_of_vengeance_casts = 0
    lay_on_hands_casts = 0
    wake_of_ashes_casts = 0
    blade_of_justice_casts = 0
    melee_strikes = 0
    consecration_casts = 0
    judgment_casts = 0
    avenging_wrath_casts = 0
    avenging_wrath_uptime = 0

    for casts in response4['data']['reportData']['report']['table']['data']['entries']:
        if 'Shield of Vengeance' in casts['name']:
            shield_of_vengeance_casts = casts['total']
        if 'Lay on Hands' in casts['name']:
            lay_on_hands_casts = casts['total']
        if 'Wake of Ashes' in casts['name']:
            wake_of_ashes_casts = casts['total']
        if 'Blade of Justice' in casts['name']:
            blade_of_justice_casts = casts['total']
        if 'Melee' in casts['name']:
            melee_strikes = casts['total']
        if 'Consecration' in casts['name']:
            consecration_casts = casts['total']
        if 'Judgment' in casts['name']:
            judgment_casts = casts['total']
        if 'Avenging Wrath' in casts['name'] and casts['guid'] == 31884:
            avenging_wrath_casts = casts['total']
            avenging_wrath_uptime = casts['uptime']

    blessing_of_dawn_uptime_perc = blessing_of_dawn_uptime / total_time * 100
    blessing_of_dawn_uptime_perc = round(blessing_of_dawn_uptime_perc,2)
    blessing_of_dusk_uptime_perc = blessing_of_dusk_uptime / total_time * 100
    blessing_of_dusk_uptime_perc = round(blessing_of_dusk_uptime_perc,2)

    # Cooldown time of each ability in milliseconds
    wake_of_ashes = 30000
    judgment = 7900
    blade_of_justice = 11000
    consecration = 20000
    shield_of_vengeance = 60000
    lay_on_hands = 420000
    avenging_wrath = 60000
    
    wake_of_ashes_potential_casts = total_time / wake_of_ashes
    wake_of_ashes_potential_casts = round(wake_of_ashes_potential_casts)
    judgment_potential_casts = total_time / judgment
    judgment_potential_casts = round(judgment_potential_casts)
    blade_of_justice_potential_casts = total_time / blade_of_justice
    blade_of_justice_potential_casts = round(blade_of_justice_potential_casts)
    consecration_potential_casts = total_time / consecration
    consecration_potential_casts = round(consecration_potential_casts)
    shield_of_vengeance_potential_casts = total_time / shield_of_vengeance
    shield_of_vengeance_potential_casts = round(shield_of_vengeance_potential_casts)
    lay_on_hands_potential_casts = total_time / lay_on_hands
    lay_on_hands_potential_casts = round(lay_on_hands_potential_casts)
    avenging_wrath_potential_casts = total_time / avenging_wrath
    avenging_wrath_potential_casts = round(avenging_wrath_potential_casts)

    if wake_of_ashes_potential_casts < 1:
        wake_of_ashes_potential_casts = 1
    if judgment_potential_casts < 1:
        judgment_potential_casts = 1
    if blade_of_justice_potential_casts < 1:
        blade_of_justice_potential_casts = 1
    if consecration_potential_casts < 1:
        consecration_potential_casts = 1
    if shield_of_vengeance_potential_casts < 1:
        shield_of_vengeance_potential_casts = 1
    if lay_on_hands_potential_casts < 1:
        lay_on_hands_potential_casts = 1
    if avenging_wrath_potential_casts < 1:
        avenging_wrath_potential_casts = 1

    # Wake of Ashes
    wake_of_ashes_efficiency = wake_of_ashes_casts / wake_of_ashes_potential_casts * 100
    wake_of_ashes_efficiency = round(wake_of_ashes_efficiency,2)
    
    # Judgment
    judgment_efficiency = judgment_casts / judgment_potential_casts * 100
    judgment_efficiency = round(judgment_efficiency,2)
    
    # Blade of Justice
    blade_of_justice_efficiency = blade_of_justice_casts / blade_of_justice_potential_casts * 100
    blade_of_justice_efficiency = round(blade_of_justice_efficiency,2)
    
    # Consecration
    consecration_efficiency = consecration_casts / consecration_potential_casts * 100
    consecration_efficiency = round(consecration_efficiency,2)

    # Shield of Vengeance
    shield_of_vengeance_efficiency = shield_of_vengeance_casts / shield_of_vengeance_potential_casts * 100
    shield_of_vengeance_efficiency = round(shield_of_vengeance_efficiency,2)
    
    # Lay on Hands
    lay_on_hands_efficiency = lay_on_hands_casts / lay_on_hands_potential_casts * 100
    lay_on_hands_efficiency = round(lay_on_hands_efficiency,2)
    
    # Avenging Wrath
    avenging_wrath_efficiency = avenging_wrath_casts / avenging_wrath_potential_casts * 100
    avenging_wrath_efficiency = round(avenging_wrath_efficiency,2)
    
    # Avenging Wrath Uptime
    avenging_wrath_uptime_perc = avenging_wrath_uptime / total_time * 100
    avenging_wrath_uptime_perc= round(avenging_wrath_uptime_perc,2)

    # Use your short cooldowns
    short_cooldowns = ((judgment_efficiency + blade_of_justice_efficiency + consecration_efficiency) / 3)
    short_cooldowns = round(short_cooldowns,2)

    # Use your long cooldowns
    long_cooldowns = ((wake_of_ashes_efficiency + avenging_wrath_efficiency) / 2)
    long_cooldowns = round(long_cooldowns,2)

    # Buffs Active
    buffs_active = ((blessing_of_dawn_uptime_perc + blessing_of_dusk_uptime_perc) / 2)
    buffs_active = round(buffs_active,2)

    # How prepared the player was
    prepared_percent = ((enchant_tally + enhanced_tally) / 9) * 100
    prepared_percent = round(prepared_percent,2)

    # Checking how efficient the player was with utility and defensive spells
    utility_defensive_spells = ((lay_on_hands_efficiency + shield_of_vengeance_efficiency) / 2)
    utility_defensive_spells = round(utility_defensive_spells,2)

    return render_template('retribution/retribution_overview.html', boss_name=boss_name, player_name=player_name, player_type=player_type, player_spec=player_spec,
                           wake_of_ashes_casts=wake_of_ashes_casts, wake_of_ashes_potential_casts=wake_of_ashes_potential_casts, wake_of_ashes_efficiency=wake_of_ashes_efficiency, 
                           judgment_casts=judgment_casts, judgment_potential_casts=judgment_potential_casts, judgment_efficiency=judgment_efficiency, 
                           blade_of_justice_casts=blade_of_justice_casts, blade_of_justice_potential_casts=blade_of_justice_potential_casts, 
                           blade_of_justice_efficiency=blade_of_justice_efficiency,melee_strikes=melee_strikes, player_itemlvl=player_itemlvl, weapon_enchant=weapon_enchant, 
                           chest_enchant=chest_enchant, legguards_enchant=legguards_enchant, boots_enchant=boots_enchant, wristguards_enchant=wristguards_enchant, 
                           ring1_enchant=ring1_enchant, ring2_enchant=ring2_enchant, cloak_enchant=cloak_enchant,active_time_percent=active_time_percent, 
                           boss_difficulty=boss_difficulty, player_potion_use=player_potion_use, player_healthstone_use=player_healthstone_use, 
                           consecration_efficiency=consecration_efficiency, enchant_tally=enchant_tally, shield_of_vengeance_casts=shield_of_vengeance_casts,
                           lay_on_hands_casts=lay_on_hands_casts,shield_of_vengeance_efficiency=shield_of_vengeance_efficiency,lay_on_hands_efficiency=lay_on_hands_efficiency,
                           short_cooldowns=short_cooldowns,long_cooldowns=long_cooldowns, buffs_active=buffs_active,prepared_percent=prepared_percent,
                           utility_defensive_spells=utility_defensive_spells, food_buff=food_buff,weapon_enhanced=weapon_enhanced,flask_used=flask_used,
                           enhanced_tally=enhanced_tally,avenging_wrath_efficiency=avenging_wrath_efficiency,avenging_wrath_uptime_perc=avenging_wrath_uptime_perc,
                           blessing_of_dawn_uptime_perc=blessing_of_dawn_uptime_perc,blessing_of_dusk_uptime_perc=blessing_of_dusk_uptime_perc)
