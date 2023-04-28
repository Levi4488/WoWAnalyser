from flask import Flask
from index import index
from boss_selection import boss_selection
from player_selection import player_selection
from dotenv import load_dotenv
load_dotenv()
import os
SESSION_KEY = os.getenv("SESSION_KEY")

# Retribution
from retribution.retribution_overview import retribution_overview
from retribution.retribution_statistics import retribution_statistics
from retribution.retribution_timeline import retribution_timeline
from retribution.retribution_character import retribution_character

# Protection
from protection.protection_overview import protection_overview
from protection.protection_statistics import protection_statistics
from protection.protection_timeline import protection_timeline
from protection.protection_character import protection_character

# Holy
from holy.holy_overview import holy_overview
from holy.holy_statistics import holy_statistics
from holy.holy_timeline import holy_timeline
from holy.holy_character import holy_character

from work_in_progress import work_in_progress

app = Flask(__name__)

app.secret_key = SESSION_KEY

app.register_blueprint(index)
app.register_blueprint(boss_selection)
app.register_blueprint(player_selection)

app.register_blueprint(retribution_overview)
app.register_blueprint(retribution_statistics)
app.register_blueprint(retribution_timeline)
app.register_blueprint(retribution_character)

app.register_blueprint(protection_overview)
app.register_blueprint(protection_statistics)
app.register_blueprint(protection_timeline)
app.register_blueprint(protection_character)

app.register_blueprint(holy_overview)
app.register_blueprint(holy_statistics)
app.register_blueprint(holy_timeline)
app.register_blueprint(holy_character)

app.register_blueprint(work_in_progress)

if __name__ == '__main__':
    app.run()