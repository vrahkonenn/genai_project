inventory = {
    "axe": {"damage": 5, "durability": 10},
    "sword": {"damage": 4, "durability": 15},
    "dagger": {"damage" : 2, "durability" : 20}
}

enemy_templates = {
    "goblin": {"health" : 10, "damage" : 3, "ac" : 8},
    "skeleton": {"health": 12, "damage": 3, "ac": 9},
    "orc": {"health": 20, "damage" : 4, "ac" : 10}
}

enemy_descriptions = {
    "goblin": {
        "type": "Goblin",
        "personality": "Goblinit ovat pieniä, ärsyttäviä ja nopeita olioita, jotka tykkäävät kiusoitella ja haukkua muita.",
        "combat_style": "Goblinit väistävät ketterästi ja iskevät nopeasti terävillä tikareillaan.",
    },
    "skeleton": {
        "type": "Luuranko",
        "personality": "Kuolleista noussut luuranko, tunteeton ja kylmä, liikkuu katkonaisin liikkein.",
        "combat_style": "Luuranko iskee mekaanisesti ruosteisella miekalla, ilman empatiaa.",
    },
    "orc": {
        "type": "Örkki",
        "personality": "Örkit ovat äänekkäitä, raivokkaita, verenhimoisia ja raa'an suoraviivaisia – ne välittävät vain voimasta ja verestä.",
        "combat_style": "Niiden hyökkäykset ovat brutaaleja ja suoria, täynnä raakaa voimaa.",
    },
}


player_start_stats = {
    "name": "Eivor",
    "health" : 15,
    "ac" : 12
}