from google import genai
from game_data import enemy_descriptions

def generate_battle_text(attacker, target, target_health, weapon, roll, hit, damage, dies, battle_state):
    client = genai.Client()

    desc = enemy_descriptions.get(target.lower(), {})
    personality = desc.get("personality", "")
    combat_style = desc.get("combat_style", "")

    prompt = f"""
Luo yksi (1) lyhyt (1-3 lauseen mittainen), eläväinen ja vaihteleva taisteluselostus. 
Älä tarjoa vaihtoehtoja tai listoja.

Tärkeää:
- Käytä *viimeisintä tapahtumaa* inspiraationa, mutta älä kopioi sitä.
- Reagoi siihen ja jatka sen luomaa tilannetta.
- Tarinan pitää edetä, älä toista aiempia taistelukertomuksia sellaisenaan.

Viimeisin tapahtuma:
{battle_state["history"][-1]}

Vihollisen kuvaus:
- Persoonallisuus: {personality}
- Taistelutyyli: {combat_style}

Tiedot:
- Hyökkääjä: {attacker}
- Vihollinen: {target}
- Vihollisen elämät: {target_health}
- Ase: {weapon}
- Heitto (d20): {roll}
- Osuma onnistui: {"Kyllä" if hit else "Ei"}
- Damage: {damage}
- Kuoleeko kohde: {"Kyllä" if dies else "Ei"}

Kirjoita vain yksi yhtenäinen kuvaus taistelun tapahtumasta, älä anna kommentteja tehtävänannosta, palauta vain kuvaus tapahtumasta. Älä kerro numeraalisia arvoja, kuten kuinka paljon vahinkoa tehtiin tai mikä roll oli,
kuvaile kuitenkin hyökkäyksen kohteen hp tilannetta sanallisesti, esimerkiksi ("Vihollinen ottaa brutaalin iskun ja kaatuu maahan, mutta nousee kuitenkin vielä viimeisillä voimillaan pystyyn.").
Jos vihollinen kuolee, kuvaile kohteen kuolemaa ja iskun vakavuutta.
Jos osumaa ei tule niin kuvaile kuinka se meni huti, vihollinen voi esimerkiksi torjua tai väistää iskun.
Jos roll on 20 niin isku on kriittinen ja kuvaile todella eeppisesti iskua.
Jos roll on 1 niin isku on todella surkea ja hyökkääjä itse kärsii iskusta, kuvaile hyökkääjän epäonnistumista.
Selostuksessasi vihollinen ei hyökkää tässä vuorossa, mutta voi puolustautua.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def generate_enemy_battle_text(attacker, target, target_health, roll, hit, damage, dies, battle_state):
    client = genai.Client()

    desc = enemy_descriptions.get(attacker.lower(), {})
    personality = desc.get("personality", "")
    combat_style = desc.get("combat_style", "")

    prompt = f"""
Luo lyhyt (1–3 virkkeen) vividinen taistelukuvaus, jossa vihollinen hyökkää pelaajaa vastaan.
Älä tarjoa vaihtoehtoja, kirjoita vain yksi kuvaus.

Tärkeää:
- Käytä *viimeisintä tapahtumaa* inspiraationa, mutta älä kopioi sitä.
- Reagoi siihen ja jatka sen luomaa tilannetta.
- Tarinan pitää edetä, älä toista aiempia taistelukertomuksia sellaisenaan.

Viimeisin tapahtuma:
{battle_state["history"][-1]}

Hyökkääjän kuvaus:
- Persoonallisuus: {personality}
- Taistelutyyli: {combat_style}

Tiedot:
- Hyökkääjä: {attacker}
- Kohde: {target}
- Kohteen elämät: {target_health}
- Heitto (d20): {roll}
- Osuma onnistui: {"Kyllä" if hit else "Ei"}
- Damage: {damage}
- Kuoleeko kohde: {"Kyllä" if dies else "Ei"}

Kirjoita tarinallinen kuvaus siitä, miten vihollinen hyökkää.
Älä mainitse numeroita tai roll-arvoja, kuvaile vain tapahtuma.
Jos huti, kuvaile miten pelaaja väistää tai torjuu.
Jos roll on 20 niin isku on kriittinen ja kuvaile todella eeppisesti iskua.
Jos roll on 1 niin isku on todella surkea ja hyökkääjä itse kärsii iskusta, kuvaile hyökkääjän epäonnistumista.
Jos kohde kuolee, kuvaile todella dramaattinen kuolema.
Selostuksessasi pelaaja ei hyökkää tässä vuorossa, mutta voi puolustautua.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text