# pipeline/schema.py

WARDROBE_TAXONOMY = {
    "base_layer": [
        "T-shirt", "long-sleeve top", "tank top", "top", "crop top", 
        "blouse", "shirt", "polo shirt", "corset", "bodysuit"
    ],
    "mid_layer": [
        "hoodie", "sweatshirt", "sweater", "cardigan", "vest", 
        "blazer", "jacket", "bolero", "knit top"
    ],
    "bottom": [
        "pants", "jeans", "leggings", "shorts", "skirt", "culottes", "capri pants"
    ],
    "one_piece": [
        "dress", "overall", "romper", "jumpsuit"
    ],
    "outerwear": [
        "coat", "raincoat", "trench coat", "down jacket", "parka", 
        "windbreaker", "fur coat", "outerwear jacket"
    ],
    "footwear": [
        "canvas sneakers", "sneakers", "dress shoes", "boots", "tall boots", 
        "ankle boots", "loafers", "ballet flats", "sandals", "flip-flops", "mules"
    ],
    "headwear": [
        "beanie", "cap", "baseball cap", "bucket hat", "beret", "headband"
    ],
    "neckwear": [
        "scarf", "neck scarf", "stole", "snood", "shawl"
    ],
    "handwear": [
        "gloves", "mittens", "fingerless gloves"
    ],
    "accessories": [
        "bag", "backpack", "clutch", "belt", "waist belt", "glasses", "watch", "jewelry"
    ]
}

ALL_CLOTHING_TYPES = [item for sublist in WARDROBE_TAXONOMY.values() for item in sublist]


ALL_LAYERS = list(WARDROBE_TAXONOMY.keys())


TYPE_TO_LAYER_MAP = {item: layer for layer, items in WARDROBE_TAXONOMY.items() for item in items}


BASIC_COLORS = [
    "black"
]

PRINT_TYPES = [
    "solid"
]

MATERIALS = [
    "cotton"
]


STYLE_CATEGORIES = [
    "all"
]


MOOD_TYPES = [
    "neutral"
]


INVENTORY_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "items": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "item_name": {"type": "STRING"},
                    "": "",
                    "type": {"type": "STRING", "enum": ALL_CLOTHING_TYPES},
                    "brand": {"type": "STRING"},
                    "main_color": {"type": "STRING", "enum": BASIC_COLORS},
                    "additional_colors": {
                        "type": "ARRAY", 
                        "items": {"type": "STRING", "enum": BASIC_COLORS}
                    },
                    "print": {
                        "type": "ARRAY", 
                        "items": {"type": "STRING", "enum": PRINT_TYPES}
                    },
                    "material": {"type": "STRING", "enum": MATERIALS},
                    "details": {"type": "STRING"},
                    "style_category": {
                        "type": "ARRAY",
                        "items": {"type": "STRING", "enum": STYLE_CATEGORIES}
                    },
                    "layer": {"type": "STRING", "enum": ALL_LAYERS},
                    "mood": {
                        "type": "ARRAY",
                        "items": {"type": "STRING", "enum": MOOD_TYPES}
                    },
                    "matched_with_weather": {"type": "STRING"},
                }, 
                "required": [
                    "item_name", 
                    "timestamp", 
                    "type", 
                    "main_color", 
                    "print", 
                    "material", 
                    "details", 
                    "style_category", 
                    "layer", 
                    "mood", 
                    "matched_with_weather"
                ]
            }
        }
    }
}


IMAGE_REFINEMENT_RESPONSE_SCHEMA = {
    ""
}