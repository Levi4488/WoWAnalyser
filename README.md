# WoWAnalyser
World of Warcraft Flask project that analyses reports from Warcraft Logs. Utilises Warcraft Logs v2 GraphQL API. Currently provides analysis for Retribution Paladins, Protection Paladins and Holy Paladins.

```
WoWAnalyser
├─ access_token.py
├─ app.py
├─ boss_selection.py
├─ holy
│  ├─ holy_character.py
│  ├─ holy_overview.py
│  ├─ holy_statistics.py
│  └─ holy_timeline.py
├─ index.py
├─ player_selection.py
├─ protection
│  ├─ protection_character.py
│  ├─ protection_overview.py
│  ├─ protection_statistics.py
│  └─ protection_timeline.py
├─ README.md
├─ requirements.txt
├─ retribution
│  ├─ retribution_character.py
│  ├─ retribution_overview.py
│  ├─ retribution_statistics.py
│  └─ retribution_timeline.py
├─ static
│  ├─ css
│  │  └─ style.css
│  └─ img
│     ├─ ability_bastion_paladin.jpg
│     ├─ ability_paladin_artofwar.jpg
│     ├─ ability_paladin_beaconoflight.jpg
│     ├─ ability_paladin_beaconsoflight.jpg
│     ├─ ability_paladin_bladeofjustice.jpg
│     ├─ ability_paladin_divinestorm.jpg
│     ├─ ability_paladin_infusionoflight.jpg
│     ├─ ability_paladin_sanctifiedwrath.jpg
│     ├─ ability_paladin_seraphim.jpg
│     ├─ ability_paladin_sheathoflight.jpg
│     ├─ ability_paladin_shieldofthetemplar.jpg
│     ├─ ability_paladin_shieldofvengeance.jpg
│     ├─ ability_paladin_swiftretribution.jpg
│     ├─ ability_paladin_toweroflight.jpg
│     ├─ achievement_bg_winsoa.jpg
│     ├─ achievement_zone_newshadowmoonvalley.jpg
│     ├─ achievement_zone_valeofeternalblossoms.jpg
│     ├─ Death_Knight_Crest.png
│     ├─ Demon_Hunter_Crest.png
│     ├─ Dracthyr_Crest.png
│     ├─ Druid_Crest.png
│     ├─ Hunter_Crest.png
│     ├─ inv_helmet_74.jpg
│     ├─ inv_helmet_96.jpg
│     ├─ inv_sword_2h_artifactashbringerfire_d_03.jpg
│     ├─ inv_sword_2h_artifactashbringerpurified_d_02.jpg
│     ├─ inv_sword_2h_artifactashbringerpurified_d_03.jpg
│     ├─ Mage_Crest.png
│     ├─ Paladin_Crest.png
│     ├─ paladin_retribution.jpg
│     ├─ Pandaren_Crest.png
│     ├─ Priest_Crest.png
│     ├─ Rogue_Crest.png
│     ├─ Shaman_Crest.png
│     ├─ spell_holy_ardentdefender.jpg
│     ├─ spell_holy_avengersshield.jpg
│     ├─ spell_holy_avenginewrath.jpg
│     ├─ spell_holy_crusaderstrike.jpg
│     ├─ spell_holy_divineprotection.jpg
│     ├─ spell_holy_divinepurpose.jpg
│     ├─ spell_holy_divineshield.jpg
│     ├─ spell_holy_flashheal.jpg
│     ├─ spell_holy_heroism.jpg
│     ├─ spell_holy_holybolt.jpg
│     ├─ spell_holy_innerfire.jpg
│     ├─ spell_holy_layonhands.jpg
│     ├─ spell_holy_righteousfury.jpg
│     ├─ spell_holy_sealofmight.jpg
│     ├─ spell_holy_searinglight.jpg
│     ├─ spell_holy_surgeoflight.jpg
│     ├─ spell_paladin_executionsentence.jpg
│     ├─ spell_paladin_hammerofwrath.jpg
│     ├─ spell_paladin_lightofdawn.jpg
│     ├─ spell_paladin_templarsverdict.jpg
│     ├─ Warlock_Crest.png
│     └─ Warrior_Crest.png
├─ templates
│  ├─ boss_selection.html
│  ├─ error500.html
│  ├─ holy
│  │  ├─ holy_character.html
│  │  ├─ holy_overview.html
│  │  ├─ holy_statistics.html
│  │  └─ holy_timeline.html
│  ├─ index.html
│  ├─ player_selection.html
│  ├─ protection
│  │  ├─ protection_character.html
│  │  ├─ protection_overview.html
│  │  ├─ protection_statistics.html
│  │  └─ protection_timeline.html
│  ├─ retribution
│  │  ├─ retribution_character.html
│  │  ├─ retribution_overview.html
│  │  ├─ retribution_statistics.html
│  │  └─ retribution_timeline.html
│  ├─ shared
│  │  └─ layout.html
│  └─ work_in_progress.html
├─ tests
│  ├─ conftest.py
│  ├─ test_boss_selection.py
│  ├─ test_form.py
│  ├─ test_index.py
│  ├─ test_player_selection.py
│  ├─ test_redirect.py
│  ├─ test_retribution_overview.py
│  └─ test_session.py
└─ work_in_progress.py

```