
""" Module data """

class Data:
    """data testing"""

    # Archetypes
    archetypes = [
        "creative",
        "symbolist",
        "astronaut",
        "revolutionary",
        "planner",
        "dreambuilder",
        "philosopher",
        "futurist",
    ]

    # Questions
    questions = {
        "0": {
            "a": {"creative", "symbolist", "astronaut", "revolutionary"},
            "b": {"planner", "dreambuilder", "philosopher", "futurist"},
        },
        "1": {"a": {"creative", "symbolist"}, "b": {"astronaut", "revolutionary"}},
        "2": {"a": {"planner", "dreambuilder"}, "b": {"philosopher", "futurist"}},
        "3": {"a": "creative", "b": "astronaut"},
        "4": {"a": "symbolist", "b": "revolutionary"},
        "5": {"a": "planner", "b": "philosopher"},
        "6": {"a": "dreambuilder", "b": "futurist"},
        "7": {"a": "creative", "b": "symbolist"},
        "8": {"a": "astronaut", "b": "revolutionary"},
        "9": {"a": "planner", "b": "dreambuilder"},
        "10": {"a": "philosopher", "b": "futurist"},
    }

    archetypes_relations = {
        "creative": ["planner", "astronaut"],
        "symbolist": ["revolutionary", "planner"],
        "astronaut": ["creative", "philosopher"],
        "revolutionary": ["dreambuilder", "symbolist"],
        "planner": ["symbolist", "creative"],
        "dreambuilder": ["futurist", "revolutionary"],
        "philosopher": ["astronaut", "futurist"],
        "futurist": ["philosopher", "dreambuilder"],
    }
