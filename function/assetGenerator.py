import random

def FPS_Game_IPFS(metadata):
    pass
    

# Example for a Game Asset
def FPS_Game_Skin():
    item_pool = {
        "Common": [
            "M4A1 - Classic Green Camo",
            "AK-47 - Black Base Coating",
            "UMP45 - Grey Coating",
            "MP9 - Blue Coating",
            "Smoke Grenade - Standard Blue"
        ],
        "Rare": [
            "M4A1 - Desert Camo Coating",
            "AK-47 - Red Coating",
            "AWP - Black Coating + Scope",
            "MP9 - Green Coating + Flashbang",
            "Frag Grenade - Standard Red"
        ],
        "Epic": [
            "M4A1 - Snow Camo Coating + Flamethrower Effect",
            "AK-47 - Gold Coating + Explosion Effect",
            "AWP - Black Coating + Scope + Flashbang",
            "MP9 - Green Coating + Smoke Grenade",
            "HE Grenade - Red Coating + Explosion Effect"
        ],
        "Legendary": [
            "M4A1 - Desert Camo Coating + Flame + Flashbang",
            "AK-47 - Red Coating + Explosion + Smoke",
            "AWP - Black Coating + Scope + Flame + Smoke",
            "MP9 - Green Coating + Explosion + Smoke",
            "Molotov Grenade - Red Coating + Flamethrower Effect"
        ],
        "Mythic": [
            "M4A1 - Desert Camo Coating + Explosion + Flashbang + Smoke + Flame",
            "AK-47 - Red Coating + Explosion + Flashbang + Smoke + Flame + Scope",
            "AWP - Black Coating + Scope + Flame + Smoke + Explosion + Flame",
            "MP9 - Green Coating + Explosion + Flashbang + Smoke + Flame + Scope",
            "Incendiary Grenade - Red Coating + Explosion + Flamethrower Effect"
        ]
    }
    probability = {
        "Mythic": 1,
        "Legendary" :4,
        "Epic": 10,
        "Rare": 25,
        "Common": 60
    }
    rarityPool = []
    for _rarity in probability.keys():
        for _ in range(probability[_rarity]):
            rarityPool.append(_rarity)
    
    rarity = random.choice(rarityPool)
    name = random.choice(item_pool[rarity])
    
    wear = round(random.random(), 4)
    
    metadata = {
        "rarity":rarity,
        "name": name,
        "wear": wear
    }
    

    return metadata


# rarity, asset = FPS_Game_Skin()
# print(rarity, asset)