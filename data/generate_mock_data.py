"""
generate_mock_data.py
=====================
生成高仿真模拟数据集，用于 B2B 智能询盘匹配系统。

数据基于真实外贸 B2B 场景设计，包含：
  - 供应商公司名、联系邮箱、所在城市、认证资质、交期等
  - 买家公司名、联系邮箱、国家、采购意向等

输出两个 CSV 文件：
  1. suppliers_products.csv — 本地供应商产品库（40 条）
  2. inquiries.csv          — 买家询盘样本（15 条）

运行方式：
    python data/generate_mock_data.py
"""

import csv
import os

# ---------------------------------------------------------------------------
# 供应商产品库数据
# ---------------------------------------------------------------------------
# 每条记录包含完整的供应商+产品信息，模拟 Alibaba/GlobalSources 真实外贸数据
# ---------------------------------------------------------------------------

SUPPLIER_PRODUCTS = [
    # === 毛绒发声玩具 ===
    {"product_id": "SP001", "product_name": "Plush Squeaky Dog Toy - Bone Shape", "material": "Plush + PP Cotton", "dimensions": "20cm", "moq": 500, "unit_price": 1.20, "supplier_name": "Yiwu Mayer Pet Products Co., Ltd.", "contact_email": "sales@mayerpet.com", "country": "China", "city": "Yiwu", "lead_time": "15 days", "certification": "BSCI, CE"},
    {"product_id": "SP002", "product_name": "Plush Squeaky Dog Toy - Ball Shape", "material": "Plush + PP Cotton", "dimensions": "15cm", "moq": 300, "unit_price": 0.95, "supplier_name": "Yangzhou Lucky Pet Toy Factory", "contact_email": "lucky.pettoy@yzlucky.cn", "country": "China", "city": "Yangzhou", "lead_time": "12 days", "certification": "ISO 9001"},
    {"product_id": "SP003", "product_name": "Soft Plush Dog Toy - Duck Design", "material": "Plush + Squeaker", "dimensions": "25cm", "moq": 500, "unit_price": 1.50, "supplier_name": "Dongguan Harmony Toys Mfg. Ltd.", "contact_email": "info@harmonytoys.cn", "country": "China", "city": "Dongguan", "lead_time": "18 days", "certification": "ICTI, BSCI"},
    {"product_id": "SP004", "product_name": "Cute Plush Cat Toy - Mouse Shape", "material": "Plush + Catnip", "dimensions": "10cm", "moq": 1000, "unit_price": 0.55, "supplier_name": "Qingdao Pawsome Pet Supplies Co.", "contact_email": "export@pawsomepet.cn", "country": "China", "city": "Qingdao", "lead_time": "10 days", "certification": "CE, RoHS"},
    {"product_id": "SP005", "product_name": "Plush Squeaker Toy - Elephant Shape", "material": "Plush + PP Cotton", "dimensions": "30cm", "moq": 500, "unit_price": 1.80, "supplier_name": "Yiwu Mayer Pet Products Co., Ltd.", "contact_email": "sales@mayerpet.com", "country": "China", "city": "Yiwu", "lead_time": "15 days", "certification": "BSCI, CE"},
    {"product_id": "SP006", "product_name": "Durable Plush Dog Toy - Rope Leg", "material": "Plush + Cotton Rope", "dimensions": "35cm", "moq": 500, "unit_price": 2.10, "supplier_name": "Cangnan Greenleaf Textile Ltd.", "contact_email": "greenleaf@cntextile.cn", "country": "China", "city": "Wenzhou", "lead_time": "20 days", "certification": "OEKO-TEX"},
    {"product_id": "SP007", "product_name": "Soft Squeaky Plush Toy - Pig Shape", "material": "Plush + Squeaker", "dimensions": "20cm", "moq": 500, "unit_price": 1.25, "supplier_name": "Dongguan Harmony Toys Mfg. Ltd.", "contact_email": "info@harmonytoys.cn", "country": "China", "city": "Dongguan", "lead_time": "18 days", "certification": "ICTI, BSCI"},
    {"product_id": "SP008", "product_name": "Plush Dog Chew Toy - Dinosaur", "material": "Plush + PP Cotton", "dimensions": "28cm", "moq": 300, "unit_price": 1.65, "supplier_name": "Yangzhou Lucky Pet Toy Factory", "contact_email": "lucky.pettoy@yzlucky.cn", "country": "China", "city": "Yangzhou", "lead_time": "12 days", "certification": "ISO 9001"},

    # === 橡胶/TPR 玩具 ===
    {"product_id": "SP009", "product_name": "Natural Rubber Dog Ball - Bouncy", "material": "Natural Rubber", "dimensions": "6.5cm", "moq": 1000, "unit_price": 0.80, "supplier_name": "Ningbo Champion Rubber Tech Ltd.", "contact_email": "champion.rubber@nbchampion.cn", "country": "China", "city": "Ningbo", "lead_time": "14 days", "certification": "SGS, FDA"},
    {"product_id": "SP010", "product_name": "TPR Squeaky Dog Toy - Star Shape", "material": "TPR (Thermoplastic Rubber)", "dimensions": "12cm", "moq": 500, "unit_price": 1.10, "supplier_name": "Shenzhen Petstar Industrial Co.", "contact_email": "petstar@szpetstar.cn", "country": "China", "city": "Shenzhen", "lead_time": "10 days", "certification": "RoHS, REACH"},
    {"product_id": "SP011", "product_name": "Rubber Dog Chew Toy - Bone Shape", "material": "Natural Rubber", "dimensions": "18cm", "moq": 500, "unit_price": 1.35, "supplier_name": "Ningbo Champion Rubber Tech Ltd.", "contact_email": "champion.rubber@nbchampion.cn", "country": "China", "city": "Ningbo", "lead_time": "14 days", "certification": "SGS, FDA"},
    {"product_id": "SP012", "product_name": "Durable Rubber Ball for Large Dogs", "material": "Natural Rubber", "dimensions": "8cm", "moq": 500, "unit_price": 1.50, "supplier_name": "Ningbo Champion Rubber Tech Ltd.", "contact_email": "champion.rubber@nbchampion.cn", "country": "China", "city": "Ningbo", "lead_time": "14 days", "certification": "SGS, FDA"},
    {"product_id": "SP013", "product_name": "TPR Dog Toy - Dispenser Treat Ball", "material": "TPR", "dimensions": "7cm", "moq": 1000, "unit_price": 1.05, "supplier_name": "Shenzhen Petstar Industrial Co.", "contact_email": "petstar@szpetstar.cn", "country": "China", "city": "Shenzhen", "lead_time": "10 days", "certification": "RoHS, REACH"},
    {"product_id": "SP014", "product_name": "Rubber Squeaky Toy - Hedgehog Shape", "material": "Natural Rubber + Squeaker", "dimensions": "14cm", "moq": 500, "unit_price": 1.20, "supplier_name": "Shenzhen Petstar Industrial Co.", "contact_email": "petstar@szpetstar.cn", "country": "China", "city": "Shenzhen", "lead_time": "10 days", "certification": "RoHS, REACH"},
    {"product_id": "SP015", "product_name": "Heavy Duty Rubber Chew Toy - Ring", "material": "Natural Rubber", "dimensions": "16cm", "moq": 300, "unit_price": 1.75, "supplier_name": "Ningbo Champion Rubber Tech Ltd.", "contact_email": "champion.rubber@nbchampion.cn", "country": "China", "city": "Ningbo", "lead_time": "14 days", "certification": "SGS, FDA"},

    # === 绳结玩具 ===
    {"product_id": "SP016", "product_name": "Cotton Rope Dog Toy - Tug Knot", "material": "Cotton Rope", "dimensions": "30cm", "moq": 500, "unit_price": 1.00, "supplier_name": "Cangnan Greenleaf Textile Ltd.", "contact_email": "greenleaf@cntextile.cn", "country": "China", "city": "Wenzhou", "lead_time": "20 days", "certification": "OEKO-TEX"},
    {"product_id": "SP017", "product_name": "Durable Rope Toy - Three Knot", "material": "Cotton Rope", "dimensions": "50cm", "moq": 300, "unit_price": 1.85, "supplier_name": "Cangnan Greenleaf Textile Ltd.", "contact_email": "greenleaf@cntextile.cn", "country": "China", "city": "Wenzhou", "lead_time": "20 days", "certification": "OEKO-TEX"},
    {"product_id": "SP018", "product_name": "Rope Tug Toy for Dogs - Bone Shape", "material": "Cotton + Polyester Rope", "dimensions": "25cm", "moq": 500, "unit_price": 1.15, "supplier_name": "Yangzhou Lucky Pet Toy Factory", "contact_email": "lucky.pettoy@yzlucky.cn", "country": "China", "city": "Yangzhou", "lead_time": "12 days", "certification": "ISO 9001"},
    {"product_id": "SP019", "product_name": "Multi-Color Rope Dog Toy - Floss", "material": "Cotton Rope", "dimensions": "20cm", "moq": 1000, "unit_price": 0.70, "supplier_name": "Cangnan Greenleaf Textile Ltd.", "contact_email": "greenleaf@cntextile.cn", "country": "China", "city": "Wenzhou", "lead_time": "20 days", "certification": "OEKO-TEX"},
    {"product_id": "SP020", "product_name": "Thick Rope Tug Toy for Large Dogs", "material": "Heavy Duty Cotton Rope", "dimensions": "60cm", "moq": 200, "unit_price": 2.50, "supplier_name": "Cangnan Greenleaf Textile Ltd.", "contact_email": "greenleaf@cntextile.cn", "country": "China", "city": "Wenzhou", "lead_time": "20 days", "certification": "OEKO-TEX"},

    # === 猫玩具 ===
    {"product_id": "SP021", "product_name": "Catnip Mouse Toy - Plush with Bell", "material": "Plush + Catnip + Bell", "dimensions": "8cm", "moq": 1000, "unit_price": 0.45, "supplier_name": "Qingdao Pawsome Pet Supplies Co.", "contact_email": "export@pawsomepet.cn", "country": "China", "city": "Qingdao", "lead_time": "10 days", "certification": "CE, RoHS"},
    {"product_id": "SP022", "product_name": "Interactive Cat Feather Wand Toy", "material": "Feather + Plastic Stick", "dimensions": "80cm", "moq": 500, "unit_price": 0.90, "supplier_name": "Qingdao Pawsome Pet Supplies Co.", "contact_email": "export@pawsomepet.cn", "country": "China", "city": "Qingdao", "lead_time": "10 days", "certification": "CE, RoHS"},
    {"product_id": "SP023", "product_name": "Cat Tunnel Toy - Crinkle Collapsible", "material": "Polyester + Crinkle Paper", "dimensions": "35x35x80cm", "moq": 300, "unit_price": 3.20, "supplier_name": "Hangzhou Furwell Home Co.", "contact_email": "furwell@hzfurwell.cn", "country": "China", "city": "Hangzhou", "lead_time": "25 days", "certification": "BSCI"},
    {"product_id": "SP024", "product_name": "Cat Ball Toy with Bell Inside", "material": "Plastic + Bell", "dimensions": "4cm", "moq": 2000, "unit_price": 0.25, "supplier_name": "Qingdao Pawsome Pet Supplies Co.", "contact_email": "export@pawsomepet.cn", "country": "China", "city": "Qingdao", "lead_time": "10 days", "certification": "CE, RoHS"},
    {"product_id": "SP025", "product_name": "Cat Scratching Board - Cardboard", "material": "Corrugated Cardboard", "dimensions": "40x25cm", "moq": 300, "unit_price": 2.80, "supplier_name": "Hangzhou Furwell Home Co.", "contact_email": "furwell@hzfurwell.cn", "country": "China", "city": "Hangzhou", "lead_time": "25 days", "certification": "BSCI"},
    {"product_id": "SP026", "product_name": "Laser Cat Toy - Interactive Pointer", "material": "Aluminum + LED", "dimensions": "10cm", "moq": 500, "unit_price": 1.95, "supplier_name": "Shenzhen Petstar Industrial Co.", "contact_email": "petstar@szpetstar.cn", "country": "China", "city": "Shenzhen", "lead_time": "10 days", "certification": "RoHS, REACH"},

    # === 宠物配件 ===
    {"product_id": "SP027", "product_name": "Pet Dog Collar - Nylon Adjustable", "material": "Nylon Webbing + Metal Buckle", "dimensions": "2.5cm x 45cm", "moq": 500, "unit_price": 1.30, "supplier_name": "Wuxi Tack & Gear Manufacturing Ltd.", "contact_email": "tackgear@wuxitg.cn", "country": "China", "city": "Wuxi", "lead_time": "15 days", "certification": "SGS"},
    {"product_id": "SP028", "product_name": "Dog Leash - Nylon Reflective", "material": "Nylon + Metal Hook", "dimensions": "1.5cm x 120cm", "moq": 500, "unit_price": 1.60, "supplier_name": "Wuxi Tack & Gear Manufacturing Ltd.", "contact_email": "tackgear@wuxitg.cn", "country": "China", "city": "Wuxi", "lead_time": "15 days", "certification": "SGS"},
    {"product_id": "SP029", "product_name": "Pet Dog Bed - Washable Soft Cushion", "material": "Fleece + PP Cotton", "dimensions": "50x40cm", "moq": 200, "unit_price": 4.50, "supplier_name": "Hangzhou Furwell Home Co.", "contact_email": "furwell@hzfurwell.cn", "country": "China", "city": "Hangzhou", "lead_time": "25 days", "certification": "BSCI"},
    {"product_id": "SP030", "product_name": "Dog Bowl - Stainless Steel Non-Slip", "material": "Stainless Steel", "dimensions": "15cm diameter", "moq": 500, "unit_price": 1.75, "supplier_name": "Guangzhou HomeWell Kitchenware Ltd.", "contact_email": "homewell@gzhomewell.cn", "country": "China", "city": "Guangzhou", "lead_time": "20 days", "certification": "FDA, LFGB"},
    {"product_id": "SP031", "product_name": "Pet Carrier Bag - Portable Travel", "material": "Oxford Cloth + Mesh", "dimensions": "45x28x28cm", "moq": 200, "unit_price": 5.80, "supplier_name": "Xiamen CargoPet Bags Co.", "contact_email": "cargopet@xmcb.cn", "country": "China", "city": "Xiamen", "lead_time": "22 days", "certification": "BSCI, REACH"},
    {"product_id": "SP032", "product_name": "Dog Poop Bag Dispenser with Leash Clip", "material": "ABS Plastic", "dimensions": "8x5cm", "moq": 2000, "unit_price": 0.35, "supplier_name": "Shenzhen Petstar Industrial Co.", "contact_email": "petstar@szpetstar.cn", "country": "China", "city": "Shenzhen", "lead_time": "10 days", "certification": "RoHS, REACH"},
    {"product_id": "SP033", "product_name": "Pet Grooming Glove - Silicone Brush", "material": "Silicone + Mesh", "dimensions": "One Size", "moq": 500, "unit_price": 1.20, "supplier_name": "Guangzhou HomeWell Kitchenware Ltd.", "contact_email": "homewell@gzhomewell.cn", "country": "China", "city": "Guangzhou", "lead_time": "20 days", "certification": "FDA, LFGB"},
    {"product_id": "SP034", "product_name": "Dog Clicker Training Tool", "material": "ABS Plastic + Metal", "dimensions": "6x4cm", "moq": 1000, "unit_price": 0.30, "supplier_name": "Shenzhen Petstar Industrial Co.", "contact_email": "petstar@szpetstar.cn", "country": "China", "city": "Shenzhen", "lead_time": "10 days", "certification": "RoHS, REACH"},
    {"product_id": "SP035", "product_name": "Pet Water Bottle - Portable Travel", "material": "PP Plastic + Silicone", "dimensions": "500ml", "moq": 500, "unit_price": 1.85, "supplier_name": "Guangzhou HomeWell Kitchenware Ltd.", "contact_email": "homewell@gzhomewell.cn", "country": "China", "city": "Guangzhou", "lead_time": "20 days", "certification": "FDA, LFGB"},
    {"product_id": "SP036", "product_name": "Dog Cooling Bandana - Summer", "material": "Cooling Fabric + PVA", "dimensions": "50x5cm", "moq": 500, "unit_price": 1.40, "supplier_name": "Wuxi Tack & Gear Manufacturing Ltd.", "contact_email": "tackgear@wuxitg.cn", "country": "China", "city": "Wuxi", "lead_time": "15 days", "certification": "SGS"},

    # === 季节性/节日主题 ===
    {"product_id": "SP037", "product_name": "Christmas Plush Dog Toy - Santa Claus", "material": "Plush + Squeaker", "dimensions": "25cm", "moq": 500, "unit_price": 1.70, "supplier_name": "Yiwu Mayer Pet Products Co., Ltd.", "contact_email": "sales@mayerpet.com", "country": "China", "city": "Yiwu", "lead_time": "15 days", "certification": "BSCI, CE"},
    {"product_id": "SP038", "product_name": "Halloween Dog Costume - Pumpkin", "material": "Polyester + Cotton", "dimensions": "M/L/XL", "moq": 300, "unit_price": 2.30, "supplier_name": "Dongguan Harmony Toys Mfg. Ltd.", "contact_email": "info@harmonytoys.cn", "country": "China", "city": "Dongguan", "lead_time": "18 days", "certification": "ICTI, BSCI"},
    {"product_id": "SP039", "product_name": "Easter Plush Bunny Dog Toy - Squeaky", "material": "Plush + PP Cotton", "dimensions": "22cm", "moq": 500, "unit_price": 1.55, "supplier_name": "Yangzhou Lucky Pet Toy Factory", "contact_email": "lucky.pettoy@yzlucky.cn", "country": "China", "city": "Yangzhou", "lead_time": "12 days", "certification": "ISO 9001"},
    {"product_id": "SP040", "product_name": "Valentine Plush Dog Toy - Heart Shape", "material": "Plush + Squeaker", "dimensions": "18cm", "moq": 500, "unit_price": 1.45, "supplier_name": "Yiwu Mayer Pet Products Co., Ltd.", "contact_email": "sales@mayerpet.com", "country": "China", "city": "Yiwu", "lead_time": "15 days", "certification": "BSCI, CE"},
]

# ---------------------------------------------------------------------------
# 买家询盘样本数据
# ---------------------------------------------------------------------------
# 每条记录包含完整的买家信息 + 询盘文本，模拟真实 RFQ（Request for Quote）
# ---------------------------------------------------------------------------

INQUIRIES = [
    {"inquiry_id": "INQ001", "buyer_text": "Looking for plush squeaky dog toys, size around 20cm, durable material, MOQ 500 pcs.", "buyer_name": "Sarah Mitchell", "buyer_email": "sarah.mitchell@petlandia.co.uk", "company": "Petlandia UK Ltd.", "country": "United Kingdom"},
    {"inquiry_id": "INQ002", "buyer_text": "Need natural rubber dog balls, bouncy and chew resistant, diameter 6-8cm, bulk order 1000 pcs.", "buyer_name": "Marcus Weber", "buyer_email": "m.weber@haustierde.de", "company": "Haustier & Co. GmbH", "country": "Germany"},
    {"inquiry_id": "INQ003", "buyer_text": "Searching for cotton rope tug toys for medium dogs, approximately 30-50cm, MOQ 500.", "buyer_name": "Emily Chen", "buyer_email": "emily.chen@petprosperity.com.au", "company": "Pet Prosperity Pty Ltd.", "country": "Australia"},
    {"inquiry_id": "INQ004", "buyer_text": "Interested in catnip mouse toys with bell, small size, wholesale 1000+ pcs.", "buyer_name": "Hiroshi Tanaka", "buyer_email": "h.tanaka@petlife.jp", "company": "PetLife Japan K.K.", "country": "Japan"},
    {"inquiry_id": "INQ005", "buyer_text": "We need durable rubber chew toys for large breed dogs, heavy duty, MOQ 300 pcs.", "buyer_name": "James O'Connor", "buyer_email": "james.oconnor@barkbox.ca", "company": "BarkBox Canada Inc.", "country": "Canada"},
    {"inquiry_id": "INQ006", "buyer_text": "Looking for interactive cat feather wand toys, 80cm length, need 500 pieces.", "buyer_name": "Sophie Dubois", "buyer_email": "s.dubois@animallie.fr", "company": "AnimalLie SARL", "country": "France"},
    {"inquiry_id": "INQ007", "buyer_text": "Want to buy plush dog toys in Christmas theme, Santa Claus design, MOQ 500.", "buyer_name": "Michael Rodriguez", "buyer_email": "mrodriguez@holidaypetsusa.com", "company": "Holiday Pets USA LLC", "country": "United States"},
    {"inquiry_id": "INQ008", "buyer_text": "Need TPR squeaky dog toys, star shape, around 12cm, order quantity 500 pcs.", "buyer_name": "Anna Kowalski", "buyer_email": "a.kowalski@zwierzopol.pl", "company": "Zwierzopol Sp. z o.o.", "country": "Poland"},
    {"inquiry_id": "INQ009", "buyer_text": "Looking for nylon dog collars adjustable, reflective preferred, 500 pcs trial order.", "buyer_name": "David Kim", "buyer_email": "d.kim@koreapetlink.kr", "company": "Korea PetLink Co., Ltd.", "country": "South Korea"},
    {"inquiry_id": "INQ010", "buyer_text": "We want washable pet dog beds, soft cushion, 50x40cm, starting at 200 pcs.", "buyer_name": "Laura Fernandez", "buyer_email": "l.fernandez@petconfort.es", "company": "PetConfort S.L.", "country": "Spain"},
    {"inquiry_id": "INQ011", "buyer_text": "Searching for cat scratching boards made of cardboard, 40x25cm, MOQ 300.", "buyer_name": "Alessandro Rossi", "buyer_email": "a.rossi@amicicani.it", "company": "AmiciCani S.r.l.", "country": "Italy"},
    {"inquiry_id": "INQ012", "buyer_text": "Need stainless steel dog bowls, non-slip bottom, 15cm, 500 pcs per shipment.", "buyer_name": "Priya Sharma", "buyer_email": "priya.sharma@petneeds.in", "company": "PetNeeds India Pvt Ltd", "country": "India"},
    {"inquiry_id": "INQ013", "buyer_text": "Looking for silicone pet grooming gloves, one size, order 500 pairs.", "buyer_name": "Lucas Oliveira", "buyer_email": "l.oliveira@petbrasil.com.br", "company": "PetBrasil Comercio Ltda", "country": "Brazil"},
    {"inquiry_id": "INQ014", "buyer_text": "Want portable pet water bottles for travel, 500ml capacity, need 500 units.", "buyer_name": "Chloe Anderson", "buyer_email": "c.anderson@petgo.co.nz", "company": "PetGo NZ Limited", "country": "New Zealand"},
    {"inquiry_id": "INQ015", "buyer_text": "Searching for plush squeaky elephant dog toy, 30cm, soft material, MOQ 500 pcs.", "buyer_name": "Henrik Nilsson", "buyer_email": "h.nilsson@svenskapet.se", "company": "Svenska Pet AB", "country": "Sweden"},
]


# ---------------------------------------------------------------------------
# 写入 CSV 文件
# ---------------------------------------------------------------------------

SUPPLIER_FIELDS = [
    "product_id", "product_name", "material", "dimensions", "moq", "unit_price",
    "supplier_name", "contact_email", "country", "city", "lead_time", "certification",
]

INQUIRY_FIELDS = [
    "inquiry_id", "buyer_text", "buyer_name", "buyer_email", "company", "country",
]


def write_suppliers_csv(filepath):
    """将供应商产品数据写入 CSV 文件。"""
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SUPPLIER_FIELDS)
        writer.writeheader()
        writer.writerows(SUPPLIER_PRODUCTS)
    print(f"[OK] suppliers_products.csv: {filepath} ({len(SUPPLIER_PRODUCTS)} rows)")


def write_inquiries_csv(filepath):
    """将买家询盘数据写入 CSV 文件。"""
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=INQUIRY_FIELDS)
        writer.writeheader()
        writer.writerows(INQUIRIES)
    print(f"[OK] inquiries.csv: {filepath} ({len(INQUIRIES)} rows)")


if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    write_suppliers_csv(os.path.join(output_dir, "suppliers_products.csv"))
    write_inquiries_csv(os.path.join(output_dir, "inquiries.csv"))
    print("\n[Done] Mock data generated successfully.")
