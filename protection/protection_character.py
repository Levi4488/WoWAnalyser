from flask import render_template, session
from flask import Blueprint
import requests
from access_token import access_token

protection_character = Blueprint('protectionCharacter', __name__, template_folder='templates')

@protection_character.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('error500.html'), 500

@protection_character.route('/protection-character', methods=['POST', 'GET'])
def protection_character_function():

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
        if gear['slot'] == 16:
            shield = gear['name']
            shield_itemlvl = gear['itemLevel']

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
        if talentTree['spellID'] == 234299:
            fistofjustice = "Fist of Justice"
            talent_tree_list.append(fistofjustice)
            fistofjustice_rank = talentTree['rank']
            rank_list.append(fistofjustice_rank)
        if talentTree['spellID'] == 190784:
            divinesteed = "Divine Steed"
            talent_tree_list.append(divinesteed)
            divinesteed_rank = talentTree['rank']
            rank_list.append(divinesteed_rank)
        if talentTree['spellID'] == 24275:
            hammerofwrath = "Hammer of Wrath"
            talent_tree_list.append(hammerofwrath)
            hammerofwrath_rank = talentTree['rank']
            rank_list.append(hammerofwrath_rank)
        if talentTree['spellID'] == 385639:
            aurasofswiftvengeance = "Auras of Swift Vengeance"
            talent_tree_list.append(aurasofswiftvengeance)
            aurasofswiftvengeance_rank = talentTree['rank']
            rank_list.append(aurasofswiftvengeance_rank)
        if talentTree['spellID'] == 231663:
            greaterjudgment = "Greater Judgment"
            talent_tree_list.append(greaterjudgment)
            greaterjudgment_rank = talentTree['rank']
            rank_list.append(greaterjudgment_rank)
        if talentTree['spellID'] == 1044:
            blessingoffreedom = "Blessing of Freedom"
            talent_tree_list.append(blessingoffreedom)
            blessingoffreedom_rank = talentTree['rank']
            rank_list.append(blessingoffreedom_rank)
        if talentTree['spellID'] == 20066:
            repentance = "Repentance"
            talent_tree_list.append(repentance)
            repentance_rank = talentTree['rank']
            rank_list.append(repentance_rank)
        if talentTree['spellID'] == 31884:
            avengingwrath = "Avenging Wrath"
            talent_tree_list.append(avengingwrath)
            avengingwrath_rank = talentTree['rank']
            rank_list.append(avengingwrath_rank)
        if talentTree['spellID'] == 1022:
            blessingofprotection = "Blessing of Protection"
            talent_tree_list.append(blessingofprotection)
            blessingofprotection_rank = talentTree['rank']
            rank_list.append(blessingofprotection_rank)
        if talentTree['spellID'] == 6940:
            blessingofsacrifice = "Blessing of Sacrifice"
            talent_tree_list.append(blessingofsacrifice)
            blessingofsacrifice_rank = talentTree['rank']
            rank_list.append(blessingofsacrifice_rank)
        if talentTree['spellID'] == 96231:
            rebuke = "Rebuke"
            talent_tree_list.append(rebuke)
            rebuke_rank = talentTree['rank']
            rank_list.append(rebuke_rank)
        if talentTree['spellID'] == 114154:
            unbreakablespirit = "Unbreakable Spirit"
            talent_tree_list.append(unbreakablespirit)
            unbreakablespirit_rank = talentTree['rank']
            rank_list.append(unbreakablespirit_rank)
        if talentTree['spellID'] == 213644:
            cleansetoxins = "Cleans Toxins"
            talent_tree_list.append(cleansetoxins)
            cleansetoxins_rank = talentTree['rank']
            rank_list.append(cleansetoxins_rank)
        if talentTree['spellID'] == 385515:
            holyaegis = "Holy Aegis"
            talent_tree_list.append(holyaegis)
            holyaegis_rank = talentTree['rank']
            rank_list.append(holyaegis_rank)
        if talentTree['spellID'] == 377053:
            sealofreprisal = "Seal of Reprisal"
            talent_tree_list.append(sealofreprisal)
            sealofreprisal_rank = talentTree['rank']
            rank_list.append(sealofreprisal_rank)
        if talentTree['spellID'] == 385464:
            incandescence = "Incandescence"
            talent_tree_list.append(incandescence)
            incandescence_rank = talentTree['rank']
            rank_list.append(incandescence_rank)
        if talentTree['spellID'] == 377128:
            goldenpath = "Golden Path"
            talent_tree_list.append(goldenpath)
            goldenpath_rank = talentTree['rank']
            rank_list.append(goldenpath_rank)
        if talentTree['spellID'] == 223817:
            divinepurpose = "Divine Purpose"
            talent_tree_list.append(divinepurpose)
            divinepurpose_rank = talentTree['rank']
            rank_list.append(divinepurpose_rank)
        if talentTree['spellID'] == 385425:
            sealofalacrity = "Seal of Alacrity"
            talent_tree_list.append(sealofalacrity)
            sealofalacrity_rank = talentTree['rank']
            rank_list.append(sealofalacrity_rank)
        if talentTree['spellID'] == 377043:
            hallowedground = "Hallowed Ground"
            talent_tree_list.append(hallowedground)
            hallowedground_rank = talentTree['rank']
            rank_list.append(hallowedground_rank)

    return render_template('protection/protection_character.html', helm=helm, helm_itemlvl=helm_itemlvl, neck=neck, neck_itemlvl=neck_itemlvl,
                           shoulders=shoulders, shoulders_itemlvl=shoulders_itemlvl, chest=chest, chest_itemlvl=chest_itemlvl,
                           belt=belt, belt_itemlvl=belt_itemlvl, legguards=legguards, legguards_itemlvl=legguards_itemlvl,
                           boots=boots, boots_itemlvl=boots_itemlvl, wrists=wrists, wrists_itemlvl=wrists_itemlvl, gloves=gloves, gloves_itemlvl=gloves_itemlvl,
                           ring1=ring1, ring1_itemlvl=ring1_itemlvl, ring2=ring2, ring2_itemlvl=ring2_itemlvl,trinket1=trinket1, trinket1_itemlvl=trinket1_itemlvl, 
                           trinket2=trinket2, trinket2_itemlvl=trinket2_itemlvl,cloak=cloak, cloak_itemlvl=cloak_itemlvl, weapon=weapon, weapon_itemlvl=weapon_itemlvl, 
                           player_name=player_name, player_type=player_type, player_itemlvl=player_itemlvl,strength=strength, stamina=stamina, crit=crit, haste=haste, 
                           mastery=mastery, versatility=versatility, talent_tree_list=talent_tree_list, shield=shield, shield_itemlvl=shield_itemlvl,
                           boss_difficulty=boss_difficulty,boss_name=boss_name,player_spec=player_spec,rank_list=rank_list)