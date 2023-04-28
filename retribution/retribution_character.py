from flask import render_template, session
from flask import Blueprint
import requests
from access_token import access_token

retribution_character = Blueprint('retributionCharacter', __name__, template_folder='templates')

@retribution_character.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@retribution_character.route('/retribution-character', methods=['POST', 'GET'])
def retribution_character_function():

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

    url = "https://www.warcraftlogs.com/api/v2/client"

    payload = "{\"query\":\"{\\n\\treportData {\\n\\t\\treport(code: \\\""+report_code+"\\\") {\\n\\t\\t\\ttable(\\n\\t\\t\\t\\tstartTime: "+start_time+"\\n\\t\\t\\t\\tendTime: "+end_time + \
        "\\n\\t\\t\\t\\tsourceID: "+source_id+"\\n\\t\\t\\t\\tencounterID: "+encounter_id + \
        "\\n\\t\\t\\t\\tdataType: Summary\\n\\t\\t\\t\\tviewBy: Source\\n\\t\\t\\t)\\n\\t\\t}\\n\\t}\\n}\\n\"}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers).json()

    for gear in response['data']['reportData']['report']['table']['data']['combatantInfo']['gear']:
        if gear['slot'] == 0:
            helm = gear['name']
            helm_itemlvl = gear['itemLevel']
        if gear['slot'] == 1:
            neck = gear['name']
            neck_itemlvl = gear['itemLevel']
        if gear['slot'] == 2:
            shoulders = gear['name']
            shoulders_itemlvl = gear['itemLevel']
        if gear['slot'] == 4:
            chest = gear['name']
            chest_itemlvl = gear['itemLevel']
        if gear['slot'] == 5:
            belt = gear['name']
            belt_itemlvl = gear['itemLevel']
        if gear['slot'] == 6:
            legguards = gear['name']
            legguards_itemlvl = gear['itemLevel']
        if gear['slot'] == 7:
            boots = gear['name']
            boots_itemlvl = gear['itemLevel']
        if gear['slot'] == 8:
            wrists = gear['name']
            wrists_itemlvl = gear['itemLevel']
        if gear['slot'] == 9:
            gloves = gear['name']
            gloves_itemlvl = gear['itemLevel']
        if gear['slot'] == 10:
            ring1 = gear['name']
            ring1_itemlvl = gear['itemLevel']
        if gear['slot'] == 11:
            ring2 = gear['name']
            ring2_itemlvl = gear['itemLevel']
        if gear['slot'] == 12:
            trinket1 = gear['name']
            trinket1_itemlvl = gear['itemLevel']
        if gear['slot'] == 13:
            trinket2 = gear['name']
            trinket2_itemlvl = gear['itemLevel']
        if gear['slot'] == 14:
            cloak = gear['name']
            cloak_itemlvl = gear['itemLevel']
        if gear['slot'] == 15:
            weapon = gear['name']
            weapon_itemlvl = gear['itemLevel']

    strength = 0
    stamina = 0
    crit = 0
    haste = 0
    mastery = 0
    versatility = 0

    for stats in response['data']['reportData']['report']['table']['data']['combatantInfo']['stats']:
        if 'Strength' in stats:
            strength = response['data']['reportData']['report']['table']['data']['combatantInfo']['stats']['Strength']['max']
        if 'Stamina' in stats:
            stamina = response['data']['reportData']['report']['table']['data']['combatantInfo']['stats']['Stamina']['max']
        if 'Crit' in stats:
            crit = response['data']['reportData']['report']['table']['data']['combatantInfo']['stats']['Crit']['max']
        if 'Haste' in stats:
            haste = response['data']['reportData']['report']['table']['data']['combatantInfo']['stats']['Haste']['max']
        if 'Mastery' in stats:
            mastery = response['data']['reportData']['report']['table']['data']['combatantInfo']['stats']['Mastery']['max']
        if 'Versatility' in stats:
            versatility = response['data']['reportData']['report']['table']['data']['combatantInfo']['stats']['Versatility']['max']

    talent_tree_list = []
    rank_list = []
    
    for talentTree in response['data']['reportData']['report']['table']['data']['combatantInfo']['talentTree']:
        if talentTree['spellID'] == 375576:
            divinetoll = "Divine Toll"
            talent_tree_list.append(divinetoll)
            divinetoll_rank = talentTree['rank']
            rank_list.append(divinetoll_rank)
        if talentTree['spellID'] == 377043:
            justification = "Justification"
            talent_tree_list.append(justification)
            justification_rank = talentTree['rank']
            rank_list.append(justification_rank)
        if talentTree['spellID'] == 383228:
            swiftjustice = "Swift Justice"
            talent_tree_list.append(swiftjustice)
            swiftjustice_rank = talentTree['rank']
            rank_list.append(swiftjustice_rank)
        if talentTree['spellID'] == 406064:
            artofwar = "Art of War"
            talent_tree_list.append(artofwar)
            artofwar_rank = talentTree['rank']
            rank_list.append(artofwar_rank)
        if talentTree['spellID'] == 31884:
            avengingwrath = "Avenging Wrath"
            talent_tree_list.append(avengingwrath)
            avengingwrath_rank = talentTree['rank']
            rank_list.append(avengingwrath_rank)
        if talentTree['spellID'] == 184575:
            bladeofjustice = "Blade of Justice"
            talent_tree_list.append(bladeofjustice)
            bladeofjustice_rank = talentTree['rank']
            rank_list.append(bladeofjustice_rank)
        if talentTree['spellID'] == 53385:
            divinestorm = "Divine Storm"
            talent_tree_list.append(divinestorm)
            divinestorm_rank = talentTree['rank']
            rank_list.append(divinestorm_rank)
        if talentTree['spellID'] == 383328:
            finalverdict = "Final Verdict"
            talent_tree_list.append(finalverdict)
            finalverdict_rank = talentTree['rank']
            rank_list.append(finalverdict_rank)
        if talentTree['spellID'] == 404512:
            highlordsjudgment = "Highlord's Judgment"
            talent_tree_list.append(highlordsjudgment)
            highlordsjudgment_rank = talentTree['rank']
            rank_list.append(highlordsjudgment_rank)
        if talentTree['spellID'] == 406157:
            adjudication = "Adjudication"
            talent_tree_list.append(adjudication)
            adjudication_rank = talentTree['rank']
            rank_list.append(adjudication_rank)
        if talentTree['spellID'] == 404306:
            divinearbiter = "Divine Arbiter"
            talent_tree_list.append(divinearbiter)
            divinearbiter_rank = talentTree['rank']
            rank_list.append(divinearbiter_rank)
        if talentTree['spellID'] == 402971:
            jurisdiction = "Jurisdiction"
            talent_tree_list.append(jurisdiction)
            jurisdiction_rank = talentTree['rank']
            rank_list.append(jurisdiction_rank)
        if talentTree['spellID'] == 403042:
            crusadersreprieve = "Crusader's Reprieve"
            talent_tree_list.append(crusadersreprieve)
            crusadersreprieve_rank = talentTree['rank']
            rank_list.append(crusadersreprieve_rank)
        if talentTree['spellID'] == 184662:
            shieldofvengeance = "Shield of Vengeance"
            talent_tree_list.append(shieldofvengeance)
            shieldofvengeance_rank = talentTree['rank']
            rank_list.append(shieldofvengeance_rank)
        if talentTree['spellID'] == 406940:
            executionerswill = "Executioner's Will"
            talent_tree_list.append(executionerswill)
            executionerswill_rank = talentTree['rank']
            rank_list.append(executionerswill_rank)
        if talentTree['spellID'] == 405355:
            seetthingflames = "Seething Flames"
            talent_tree_list.append(seetthingflames)
            seetthingflames_rank = talentTree['rank']
            rank_list.append(seetthingflames_rank)
        if talentTree['spellID'] == 403654:
            aegisofprotection = "Aegis of Protection"
            talent_tree_list.append(aegisofprotection)
            aegisofprotection_rank = talentTree['rank']
            rank_list.append(aegisofprotection_rank)
        if talentTree['spellID'] == 633:
            layonhands = "Lay on Hands"
            talent_tree_list.append(layonhands)
            layonhands_rank = talentTree['rank']
            rank_list.append(layonhands_rank)
        if talentTree['spellID'] == 385633:
            aurasoftheresolute = "Auras of the Resolute"
            talent_tree_list.append(aurasoftheresolute)
            aurasoftheresolute_rank = talentTree['rank']
            rank_list.append(aurasoftheresolute_rank)
        if talentTree['spellID'] == 231663:
            greaterjudgment = "Greater Judgment"
            talent_tree_list.append(greaterjudgment)
            greaterjudgment_rank = talentTree['rank']
            rank_list.append(greaterjudgment_rank)

    return render_template('retribution/retribution_character.html', helm=helm, helm_itemlvl=helm_itemlvl, neck=neck, 
                           neck_itemlvl=neck_itemlvl,shoulders=shoulders, shoulders_itemlvl=shoulders_itemlvl, chest=chest, 
                           chest_itemlvl=chest_itemlvl,belt=belt, belt_itemlvl=belt_itemlvl, legguards=legguards, 
                           legguards_itemlvl=legguards_itemlvl,boots=boots, boots_itemlvl=boots_itemlvl, wrists=wrists, 
                           wrists_itemlvl=wrists_itemlvl, gloves=gloves, gloves_itemlvl=gloves_itemlvl,ring1=ring1, 
                           ring1_itemlvl=ring1_itemlvl, ring2=ring2, ring2_itemlvl=ring2_itemlvl,trinket1=trinket1, 
                           trinket1_itemlvl=trinket1_itemlvl, trinket2=trinket2, trinket2_itemlvl=trinket2_itemlvl,
                           cloak=cloak, cloak_itemlvl=cloak_itemlvl, weapon=weapon, weapon_itemlvl=weapon_itemlvl, 
                           player_name=player_name, player_type=player_type, player_itemlvl=player_itemlvl,
                           strength=strength, stamina=stamina, crit=crit, haste=haste, mastery=mastery, versatility=versatility, 
                           talent_tree_list=talent_tree_list, boss_difficulty=boss_difficulty, boss_name=boss_name, player_spec=player_spec, 
                           rank_list=rank_list)