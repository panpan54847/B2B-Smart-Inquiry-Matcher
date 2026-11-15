"""
generate_mock_data.py
=====================
Large-scale mock data generator for B2B Smart Inquiry Matcher.

Outputs:
  1. suppliers_products.csv - 3000+ supplier products spanning 15+ countries
  2. inquiries.csv          - 500+ buyer inquiries spanning 40+ countries

Run:
    python data/generate_mock_data.py
"""

import csv
import os
import random

random.seed(42)

# ---------------------------------------------------------------------------
# Product dimension pools
# ---------------------------------------------------------------------------

PRODUCT_CATEGORIES = {
    "plush_squeaky": {
        "names": [
            "Plush Squeaky Dog Toy - {shape} Shape",
            "Soft Squeaky Plush Toy - {animal}",
            "Plush Dog Chew Toy - {shape} Design",
            "Cute Plush Squeaker - {animal} Shape",
            "Durable Plush Toy - {shape} with Squeaker",
            "Plush Squeaky {animal} Dog Toy",
            "Soft Plush {animal} Toy with Sound",
            "Plush Squeaker Toy - {shape} for Dogs",
        ],
        "materials": [
            "Plush + PP Cotton", "Plush + Squeaker", "Plush + Catnip",
            "Plush + Cotton Rope", "Plush + PP Cotton + Squeaker",
            "Plush + Recycled Fiber",
        ],
        "sizes": ["10cm", "12cm", "15cm", "18cm", "20cm", "22cm", "25cm", "28cm", "30cm", "35cm"],
        "moq_range": (200, 2000),
        "base_price": (0.45, 3.20),
    },
    "rubber_ball": {
        "names": [
            "Natural Rubber Dog Ball - {feature}",
            "Rubber Bouncy Ball - {size_label}",
            "Durable Rubber Ball for Dogs - {feature}",
            "TPR Dog Ball - {feature}",
            "Heavy Duty Rubber Ball - {size_label}",
            "Natural Rubber Chew Ball - {feature}",
        ],
        "materials": [
            "Natural Rubber", "TPR (Thermoplastic Rubber)", "TPR",
            "Natural Rubber + Squeaker", "Food Grade Rubber",
        ],
        "sizes": ["4cm", "5cm", "6cm", "6.5cm", "7cm", "8cm", "9cm", "10cm", "12cm"],
        "moq_range": (300, 3000),
        "base_price": (0.25, 2.50),
    },
    "rubber_chew": {
        "names": [
            "Rubber Dog Chew Toy - {shape} Shape",
            "Heavy Duty Chew Toy - {shape}",
            "Durable Rubber Chew - {feature}",
            "TPR Chew Toy - {shape} Design",
            "Natural Rubber Chew - {shape} for Dogs",
            "Tough Rubber Chew Toy - {shape}",
        ],
        "materials": [
            "Natural Rubber", "TPR", "Natural Rubber + Nylon",
            "Heavy Duty Rubber", "Food Grade Rubber + Squeaker",
        ],
        "sizes": ["10cm", "12cm", "14cm", "16cm", "18cm", "20cm"],
        "moq_range": (200, 1500),
        "base_price": (0.80, 3.50),
    },
    "rope_tug": {
        "names": [
            "Cotton Rope Dog Toy - {feature}",
            "Rope Tug Toy - {shape} Shape",
            "Durable Rope Toy - {feature}",
            "Thick Rope Tug - {size_label}",
            "Multi-Color Rope Dog Toy - {feature}",
            "Heavy Duty Rope Toy - {shape}",
        ],
        "materials": [
            "Cotton Rope", "Cotton + Polyester Rope", "Heavy Duty Cotton Rope",
            "Organic Cotton Rope", "Cotton Rope + Squeaker",
        ],
        "sizes": ["20cm", "25cm", "30cm", "40cm", "50cm", "60cm"],
        "moq_range": (200, 2000),
        "base_price": (0.50, 3.80),
    },
    "cat_toy": {
        "names": [
            "Catnip Mouse Toy - {feature}",
            "Interactive Cat Toy - {feature}",
            "Cat Feather Wand - {feature}",
            "Cat Ball Toy - {feature}",
            "Cat Tunnel Toy - {feature}",
            "Cat Scratching Board - {mat_short}",
        ],
        "materials": [
            "Plush + Catnip + Bell", "Feather + Plastic Stick", "Polyester + Crinkle Paper",
            "Plastic + Bell", "Corrugated Cardboard", "Plush + Catnip",
            "Catnip + Cotton",
        ],
        "sizes": ["4cm", "8cm", "10cm", "35x35x80cm", "40x25cm", "50x30cm", "30x15cm"],
        "moq_range": (300, 3000),
        "base_price": (0.15, 5.00),
    },
    "collar_leash": {
        "names": [
            "Pet Dog Collar - {mat_short} {feature}",
            "Dog Leash - {mat_short} {feature}",
            "Adjustable Dog Collar - {feature}",
            "Reflective Dog Leash - {feature}",
            "Retractable Dog Leash - {size_label}",
            "Dog Harness - {mat_short} {feature}",
        ],
        "materials": [
            "Nylon Webbing + Metal Buckle", "Nylon + Metal Hook",
            "Leather + Brass", "Polyester + Plastic Buckle",
            "Neoprene + Nylon", "Reflective Nylon + Metal",
        ],
        "sizes": ["1.5cm x 120cm", "2cm x 45cm", "2.5cm x 50cm", "1.2cm x 100cm", "2cm x 150cm"],
        "moq_range": (300, 2000),
        "base_price": (0.50, 4.50),
    },
    "pet_bed": {
        "names": [
            "Pet Dog Bed - {feature}",
            "Washable Pet Bed - {mat_short}",
            "Soft Cushion Pet Bed - {feature}",
            "Orthopedic Dog Bed - {feature}",
            "Cat Bed - {mat_short} {feature}",
            "Round Pet Bed - {size_label}",
        ],
        "materials": [
            "Fleece + PP Cotton", "Cotton + Memory Foam", "Plush + Polyester",
            "Microfiber + PP Cotton", "Oxford Cloth + Cotton",
        ],
        "sizes": ["40x30cm", "50x40cm", "60x45cm", "70x50cm", "80x60cm", "100x70cm"],
        "moq_range": (100, 800),
        "base_price": (1.80, 12.00),
    },
    "pet_bowl": {
        "names": [
            "Dog Bowl - {mat_short} {feature}",
            "Stainless Steel Dog Bowl - {feature}",
            "Ceramic Pet Bowl - {feature}",
            "Slow Feeder Bowl - {mat_short}",
            "Travel Dog Bowl - {feature}",
            "Double Dog Bowl Set - {feature}",
        ],
        "materials": [
            "Stainless Steel", "Ceramic", "Bamboo Fiber + Ceramic",
            "PP Plastic + Silicone", "Melamine", "Silicone + Stainless Steel",
        ],
        "sizes": ["10cm", "12cm", "15cm", "18cm", "20cm diameter", "6cm x 15cm"],
        "moq_range": (200, 2000),
        "base_price": (0.30, 5.50),
    },
    "pet_accessory": {
        "names": [
            "Pet Carrier Bag - {feature}",
            "Pet Grooming Glove - {mat_short}",
            "Pet Water Bottle - {feature}",
            "Dog Clicker - {feature}",
            "Dog Poop Bag Dispenser - {feature}",
            "Dog Cooling Bandana - {feature}",
            "Pet First Aid Kit - {feature}",
            "Dog Seat Cover - {mat_short}",
        ],
        "materials": [
            "Oxford Cloth + Mesh", "Silicone + Mesh", "PP Plastic + Silicone",
            "ABS Plastic + Metal", "ABS Plastic", "Cooling Fabric + PVA",
            "Polyester + Waterproof Coating", "Nylon + PVC",
        ],
        "sizes": ["One Size", "8x5cm", "6x4cm", "500ml", "50x5cm", "45x28x28cm", "140x60cm"],
        "moq_range": (300, 3000),
        "base_price": (0.20, 8.00),
    },
    "seasonal": {
        "names": [
            "Christmas Plush Dog Toy - {character}",
            "Halloween Dog Costume - {character}",
            "Easter Plush Toy - {character}",
            "Valentine Pet Toy - {character} Shape",
            "Holiday Dog Sweater - {character}",
            "New Year Pet Bandana - {character}",
        ],
        "materials": [
            "Plush + Squeaker", "Polyester + Cotton", "Plush + PP Cotton",
            "Acrylic + Cotton", "Polyester + Bell",
        ],
        "sizes": ["S/M/L", "M/L/XL", "20cm", "25cm", "One Size"],
        "moq_range": (200, 1000),
        "base_price": (0.60, 4.00),
    },
}

SHAPES = ["Bone", "Ball", "Star", "Ring", "Heart", "Triangle", "Square", "Disc", "Cylinder", "Figure 8"]
ANIMALS = ["Duck", "Pig", "Elephant", "Dinosaur", "Rabbit", "Bear", "Frog", "Hedgehog", "Monkey", "Penguin", "Lion", "Tiger", "Fish", "Bird", "Turtle"]
FEATURES = ["Bouncy", "Durable", "Squeaky", "Interactive", "Washable", "Non-Slip", "Reflective", "Adjustable", "Collapsible", "Heavy Duty", "Lightweight", "Portable", "Foldable", "Waterproof", "Breathable", "Orthopedic", "Slow Feeder", "Double Layer", "Eco-Friendly", "Machine Washable"]
SIZE_LABELS = ["Small", "Medium", "Large", "Extra Large", "Mini", "Jumbo"]
CHARACTERS = ["Santa Claus", "Reindeer", "Snowman", "Pumpkin", "Ghost", "Witch", "Bunny", "Egg", "Heart", "Cupid", "Dragon", "Lantern"]
MAT_SHORT_MAP = {
    "Plush + PP Cotton": "Plush", "Natural Rubber": "Rubber", "Cotton Rope": "Cotton",
    "Nylon Webbing + Metal Buckle": "Nylon", "Stainless Steel": "Steel",
    "Silicone + Mesh": "Silicone", "Fleece + PP Cotton": "Fleece",
    "Polyester + Cotton": "Polyester", "Oxford Cloth + Mesh": "Oxford",
    "Corrugated Cardboard": "Cardboard", "TPR (Thermoplastic Rubber)": "TPR",
    "TPR": "TPR", "Ceramic": "Ceramic", "Leather + Brass": "Leather",
    "Acrylic + Cotton": "Acrylic",
}


def get_mat_short(material):
    for key, short in MAT_SHORT_MAP.items():
        if key in material:
            return short
    return material.split(" ")[0]


def fill_name(template):
    return template.format(
        shape=random.choice(SHAPES),
        animal=random.choice(ANIMALS),
        feature=random.choice(FEATURES),
        size_label=random.choice(SIZE_LABELS),
        character=random.choice(CHARACTERS),
        mat_short=get_mat_short(random.choice(list(MAT_SHORT_MAP.keys()))),
    )


# ---------------------------------------------------------------------------
# Supplier regions
# ---------------------------------------------------------------------------

SUPPLIER_REGIONS = {
    "China": {
        "cities": ["Yiwu", "Yangzhou", "Dongguan", "Qingdao", "Ningbo", "Shenzhen", "Wenzhou",
                    "Hangzhou", "Guangzhou", "Xiamen", "Wuxi", "Shanghai", "Foshan", "Zhongshan",
                    "Suzhou", "Changzhou", "Tianjin", "Jinan", "Chengdu", "Wuhan", "Taizhou",
                    "Shantou", "Linyi", "Hebei", "Hefei"],
        "company_prefixes": ["Yiwu", "Yangzhou", "Dongguan", "Qingdao", "Ningbo", "Shenzhen",
                             "Wenzhou", "Hangzhou", "Guangzhou", "Xiamen", "Wuxi", "Foshan",
                             "Suzhou", "Zhongshan", "Tianjin", "Chengdu"],
        "company_suffixes": ["Pet Products Co., Ltd.", "Pet Toy Factory", "Pet Supplies Mfg. Co.",
                             "Animal Products Ltd.", "Pet Industry Co.", "Toys Manufacturing Ltd.",
                             "Pet Tech Co., Ltd.", "Companion Pet Supplies Ltd."],
        "email_domains": ["pet.cn", "pettoys.cn", "petmfg.cn", "animal.cn", "petpro.cn",
                          "petexport.cn", "tradepet.cn", "petsupply.cn"],
        "lead_time_range": (7, 30),
        "certifications": ["BSCI, CE", "ISO 9001", "SGS, FDA", "ICTI, BSCI", "RoHS, REACH",
                           "CE, RoHS", "OEKO-TEX", "BSCI", "ISO 9001, CE", "FDA, LFGB",
                           "SGS", "BSCI, SGS", "ISO 14001"],
        "price_factor": 1.0,
        "weight": 1200,
    },
    "Vietnam": {
        "cities": ["Ho Chi Minh City", "Hanoi", "Hai Phong", "Da Nang", "Binh Duong", "Can Tho"],
        "company_prefixes": ["Saigon", "Hanoi", "Vietnam", "Mekong", "Vina", "Dong Nai", "Binh Duong"],
        "company_suffixes": ["Pet Products JSC", "Pet Manufacturing Ltd.", "Animal Supplies Co.",
                             "Pet Export Co.", "Pet Industry JSC"],
        "email_domains": ["pet.vn", "vietpet.vn", "petsupply.vn", "animal.vn"],
        "lead_time_range": (10, 35),
        "certifications": ["ISO 9001", "BSCI", "CE", "SGS", "ISO 9001, BSCI"],
        "price_factor": 0.85,
        "weight": 200,
    },
    "India": {
        "cities": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Pune", "Ahmedabad",
                   "Surat", "Jaipur", "Lucknow"],
        "company_prefixes": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Bharat", "Indian",
                             "Hindustan", "Pune", "Gujarat"],
        "company_suffixes": ["Pet Products Pvt Ltd", "Pet Supplies India Pvt Ltd",
                             "Animal Care Ltd.", "Pet Manufacturing India",
                             "Pet Export House", "Pet Industry Pvt Ltd"],
        "email_domains": ["pet.in", "indianpet.in", "petsupply.in", "animal.in", "petpro.in"],
        "lead_time_range": (12, 35),
        "certifications": ["ISO 9001", "BIS, CE", "SGS", "ISO 9001, ISO 22000", "BSCI"],
        "price_factor": 0.80,
        "weight": 250,
    },
    "Thailand": {
        "cities": ["Bangkok", "Chiang Mai", "Phuket", "Rayong", "Chonburi", "Ayutthaya"],
        "company_prefixes": ["Bangkok", "Thai", "Siam", "Chiang Mai", "Rayong", "Oriental"],
        "company_suffixes": ["Pet Products Co. Ltd.", "Pet Manufacturing Co.",
                             "Animal Supplies Ltd.", "Pet Export Co. Ltd."],
        "email_domains": ["pet.co.th", "thaipet.co.th", "petsupply.co.th"],
        "lead_time_range": (10, 30),
        "certifications": ["ISO 9001", "CE", "GMP", "SGS"],
        "price_factor": 0.90,
        "weight": 150,
    },
    "Turkey": {
        "cities": ["Istanbul", "Izmir", "Ankara", "Bursa", "Konya", "Antalya"],
        "company_prefixes": ["Istanbul", "Anatolia", "Marmara", "Aegean", "Turkish", "Bursa"],
        "company_suffixes": ["Pet Products Ltd.", "Pet Manufacturing Co.",
                             "Animal Supplies Ltd.", "Pet Trade Ltd."],
        "email_domains": ["pet.com.tr", "turkishpet.com.tr", "petsupply.com.tr"],
        "lead_time_range": (10, 30),
        "certifications": ["CE", "ISO 9001", "BSCI", "REACH"],
        "price_factor": 1.05,
        "weight": 150,
    },
    "Brazil": {
        "cities": ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre",
                   "Salvador", "Recife", "Fortaleza"],
        "company_prefixes": ["Sao Paulo", "Brasil", "Rio", "Mineiro", "Gaucho", "Tropical"],
        "company_suffixes": ["Pet Products Ltda", "Pet Comercio Ltda", "Animal Supplies Ltda",
                             "Pet Manufacturing Ltda", "Pet Export Ltda"],
        "email_domains": ["pet.com.br", "brasilpet.com.br", "petsupply.com.br"],
        "lead_time_range": (15, 40),
        "certifications": ["ISO 9001", "INMETRO", "CE", "SGS"],
        "price_factor": 1.15,
        "weight": 180,
    },
    "Mexico": {
        "cities": ["Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana", "Queretaro",
                   "Leon", "Merida"],
        "company_prefixes": ["Mexico", "Guadalajara", "Monterrey", "Azteca", "Maya", "Queretaro"],
        "company_suffixes": ["Pet Products S.A. de C.V.", "Pet Manufacturing S.A.",
                             "Animal Supplies S.A.", "Pet Comercio S.A. de C.V."],
        "email_domains": ["pet.com.mx", "mexpet.com.mx", "petsupply.com.mx"],
        "lead_time_range": (12, 35),
        "certifications": ["ISO 9001", "NOM", "CE", "FDA"],
        "price_factor": 1.10,
        "weight": 150,
    },
    "Indonesia": {
        "cities": ["Jakarta", "Surabaya", "Bandung", "Medan", "Semarang", "Makassar"],
        "company_prefixes": ["Jakarta", "Indonesia", "Jawa", "Surabaya", "Nusantara"],
        "company_suffixes": ["Pet Products Pt", "Pet Manufacturing Pt", "Animal Supplies Pt",
                             "Pet Export Pt"],
        "email_domains": ["pet.co.id", "indopet.co.id", "petsupply.co.id"],
        "lead_time_range": (14, 35),
        "certifications": ["ISO 9001", "Halal", "CE", "SGS"],
        "price_factor": 0.88,
        "weight": 120,
    },
    "Bangladesh": {
        "cities": ["Dhaka", "Chittagong", "Khulna", "Sylhet", "Rajshahi"],
        "company_prefixes": ["Dhaka", "Bengal", "Bangladesh", "Ganges"],
        "company_suffixes": ["Pet Products Ltd.", "Pet Manufacturing Co.",
                             "Animal Supplies Ltd.", "Pet Export Ltd."],
        "email_domains": ["pet.com.bd", "bengalpet.com.bd"],
        "lead_time_range": (15, 40),
        "certifications": ["ISO 9001", "BSCI", "WRAP"],
        "price_factor": 0.75,
        "weight": 100,
    },
    "South Korea": {
        "cities": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon", "Gwangju"],
        "company_prefixes": ["Seoul", "Korea", "Hanjin", "Busan", "Daegu"],
        "company_suffixes": ["Pet Products Co. Ltd.", "Pet Manufacturing Co. Ltd.",
                             "Animal Supplies Co. Ltd.", "Pet Tech Co. Ltd."],
        "email_domains": ["pet.co.kr", "koreapet.co.kr", "petsupply.co.kr"],
        "lead_time_range": (7, 25),
        "certifications": ["ISO 9001", "KC", "CE", "RoHS", "FDA"],
        "price_factor": 1.25,
        "weight": 120,
    },
    "Poland": {
        "cities": ["Warsaw", "Krakow", "Gdansk", "Wroclaw", "Poznan", "Lodz"],
        "company_prefixes": ["Warsaw", "Poland", "Krakow", "Baltic", "Wroclaw"],
        "company_suffixes": ["Pet Products Sp. z o.o.", "Pet Manufacturing Sp. z o.o.",
                             "Animal Supplies Sp. z o.o.", "Pet Trade Sp. z o.o."],
        "email_domains": ["pet.pl", "polishpet.pl", "petsupply.pl"],
        "lead_time_range": (10, 28),
        "certifications": ["CE", "ISO 9001", "BSCI", "REACH"],
        "price_factor": 1.05,
        "weight": 100,
    },
    "Italy": {
        "cities": ["Milan", "Rome", "Turin", "Bologna", "Florence", "Naples", "Venice",
                   "Verona", "Bari", "Parma"],
        "company_prefixes": ["Milano", "Italia", "Roma", "Torino", "Bologna", "Tuscan",
                             "Veneto", "Lombardia"],
        "company_suffixes": ["Pet Products S.r.l.", "Pet Manufacturing S.r.l.",
                             "Animal Supplies S.r.l.", "Pet Comercio S.r.l."],
        "email_domains": ["pet.it", "italypet.it", "petsupply.it"],
        "lead_time_range": (10, 30),
        "certifications": ["CE", "ISO 9001", "REACH", "BSCI", "LFGB"],
        "price_factor": 1.30,
        "weight": 120,
    },
    "United States": {
        "cities": ["Los Angeles", "New York", "Chicago", "Houston", "Phoenix", "Philadelphia",
                   "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Seattle",
                   "Denver", "Boston", "Atlanta", "Miami"],
        "company_prefixes": ["American", "USA", "Pacific", "Atlantic", "Continental",
                             "Liberty", "Eagle", "Pioneer", "Frontier", "Summit"],
        "company_suffixes": ["Pet Products LLC", "Pet Supply Inc.", "Animal Care Co.",
                             "Pet Manufacturing Corp.", "Pet Innovations LLC",
                             "Companion Pet Co.", "Pet Solutions Inc."],
        "email_domains": ["pet.com", "usapet.com", "petsupply.com", "animalcare.com",
                          "petmfg.com", "petinnovations.com"],
        "lead_time_range": (5, 20),
        "certifications": ["FDA", "ASTM", "ISO 9001", "UL", "CE, FDA", "USDA Organic"],
        "price_factor": 1.50,
        "weight": 200,
    },
    "Germany": {
        "cities": ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt", "Stuttgart",
                   "Dusseldorf", "Leipzig", "Dortmund", "Bremen"],
        "company_prefixes": ["Berlin", "Munich", "German", "Hansa", "Bavarian", "Rhein",
                             "Schwaben", "Nord"],
        "company_suffixes": ["Pet Products GmbH", "Pet Manufacturing GmbH",
                             "Animal Supplies GmbH & Co. KG", "Pet Trade GmbH",
                             "Pet Innovations GmbH"],
        "email_domains": ["pet.de", "germanpet.de", "petsupply.de", "haustier.de"],
        "lead_time_range": (7, 25),
        "certifications": ["CE", "REACH", "ISO 9001", "LFGB", "TUV", "BSCI, REACH"],
        "price_factor": 1.40,
        "weight": 180,
    },
    "United Kingdom": {
        "cities": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Liverpool",
                   "Sheffield", "Bristol", "Nottingham", "Leicester"],
        "company_prefixes": ["London", "British", "Manchester", "Royal", "Thames",
                             "Highland", "Anglia", "Mercia"],
        "company_suffixes": ["Pet Products Ltd.", "Pet Manufacturing Ltd.",
                             "Animal Supplies Ltd.", "Pet Trade Ltd.",
                             "Pet Innovations Ltd."],
        "email_domains": ["pet.co.uk", "ukpet.co.uk", "petsupply.co.uk"],
        "lead_time_range": (7, 25),
        "certifications": ["CE", "ISO 9001", "BSCI", "UKCA", "FSC"],
        "price_factor": 1.35,
        "weight": 150,
    },
}


def generate_supplier(region_name, rd):
    city = random.choice(rd["cities"])
    prefix = random.choice(rd["company_prefixes"])
    suffix = random.choice(rd["company_suffixes"])
    company_name = f"{prefix} {suffix}"
    domain = random.choice(rd["email_domains"])
    email_prefix = random.choice(["sales", "info", "export", "contact", "office", "trade", "purchasing", "wholesale"])
    email = f"{email_prefix}@{domain}"
    lead_time = f"{random.randint(*rd['lead_time_range'])} days"
    cert = random.choice(rd["certifications"])
    return {
        "supplier_name": company_name,
        "contact_email": email,
        "country": region_name,
        "city": city,
        "lead_time": lead_time,
        "certification": cert,
        "price_factor": rd["price_factor"],
    }


# ---------------------------------------------------------------------------
# Buyer countries
# ---------------------------------------------------------------------------

BUYER_COUNTRIES = [
    {"country": "United States",
     "email_domains": ["gmail.com", "outlook.com", "petco.com", "chewy.com", "petsmart.com"],
     "names": [["James", "Smith"], ["Mary", "Johnson"], ["Robert", "Williams"], ["Patricia", "Brown"],
               ["Michael", "Rodriguez"], ["Jennifer", "Davis"], ["William", "Martinez"], ["Linda", "Garcia"],
               ["David", "Wilson"], ["Elizabeth", "Anderson"], ["Richard", "Taylor"], ["Susan", "Thomas"],
               ["Joseph", "Harris"], ["Jessica", "Moore"], ["Thomas", "Jackson"], ["Sarah", "Martin"],
               ["Charles", "Lee"], ["Karen", "Thompson"], ["Christopher", "White"], ["Nancy", "Harris"]],
     "company_suffixes": ["LLC", "Inc.", "Corp.", "Co.", "LLP", "Group"]},
    {"country": "United Kingdom",
     "email_domains": ["gmail.com", "outlook.com", "petlandia.co.uk", "petplanet.co.uk"],
     "names": [["James", "Wilson"], ["Sarah", "Mitchell"], ["David", "Brown"], ["Emma", "Taylor"],
               ["Michael", "Davies"], ["Jessica", "Evans"], ["Robert", "Thomas"], ["Sophie", "Roberts"],
               ["William", "Walker"], ["Olivia", "Hughes"], ["Thomas", "Clarke"], ["Emily", "Green"],
               ["Daniel", "Wright"], ["Grace", "Cooper"], ["Andrew", "Edwards"], ["Chloe", "Bennett"]],
     "company_suffixes": ["Ltd.", "PLC", "LLP", "Co.", "Group"]},
    {"country": "Germany",
     "email_domains": ["gmail.com", "web.de", "gmx.de", "haustier.de", "petworld.de"],
     "names": [["Markus", "Weber"], ["Anna", "Schmidt"], ["Stefan", "Schneider"], ["Julia", "Fischer"],
               ["Andreas", "Meyer"], ["Lisa", "Wagner"], ["Thomas", "Becker"], ["Sarah", "Schulz"],
               ["Michael", "Hoffmann"], ["Katrin", "Schmidt"], ["Christian", "Lange"], ["Nina", "Wolf"],
               ["Peter", "Muller"], ["Laura", "Klein"], ["Martin", "Lehmann"], ["Sandra", "Krause"]],
     "company_suffixes": ["GmbH", "GmbH & Co. KG", "AG"]},
    {"country": "France",
     "email_domains": ["gmail.com", "orange.fr", "wanadoo.fr", "animallie.fr", "petmag.fr"],
     "names": [["Pierre", "Dubois"], ["Sophie", "Moreau"], ["Jean", "Laurent"], ["Marie", "Lefebvre"],
               ["Thomas", "Roux"], ["Camille", "Fournier"], ["Nicolas", "Girard"], ["Julie", "Bonnet"],
               ["Antoine", "Gautier"], ["Claire", "Picard"], ["Francois", "Leroy"], ["Manon", "Renaud"],
               ["Louis", "Mercier"], ["Lea", "Guerin"], ["Paul", "Blanc"], ["Emma", "Henry"]],
     "company_suffixes": ["SARL", "SA", "SAS"]},
    {"country": "Canada",
     "email_domains": ["gmail.com", "outlook.com", "barkbox.ca", "petmac.ca"],
     "names": [["James", "OConnor"], ["Emily", "MacDonald"], ["William", "Campbell"], ["Jessica", "Stewart"],
               ["Michael", "Thompson"], ["Sarah", "Clarke"], ["David", "Wilson"], ["Ashley", "MacKenzie"],
               ["Ryan", "Murphy"], ["Amanda", "Brooks"], ["Kevin", "Reid"], ["Lauren", "Howard"]],
     "company_suffixes": ["Inc.", "Corp.", "Ltd.", "LLP"]},
    {"country": "Australia",
     "email_domains": ["gmail.com", "bigpond.com", "petprosperity.com.au", "petcircle.com.au"],
     "names": [["James", "Anderson"], ["Emily", "Chen"], ["Liam", "Williams"], ["Olivia", "Brown"],
               ["Noah", "Taylor"], ["Charlotte", "Wilson"], ["Lucas", "Nguyen"], ["Mia", "Lee"],
               ["Ethan", "Clark"], ["Ava", "Harris"], ["Jack", "Martin"], ["Ruby", "Walker"]],
     "company_suffixes": ["Pty Ltd", "Pty. Ltd.", "Ltd."]},
    {"country": "Japan",
     "email_domains": ["gmail.com", "yahoo.co.jp", "petlife.jp", "pethome.jp"],
     "names": [["Hiroshi", "Tanaka"], ["Yuki", "Suzuki"], ["Takeshi", "Watanabe"], ["Akiko", "Ito"],
               ["Kenji", "Yamamoto"], ["Sakura", "Takahashi"], ["Ryo", "Kobayashi"], ["Mai", "Sato"],
               ["Daisuke", "Nakamura"], ["Aya", "Kato"], ["Taro", "Yoshida"], ["Haruka", "Yamada"]],
     "company_suffixes": ["K.K.", "Co. Ltd.", "Inc.", "Ltd."]},
    {"country": "South Korea",
     "email_domains": ["gmail.com", "naver.com", "koreapetlink.kr", "petplus.kr"],
     "names": [["Minjun", "Kim"], ["Seoyeon", "Lee"], ["Doyoon", "Park"], ["Jiwoo", "Choi"],
               ["David", "Kim"], ["Emily", "Park"], ["Daniel", "Lee"], ["Yuna", "Jung"],
               ["Jin", "Song"], ["Hana", "Lim"]],
     "company_suffixes": ["Co. Ltd.", "Inc.", "Ltd."]},
    {"country": "Brazil",
     "email_domains": ["gmail.com", "uol.com.br", "petbrasil.com.br", "petlove.com.br"],
     "names": [["Lucas", "Oliveira"], ["Sofia", "Silva"], ["Pedro", "Santos"], ["Helena", "Costa"],
               ["Gabriel", "Pereira"], ["Valentina", "Rodrigues"], ["Miguel", "Almeida"],
               ["Beatriz", "Nascimento"], ["Theo", "Gomes"], ["Alice", "Lima"]],
     "company_suffixes": ["Ltda", "S.A.", "Comercio Ltda"]},
    {"country": "Spain",
     "email_domains": ["gmail.com", "hotmail.es", "petconfort.es", "tiendanimal.es"],
     "names": [["Alejandro", "Garcia"], ["Laura", "Fernandez"], ["Pablo", "Martinez"], ["Lucia", "Sanchez"],
               ["Diego", "Gomez"], ["Maria", "Lopez"], ["Carlos", "Rodriguez"], ["Elena", "Ruiz"],
               ["Javier", "Torres"], ["Carmen", "Diaz"]],
     "company_suffixes": ["S.L.", "S.A.", "S.L.U."]},
    {"country": "Italy",
     "email_domains": ["gmail.com", "libero.it", "amicicani.it", "petstore.it"],
     "names": [["Alessandro", "Rossi"], ["Giulia", "Russo"], ["Marco", "Ferrari"], ["Sofia", "Esposito"],
               ["Francesco", "Bianchi"], ["Aurora", "Romano"], ["Lorenzo", "Colombo"], ["Greta", "Ricci"],
               ["Matteo", "Marino"], ["Anna", "Greco"]],
     "company_suffixes": ["S.r.l.", "S.p.A.", "S.n.c."]},
    {"country": "Netherlands",
     "email_domains": ["gmail.com", "kpn.nl", "dierenvoor.nl", "petworld.nl"],
     "names": [["Daan", "Jansen"], ["Sofia", "deVries"], ["Lars", "Bakker"], ["Emma", "Visser"],
               ["Sem", "Smit"], ["Julia", "deBoer"], ["Lucas", "Mulder"], ["Sophie", "deWit"]],
     "company_suffixes": ["B.V.", "N.V."]},
    {"country": "Sweden",
     "email_domains": ["gmail.com", "telia.com", "svenskapet.se", "petworld.se"],
     "names": [["Erik", "Nilsson"], ["Astrid", "Andersson"], ["Oskar", "Karlsson"], ["Elsa", "Eriksson"],
               ["Liam", "Berg"], ["Ebba", "Lindberg"], ["Noah", "Lundgren"], ["Maja", "Forsberg"]],
     "company_suffixes": ["AB", "KB"]},
    {"country": "Poland",
     "email_domains": ["gmail.com", "wp.pl", "zwierzopol.pl", "petstore.pl"],
     "names": [["Anna", "Kowalski"], ["Piotr", "Nowak"], ["Kasia", "Wojcik"], ["Tomasz", "Kowalczyk"],
               ["Magda", "Kaminski"], ["Jakub", "Lewandowski"], ["Zofia", "Zielinski"]],
     "company_suffixes": ["Sp. z o.o.", "S.A."]},
    {"country": "Mexico",
     "email_domains": ["gmail.com", "hotmail.com", "petmex.mx", "petshop.mx"],
     "names": [["Juan", "Hernandez"], ["Ana", "Garcia"], ["Carlos", "Martinez"], ["Maria", "Lopez"],
               ["Jose", "Gonzalez"], ["Patricia", "Rodriguez"], ["Miguel", "Torres"], ["Daniela", "Flores"]],
     "company_suffixes": ["S.A. de C.V.", "S.A.", "Ltda."]},
    {"country": "India",
     "email_domains": ["gmail.com", "rediffmail.com", "petneeds.in", "petmarket.in"],
     "names": [["Rahul", "Sharma"], ["Priya", "Sharma"], ["Amit", "Patel"], ["Sneha", "Gupta"],
               ["Vikram", "Singh"], ["Ananya", "Reddy"], ["Rohit", "Verma"], ["Deepika", "Nair"],
               ["Arjun", "Mehta"], ["Pooja", "Joshi"]],
     "company_suffixes": ["Pvt Ltd", "Ltd.", "LLP"]},
    {"country": "United Arab Emirates",
     "email_domains": ["gmail.com", "etisalat.ae", "petworld.ae", "petdubai.ae"],
     "names": [["Ahmed", "AlRashid"], ["Fatima", "AlMansouri"], ["Mohammed", "AlMaktoum"],
               ["Aisha", "AlHashimi"], ["Omar", "AlNahyan"], ["Layla", "AlZaabi"]],
     "company_suffixes": ["L.L.C.", "FZE", "FZ-LLC"]},
    {"country": "Singapore",
     "email_domains": ["gmail.com", "singnet.com.sg", "petsg.sg", "petmart.sg"],
     "names": [["Wei", "Tan"], ["Mei", "Lim"], ["Jia", "Ong"], ["Hao", "Goh"],
               ["Xin", "Chua"], ["Boon", "Lee"]],
     "company_suffixes": ["Pte Ltd", "Pte. Ltd."]},
    {"country": "New Zealand",
     "email_domains": ["gmail.com", "xtra.co.nz", "petgo.co.nz", "petworld.nz"],
     "names": [["Jack", "Anderson"], ["Chloe", "Anderson"], ["Oliver", "Smith"], ["Charlotte", "Brown"],
               ["William", "Taylor"], ["Isabella", "Wilson"]],
     "company_suffixes": ["Ltd.", "Limited"]},
    {"country": "Switzerland",
     "email_domains": ["gmail.com", "bluewin.ch", "haustier.ch", "petworld.ch"],
     "names": [["Lukas", "Muller"], ["Laura", "Meier"], ["Stefan", "Schmid"], ["Nina", "Weber"],
               ["Andreas", "Keller"], ["Eva", "Gerber"]],
     "company_suffixes": ["AG", "GmbH"]},
    {"country": "Belgium",
     "email_domains": ["gmail.com", "telenet.be", "dierenvoor.be", "petworld.be"],
     "names": [["Luc", "Janssens"], ["Marie", "Peeters"], ["Tom", "Maes"], ["Els", "Jacobs"],
               ["Jan", "Mertens"], ["Sofie", "Willems"]],
     "company_suffixes": ["BVBA", "NV/SA"]},
    {"country": "Norway",
     "email_domains": ["gmail.com", "online.no", "dyrevenn.no", "petworld.no"],
     "names": [["Henrik", "Nilsson"], ["Ingrid", "Hansen"], ["Erik", "Olsen"], ["Marte", "Larsen"]],
     "company_suffixes": ["AS", "BA"]},
    {"country": "Denmark",
     "email_domains": ["gmail.com", "youmail.dk", "kjaledyr.dk", "petworld.dk"],
     "names": [["Magnus", "Nielsen"], ["Freja", "Jensen"], ["Christian", "Hansen"], ["Sofie", "Pedersen"]],
     "company_suffixes": ["ApS", "A/S"]},
    {"country": "Finland",
     "email_domains": ["gmail.com", "luukku.com", "lemmikki.fi", "petworld.fi"],
     "names": [["Mikko", "Korhonen"], ["Aino", "Virtanen"], ["Jari", "Makinen"], ["Emma", "Nieminen"]],
     "company_suffixes": ["Oy", "Oyj"]},
    {"country": "Austria",
     "email_domains": ["gmail.com", "chello.at", "haustier.at", "petworld.at"],
     "names": [["Stefan", "Gruber"], ["Anna", "Huber"], ["Markus", "Bauer"], ["Lisa", "Steiner"]],
     "company_suffixes": ["GmbH", "OG"]},
    {"country": "Ireland",
     "email_domains": ["gmail.com", "eircom.net", "petworld.ie", "petstore.ie"],
     "names": [["Sean", "Murphy"], ["Aoife", "Kelly"], ["Conor", "Byrne"], ["Niamh", "Ryan"]],
     "company_suffixes": ["Ltd.", "Teo"]},
    {"country": "Portugal",
     "email_domains": ["gmail.com", "sapo.pt", "animal.pt", "petworld.pt"],
     "names": [["Joao", "Silva"], ["Beatriz", "Santos"], ["Tiago", "Fernandes"], ["Mariana", "Costa"]],
     "company_suffixes": ["Lda.", "S.A."]},
    {"country": "Greece",
     "email_domains": ["gmail.com", "otenet.gr", "petworld.gr", "petshop.gr"],
     "names": [["Nikos", "Papadopoulos"], ["Maria", "Georgiou"], ["Yannis", "Pavlidis"], ["Eleni", "Antoniou"]],
     "company_suffixes": ["AE", "EE"]},
    {"country": "Czech Republic",
     "email_domains": ["gmail.com", "seznam.cz", "petworld.cz", "petshop.cz"],
     "names": [["Tomas", "Novak"], ["Klara", "Svobodova"], ["Jan", "Dvorak"], ["Lucie", "Prochazkova"]],
     "company_suffixes": ["s.r.o.", "a.s."]},
    {"country": "Hungary",
     "email_domains": ["gmail.com", "freemail.hu", "petworld.hu", "petshop.hu"],
     "names": [["Gabor", "Nagy"], ["Eszter", "Kovacs"], ["Peter", "Toth"], ["Anna", "Szabo"]],
     "company_suffixes": ["Kft.", "Zrt."]},
    {"country": "Romania",
     "email_domains": ["gmail.com", "yahoo.com", "petworld.ro", "petshop.ro"],
     "names": [["Andrei", "Popescu"], ["Ioana", "Dumitrescu"], ["Mihai", "Stan"], ["Elena", "Ionescu"]],
     "company_suffixes": ["S.R.L.", "S.A."]},
    {"country": "South Africa",
     "email_domains": ["gmail.com", "telkomsa.net", "petworld.co.za", "petshop.co.za"],
     "names": [["Thabo", "Naidoo"], ["Sarah", "Botha"], ["Sipho", "Mthembu"], ["Emma", "VanderMerwe"]],
     "company_suffixes": ["Pty Ltd", "Ltd.", "Inc."]},
    {"country": "Argentina",
     "email_domains": ["gmail.com", "hotmail.com", "petmundo.ar", "petshop.ar"],
     "names": [["Mateo", "Gonzalez"], ["Sofia", "Rodriguez"], ["Tomas", "Fernandez"], ["Valentina", "Lopez"]],
     "company_suffixes": ["S.A.", "S.R.L."]},
    {"country": "Chile",
     "email_domains": ["gmail.com", "hotmail.com", "petmundo.cl", "petshop.cl"],
     "names": [["Matias", "Gonzalez"], ["Isabella", "Munoz"], ["Benjamin", "Rojas"], ["Francisca", "Diaz"]],
     "company_suffixes": ["Ltda.", "S.A."]},
    {"country": "Egypt",
     "email_domains": ["gmail.com", "yahoo.com", "petworld.eg", "petshop.eg"],
     "names": [["Ahmed", "Hassan"], ["Fatma", "Mahmoud"], ["Mohamed", "Ibrahim"], ["Yasmin", "Said"]],
     "company_suffixes": ["LLC", "S.A.E."]},
    {"country": "Israel",
     "email_domains": ["gmail.com", "walla.co.il", "petworld.co.il", "petshop.co.il"],
     "names": [["Noam", "Cohen"], ["Maya", "Levi"], ["Itai", "Mizrahi"], ["Tamar", "Friedman"]],
     "company_suffixes": ["Ltd.", "Inc."]},
    {"country": "Saudi Arabia",
     "email_domains": ["gmail.com", "hotmail.com", "petworld.sa", "petshop.sa"],
     "names": [["Abdullah", "AlSaud"], ["Noura", "AlQahtani"], ["Faisal", "AlHarbi"], ["Reem", "AlOtibi"]],
     "company_suffixes": ["Ltd.", "LLC"]},
    {"country": "Thailand",
     "email_domains": ["gmail.com", "hotmail.co.th", "petworld.co.th", "petshop.co.th"],
     "names": [["Chai", "Suwannapong"], ["Niran", "Phakdee"], ["Ploy", "Charoen"], ["Tanakorn", "Wong"]],
     "company_suffixes": ["Co. Ltd.", "Ltd."]},
    {"country": "Malaysia",
     "email_domains": ["gmail.com", "hotmail.com", "petworld.my", "petshop.my"],
     "names": [["Ahmad", "Rahman"], ["Siti", "Ismail"], ["Wei", "Tan"], ["Nurul", "Abdullah"]],
     "company_suffixes": ["Sdn Bhd", "Sdn. Bhd."]},
    {"country": "Philippines",
     "email_domains": ["gmail.com", "yahoo.com", "petworld.ph", "petshop.ph"],
     "names": [["Juan", "Cruz"], ["Maria", "Santos"], ["Pedro", "Reyes"], ["Ana", "Torres"]],
     "company_suffixes": ["Inc.", "Corp."]},
    {"country": "Colombia",
     "email_domains": ["gmail.com", "hotmail.com", "petmundo.co", "petshop.co"],
     "names": [["Carlos", "Gomez"], ["Valentina", "Restrepo"], ["Andres", "Lopez"], ["Camila", "Moreno"]],
     "company_suffixes": ["S.A.S.", "Ltda."]},
    {"country": "Peru",
     "email_domains": ["gmail.com", "hotmail.com", "petmundo.pe", "petshop.pe"],
     "names": [["Diego", "Quispe"], ["Valeria", "Flores"], ["Joaquin", "Vargas"], ["Mariana", "Rios"]],
     "company_suffixes": ["S.A.C.", "S.R.L."]},
]


# ---------------------------------------------------------------------------
# Inquiry text templates
# ---------------------------------------------------------------------------

INQUIRY_TEMPLATES = [
    "Looking for {product_keyword}, {feature}, MOQ {qty} pcs.",
    "Need {product_keyword} for {pet_type}, {feature}, {size_desc}, order {qty} pcs.",
    "Searching for {product_keyword}, {material_desc}, {size_desc}, MOQ {qty}.",
    "We are looking for {product_keyword} with {feature}, {size_desc}, starting at {qty} pcs.",
    "Interested in {product_keyword}, {feature}, wholesale {qty}+ pcs for {market}.",
    "Want to buy {product_keyword} for {pet_type}, {feature}, {size_desc}, need {qty} pieces.",
    "Require {product_keyword}, {material_desc}, {feature}, MOQ {qty} pcs per shipment.",
    "Looking for {product_keyword} in {seasonal} theme, {feature}, MOQ {qty}.",
    "We need {product_keyword}, {feature}, {size_desc}, bulk order {qty} pcs.",
    "Searching for {product_keyword} for {pet_type}, {material_desc}, {size_desc}, starting at {qty} pcs.",
    "Looking to source {product_keyword}, {feature}, approximately {size_desc}, order quantity {qty} pcs.",
    "Need {product_keyword}, {feature}, for our {market} market, MOQ {qty} pcs.",
    "Interested in wholesale {product_keyword}, {material_desc}, {size_desc}, need {qty}+ units.",
    "Require {product_keyword} for {pet_type}, {feature}, {size_desc}, initial order {qty} pcs.",
    "Want to purchase {product_keyword}, {feature}, {material_desc}, MOQ {qty}.",
    "Looking for {product_keyword}, {feature}, for {seasonal} season, order {qty} pcs.",
    "We want to source {product_keyword}, {feature}, {size_desc}, starting with {qty} pcs trial order.",
    "Need {product_keyword} for our retail chain in {market}, {feature}, {size_desc}, MOQ {qty}.",
    "Searching for {product_keyword}, {material_desc}, {feature}, {size_desc}, order {qty} pcs.",
    "Looking for {product_keyword} suitable for {pet_type}, {feature}, approximate {size_desc}, MOQ {qty} pcs.",
]

PRODUCT_KEYWORDS = [
    "plush squeaky dog toys", "natural rubber dog balls", "cotton rope tug toys",
    "catnip mouse toys", "rubber chew toys", "TPR squeaky toys",
    "plush dog toys", "cat feather wand toys", "nylon dog collars",
    "stainless steel dog bowls", "washable pet beds", "pet carrier bags",
    "silicone grooming gloves", "pet water bottles", "dog cooling bandanas",
    "interactive cat toys", "cat scratching boards", "dog leashes",
    "dog training clickers", "dog poop bag dispensers", "heavy duty rubber chew toys",
    "plush squeaky cat toys", "rope tug toys for dogs", "TPR treat dispenser balls",
    "Christmas plush dog toys", "Halloween dog costumes", "Easter bunny pet toys",
    "valentine pet toys", "reflective dog collars", "orthopedic dog beds",
    "ceramic pet bowls", "slow feeder bowls", "collapsible pet travel bowls",
    "cat tunnel toys", "laser cat toys", "automatic pet feeders",
    "dog seat covers", "pet first aid kits", "retractable dog leashes",
    "dog harnesses", "catnip plush toys", "feather cat wands",
    "rubber bouncy balls", "plush dinosaur dog toys", "cotton rope floss toys",
    "multi-color rope toys", "stainless steel non-slip bowls", "portable pet water bottles",
]

PET_TYPES = ["dogs", "cats", "small dogs", "medium dogs", "large dogs", "puppies", "kittens", "pets"]
MARKETS = ["European", "North American", "Asian", "Middle Eastern", "Australian", "South American", "African"]
SEASONALS = ["Christmas", "Halloween", "Easter", "Valentine", "Summer", "Winter", "Holiday", "New Year"]
SIZE_DESCS = [
    "size around 10cm", "size around 15cm", "size around 20cm", "size around 25cm",
    "size around 30cm", "6-8cm diameter", "40x25cm", "50x40cm",
    "15cm diameter", "80cm length", "One Size", "S/M/L",
    "approx 12cm", "approx 18cm", "45x28x28cm", "small size",
    "medium size", "large size", "2.5cm x 45cm",
]
MATERIAL_DESCS = [
    "durable material", "natural rubber", "plush material", "cotton rope",
    "TPR material", "stainless steel", "nylon material", "silicone material",
    "eco-friendly material", "food grade material", "non-toxic material",
    "washable material", "heavy duty material", "soft material",
]


def generate_inquiry_text():
    template = random.choice(INQUIRY_TEMPLATES)
    return template.format(
        product_keyword=random.choice(PRODUCT_KEYWORDS),
        feature=random.choice(FEATURES).lower(),
        size_desc=random.choice(SIZE_DESCS),
        material_desc=random.choice(MATERIAL_DESCS),
        qty=random.choice([100, 200, 300, 500, 1000, 1500, 2000, 3000, 5000]),
        pet_type=random.choice(PET_TYPES),
        market=random.choice(MARKETS),
        seasonal=random.choice(SEASONALS),
    )


def generate_buyer(ci):
    first, last = random.choice(ci["names"])
    buyer_name = f"{first} {last}"
    domain = random.choice(ci["email_domains"])
    email_prefix = f"{first.lower()}.{last.lower()}"
    buyer_email = f"{email_prefix}@{domain}"

    company_words = ["Pet", "Animal", "Companion", "Paws", "Tails", "Furry", "Happy Pet",
                     "Pet World", "Pet Zone", "Pet Land", "Animal Care", "Pet Solutions",
                     "Pet Pro", "Best Pet", "Pet Plus", "Pet Go", "Pet Mart", "Pet Direct",
                     "Pet Express", "Pet Club", "Pawfect", "Wagging", "Purrfect"]
    company_name = f"{random.choice(company_words)} {last} {random.choice(ci['company_suffixes'])}"

    return buyer_name, buyer_email, company_name


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def generate_all_data():
    suppliers = []
    sid = 1

    for region_name, rd in SUPPLIER_REGIONS.items():
        target = rd["weight"]
        num_companies = max(target // random.randint(3, 8), 5)
        generated = 0

        for ci in range(num_companies):
            if generated >= target:
                break
            sup = generate_supplier(region_name, rd)
            num_products = random.randint(3, 12)
            used_names = set()

            for _ in range(num_products):
                if generated >= target:
                    break
                cat_key = random.choice(list(PRODUCT_CATEGORIES.keys()))
                cat = PRODUCT_CATEGORIES[cat_key]

                attempts = 0
                while attempts < 5:
                    name_tpl = random.choice(cat["names"])
                    pname = fill_name(name_tpl)
                    if pname not in used_names:
                        used_names.add(pname)
                        break
                    attempts += 1
                else:
                    continue

                material = random.choice(cat["materials"])
                dimensions = random.choice(cat["sizes"])
                moq = random.randint(*cat["moq_range"])
                moq = max(100, (moq // 100) * 100)
                low, high = cat["base_price"]
                unit_price = round(random.uniform(low, high) * sup["price_factor"], 2)

                suppliers.append({
                    "product_id": f"SP{sid:05d}",
                    "product_name": pname,
                    "material": material,
                    "dimensions": dimensions,
                    "moq": moq,
                    "unit_price": unit_price,
                    "supplier_name": sup["supplier_name"],
                    "contact_email": sup["contact_email"],
                    "country": sup["country"],
                    "city": sup["city"],
                    "lead_time": sup["lead_time"],
                    "certification": sup["certification"],
                })
                sid += 1
                generated += 1

    # Generate inquiries
    inquiries = []
    iid = 1
    target_inq = 500
    used_emails = set()

    while len(inquiries) < target_inq:
        ci = random.choice(BUYER_COUNTRIES)
        bname, bemail, company = generate_buyer(ci)
        if bemail in used_emails:
            continue
        used_emails.add(bemail)

        inquiries.append({
            "inquiry_id": f"INQ{iid:04d}",
            "buyer_text": generate_inquiry_text(),
            "buyer_name": bname,
            "buyer_email": bemail,
            "company": company,
            "country": ci["country"],
        })
        iid += 1

    return suppliers, inquiries


SUPPLIER_FIELDS = [
    "product_id", "product_name", "material", "dimensions", "moq", "unit_price",
    "supplier_name", "contact_email", "country", "city", "lead_time", "certification",
]
INQUIRY_FIELDS = [
    "inquiry_id", "buyer_text", "buyer_name", "buyer_email", "company", "country",
]


def write_csv(filepath, fields, data):
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
    print(f"[OK] {os.path.basename(filepath)}: {filepath} ({len(data)} rows)")


if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    suppliers, inquiries = generate_all_data()

    print(f"\n=== Data Stats ===")
    print(f"Total products:    {len(suppliers)}")
    print(f"Unique suppliers:  {len(set(s['supplier_name'] for s in suppliers))}")
    print(f"Supplier countries:{len(set(s['country'] for s in suppliers))}")
    print(f"Supplier cities:   {len(set(s['city'] for s in suppliers))}")
    print(f"Total inquiries:   {len(inquiries)}")
    print(f"Buyer countries:   {len(set(i['country'] for i in inquiries))}")
    print()

    write_csv(os.path.join(output_dir, "suppliers_products.csv"), SUPPLIER_FIELDS, suppliers)
    write_csv(os.path.join(output_dir, "inquiries.csv"), INQUIRY_FIELDS, inquiries)
    print("\n[Done] Large-scale mock data generated successfully.")
