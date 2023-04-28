from flask import render_template, session
from flask import Blueprint
import requests
from math import comb
from access_token import access_token

holy_statistics = Blueprint('holyStatistics', __name__,
                            template_folder='templates')


@holy_statistics.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500


@holy_statistics.route('/holy-statistics', methods=['POST', 'GET'])
def holy_statistics_function():

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
        "\\n\\t\\t\\t\\tdataType: Healing\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload5 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: " + \
        end_time+"\\n\\t\\t\\t\\tencounterID: "+encounter_id + \
        "\\n\\t\\t\\t\\tdataType: Buffs\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload6 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID: "+source_id + \
        "\\n\\t\\t\\t\\tdataType: Casts\\n\\t\\t\\t\\tviewBy: Ability\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload7 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID: "+source_id + \
        "\\n\\t\\t\\t\\tdataType: Healing\\n\\t\\t\\t\\tviewBy: Ability\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
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
    response6 = requests.request(
        "POST", url, data=payload6, headers=headers).json()
    response7 = requests.request(
        "POST", url, data=payload7, headers=headers).json()

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
    active_time_percent = active_time / total_time * 100
    active_time_percent = round(active_time_percent,2)

    # Overheal
    total_heal = response4['data']['reportData']['report']['table']['data']['entries'][0]['total']
    overheal = response4['data']['reportData']['report']['table']['data']['entries'][0]['overheal']
    heal_result = total_heal + overheal
    overheal_percent = overheal / heal_result * 100
    overheal_percent = round(overheal_percent,2)

    beacon_of_light_uptime = 0
    beacon_of_faith_uptime = 0
    divine_purpose_procs = 0
    infusion_of_light_procs = 0
    blessing_of_dawn_uptime = 0
    blessing_of_dusk_uptime = 0

    for auras in response5['data']['reportData']['report']['table']['data']['auras']:
        if 'Beacon of Light' in auras['name']:
            beacon_of_light_uptime = auras['totalUptime']
        if 'Beacon of Faith' in auras['name']:
            beacon_of_faith_uptime = auras['totalUptime']
        if 'Divine Purpose' in auras['name']:
            divine_purpose_procs = auras['totalUses']
        if 'Infusion of Light' in auras['name']:
            infusion_of_light_procs = auras['totalUses']
        if 'Blessing of Dawn' in auras['name']:
            blessing_of_dawn_uptime = auras['totalUptime']
        if 'Blessing of Dusk' in auras['name']:
            blessing_of_dusk_uptime = auras['totalUptime']

    light_of_dawn_casts = 0
    word_of_glory_casts = 0
    crusader_strike_casts = 0
    holy_shock_casts = 0
    avenging_wrath_casts = 0
    lay_on_hands_casts = 0
    hammer_of_wrath_casts = 0
    divine_shield_casts = 0
    judgment_casts = 0
    holy_light_casts = 0
    divine_toll_casts = 0
    divine_protection_casts = 0

    for casts in response6['data']['reportData']['report']['table']['data']['entries']:
        if 'Light of Dawn' in casts['name']:
            light_of_dawn_casts = casts['total']
        if 'Word of Glory' in casts['name']:
            word_of_glory_casts = casts['total']
        if 'Crusader Strike' in casts['name']:
            crusader_strike_casts = casts['total']
        if 'Holy Shock' in casts['name']:
            holy_shock_casts = casts['total']
        if 'Avenging Wrath' in casts['name']:
            avenging_wrath_casts = casts['total']
        if 'Lay on Hands' in casts['name']:
            lay_on_hands_casts = casts['total']
        if 'Hammer of Wrath' in casts['name']:
            hammer_of_wrath_casts = casts['total']
        if 'Divine Shield' in casts['name']:
            divine_shield_casts = casts['total']
        if 'Judgment' in casts['name']:
            judgment_casts = casts['total']
        if 'Holy Light' in casts['name']:
            holy_light_casts = casts['total']
        if 'Divine Toll' in casts['name']:
            divine_toll_casts = casts['total']
        if 'Divine Protection' in casts['name']:
            divine_protection_casts = casts['total']

    light_of_dawn_hit_count = 0
    
    for healing in response7['data']['reportData']['report']['table']['data']['entries']:
        if 'Light of Dawn' in healing['name']:
            light_of_dawn_hit_count = healing['hitCount']

    beacon_of_light_uptime_percent = beacon_of_light_uptime / total_time * 100
    beacon_of_light_uptime_percent = round(beacon_of_light_uptime_percent,2)
    beacon_of_faith_uptime_percent = beacon_of_faith_uptime / total_time * 100
    beacon_of_faith_uptime_percent = round(beacon_of_faith_uptime_percent,2)
    blessing_of_dawn_efficiency = blessing_of_dawn_uptime / total_time * 100
    blessing_of_dawn_efficiency = round(blessing_of_dawn_efficiency,2)
    blessing_of_dusk_efficiency = blessing_of_dusk_uptime / total_time * 100
    blessing_of_dusk_efficiency = round(blessing_of_dusk_efficiency,2)

    # Cooldowns
    holy_shock = 6600
    avenging_wrath = 120000
    lay_on_hands = 600000
    crusader_strike = 5300
    hammer_of_wrath = 6600
    divine_shield = 300000
    judgment = 11000
    divine_toll = 60000
    divine_protection = 42000

    holy_shock_potential_casts = total_time / holy_shock
    holy_shock_potential_casts = round(holy_shock_potential_casts)

    avenging_wrath_potential_casts = total_time / avenging_wrath
    avenging_wrath_potential_casts = round(avenging_wrath_potential_casts)

    lay_on_hands_potential_casts = total_time / lay_on_hands
    lay_on_hands_potential_casts = round(lay_on_hands_potential_casts)

    crusader_strike_potential_casts = total_time / crusader_strike
    crusader_strike_potential_casts = round(crusader_strike_potential_casts)

    hammer_of_wrath_potential_casts = total_time / hammer_of_wrath
    hammer_of_wrath_potential_casts = round(hammer_of_wrath_potential_casts)

    divine_shield_potential_casts = total_time / divine_shield
    divine_shield_potential_casts = round(divine_shield_potential_casts)

    judgment_potential_casts = total_time / judgment
    judgment_potential_casts = round(judgment_potential_casts)

    divine_toll_potential_casts = total_time / divine_toll
    divine_toll_potential_casts = round(divine_toll_potential_casts)

    divine_protection_potential_casts = total_time / divine_protection
    divine_protection_potential_casts = round(divine_protection_potential_casts)

    if holy_shock_potential_casts < 1:
        holy_shock_potential_casts = 1
    if avenging_wrath_potential_casts < 1:
        avenging_wrath_potential_casts = 1
    if lay_on_hands_potential_casts < 1:
        lay_on_hands_potential_casts = 1
    if crusader_strike_potential_casts < 1:
        crusader_strike_potential_casts = 1
    if hammer_of_wrath_potential_casts < 1:
        hammer_of_wrath_potential_casts = 1
    if divine_shield_potential_casts < 1:
        divine_shield_potential_casts = 1
    if judgment_potential_casts < 1:
        judgment_potential_casts = 1
    if divine_toll_potential_casts < 1:
        divine_toll_potential_casts = 1
    if divine_protection_potential_casts < 1:
        divine_protection_potential_casts = 1

    # Holy Shock
    holy_shock_efficiency = holy_shock_casts / holy_shock_potential_casts * 100
    holy_shock_efficiency = round(holy_shock_efficiency,2)
    
    # Avenging Wrath
    avenging_wrath_efficiency = avenging_wrath_casts / avenging_wrath_potential_casts * 100
    avenging_wrath_efficiency = round(avenging_wrath_efficiency,2)
    
    # Lay on Hands
    lay_on_hands_efficiency = lay_on_hands_casts / lay_on_hands_potential_casts * 100
    lay_on_hands_efficiency = round(lay_on_hands_efficiency,2)
    
    # Divine Shield
    divine_shield_efficiency = divine_shield_casts / divine_shield_potential_casts * 100
    divine_shield_efficiency = round(divine_shield_efficiency,2)
    
    # Judgment
    judgment_efficiency = judgment_casts / judgment_potential_casts * 100
    judgment_efficiency = round(judgment_efficiency,2)
    
    # Crusader Strike
    crusader_strike_efficiency = crusader_strike_casts / crusader_strike_potential_casts * 100
    crusader_strike_efficiency = round(crusader_strike_efficiency,2)
    
    # Hammer of Wrath
    hammer_of_wrath_efficiency = hammer_of_wrath_casts / hammer_of_wrath_potential_casts * 100
    hammer_of_wrath_efficiency = round(hammer_of_wrath_efficiency,2)
    
    # Divine Toll
    divine_toll_efficiency = divine_toll_casts / divine_toll_potential_casts * 100
    divine_toll_efficiency = round(divine_toll_efficiency,2)

    # Divine Protection
    divine_protection_efficiency = divine_protection_casts / divine_protection_potential_casts * 100
    divine_protection_efficiency = round(divine_protection_efficiency,2)
    
    # CPM
    holy_shock_cpm = holy_shock_casts / total_time * 60000
    holy_shock_cpm = round(holy_shock_cpm,2)
    avenging_wrath_cpm = avenging_wrath_casts / total_time * 60000
    avenging_wrath_cpm = round(avenging_wrath_cpm,2)
    lay_on_hands_cpm = lay_on_hands_casts / total_time * 60000
    lay_on_hands_cpm = round(lay_on_hands_cpm,2)
    divine_shield_cpm = divine_shield_casts / total_time * 60000
    divine_shield_cpm = round(divine_shield_cpm,2)
    light_of_dawn_cpm = light_of_dawn_casts / total_time * 60000
    light_of_dawn_cpm = round(light_of_dawn_cpm,2)
    judgment_cpm = judgment_casts / total_time * 60000
    judgment_cpm = round(judgment_cpm,2)
    crusader_strike_cpm = crusader_strike_casts / total_time * 60000
    crusader_strike_cpm = round(crusader_strike_cpm,2)
    word_of_glory_cpm = word_of_glory_casts / total_time * 60000
    word_of_glory_cpm = round(word_of_glory_cpm,2)
    hammer_of_wrath_cpm = hammer_of_wrath_casts / total_time * 60000
    hammer_of_wrath_cpm = round(hammer_of_wrath_cpm,2)
    holy_light_cpm = holy_light_casts / total_time * 60000
    holy_light_cpm = round(holy_light_cpm,2)
    divine_toll_cpm = divine_toll_casts / total_time * 60000
    divine_toll_cpm = round(divine_toll_cpm,2)
    divine_protection_cpm = divine_protection_casts / total_time * 60000
    divine_protection_cpm = round(divine_protection_cpm,2)

    # Holy generation
    holy_generation = holy_shock_casts + crusader_strike_casts + hammer_of_wrath_casts + infusion_of_light_procs
    
    # Calculating Holy Power Per Minute
    holy_power_per_min = holy_generation / total_time * 60000
    holy_power_per_min = round(holy_power_per_min)

    # Holy Power spent
    word_of_glory_spent = word_of_glory_casts * 3
    light_of_dawn_spent = light_of_dawn_casts * 3
    total_holy_power_spent = word_of_glory_spent + light_of_dawn_spent

    # Holy Power wasted
    holy_power_wasted = holy_generation - total_holy_power_spent
    holy_power_wasted_percent = total_holy_power_spent / holy_generation * 100

    if holy_power_wasted < 0:
        holy_power_wasted = 0
    if holy_power_wasted_percent < 0:
        holy_power_wasted_percent = 0

    # Holy gen per ability percentage
    holy_shock_gen_percent = holy_shock_casts / holy_generation * 100
    crusader_strike_gen_percent = crusader_strike_casts / holy_generation * 100
    hammer_of_wrath_gen_percent = hammer_of_wrath_casts / holy_generation * 100
    infusion_of_light_gen_percent = infusion_of_light_procs / holy_generation * 100

    # Holy Power cast
    total_holy_power_casts = word_of_glory_casts + light_of_dawn_casts

    # Calculating power of for each holy power ability for the chance formula
    power_of_holy_power_uses0 = total_holy_power_casts - 0
    power_of_holy_power_uses1 = total_holy_power_casts - 1
    power_of_holy_power_uses2 = total_holy_power_casts - 2
    power_of_holy_power_uses3 = total_holy_power_casts - 3
    power_of_holy_power_uses4 = total_holy_power_casts - 4
    power_of_holy_power_uses5 = total_holy_power_casts - 5

    # Calculating chances of 0-5 Divine Purpose procs
    # zero chance
    divine_purpose_chance0 = comb(total_holy_power_casts, 0) * pow(0.15, 0) * \
        pow(0.85, power_of_holy_power_uses0) * 100
    # one chance
    divine_purpose_chance1 = comb(total_holy_power_casts, 1) * pow(0.15, 1) * \
        pow(0.85, power_of_holy_power_uses1) * 100
    # two chances
    divine_purpose_chance2 = comb(total_holy_power_casts, 2) * pow(0.15, 2) * \
        pow(0.85, power_of_holy_power_uses2) * 100
    # three chances
    divine_purpose_chance3 = comb(total_holy_power_casts, 3) * pow(0.15, 3) * \
        pow(0.85, power_of_holy_power_uses3) * 100
    # four chances
    divine_purpose_chance4 = comb(total_holy_power_casts, 4) * pow(0.15, 4) * \
        pow(0.85, power_of_holy_power_uses4) * 100
    # five chances
    divine_purpose_chance5 = comb(total_holy_power_casts, 5) * pow(0.15, 5) * \
        pow(0.85, power_of_holy_power_uses5) * 100
    
    divine_purpose_chance0 = round(divine_purpose_chance0,2)
    divine_purpose_chance1 = round(divine_purpose_chance1,2)
    divine_purpose_chance2 = round(divine_purpose_chance2,2)
    divine_purpose_chance3 = round(divine_purpose_chance3,2)
    divine_purpose_chance4 = round(divine_purpose_chance4,2)
    divine_purpose_chance5 = round(divine_purpose_chance5,2)

    # Average Heals
    average_heal_per_holy_power = total_heal / holy_generation
    average_heal_per_holy_power = round(average_heal_per_holy_power)

    return render_template('holy/holy_statistics.html', damage_per_second=damage_per_second, heals_per_second=heals_per_second, damage_taken_per_second=damage_taken_per_second,
                           damage_graph=damage_graph, damage_length=damage_length, heals_graph=heals_graph, heals_length=heals_length, dtps_graph=dtps_graph, dtps_length=dtps_length,
                           active_time_percent=active_time_percent, beacon_of_light_uptime_percent=beacon_of_light_uptime_percent, beacon_of_faith_uptime_percent=beacon_of_faith_uptime_percent,
                           holy_generation=holy_generation, word_of_glory_spent=word_of_glory_spent, light_of_dawn_spent=light_of_dawn_spent, total_holy_power_spent=total_holy_power_spent, 
                           holy_power_wasted=holy_power_wasted, total_holy_power_casts=total_holy_power_casts,holy_shock_cpm=holy_shock_cpm, holy_shock_casts=holy_shock_casts, 
                           holy_shock_potential_casts=holy_shock_potential_casts, holy_shock_efficiency=holy_shock_efficiency,avenging_wrath_cpm=avenging_wrath_cpm, 
                           avenging_wrath_casts=avenging_wrath_casts, avenging_wrath_potential_casts=avenging_wrath_potential_casts, avenging_wrath_efficiency=avenging_wrath_efficiency,
                           lay_on_hands_cpm=lay_on_hands_cpm, lay_on_hands_casts=lay_on_hands_casts, lay_on_hands_potential_casts=lay_on_hands_potential_casts, lay_on_hands_efficiency=lay_on_hands_efficiency,
                           divine_purpose_chance0=divine_purpose_chance0, divine_purpose_chance1=divine_purpose_chance1, divine_purpose_chance2=divine_purpose_chance2, divine_purpose_chance3=divine_purpose_chance3,
                           divine_purpose_chance4=divine_purpose_chance4, divine_purpose_chance5=divine_purpose_chance5, divine_purpose_procs=divine_purpose_procs, word_of_glory_casts=word_of_glory_casts, 
                           word_of_glory_cpm=word_of_glory_cpm, light_of_dawn_casts=light_of_dawn_casts, boss_difficulty=boss_difficulty, boss_name=boss_name, player_name=player_name, player_type=player_type, 
                           player_spec=player_spec, overheal_percent=overheal_percent, infusion_of_light_procs=infusion_of_light_procs, divine_shield_casts=divine_shield_casts, 
                           divine_shield_potential_casts=divine_shield_potential_casts, divine_shield_cpm=divine_shield_cpm, divine_shield_efficiency=divine_shield_efficiency, light_of_dawn_cpm=light_of_dawn_cpm, 
                           judgment_casts=judgment_casts, judgment_potential_casts=judgment_potential_casts, judgment_cpm=judgment_cpm, judgment_efficiency=judgment_efficiency, crusader_strike_casts=crusader_strike_casts, 
                           crusader_strike_potential_casts=crusader_strike_potential_casts, crusader_strike_cpm=crusader_strike_cpm, crusader_strike_efficiency=crusader_strike_efficiency, hammer_of_wrath_casts=hammer_of_wrath_casts, 
                           hammer_of_wrath_potential_casts=hammer_of_wrath_potential_casts, hammer_of_wrath_cpm=hammer_of_wrath_cpm, hammer_of_wrath_efficiency=hammer_of_wrath_efficiency,average_heal_per_holy_power=average_heal_per_holy_power, 
                           light_of_dawn_hit_count=light_of_dawn_hit_count, holy_light_casts=holy_light_casts,holy_light_cpm=holy_light_cpm,divine_toll_casts=divine_toll_casts,divine_toll_potential_casts=divine_toll_potential_casts,
                           divine_toll_cpm=divine_toll_cpm, divine_toll_efficiency=divine_toll_efficiency,blessing_of_dawn_efficiency=blessing_of_dawn_efficiency,blessing_of_dusk_efficiency=blessing_of_dusk_efficiency,
                           holy_shock_gen_percent=holy_shock_gen_percent, crusader_strike_gen_percent=crusader_strike_gen_percent,hammer_of_wrath_gen_percent=hammer_of_wrath_gen_percent,
                           infusion_of_light_gen_percent=infusion_of_light_gen_percent,holy_power_per_min=holy_power_per_min, divine_protection_cpm=divine_protection_cpm,divine_protection_casts=divine_protection_casts,
                           divine_protection_potential_casts=divine_protection_potential_casts,divine_protection_efficiency=divine_protection_efficiency)
