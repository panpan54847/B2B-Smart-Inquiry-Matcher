"""
generate_mock_data.py
=====================
生成模拟数据集（Mock Data），用于 B2B 智能询盘匹配系统。

输出两个 CSV 文件：
  1. suppliers_products.csv — 本地供应商产品库（40 条宠物玩具/外贸商品数据）
  2. inquiries.csv          — 买家询盘样本（15 条英文询盘文本）

运行方式：
    python data/generate_mock_data.py
"""

import csv
import os
import random

# ---------------------------------------------------------------------------
# 供应商产品库数据
# ---------------------------------------------------------------------------
# 每条记录：product_id, product_name, material, dimensions, moq, unit_price
# 涵盖：毛绒玩具、橡胶玩具、绳结玩具、猫玩具、宠物用品等外贸常见品类
# ---------------------------------------------------------------------------

SUPPLIER_PRODUCTS = [
    # --- 毛绒发声玩具 ---
    {"product_id": "SP001", "product_name": "Plush Squeaky Dog Toy - Bone Shape", "material": "Plush + PP Cotton", "dimensions": "20cm", "moq": 500, "unit_price": 1.20},
    {"product_id": "SP002", "product_name": "Plush Squeaky Dog Toy - Ball Shape", "material": "Plush + PP Cotton", "dimensions": "15cm", "moq": 300, "unit_price": 0.95},
    {"product_id": "SP003", "product_name": "Soft Plush Dog Toy - Duck Design", "material": "Plush + Squeaker", "dimensions": "25cm", "moq": 500, "unit_price": 1.50},
    {"product_id": "SP004", "product_name": "Cute Plush Cat Toy - Mouse Shape", "material": "Plush + Catnip", "dimensions": "10cm", "moq": 1000, "unit_price": 0.55},
    {"product_id": "SP005", "product_name": "Plush Squeaker Toy - Elephant Shape", "material": "Plush + PP Cotton", "dimensions": "30cm", "moq": 500, "unit_price": 1.80},
    {"product_id": "SP006", "product_name": "Durable Plush Dog Toy - Rope Leg", "material": "Plush + Cotton Rope", "dimensions": "35cm", "moq": 500, "unit_price": 2.10},
    {"product_id": "SP007", "product_name": "Soft Squeaky Plush Toy - Pig Shape", "material": "Plush + Squeaker", "dimensions": "20cm", "moq": 500, "unit_price": 1.25},
    {"product_id": "SP008", "product_name": "Plush Dog Chew Toy - Dinosaur", "material": "Plush + PP Cotton", "dimensions": "28cm", "moq": 300, "unit_price": 1.65},

    # --- 橡胶/TPR 玩具 ---
    {"product_id": "SP009", "product_name": "Natural Rubber Dog Ball - Bouncy", "material": "Natural Rubber", "dimensions": "6.5cm", "moq": 1000, "unit_price": 0.80},
    {"product_id": "SP010", "product_name": "TPR Squeaky Dog Toy - Star Shape", "material": "TPR (Thermoplastic Rubber)", "dimensions": "12cm", "moq": 500, "unit_price": 1.10},
    {"product_id": "SP011", "product_name": "Rubber Dog Chew Toy - Bone Shape", "material": "Natural Rubber", "dimensions": "18cm", "moq": 500, "unit_price": 1.35},
    {"product_id": "SP012", "product_name": "Durable Rubber Ball for Large Dogs", "material": "Natural Rubber", "dimensions": "8cm", "moq": 500, "unit_price": 1.50},
    {"product_id": "SP013", "product_name": "TPR Dog Toy - Dispenser Treat Ball", "material": "TPR", "dimensions": "7cm", "moq": 1000, "unit_price": 1.05},
    {"product_id": "SP014", "product_name": "Rubber Squeaky Toy - Hedgehog Shape", "material": "Natural Rubber + Squeaker", "dimensions": "14cm", "moq": 500, "unit_price": 1.20},
    {"product_id": "SP015", "product_name": "Heavy Duty Rubber Chew Toy - Ring", "material": "Natural Rubber", "dimensions": "16cm", "moq": 300, "unit_price": 1.75},

    # --- 绳结玩具 ---
    {"product_id": "SP016", "product_name": "Cotton Rope Dog Toy - Tug Knot", "material": "Cotton Rope", "dimensions": "30cm", "moq": 500, "unit_price": 1.00},
    {"product_id": "SP017", "product_name": "Durable Rope Toy - Three Knot", "material": "Cotton Rope", "dimensions": "50cm", "moq": 300, "unit_price": 1.85},
    {"product_id": "SP018", "product_name": "Rope Tug Toy for Dogs - Bone Shape", "material": "Cotton + Polyester Rope", "dimensions": "25cm", "moq": 500, "unit_price": 1.15},
    {"product_id": "SP019", "product_name": "Multi-Color Rope Dog Toy - Floss", "material": "Cotton Rope", "dimensions": "20cm", "moq": 1000, "unit_price": 0.70},
    {"product_id": "SP020", "product_name": "Thick Rope Tug Toy for Large Dogs", "material": "Heavy Duty Cotton Rope", "dimensions": "60cm", "moq": 200, "unit_price": 2.50},

    # --- 猫玩具 ---
    {"product_id": "SP021", "product_name": "Catnip Mouse Toy - Plush with Bell", "material": "Plush + Catnip + Bell", "dimensions": "8cm", "moq": 1000, "unit_price": 0.45},
    {"product_id": "SP022", "product_name": "Interactive Cat Feather Wand Toy", "material": "Feather + Plastic Stick", "dimensions": "80cm", "moq": 500, "unit_price": 0.90},
    {"product_id": "SP023", "product_name": "Cat Tunnel Toy - Crinkle Collapsible", "material": "Polyester + Crinkle Paper", "dimensions": "35x35x80cm", "moq": 300, "unit_price": 3.20},
    {"product_id": "SP024", "product_name": "Cat Ball Toy with Bell Inside", "material": "Plastic + Bell", "dimensions": "4cm", "moq": 2000, "unit_price": 0.25},
    {"product_id": "SP025", "product_name": "Cat Scratching Board - Cardboard", "material": "Corrugated Cardboard", "dimensions": "40x25cm", "moq": 300, "unit_price": 2.80},
    {"product_id": "SP026", "product_name": "Laser Cat Toy - Interactive Pointer", "material": "Aluminum + LED", "dimensions": "10cm", "moq": 500, "unit_price": 1.95},

    # --- 宠物配件/其他 ---
    {"product_id": "SP027", "product_name": "Pet Dog Collar - Nylon Adjustable", "material": "Nylon Webbing + Metal Buckle", "dimensions": "2.5cm x 45cm", "moq": 500, "unit_price": 1.30},
    {"product_id": "SP028", "product_name": "Dog Leash - Nylon Reflective", "material": "Nylon + Metal Hook", "dimensions": "1.5cm x 120cm", "moq": 500, "unit_price": 1.60},
    {"product_id": "SP029", "product_name": "Pet Dog Bed - Washable Soft Cushion", "material": "Fleece + PP Cotton", "dimensions": "50x40cm", "moq": 200, "unit_price": 4.50},
    {"product_id": "SP030", "product_name": "Dog Bowl - Stainless Steel Non-Slip", "material": "Stainless Steel", "dimensions": "15cm diameter", "moq": 500, "unit_price": 1.75},
    {"product_id": "SP031", "product_name": "Pet Carrier Bag - Portable Travel", "material": "Oxford Cloth + Mesh", "dimensions": "45x28x28cm", "moq": 200, "unit_price": 5.80},
    {"product_id": "SP032", "product_name": "Dog Poop Bag Dispenser with Leash Clip", "material": "ABS Plastic", "dimensions": "8x5cm", "moq": 2000, "unit_price": 0.35},
    {"product_id": "SP033", "product_name": "Pet Grooming Glove - Silicone Brush", "material": "Silicone + Mesh", "dimensions": "One Size", "moq": 500, "unit_price": 1.20},
    {"product_id": "SP034", "product_name": "Dog Clicker Training Tool", "material": "ABS Plastic + Metal", "dimensions": "6x4cm", "moq": 1000, "unit_price": 0.30},
    {"product_id": "SP035", "product_name": "Pet Water Bottle - Portable Travel", "material": "PP Plastic + Silicone", "dimensions": "500ml", "moq": 500, "unit_price": 1.85},
    {"product_id": "SP036", "product_name": "Dog Cooling Bandana - Summer", "material": "Cooling Fabric + PVA", "dimensions": "50x5cm", "moq": 500, "unit_price": 1.40},

    # --- 季节性 / 节日主题 ---
    {"product_id": "SP037", "product_name": "Christmas Plush Dog Toy - Santa Claus", "material": "Plush + Squeaker", "dimensions": "25cm", "moq": 500, "unit_price": 1.70},
    {"product_id": "SP038", "product_name": "Halloween Dog Costume - Pumpkin", "material": "Polyester + Cotton", "dimensions": "M/L/XL", "moq": 300, "unit_price": 2.30},
    {"product_id": "SP039", "product_name": "Easter Plush Bunny Dog Toy - Squeaky", "material": "Plush + PP Cotton", "dimensions": "22cm", "moq": 500, "unit_price": 1.55},
    {"product_id": "SP040", "product_name": "Valentine Plush Dog Toy - Heart Shape", "material": "Plush + Squeaker", "dimensions": "18cm", "moq": 500, "unit_price": 1.45},
]

# ---------------------------------------------------------------------------
# 买家询盘样本数据
# ---------------------------------------------------------------------------

INQUIRIES = [
    {"inquiry_id": "INQ001", "buyer_text": "Looking for plush squeaky dog toys, size around 20cm, durable material, MOQ 500 pcs."},
    {"inquiry_id": "INQ002", "buyer_text": "Need natural rubber dog balls, bouncy and chew resistant, diameter 6-8cm, bulk order 1000 pcs."},
    {"inquiry_id": "INQ003", "buyer_text": "Searching for cotton rope tug toys for medium dogs, approximately 30-50cm, MOQ 500."},
    {"inquiry_id": "INQ004", "buyer_text": "Interested in catnip mouse toys with bell, small size, wholesale 1000+ pcs."},
    {"inquiry_id": "INQ005", "buyer_text": "We need durable rubber chew toys for large breed dogs, heavy duty, MOQ 300 pcs."},
    {"inquiry_id": "INQ006", "buyer_text": "Looking for interactive cat feather wand toys, 80cm length, need 500 pieces."},
    {"inquiry_id": "INQ007", "buyer_text": "Want to buy plush dog toys in Christmas theme, Santa Claus design, MOQ 500."},
    {"inquiry_id": "INQ008", "buyer_text": "Need TPR squeaky dog toys, star shape, around 12cm, order quantity 500 pcs."},
    {"inquiry_id": "INQ009", "buyer_text": "Looking for nylon dog collars adjustable, reflective preferred, 500 pcs trial order."},
    {"inquiry_id": "INQ010", "buyer_text": "We want washable pet dog beds, soft cushion, 50x40cm, starting at 200 pcs."},
    {"inquiry_id": "INQ011", "buyer_text": "Searching for cat scratching boards made of cardboard, 40x25cm, MOQ 300."},
    {"inquiry_id": "INQ012", "buyer_text": "Need stainless steel dog bowls, non-slip bottom, 15cm, 500 pcs per shipment."},
    {"inquiry_id": "INQ013", "buyer_text": "Looking for silicone pet grooming gloves, one size, order 500 pairs."},
    {"inquiry_id": "INQ014", "buyer_text": "Want portable pet water bottles for travel, 500ml capacity, need 500 units."},
    {"inquiry_id": "INQ015", "buyer_text": "Searching for plush squeaky elephant dog toy, 30cm, soft material, MOQ 500 pcs."},
]


# ---------------------------------------------------------------------------
# 写入 CSV 文件
# ---------------------------------------------------------------------------

def write_suppliers_csv(filepath):
    """将供应商产品数据写入 CSV 文件。"""
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["product_id", "product_name", "material", "dimensions", "moq", "unit_price"])
        writer.writeheader()
        writer.writerows(SUPPLIER_PRODUCTS)
    print(f"[OK] 已生成供应商产品库: {filepath} ({len(SUPPLIER_PRODUCTS)} 条记录)")


def write_inquiries_csv(filepath):
    """将买家询盘数据写入 CSV 文件。"""
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["inquiry_id", "buyer_text"])
        writer.writeheader()
        writer.writerows(INQUIRIES)
    print(f"[OK] 已生成买家询盘样本: {filepath} ({len(INQUIRIES)} 条记录)")


if __name__ == "__main__":
    # 输出目录（与脚本同级）
    output_dir = os.path.dirname(os.path.abspath(__file__))
    write_suppliers_csv(os.path.join(output_dir, "suppliers_products.csv"))
    write_inquiries_csv(os.path.join(output_dir, "inquiries.csv"))
    print("\n[完成] 模拟数据集已生成完毕，可直接用于匹配算法测试。")
