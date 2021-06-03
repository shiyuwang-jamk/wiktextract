# List of valid topics and canonicalization & generalization mappings
# for topics
#
# Copyright (c) 2020-2021 Tatu Ylonen.  See file LICENSE and https://ylonen.org

# Set of valid topic tags.  (Other tags may be canonicalized to these)
valid_topics = set([
    "Catholicism",
    "Christianity",
    "Internet",
    "aeronautics",
    "agriculture",
    "anatomy",
    "animal",
    "anthropology",
    "arachnology",
    "archeology",
    "architecture",
    "arithmetic",
    "arts",
    "astrology",
    "astronomy",
    "astrophysics",
    "ball-games",
    "biology",
    "board-games",
    "botany",
    "broadcasting",
    "business",
    "card-games",
    "carpentry",
    "cartography",
    "cause",
    "chemistry",
    "cities",
    "color",
    "commerce",
    "communications",
    "computing",
    "construction",
    "cosmology",
    "countries",
    "court",
    "crafts",
    "criminology",
    "demography",
    "dancing",
    "dentistry",
    "diving",
    "drama",
    "drugs",
    "ecology",
    "economics",
    "education",
    "electrical-engineering",
    "electricity",
    "electromagnetism",
    "energy",
    "engineering",
    "epistemology",
    "error",
    "ethnography",
    "fantasy",
    "fashion",
    "film",
    "finance",
    "food",
    "fortifications",
    "games",
    "gemology",
    "geography",
    "geology",
    "government",
    "heading",
    "healthcare",
    "histology",
    "history",
    "hobbies",
    "horology",
    "horses",
    "human-sciences",
    "hunting",
    "hydrology",
    "ideology",
    "journalism",
    "legal",
    "lifestyle",
    "linguistics",
    "literature",
    "location",
    "management",
    "manner",
    "manufacturing",
    "marketing",
    "martial-arts",
    "masonry",
    "mathematics",
    "combinatorics",
    "meats",
    "mechanical-engineering",
    "media",
    "medicine",
    "meteorology",
    "metrology",
    "microbiology",
    "military",
    "mineralogy",
    "mining",
    "monarchy",
    "morphology",
    "music",
    "mysticism",
    "mythology",
    "natural-sciences",
    "naturism",
    "nautical",
    "navy",
    "neurology",
    "neuroscience",
    "nobility",
    "oceanography",
    "oenology",
    "organization",
    "origin",
    "ornithology",
    "paleontology",
    "pathology",
    "petrology",
    "pharmacology",
    "philosophy",
    "phonology",
    "photography",
    "physical-sciences",
    "physics",
    "physiology",
    "planets",
    "political-science",
    "politics",
    "position",
    "publishing",
    "pulmonology",
    "prefectures",
    "printing",
    "property",
    "pseudoscience",
    "psychiatry",
    "psychology",
    "radio",
    "radiology",
    "railways",
    "region",
    "religion",
    "science-fiction",
    "sciences",
    "sexuality",
    "social-science",
    "socialism",
    "source",
    "sports",
    "state",
    "states",
    "statistics",
    "telecommunications",
    "telegraphy",
    "telephone",
    "television",
    "temperature",
    "textiles",
    "theater",
    "theology",
    "time",
    "tools",
    "topology",
    "tourism",
    "toxicology",
    "transport",
    "vehicles",
    "weaponry",
    "weather",
    "weekdays",
    "wrestling",
    "writing",
    "zoology",
])

# Translation map for topics.
# XXX revisit this mapping.  Create more fine-tuned hierarchy
# XXX or should probably not try to generalize here
topic_generalize_map = {
    "(sport)": "sports",
    "card games": "games",
    "board games": "games",
    "ball games": "games",
    "rock paper scissors": "games",
    '"manner of action"': "manner",
    "manner of action": "manner",
    "planets of the Solar system": "planets",
    "planets": "astronomy region",
    "continents": "geography region",
    "countries of Africa": "countries",
    "countries of Europe": "countries",
    "countries of Asia": "countries",
    "countries of South America": "countries",
    "countries of North America": "countries",
    "countries of Central America": "countries",
    "countries of Oceania": "countries",
    "countries": "region",
    "country": "countries",
    "the country": "countries",
    "regions of Armenia": "region",
    "region around the Ruppel river": "region",
    "geographical region": "region",
    "winegrowing region": "region",
    "the historical region": "region",
    "region": "geography location",
    "geography": "sciences",
    "natural-sciences": "sciences",
    "states of India": "states",
    "states of Australia": "states",
    "states": "region",
    "city": "cities",
    "cities": "region",
    "prefectures of Japan": "prefectures",
    "prefecture": "region",
    "software": "computing",
    "text messaging": "communications telephone",
    "billiards": "games",
    "blackjack": "games",
    "backgammon": "games",
    "bridge": "games",
    "darts": "games",
    "human-sciences": "sciences",
    "anthropology": "human-sciences",
    "anthropodology": "anthropology",
    "ornithology": "biology",
    "ornitology": "ornithology",
    "entomology": "biology",
    "medicine": "sciences",
    "anatomy": "medicine",
    "bone": "anatomy",
    "body": "anatomy",
    "scientific": "sciences",
    "scholarly": "sciences",
    "neuroanatomy": "anatomy neurology",
    "neurotoxicology": "neurology toxicology",
    "neurobiology": "neurology",
    "neurophysiology": "physiology neurology",
    "nephrology": "medicine",
    "hepatology": "medicine",
    "endocrinology": "medicine",
    "gynaecology": "medicine",
    "mammology": "medicine",
    "urology": "medicine",
    "neurology": "medicine neuroscience",
    "neuroscience": "human-sciences",
    "gerontology": "medicine",
    "andrology": "medicine",
    "phycology": "botany",
    "planktology": "botany",
    "oncology": "medicine",
    "hematology": "medicine",
    "physiology": "medicine",
    "gastroenterology": "medicine",
    "surgery": "medicine",
    "pharmacology": "medicine",
    "drugs": "pharmacology",
    "cytology": "biology medicine",
    "healthcare": "government",
    "cardiology": "medicine",
    "dentistry": "medicine",
    "odontology": "dentistry",
    "pathology": "medicine",
    "toxicology": "medicine",
    "dermatology": "medicine",
    "epidemiology": "medicine",
    "psychiatry": "medicine psychology",
    "psychoanalysis": "medicine psychology",
    "phrenology": "medicine psychology",
    "psychology": "medicine human-sciences",
    "sociology": "social-science",
    "social science": "social-science",
    "social sciences": "social-science",
    "social-science": "human-sciences",
    "demographics": "demography",
    "immunology": "medicine",
    "immunologic sense": "medicine",
    "anesthesiology": "medicine",
    "xenobiology": "biology",
    "sinology": "geography",
    "psychopathology": "psychiatry",
    "histopathology": "pathology histology",
    "histology": "biology",
    "patology": "pathology",
    "virology": "medicine",
    "bacteriology": "medicine",
    "parapsychology": "psychology pseudoscience",
    "psyschology": "psychology error",
    "printing technology": "printing",
    "litography": "printing",
    "iconography": "history",
    "geomorphology": "geology",
    "phytopathology": "botany pathology",
    "bryology": "botany",
    "opthalmology": "medicine",
    "embryology": "medicine",
    "illness": "medicine",
    "parasitology": "medicine",
    "teratology": "medicine",
    "speech therapy": "medicine",
    "speech pathology": "medicine",
    "radiology": "medicine",
    "radiography": "radiology",
    "vaccinology": "medicine",
    "traumatology": "medicine",
    "microbiology": "biology medicine",
    "pulmonology": "medicine",
    "pneumology": "pulmonology",
    "biology": "natural-sciences",
    "strong topology": "topology",
    "sociobiology": "social-science biology",
    "radio technology": "electrical-engineering radio",
    "authorship": "legal",
    "volcanology": "geology",
    "gemmology": "gemology",
    "gemology": "geology",
    "conchology": "zoology",
    "comics": "literature",
    "codicology": "history",
    "zoology": "biology",
    "botany": "biology",
    "malacology": "biology",
    "taxonomy": "biology",
    "geology": "geography",
    "mineralogy": "geology chemistry",
    "mineralology": "mineralogy",
    "biochemistry": "microbiology chemistry",
    "language": "linguistics",
    "grammar": "linguistics",
    "syntax": "linguistics",
    "semantics": "linguistics",
    "epistemology": "philosophy",
    "ontology": "epistemology",
    "etymology": "linguistics",
    "ethnology": "anthropology",
    "ethnography": "anthropology",
    "historical ethnography": "ethnography history",
    "entertainment industry": "economics",
    "electrochemistry": "chemistry",
    "classical studies": "history",
    "textual criticism": "linguistics",
    "nanotechnology": "engineering",
    "electromagnetism": "physics",
    "biotechnology": "engineering medicine",
    "systems theory": "mathematics",
    "computer games": "games",
    "graphic design": "arts",
    "criminology": "legal human-sciences",
    "penology": "criminology",
    "pragmatics": "linguistics",
    "morphology": "linguistics",
    "phonology": "linguistics",
    "phonetics": "phonology",
    "prosody": "phonology",
    "lexicography": "linguistics",
    "lexicology": "linguistics",
    "narratology": "linguistics",
    "linguistic": "linguistics",
    "translation studies": "linguistics",
    "semiotics": "linguistics",
    "dialectology": "linguistics",
    "ortography": "linguistics",
    "beekeeping": "agriculture",
    "officialese": "government",
    "textiles": "manufacturing",
    "weaving": "textiles",
    "quilting": "textiles",
    "knitting": "textiles",
    "sewing": "textiles",
    "cutting": "textiles",
    "furniture": "manufacturing lifestyle",
    "caving": "sports",
    "country dancing": "dancing",
    "dance": "dancing",
    "dancing": "sports",
    "hip-hop": "dancing",
    "cheerleading": "sports",
    "bowling": "sports",
    "athletics": "sports",
    "acrobatics": "sports",
    "martial arts": "martial-arts",
    "martial-arts": "sports military",
    "meterology": "meteorology",
    "meteorology": "geography",
    "weather": "meteorology",
    "climate": "meteorology",
    "cryptozoology": "zoology",
    "lepidopterology": "zoology",
    "nematology": "zoology",
    "campanology": "history",
    "vexillology": "history",
    "phenomenology": "philosophy",
    "seismology": "geology",
    "cosmology": "astronomy",
    "astrogeology": "astronomy geology",
    "areology": "astrology geology",
    "stratigraphy": "geology",
    "orography": "geology",
    "stenography": "writing",
    "palynology": "chemistry microbiology",
    "lichenology": "botany",
    "seasons": "weather",
    "information technology": "computing",
    "algebra": "mathematics",
    "calculus": "mathematics",
    "arithmetics": "mathematics",
    "statistics": "mathematics",
    "geometry": "mathematics",
    "logic": "mathematics philosophy",
    "trigonometry": "mathematics",
    "mathematical analysis": "mathematics",
    "ethics": "philosophy",
    "existentialism": "philosophy",
    "religion": "philosophy lifestyle",
    "philosophy": "human-sciences",
    "transport": "economics",
    "shipping": "economics",
    "railways": "vehicles",
    "automotive": "vehicles",
    "automobile": "vehicles",
    "vehicles": "transport",
    "tourism": "economics",
    "travel": "tourism lifestyle",
    "travel industry": "tourism",
    "parliamentary procedure": "government",
    "food": "lifestyle",
    "vegetable": "food",
    "beer": "food",
    "brewing": "food manufacturing",
    "cooking": "food",
    "sexuality": "lifestyle",
    "seduction community": "sexuality",
    "BDSM": "sexuality",
    "LGBT": "sexuality",
    "sexual orientations": "sexuality",
    "romantic orientations": "sexuality",
    "prostitution": "sexuality",
    "sexology": "sexuality",
    "biblical": "religion",
    "ecclesiastical": "religion",
    "genetics": "biology medicine",
    "medical terminology": "medicine",
    "mycology": "biology",
    "paganism": "religion",
    "mechanical-engineering": "engineering",
    "mechanics": "mechanical-engineering",
    "lubricants": "mechanical-engineering",
    "measurement": "property",
    "thermodynamics": "physics",
    "signal processing": "computing mathematics",
    "topology": "mathematics",
    "algebraic topology": "topology",
    "algebraic geometry": "geometry",
    "norm topology": "topology",
    "linear algebra": "mathematics",
    "number theory": "mathematics",
    "insurance": "economics",
    "taxation": "economics government",
    "sugar-making": "manufacturing",
    "glassmaking": "manufacturing",
    "food manufacture": "manufacturing",
    "manufacturing": "economics",
    "optics": "physics engineering",
    "physical-sciences": "sciences",
    "chemistry": "physical-sciences",
    "ceramics": "chemistry engineering",
    "chess": "games",
    "checkers": "games",
    "mahjong": "games",
    "crystallography": "chemistry",
    "fluids": "chemistry physics engineering",
    "science": "sciences",
    "physics": "physical-sciences",
    "electrical-engineering": "engineering",
    "electricity": "electrical-engineering physics",
    "electronics": "electrical-engineering",
    "programming": "computing",
    "databases": "computing",
    "visual art": "arts",
    "crafts": "arts hobbies",
    "papercraft": "crafts",
    "bowmaking": "crafts",
    "lutherie": "crafts",
    "history": "human-sciences",
    "heraldry": "hobbies nobility",
    "philately": "hobbies",
    "hobbies": "lifestyle",
    "numismatics": "hobbies",
    "chronology": "horology",
    "horology": "hobbies",
    "cryptography": "computing",
    "finance": "economics",
    "finances": "finance",
    "accounting": "finance",
    "business": "economics",
    "politics": "government",
    "communism": "ideology",
    "socialism": "ideology",
    "capitalism": "ideology",
    "feudalism": "politics",
    "fascism": "ideology",
    "white supremacist ideology": "ideology",
    "pedology": "geography",
    "biogeography": "geography biology",
    "cryptocurrency": "finance",
    "nobility": "monarchy",
    "monarchy": "politics",
    "demography": "social-science statistics government",
    "historical demography": "demography",
    "chromatography": "chemistry",
    "anarchism": "politics",
    "diplomacy": "politics",
    "regionalism": "politics",
    "economic liberalism": "politics",
    "agri.": "agriculture",
    "agriculture": "lifestyle",
    "horticulture": "agriculture",
    "fashion": "lifestyle textiles",
    "cosmetics": "lifestyle",
    "design": "arts lifestyle",
    "money": "finance",
    "oceanography": "geography",
    "geological oceanography": "geology oceanography",
    "angelology": "theology",
    "woodworking": "carpentry",
    "art": "arts",
    "television": "broadcasting",
    "broadcasting": "media",
    "radio": "broadcasting",
    "radio communications": "radio",
    "journalism": "media",
    "writing": "journalism literature",
    "editing": "writing",
    "film": "television",
    "cinematography": "film",
    "drama": "film theater",
    "printing": "publishing",
    "publishing": "media",
    "science fiction": "literature",
    "space science": "aerospace",
    "fiction": "literature",
    "pornography": "media sexuality",
    "information science": "human-sciences",
    "naturism": "lifestyle",
    "veganism": "lifestyle",
    "urbanism": "lifestyle",
    "Kantianism": "philosophy",
    "newspapers": "journalism",
    "telegraphy": "telecommunications",
    "wireless telegraphy": "telegraphy",
    "telegram": "telegraphy",
    "audio": "radio television electrical-engineering",
    "literature": "publishing",
    "folklore": "arts history",
    "music": "publishing arts",
    "guitar": "music",
    "musicology": "music human-sciences",
    "talking": "communications",
    "militaryu": "military",
    "army": "military",
    "navy": "military",
    "naval": "navy",
    "weaponry": "military tools",
    "weapon": "weaponry",
    "firearms": "weaponry",
    "fortifications": "military",
    "fortification": "fortifications",
    "law enforcement": "government",
    "archaeology": "history",
    "epigraphy": "history",
    "paleontology": "history natural-sciences",
    "palæontology": "paleontology",
    "paleobiology": "paleontology biology",
    "paleoanthropology": "paleontology anthropology",
    "paleogeography": "paleontology geography",
    "palentology": "paleontology error",
    "papyrology": "history",
    "hagiography": "history religion",
    "palaeography": "history",
    "historical geography": "geography history",
    "historiography": "history",
    "calligraphy": "arts",
    "ichthyology": "zoology",
    "herpetology": "zoology",
    "glaciology": "geography",
    "arachnology": "zoology",
    "veterinary pathology": "zoology pathology",
    "patology": "pathology",
    "acarology": "arachnology",
    "mythology": "human-sciences",
    "ufology": "mythology",
    "fundamental interactions": "physics",
    "quantum field theory": "physics",
    "extragalactic medium": "cosmology",
    "extra-cluster medium": "cosmology",
    "uranography": "cartography astronomy",
    "astrocartography": "cartography astronomy",
    "mining": "manufacturing",
    "forestry": "manufacturing",
    "metalworking": "crafts",
    "metallurgy": "engineering",
    "communication": "communications",
    "telecommunications": "electrical-engineering communications",
    "telephony": "telecommunications communications",
    "bookbinding": "crafts publishing",
    "petrology": "geology",
    "petroleum": "petrology energy",
    "petrography": "petrology",
    "energy": "engineering physics",
    "shipbuilding": "manufacturing",
    "plumbing": "construction",
    "roofing": "construction",
    "carpentry": "construction",
    "construction": "manufacturing",
    "piledriving": "construction",
    "masonry": "construction",
    "stone": "masonry",
    "tools": "engineering",
    "cranes": "tools",
    "colleges": "education",
    "higher education": "education",
    "clothing": "textiles fashion",
    "alchemy": "pseudoscience",
    "photography": "hobbies arts",
    "videography": "photography film",
    "horses": "sports lifestyle",
    "equestrianism": "horses",
    "demoscene": "computing",
    "golf": "sports lifestyle",
    "tennis": "sports",
    "hunting": "lifestyle agriculture",
    "fishing": "lifestyle agriculture",
    "birdwashing": "hobbies",
    "fisheries": "ecology",
    "climatology": "geography ecology",
    "limnology": "ecology",
    "informatics": "computing",
    "marketing": "business",
    "advertising": "marketing",
    "electrotechnology": "electrical-engineering",
    "electromagnetic radiation": "electromagnetism",
    "electronics manufacturing": "manufacturing electrical-engineering",
    "electric power": "energy electrical-engineering",
    "electronic communication": "telecommunications",
    "electrical device": "electrical-engineering",
    "enology": "oenology",
    "oenology": "food",
    "wine": "oenology lifestyle",
    "cigars": "lifestyle",
    "smoking": "lifestyle",
    "gambling": "games",
    "exercise": "sports",
    "acting": "drama",
    "theater": "arts",
    "comedy": "theater film",
    "dominoes": "games",
    "pocket billiards": "games",
    "pool": "games",
    "graphical user interface": "computing",
    "mysticism": "philosophy",
    "philology": "philosophy",
    "enthnology": "human-sciences",
    "feminism": "ideology",
    "creationism": "ideology religion",
    "shamanism": "religion",
    "ideology": "politics philosophy",
    "politology": "political-science",
    "political-science": "human-sciences",
    "political science": "political-science",
    "cartomancy": "mysticism",
    "tarot": "mysticism",
    "tasseography": "mysticism",
    "theology": "religion",
    "religionists": "religion",
    "spiritualism": "religion",
    "horse racing": "horses",
    "horse-racing": "horses",
    "equitation": "horses",
    "farriery": "horses",
    "motor racing": "sports",
    "racing": "sports",
    "spinning": "sports",
    "gymnastics": "sports",
    "cricket": "sports",
    "volleyball": "sports",
    "lacrosse": "sports",
    "rugby": "sports",
    "bodybuilding": "sports",
    "falconry": "hunting",
    "parachuting": "sports",
    "squash": "sports",
    "curling": "sports",
    "motorcycling": "sports",
    "swimming": "sports",
    "diving": "sports",
    "underwater diving": "diving",
    "basketball": "sports",
    "baseball": "sports",
    "soccer": "sports",
    "snooker": "sports",
    "snowboarding": "sports",
    "skateboarding": "sports",
    "weightlifting": "sports",
    "skiing": "sports",
    "mountaineering": "sports",
    "skating": "sports",
    "cycling": "sports",
    "rowing": "sports",
    "boxing": "martial-arts",
    "bullfighting": "sports",
    "archery": "martial-arts",
    "fencing": "martial-arts",
    "climbing": "sports",
    "surfing": "sports",
    "ballooning": "sports",
    "sailmaking": "manufacturing nautical",
    "sailing": "nautical",
    "maritime": "nautical",
    "ropemaking": "manufacturing nautical",
    "retail": "commerce",
    "commercial": "commerce",
    "retailing": "commerce",
    "electrical": "electricity",
    "category theory": "mathematics computing",
    "in technical contexts": "engineering physics chemistry",
    "technology": "engineering",
    "technical": "engineering",
    "stock exchange": "finance",
    "surveying": "geography",
    "networking": "computing",
    "computer sciences": "computing",
    "computer software": "computing",
    "software compilation": "computing",
    "computer languages": "computing",
    "computer hardware": "computing",
    "computer graphics": "computing",
    "meats": "food",
    "meat": "meats",
    "web design": "computing",
    "aviation": "aeronautics",
    "aerospace": "aeronautics",
    "investment": "finance",
    "computing theory": "computing mathematics",
    "information theory": "mathematics computing",
    "probability": "mathematics",
    "probability theory": "mathematics",
    "set theory": "mathematics",
    "sets": "mathematics",
    "order theory": "mathematics",
    "graph theory": "mathematics",
    "mathematical analysis": "mathematics",
    "combinatorics": "mathematics",
    "cellular automata": "computing mathematics",
    "game theory": "mathematics computing",
    "computational": "computing",
    "behavioral sciences": "psychology",
    "space sciences": "astronomy",
    "applied sciences": "sciences engineering",
    "(sport)": "sports",
    "stock ticker symbol": "finance",
    "banking": "economics",
    "commerce": "economics",
    "cryptocurrency": "finance",
    "cartography": "geography",
    "ecology": "biology",
    "hydrology": "geography",
    "hydrography": "hydrology oceanography",
    "topography": "geography",
    "bibliography": "history literature",
    "polygraphy": "legal",
    "planetology": "astronomy",
    "astrology": "mysticism",
    "astrology signs": "astrology",
    "linguistic morphology": "morphology",
    "science": "sciences",
    "video games": "games",
    "role-playing games": "games",
    "poker": "games",
    "waterpolo": "games",
    "wrestling": "martial-arts",
    "professional wrestling": "wrestling",
    "sumo": "wrestling",
    "law": "legal",
    "court": "legal government",
    "rail transport": "railways",
    "colour": "color",
    "color": "property",
    "time": "property",
    "days of the week": "weekdays",
    "weekdays": "time",
    "temporal location": "time",
    "location": "property",
    "time": "property",
    "heading": "property",
    "manner": "property",
    "monotheism": "religion",
    "Catholicism": "Christianity",
    "Protestantism": "Christianity",
    "occultism": "religion",
    "buddhism": "religion",
    "hinduism": "religion",
    "Roman Catholicism": "Catholicism",
    "position": "location",
    "origin": "location",
    "source": "location",
    "cause": "property",
    "state": "property",
    "naturism": "lifestyle",
    "organic chemistry": "chemistry",
}
