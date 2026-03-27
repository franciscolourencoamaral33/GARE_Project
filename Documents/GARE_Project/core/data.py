# ==============================================================================
# Core data and business logic
# ==============================================================================

# Mineral database (business logic / domain data)
MINERALS_DATA = {
    "quartz": {
        "name": "Quartz",
        "class": "Oxide (SiO₂)",
        "brightness": "Vitreous",
        "texture": "Crystalline",
        "geological_context": "Formed in igneous, metamorphic, and sedimentary rocks. Most abundant mineral in Earth's crust.",
        "deposit_type": "Hydrothermal veins, pegmatites, sedimentary formations, metamorphic rocks",
        "tectonic_context": "Associated with convergent and divergent plate boundaries, found in all tectonic settings",
        "extra_characteristics": "Hardness: 7 | Density: 2.65 g/cm³ | Colors: Clear, purple, rose, smoky"
    },
    "feldspar": {
        "name": "Feldspar",
        "class": "Silicate (KAlSi₃O₈)",
        "brightness": "Vitreous to pearly",
        "texture": "Crystalline, striated",
        "geological_context": "Most abundant mineral in Earth's continental crust. Forms in igneous and metamorphic rocks.",
        "deposit_type": "Granites, pegmatites, metamorphic rocks, some sedimentary formations",
        "tectonic_context": "Found in all tectonic settings; especially common in felsic intrusions at convergent margins",
        "extra_characteristics": "Hardness: 6-6.5 | Density: 2.56-2.76 g/cm³ | Common mineral in all rock types"
    },
    "mica": {
        "name": "Mica",
        "class": "Silicate (Phyllosilicate)",
        "brightness": "Vitreous to pearly",
        "texture": "Layered, sheets, perfect cleavage",
        "geological_context": "Common in granites and metamorphic rocks. Indicator of metamorphic grade.",
        "deposit_type": "Igneous rocks (granites), metamorphic rocks, pegmatites, some sedimentary rocks",
        "tectonic_context": "Associated with continental collision zones and high-pressure metamorphism",
        "extra_characteristics": "Hardness: 2-3 | Density: 2.77-3.1 g/cm³ | Perfect basal cleavage into thin sheets"
    }
}

# Europe occurrences (mock data for mapping)
EUROPE_OCCURRENCES = {
    "quartz": [
        {"country": "France", "region": "Massif Central", "lat": 45.0, "lon": 3.0, "score": 90, "type": "Hydrothermal"},
        {"country": "Italy", "region": "Apuan Alps", "lat": 44.1, "lon": 10.1, "score": 85, "type": "Metamorphic"},
        {"country": "Germany", "region": "Black Forest", "lat": 48.0, "lon": 8.2, "score": 78, "type": "Pegmatite"},
        {"country": "Spain", "region": "Sierra de Guadarrama", "lat": 40.8, "lon": -3.9, "score": 73, "type": "Granite"},
        {"country": "Sweden", "region": "Bergslagen", "lat": 59.9, "lon": 15.1, "score": 69, "type": "Metamorphic"}
    ],
    "feldspar": [
        {"country": "Norway", "region": "Hardangervidda", "lat": 60.4, "lon": 7.0, "score": 88, "type": "Pegmatite"},
        {"country": "Portugal", "region": "Beiras", "lat": 40.2, "lon": -7.5, "score": 82, "type": "Granite"},
        {"country": "Finland", "region": "Karelian Isthmus", "lat": 60.2, "lon": 25.0, "score": 76, "type": "Metamorphic"},
        {"country": "United Kingdom", "region": "Cornwall", "lat": 50.3, "lon": -4.8, "score": 70, "type": "Hydrothermal"},
        {"country": "Czech Republic", "region": "Bohemian Massif", "lat": 50.0, "lon": 14.5, "score": 65, "type": "Granite"}
    ],
    "mica": [
        {"country": "Austria", "region": "Salzkammergut", "lat": 47.7, "lon": 13.5, "score": 91, "type": "Metamorphic"},
        {"country": "Switzerland", "region": "Central Alps", "lat": 46.8, "lon": 9.8, "score": 84, "type": "Pegmatite"},
        {"country": "Slovenia", "region": "Idrija", "lat": 46.0, "lon": 14.0, "score": 76, "type": "Hydrothermal"},
        {"country": "Greece", "region": "Thessaly", "lat": 39.0, "lon": 22.0, "score": 71, "type": "Metamorphic"},
        {"country": "Bulgaria", "region": "Rila Mountains", "lat": 42.1, "lon": 23.3, "score": 67, "type": "Metamorphic"}
    ]
}


# ------------------------------------------------------------------------------
# Business logic / helper functions
# ------------------------------------------------------------------------------

def mineral_exists(mineral_key: str) -> bool:
    """Return True if the mineral exists in the database."""
    return mineral_key.lower().strip() in MINERALS_DATA


def get_mineral(mineral_key: str) -> dict:
    """Get mineral details by key (case-insensitive)."""
    return MINERALS_DATA.get(mineral_key.lower().strip(), {})


def get_mineral_names() -> list:
    """List all mineral display names."""
    return [m["name"] for m in MINERALS_DATA.values()]


def get_europe_occurrences(mineral_key: str) -> list:
    """Return Europe occurrence list for a given mineral."""
    return EUROPE_OCCURRENCES.get(mineral_key.lower().strip(), [])


def get_top_occurrences(mineral_key: str, limit: int = 5) -> list:
    """Return top occurrences sorted by score."""
    occurrences = get_europe_occurrences(mineral_key)
    return sorted(occurrences, key=lambda x: x.get("score", 0), reverse=True)[:limit]
