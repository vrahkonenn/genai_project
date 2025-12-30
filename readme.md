Harjoitustyön aiheena oli tehdä roolipeli henkinen tekstiseikkailupeli. Tuotos jäi kesken, jonka myötä pelissä on joitain loogisia virheitä, esimerkiksi tappelun tai keskustelun voi aloittaa örkin kanssa, vaikka örkki ei olisi edes näkyvillä. Tarinankerronta ei ole aina myöskään loogista (pelin alussa jos eliminoit goblinin, on se silti teknisesti elossa tarinassa). Sain kuitenkin aikaiseksi tällaisen "MVP" version, jossa on suurinpiirtein kaikki haluamani toiminnallisuudet toimivana. Pelin kehitys jatkuu.

Pelissä pelaaja voi tehdä toimintoja melko vapaasti tekoälyn avulla, kuten tutkia maailmaa, liikkua siinä ja kanssakäydä pelihahmojen kanssa. Vain mielikuvitus on rajana, sekä muutamat loogiset rajoitteet (et voi esim. lähteä lentämään yhtäkkiä avaruuteen). Pelissä AI pohtii pelaajan syötettä ja päättää sopiiko se tähän fantasiamaailmaan, jos ei, pelaajan täytyy antaa uusi syöte.

Kuinka AI:ta on käytetty pelissä?
- Pelin pääloopissa annetaan AI:lle prompteja, joka toimii annettujen ohjeiden mukaan, kutsuen ennalta määriteltyjä function tooleja, tai vaihtoehtoisesti kuvaillen maailmaa ja kertoen tarinaa mikäli tool kutsulle ei ole tarvetta. AI:lle on annettu "GAME_MASTER_PROMPT" joka kertoo sen olevan fantasiateemainen tarinankertoja sekä antaa sääntöjä kuinka toimia. 

- Pelaaja voi jutella muille hahmoille ja tekoäly hoitaa täysin vastausdialogin. AI:lle on annettu prompti, että hänen täytyy roolipelata henkilöä x, hänelle annetaan henkilöstä oleellisia tietoja jotta rooliin eläytyminen onnistuu paremmin. AI:lle lähetetään jokaisen keskustelupromptin yhteydessä keskusteluhistoria, joten se muistaa mistä puhutaan ja vastaa viimeisimpään viestiin

- AI generoi myös taistelun yhteydessä taisteluselostuksia iskuista. Toimii samalla periaatteella kuin NPC:n kanssa dialogi. AI:lle annetaan prompti, jossa kerrotaan hänen olevan taistelun selostaja, sekä oleellisia tietoja iskusta jotta kuvailu onnistuisi hyvin. Taisteluhistoria annetaan myös ja taisteluista tulee hyvin dynaamisia (vihollinen voi esim reagoida siihen kun pelaajan isku menee ohi, ja täten pelaaja horjahtaa)

Pelissä on kolme tilaa (EXPLORATION, DIALOG, COMBAT), jokaisella vaihtoehdolla pelin pääloop toimii hieman eri tavalla, dialogin sisällä on oma while true looppi, exploration ja combat tila käyttää samaa inputtia, mutta tekoälylle annettava prompti ja käytettävät toolit vaihtuvat.


Asennus:
1. Hanki itsellesi Google AI Studion api key: https://aistudio.google.com/app/api-keys
2. Luo itsellesi tietokoneelle omiin tilin ympäristömuuttujiin uusi muuttuja "GOOGLE_API_KEY", aseta arvoksi juuri tekemäsi api-key
3. Lataa repositorio paikallisesti itsellesi "git clone https://github.com/vrahkonenn/genai_project"
4. Mene terminaalista kloonattuun repositorioon
5. Asenna google-genai kirjasto. "pip install google-genai"
6. Käynnistä peli app.py tiedostosta "py app.py"

Pelin pelaaminen:
- Pelissä on kolme tilaa "EXPLORATION", "COMBAT" "DIALOGUE". 

- EXPLORATION tilassa tekoäly kuvailee sinulle maailmaa, ja voit kertoa sille mitä haluat tehdä, voit esimerkiksi sanoa "Tutkin mitä metsästä löytyy". Tilassa sinulla on käytössä "start_combat" tool, jolla voit aloittaa taistelun vihollisen kanssa. "get_inventory" tool, jolla näet oman inventoryn. "start_dialogue" tool, jolla voit aloittaa keskustelun halutun henkilön kanssa, sekä "use_item" tool, jolla voi toistaiseksi vain käyttää health potionin. Tooleja käytetään yksinkertaisesti kirjoittamalla haluttu toiminto, esim. "Aloitan keskustelun noidan kanssa"

- COMBAT tilassa voit hyökätä "attack_enemy" toolilla, täytyy kertoa millä aseella hyökkää. "flee_combat" toolilla voit paeta taistelusta, lisäksi sinulla on myös "use_item" ja "get_inventory" tool käytössä. Taistelu loppuu toisen osapuolen kuollessa, tai taistelusta paetessa.

- DIALOGUE tilassa keskustelet toisen hahmon kanssa. Kerrot yksinkertaisesti mitä haluat sanoa. Dialogissa voi myös kuvata tekemistä, esim "*Eivor ojentaa käden ja sanoo*: Hyvää päivää, olen Eivor"

- Vaikka tekoäly ymmärtää välillä hyvin Suomea, kannattaa komennot kirjoittaa selkeästi selkosuomella, tai englannilla. 
Erityisesti hyökätessä kannattaa käyttää juuri sitä nimitystä mikä game_data.py tiedostossa on.
Esim. "Hyökkään axella", tai "Aloitan taistelun orcin kanssa"

Pelissä ei varsinaisesti ole mitään tavoitetta, eikä sitä voi "voittaa". Pelissä ei ole myöskään juurikaan ennalta määrättyä tarinaa, vain vähän alkuun johdattavaa toimintaa. Peli keksii itse suhteellisen hyvin omaa tarinaa ja on aina erilainen (riippuen toki pelaajan toimintatavoista). Itse esimerkiksi löysin metsästä haltijan nimeltä Elara, joka lähetti minut tehtävälle örkkijahtiin. Tässä piti toki hieman itsekkin mielikuvitusta käyttää, eräässä promptissa esimerkiksi sanoin että "Näen metsän keskellä vanhan mökin, menen tutkimaan lähempää".

Peli ei mekaanisesti pääty ollenkaan, edes pelaajan kuollessa. Jos pelaaja kuolee, kannataa peli itse lopettaa "CTRL + C". Peli ei myöskään tallenna itseään ja se kaatuu välillä ylikuormituksen tai vaikean promptin takia, peli tulee siis aloittaa alusta.