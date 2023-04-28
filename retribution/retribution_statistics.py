from flask import render_template, session
from flask import Blueprint
import requests
from math import comb
from access_token import access_token

retribution_statistics = Blueprint(
    'retributionStatistics', __name__, template_folder='templates')


@retribution_statistics.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500


@retribution_statistics.route('/retribution-statistics', methods=['POST', 'GET'])
def retribution_statistics_function():

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

    payload1 = "{\"query\":\"{\\n\\treportData{\\n\\t\\treport(code:\\\""+report_code+"\\\"){\\n\\t\\t\\ttable(startTime:"+start_time+",endTime:" + \
        end_time+",dataType:DamageDone,viewBy:Ability,encounterID:" + \
        encounter_id+",sourceID:"+source_id+")\\n\\t\\t}\\n\\t}\\n}\\n\\n\\n\\n\"}"
    payload2 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\tgraph(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID:"+source_id + \
        "\\n\\t\\t\\t\\tdataType: DamageDone\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload3 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\tgraph(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID:"+source_id + \
        "\\n\\t\\t\\t\\tdataType: Healing\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload4 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\tgraph(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID:"+source_id + \
        "\\n\\t\\t\\t\\tdataType: DamageTaken\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload5 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tencounterID: "+encounter_id+"\\n\\t\\t\\t\\tsourceID: "+source_id + \
        "\\n\\t\\t\\t\\tdataType: Buffs\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload6 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(startTime:"+start_time + \
        ",endTime:"+end_time+",sourceID:"+source_id+",encounterID:"+encounter_id + \
        ",dataType:Casts,viewBy:Ability)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    payload7 = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(startTime:"+start_time + \
        ",endTime:"+end_time+",encounterID:"+encounter_id + \
        ",dataType:DamageDone,viewBy:Source,sourceID:" + \
        source_id+")\\n\\t\\t}\\n\\t}\\n}\\n\"}"
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

    wake_of_ashes_hit_count = 0
    melee_strikes = 0
    consecration_hit_count = 0
    final_verdict_damage = 0

    for abilities in response1['data']['reportData']['report']['table']['data']['entries']:
        if 'Wake of Ashes' in abilities['name'] and abilities['guid'] == 255937:
            wake_of_ashes_hit_count = abilities['hitCount']
        if 'Melee' in abilities['name'] and abilities['guid'] == 1:
            melee_strikes = abilities['uses']
        if 'Consecration' in abilities['name'] and abilities['guid'] == 81297:
            consecration_hit_count = abilities['hitCount']
        if 'Final Verdict' in abilities['name'] and abilities['guid'] == 383328:
            final_verdict_damage = abilities['total']

    # DPS
    total_damage = 0
    damage_data = response2['data']['reportData']['report']['graph']['data']['series'][0]
    if 'total' in response2['data']['reportData']['report']['graph']['data']['series'][0]:
        total_damage = response2['data']['reportData']['report']['graph']['data']['series'][0]['total']
    damage_graph = damage_data['data']
    damage_length = len(damage_data['data'])

    # Calculating DPS
    damage_per_second = total_damage / total_time * 1000
    damage_per_second = round(damage_per_second)

    # HPS
    total_heals = 0
    heals_data = response3['data']['reportData']['report']['graph']['data']['series'][0]
    if 'total' in response3['data']['reportData']['report']['graph']['data']['series'][0]:
        total_heals = response3['data']['reportData']['report']['graph']['data']['series'][0]['total']
    heals_graph = heals_data['data']
    heals_length = len(heals_data['data'])

    # Calculating HPS
    heals_per_second = total_heals / total_time * 1000
    heals_per_second = round(heals_per_second)

    # DTPS
    total_dtps = 0
    dtps_data = response4['data']['reportData']['report']['graph']['data']['series'][0]
    if 'total' in response4['data']['reportData']['report']['graph']['data']['series'][0]:
        total_dtps = response4['data']['reportData']['report']['graph']['data']['series'][0]['total']
    dtps_graph = dtps_data['data']
    dtps_length = len(dtps_data['data'])

    # Calculating DTPS
    damage_taken_per_second = total_dtps / total_time * 1000
    damage_taken_per_second = round(damage_taken_per_second)

    # Getting buff data
    art_of_war_procs = 0
    blessing_of_dawn_uptime = 0
    blessing_of_dusk_uptime = 0

    for auras in response5['data']['reportData']['report']['table']['data']['auras']:
        if 'Art of War' in auras['name']:
            art_of_war_procs = auras['totalUses']
        if 'Blessing of Dawn' in auras['name']:
            blessing_of_dawn_uptime = auras['totalUptime']
        if 'Blessing of Dusk' in auras['name']:
            blessing_of_dusk_uptime = auras['totalUptime']

    wake_of_ashes_casts = 0
    judgment_casts = 0
    blade_of_justice_casts = 0
    hammer_of_justice_casts = 0
    flash_of_light_casts = 0
    lay_on_hands_casts = 0
    shield_of_vengeance_casts = 0
    divine_shield_casts = 0
    divine_storm_casts = 0
    consecration_casts = 0
    hammer_of_wrath_casts = 0
    word_of_glory_casts = 0
    divine_toll_casts = 0
    final_verdict_casts = 0
    templar_strike_casts = 0
    avenging_wrath_casts = 0
    avenging_wrath_uptime = 0
    execution_sentence_casts = 0
    divine_protection_casts = 0
    templar_slash_casts = 0

    for casts in response6['data']['reportData']['report']['table']['data']['entries']:
        if 'Judgment' in casts['name'] and casts['guid'] == 20271:
            judgment_casts = casts['total']
        if 'Blade of Justice' in casts['name'] and casts['guid'] == 184575:
            blade_of_justice_casts = casts['total']
        if 'Wake of Ashes' in casts['name'] and casts['guid'] == 255937:
            wake_of_ashes_casts = casts['total']
        if 'Hammer of Justice' in casts['name'] and casts['guid'] == 853:
            hammer_of_justice_casts = casts['total']
        if 'Flash of Light' in casts['name'] and casts['guid'] == 19750:
            flash_of_light_casts = casts['total']
        if 'Lay on Hands' in casts['name']:
            lay_on_hands_casts = casts['total']
        if 'Shield of Vengeance' in casts['name']:
            shield_of_vengeance_casts = casts['total']
        if 'Divine Shield' in casts['name']:
            divine_shield_casts = casts['total']
        if 'Divine Storm' in casts['name']:
            divine_storm_casts = casts['total']
        if 'Consecration' in casts['name']:
            consecration_casts = casts['total']
        if 'Hammer of Wrath' in casts['name']:
            hammer_of_wrath_casts = casts['total']
        if 'Word of Glory' in casts['name']:
            word_of_glory_casts = casts['total']
        if 'Divine Toll' in casts['name']:
            divine_toll_casts = casts['total']
        if 'Final Verdict' in casts['name']:
            final_verdict_casts = casts['total']
        if 'Templar Strike' in casts['name']:
            templar_strike_casts = casts['total']
            for templarCasts in casts['subentries']:
                if 'Templar Slash' in templarCasts['name']:
                    templar_slash_casts = templarCasts['total']
        if 'Avenging Wrath' in casts['name'] and casts['guid'] == 31884:
            avenging_wrath_casts = casts['total']
            avenging_wrath_uptime = casts['uptime']
        if 'Execution Sentence' in casts['name']:
            execution_sentence_casts = casts['total']
        if 'Divine Protection' in casts['name']:
            divine_protection_casts = casts['total']

    blessing_of_dawn_uptime_perc = blessing_of_dawn_uptime / total_time * 100
    blessing_of_dawn_uptime_perc = round(blessing_of_dawn_uptime_perc,2)
    blessing_of_dusk_uptime_perc = blessing_of_dusk_uptime / total_time * 100
    blessing_of_dusk_uptime_perc = round(blessing_of_dusk_uptime_perc,2)

    # Getting Active Time and Percentage
    active_time = response7['data']['reportData']['report']['table']['data']['entries'][0]['activeTime']
    active_time_percent = ((active_time / total_time) * 100)
    active_time_percent = round(active_time_percent,2)

    # Cooldown time of each ability in milliseconds
    wake_of_ashes = 30000
    judgment = 7900
    blade_of_justice = 11000
    hammer_of_justice = 60000
    shield_of_vengeance = 60000
    divine_shield = 210000
    consecration = 20000
    lay_on_hands = 420000
    hammer_of_wrath = 6600
    divine_toll = 60000
    avenging_wrath = 60000
    execution_sentence = 30000
    divine_protection = 60000

    # Potential Casts
    wake_of_ashes_potential_casts = total_time / wake_of_ashes
    wake_of_ashes_potential_casts = round(wake_of_ashes_potential_casts)

    judgment_potential_casts = total_time / judgment
    judgment_potential_casts = round(judgment_potential_casts)

    blade_of_justice_potential_casts = total_time / blade_of_justice
    blade_of_justice_potential_casts = round(blade_of_justice_potential_casts)

    hammer_of_justice_potential_casts = total_time / hammer_of_justice
    hammer_of_justice_potential_casts = round(hammer_of_justice_potential_casts)

    shield_of_vengeance_potential_casts = total_time / shield_of_vengeance
    shield_of_vengeance_potential_casts = round(shield_of_vengeance_potential_casts)

    divine_shield_potential_casts = total_time / divine_shield
    divine_shield_potential_casts = round(divine_shield_potential_casts)

    consecration_potential_casts = total_time / consecration
    consecration_potential_casts = round(consecration_potential_casts)

    lay_on_hands_potential_casts = total_time / lay_on_hands
    lay_on_hands_potential_casts = round(lay_on_hands_potential_casts)

    hammer_of_wrath_potential_casts = total_time / hammer_of_wrath
    hammer_of_wrath_potential_casts = round(hammer_of_wrath_potential_casts)

    divine_toll_potential_casts = total_time / divine_toll
    divine_toll_potential_casts = round(divine_toll_potential_casts)

    avenging_wrath_potential_casts = total_time / avenging_wrath
    avenging_wrath_potential_casts = round(avenging_wrath_potential_casts)

    execution_sentence_potential_casts = total_time / execution_sentence
    execution_sentence_potential_casts = round(execution_sentence_potential_casts)

    divine_protection_potential_casts = total_time / divine_protection
    divine_protection_potential_casts = round(divine_protection_potential_casts)

    if wake_of_ashes_potential_casts < 1:
        wake_of_ashes_potential_casts = 1
    if judgment_potential_casts < 1:
        judgment_potential_casts = 1
    if blade_of_justice_potential_casts < 1:
        blade_of_justice_potential_casts = 1
    if hammer_of_justice_potential_casts < 1:
        hammer_of_justice_potential_casts = 1
    if shield_of_vengeance_potential_casts < 1:
        shield_of_vengeance_potential_casts = 1
    if divine_shield_potential_casts < 1:
        divine_shield_potential_casts = 1
    if consecration_potential_casts < 1:
        consecration_potential_casts = 1
    if lay_on_hands_potential_casts < 1:
        lay_on_hands_potential_casts = 1
    if hammer_of_wrath_potential_casts < 1:
        hammer_of_wrath_potential_casts = 1
    if divine_toll_potential_casts < 1:
        divine_toll_potential_casts = 1
    if avenging_wrath_potential_casts < 1:
        avenging_wrath_potential_casts = 1
    if execution_sentence_potential_casts < 1:
        execution_sentence_potential_casts = 1
    if divine_protection_potential_casts < 1:
        divine_protection_potential_casts = 1

    # Calculating Holy Power Generated
    inner_grace = 12000
    inner_grace_gen = total_time / inner_grace
    inner_grace_gen = round(inner_grace_gen)
    wake_of_ashes_gen = wake_of_ashes_casts * 3
    blade_of_justice_gen = blade_of_justice_casts * 2
    judgment_gen = judgment_casts * 2
    total_gen = wake_of_ashes_gen + judgment_gen + blade_of_justice_gen + hammer_of_wrath_casts + inner_grace_gen + templar_strike_casts + templar_slash_casts

    # Calculating Holy Power Per Minute
    holy_power_per_min = total_gen / total_time * 60000
    holy_power_per_min = round(holy_power_per_min)

    # Calculating Holy Power Used
    divine_storm_holy_power = divine_storm_casts * 4
    final_verdict_holy_power = final_verdict_casts * 4
    holy_power_casts = divine_storm_casts + final_verdict_casts
    holy_power_spent = divine_storm_holy_power + final_verdict_holy_power

    # Calculating Holy Power wasted num and perc
    holy_power_wasted = total_gen - holy_power_spent
    holy_power_wasted_percent = (holy_power_spent / total_gen) * 100

    if holy_power_wasted < 0:
        holy_power_wasted = 0
    if holy_power_wasted_percent < 0:
        holy_power_wasted_percent = 0

    # Calculating Holy Gen per ability in %
    blade_of_justice_gen_perc = blade_of_justice_gen / total_gen * 100
    wake_of_ashes_gen_perc = wake_of_ashes_gen / total_gen * 100
    judgment_gen_perc = judgment_gen / total_gen * 100
    hammer_of_wrath_gen_perc = hammer_of_wrath_casts / total_gen * 100
    inner_grace_gen_perc = inner_grace_gen / total_gen * 100
    templar_strike_gen_perc = templar_strike_casts / total_gen * 100
    templar_slash_gen_perc = templar_slash_casts / total_gen * 100

    # Calculating chance of Art of War
    art_of_war_percent_chance = (1 - pow(0.88, melee_strikes)) * 100
    art_of_war_percent_chance = round(art_of_war_percent_chance,2)

    # Calculating power of for each melee for the chance formula
    power_of_strikes0 = melee_strikes - 0
    power_of_strikes1 = melee_strikes - 1
    power_of_strikes2 = melee_strikes - 2
    power_of_strikes3 = melee_strikes - 3
    power_of_strikes4 = melee_strikes - 4
    power_of_strikes5 = melee_strikes - 5

    # Calculating chances of 0-5 Art of War procs
    # zero chance
    art_of_war_chance0 = comb(melee_strikes, 0) * pow(0.12, 0) * \
        pow(0.88, power_of_strikes0) * 100
    # one chance
    art_of_war_chance1 = comb(melee_strikes, 1) * pow(0.12, 1) * \
        pow(0.88, power_of_strikes1) * 100
    # two chances
    art_of_war_chance2 = comb(melee_strikes, 2) * pow(0.12, 2) * \
        pow(0.88, power_of_strikes2) * 100
    # three chances
    art_of_war_chance3 = comb(melee_strikes, 3) * pow(0.12, 3) * \
        pow(0.88, power_of_strikes3) * 100
    # four chances
    art_of_war_chance4 = comb(melee_strikes, 4) * pow(0.12, 4) * \
        pow(0.88, power_of_strikes4) * 100
    # five chances
    art_of_war_chance5 = comb(melee_strikes, 5) * pow(0.12, 5) * \
        pow(0.88, power_of_strikes5) * 100
    
    art_of_war_chance0 = round(art_of_war_chance0,2)
    art_of_war_chance1 = round(art_of_war_chance1,2)
    art_of_war_chance2 = round(art_of_war_chance2,2)
    art_of_war_chance3 = round(art_of_war_chance3,2)
    art_of_war_chance4 = round(art_of_war_chance4,2)
    art_of_war_chance5 = round(art_of_war_chance5,2)

    # Wake of Ashes
    wake_of_ashes_efficiency = wake_of_ashes_casts / wake_of_ashes_potential_casts * 100
    wake_of_ashes_efficiency = round(wake_of_ashes_efficiency,2)
    
    # Judgment
    judgment_efficiency = judgment_casts / judgment_potential_casts * 100
    judgment_efficiency = round(judgment_efficiency,2)
    
    # Blade of Justice
    blade_of_justice_efficiency = blade_of_justice_casts / blade_of_justice_potential_casts * 100
    blade_of_justice_efficiency = round(blade_of_justice_efficiency,2)
    
    # Hammer of Justice
    hammer_of_justice_efficiency = hammer_of_justice_casts / hammer_of_justice_potential_casts * 100
    hammer_of_justice_efficiency = round(hammer_of_justice_efficiency,2)
    
    # Shield of Vengeance
    shield_of_vengeance_efficiency = shield_of_vengeance_casts / shield_of_vengeance_potential_casts * 100
    shield_of_vengeance_efficiency = round(shield_of_vengeance_efficiency,2)
    
    # Divine Shield
    divine_shield_efficiency = divine_shield_casts / divine_toll_potential_casts * 100
    divine_shield_efficiency = round(divine_shield_efficiency,2)
    
    # Consecration
    consecration_efficiency = consecration_casts / consecration_potential_casts * 100
    consecration_efficiency = round(consecration_efficiency,2)
    
    # Lay on Hands
    lay_on_hands_efficiency = lay_on_hands_casts / lay_on_hands_potential_casts * 100
    lay_on_hands_efficiency = round(lay_on_hands_efficiency,2)
    
    # Hammer of Wrath
    hammer_of_wrath_efficiency = hammer_of_wrath_casts / hammer_of_wrath_potential_casts * 100
    hammer_of_wrath_efficiency = round(hammer_of_wrath_efficiency,2)
    
    # Divine Toll
    divine_toll_efficiency = divine_toll_casts / divine_toll_potential_casts * 100
    divine_toll_efficiency = round(divine_toll_efficiency,2)
    
    # Avenging Wrath
    avenging_wrath_efficiency = avenging_wrath_casts / avenging_wrath_potential_casts * 100
    avenging_wrath_efficiency = round(avenging_wrath_efficiency,2)
    
    # Avenging Wrath Uptime
    avenging_wrath_uptime_perc = avenging_wrath_uptime / total_time * 100
    avenging_wrath_uptime_perc= round(avenging_wrath_uptime_perc,2)

    # Execution Sentence
    execution_sentence_efficiency = execution_sentence_casts / execution_sentence_potential_casts * 100
    execution_sentence_efficiency = round(execution_sentence_efficiency,2)
    
    # Divine Protection
    divine_protection_efficiency = divine_protection_casts / divine_protection_potential_casts * 100
    divine_protection_efficiency = round(divine_protection_efficiency,2)
    
    # Casts Per Minute
    judgment_cpm = judgment_casts / total_time * 60000
    judgment_cpm = round(judgment_cpm,2)
    blade_of_justice_cpm = blade_of_justice_casts / total_time * 60000
    blade_of_justice_cpm = round(blade_of_justice_cpm,2)
    wake_of_ashes_cpm = wake_of_ashes_casts / total_time * 60000
    wake_of_ashes_cpm = round(wake_of_ashes_cpm,2)
    hammer_of_justice_cpm = hammer_of_justice_casts / total_time * 60000
    hammer_of_justice_cpm = round(hammer_of_justice_cpm,2)
    flash_of_light_cpm = flash_of_light_casts / total_time * 60000
    flash_of_light_cpm = round(flash_of_light_cpm,2)
    lay_on_hands_cpm = lay_on_hands_casts / total_time * 60000
    lay_on_hands_cpm = round(lay_on_hands_cpm,2)
    shield_of_vengeance_cpm = shield_of_vengeance_casts / total_time * 60000
    shield_of_vengeance_cpm = round(shield_of_vengeance_cpm,2)
    divine_shield_cpm = divine_shield_casts / total_time * 60000
    divine_shield_cpm = round(divine_shield_cpm,2)
    divine_storm_cpm = divine_storm_casts / total_time * 60000
    divine_storm_cpm = round(divine_storm_cpm,2)
    consecration_cpm = consecration_casts / total_time * 60000
    consecration_cpm = round(consecration_cpm,2)
    hammer_of_wrath_cpm = hammer_of_wrath_casts / total_time * 60000
    hammer_of_wrath_cpm = round(hammer_of_wrath_cpm,2)
    word_of_glory_cpm = word_of_glory_casts / total_time * 60000
    word_of_glory_cpm = round(word_of_glory_cpm,2)
    divine_toll_cpm = divine_toll_casts / total_time * 60000
    divine_toll_cpm = round(divine_toll_cpm,2)
    final_verdict_cpm = final_verdict_casts / total_time * 60000
    final_verdict_cpm = round(final_verdict_cpm,2)
    templar_strike_cpm = templar_strike_casts / total_time * 60000
    templar_strike_cpm = round(templar_strike_cpm,2)
    avenging_wrath_cpm = avenging_wrath_casts / total_time * 60000
    avenging_wrath_cpm = round(avenging_wrath_cpm,2)
    execution_sentence_cpm = execution_sentence_casts / total_time * 60000
    execution_sentence_cpm = round(execution_sentence_cpm,2)
    divine_protection_cpm = divine_protection_casts / total_time * 60000
    divine_protection_cpm = round(divine_protection_cpm,2)
    templar_slash_cpm = templar_slash_casts / total_time * 60000
    templar_slash_cpm = round(templar_slash_cpm,2)

    return render_template('retribution/retribution_statistics.html', damage_per_second=damage_per_second, heals_per_second=heals_per_second, damage_taken_per_second=damage_taken_per_second,
                           damage_graph=damage_graph, damage_length=damage_length, heals_graph=heals_graph, heals_length=heals_length, dtps_graph=dtps_graph, dtps_length=dtps_length,
                           art_of_war_percent_chance=art_of_war_percent_chance, art_of_war_chance0=art_of_war_chance0, art_of_war_chance1=art_of_war_chance1, art_of_war_chance2=art_of_war_chance2, 
                           art_of_war_chance3=art_of_war_chance3, art_of_war_chance4=art_of_war_chance4, art_of_war_chance5=art_of_war_chance5,melee_strikes=melee_strikes, art_of_war_procs=art_of_war_procs, 
                           holy_power_wasted=holy_power_wasted, holy_power_wasted_percent=holy_power_wasted_percent, holy_power_casts=holy_power_casts, divine_storm_holy_power=divine_storm_holy_power, 
                           total_gen=total_gen, holy_power_per_min=holy_power_per_min, wake_of_ashes_casts=wake_of_ashes_casts, wake_of_ashes_potential_casts=wake_of_ashes_potential_casts, 
                           wake_of_ashes_efficiency=wake_of_ashes_efficiency, judgment_casts=judgment_casts, judgment_potential_casts=judgment_potential_casts, judgment_efficiency=judgment_efficiency, 
                           blade_of_justice_casts=blade_of_justice_casts, blade_of_justice_potential_casts=blade_of_justice_potential_casts, blade_of_justice_efficiency=blade_of_justice_efficiency, 
                           hammer_of_justice_casts=hammer_of_justice_casts, hammer_of_justice_potential_casts=hammer_of_justice_potential_casts, hammer_of_justice_efficiency=hammer_of_justice_efficiency, 
                           flash_of_light_casts=flash_of_light_casts, judgment_cpm=judgment_cpm,blade_of_justice_cpm=blade_of_justice_cpm, wake_of_ashes_cpm=wake_of_ashes_cpm, hammer_of_justice_cpm=hammer_of_justice_cpm, 
                           flash_of_light_cpm=flash_of_light_cpm,blade_of_justice_gen=blade_of_justice_gen, wake_of_ashes_gen=wake_of_ashes_gen, blade_of_justice_gen_perc=blade_of_justice_gen_perc, 
                           wake_of_ashes_gen_perc=wake_of_ashes_gen_perc, judgment_gen_perc=judgment_gen_perc,shield_of_vengeance_casts=shield_of_vengeance_casts, shield_of_vengeance_cpm=shield_of_vengeance_cpm, 
                           shield_of_vengeance_potential_casts=shield_of_vengeance_potential_casts, shield_of_vengeance_efficiency=shield_of_vengeance_efficiency, divine_shield_cpm=divine_shield_cpm, 
                           divine_shield_casts=divine_shield_casts, divine_shield_potential_casts=divine_shield_potential_casts, divine_shield_efficiency=divine_shield_efficiency, divine_storm_cpm=divine_storm_cpm, 
                           divine_storm_casts=divine_storm_casts,consecration_cpm=consecration_cpm, consecration_casts=consecration_casts, consecration_potential_casts=consecration_potential_casts, 
                           consecration_efficiency=consecration_efficiency, boss_difficulty=boss_difficulty, boss_name=boss_name, player_name=player_name, player_type=player_type, player_spec=player_spec, 
                           lay_on_hands_casts=lay_on_hands_casts, lay_on_hands_potential_casts=lay_on_hands_potential_casts, lay_on_hands_cpm=lay_on_hands_cpm, lay_on_hands_efficiency=lay_on_hands_efficiency,
                           hammer_of_wrath_casts=hammer_of_wrath_casts, hammer_of_wrath_potential_casts=hammer_of_wrath_potential_casts, hammer_of_wrath_cpm=hammer_of_wrath_cpm, 
                           hammer_of_wrath_efficiency=hammer_of_wrath_efficiency, word_of_glory_casts=word_of_glory_casts, word_of_glory_cpm=word_of_glory_cpm, hammer_of_wrath_gen_perc=hammer_of_wrath_gen_perc,
                           wake_of_ashes_hit_count=wake_of_ashes_hit_count,consecration_hit_count=consecration_hit_count,inner_grace_gen=inner_grace_gen,inner_grace_gen_perc=inner_grace_gen_perc,
                           divine_toll_casts=divine_toll_casts,divine_toll_cpm=divine_toll_cpm,divine_toll_potential_casts=divine_toll_potential_casts,divine_toll_efficiency=divine_toll_efficiency,
                           active_time_percent=active_time_percent,final_verdict_damage=final_verdict_damage,final_verdict_casts=final_verdict_casts,final_verdict_cpm=final_verdict_cpm,
                           templar_strike_casts=templar_strike_casts,templar_strike_cpm=templar_strike_cpm,avenging_wrath_casts=avenging_wrath_casts,avenging_wrath_potential_casts=avenging_wrath_potential_casts,
                           avenging_wrath_cpm=avenging_wrath_cpm,avenging_wrath_efficiency=avenging_wrath_efficiency,blessing_of_dawn_uptime_perc=blessing_of_dawn_uptime_perc,
                           blessing_of_dusk_uptime_perc=blessing_of_dusk_uptime_perc,execution_sentence_cpm=execution_sentence_cpm,execution_sentence_casts=execution_sentence_casts,
                           execution_sentence_potential_casts=execution_sentence_potential_casts,execution_sentence_efficiency=execution_sentence_efficiency,judgment_gen=judgment_gen,
                           templar_strike_gen_perc=templar_strike_gen_perc,final_verdict_holy_power=final_verdict_holy_power,holy_power_spent=holy_power_spent,divine_protection_cpm=divine_protection_cpm,
                           divine_protection_casts=divine_protection_casts,divine_protection_efficiency=divine_protection_efficiency,templar_slash_casts=templar_slash_casts,templar_slash_cpm=templar_slash_cpm,
                           templar_slash_gen_perc=templar_slash_gen_perc,divine_protection_potential_casts=divine_protection_potential_casts,avenging_wrath_uptime_perc=avenging_wrath_uptime_perc)
