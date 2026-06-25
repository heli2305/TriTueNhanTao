#Bai toan to mau ban do TP.HCM

SEEDS = {
    "12": (600, 200),
    "Go Vap": (600, 320),
    "Thu Duc": (950, 280),
    "9": (1250, 400),
    "2": (950, 550),
    "Binh Thanh": (800, 480),
    "Phu Nhuan": (680, 480),
    "Tan Binh": (560, 480),
    "Tan Phu": (440, 540),
    "Binh Tan": (320, 670),
    "11": (530, 660),
    "10": (610, 630),
    "3": (680, 580),
    "1": (760, 610),
    "4": (780, 690),
    "5": (650, 715),
    "6": (480, 740),
    "7": (880, 830),
    "8": (400, 940)
}

ADJACENCY = {
    "12": ["Binh Tan", "Tan Phu", "Tan Binh", "Go Vap", "Binh Thanh", "Thu Duc"],
    "Go Vap": ["12", "Tan Binh", "Phu Nhuan", "Binh Thanh"],
    "Thu Duc": ["12", "Binh Thanh", "2", "9"],
    "9": ["Thu Duc", "2"],
    "2": ["Thu Duc", "9", "Binh Thanh", "1", "4", "7"],
    "Binh Thanh": ["Go Vap", "12", "Thu Duc", "2", "Phu Nhuan", "1"],
    "Phu Nhuan": ["Go Vap", "Binh Thanh", "Tan Binh", "3", "1"],
    "Tan Binh": ["12", "Go Vap", "Phu Nhuan", "Tan Phu", "11", "10", "3"],
    "Tan Phu": ["12", "Tan Binh", "Binh Tan", "11", "6"],
    "Binh Tan": ["12", "Tan Phu", "6", "8"],
    "11": ["Tan Phu", "Tan Binh", "6", "10", "5"],
    "10": ["Tan Binh", "11", "3", "5"],
    "3": ["Tan Binh", "Phu Nhuan", "1", "10"],
    "1": ["Binh Thanh", "Phu Nhuan", "3", "5", "4", "2"],
    "4": ["1", "5", "2", "7", "8"],
    "5": ["10", "1", "11", "6", "8", "4"],
    "6": ["11", "Binh Tan", "Tan Phu", "5", "8"],
    "7": ["2", "4", "8"],
    "8": ["Binh Tan", "6", "5", "4", "7"]
}

VARIABLES = [
    "12", "Go Vap", "Thu Duc", "9", "2", "Binh Thanh", "Phu Nhuan",
    "Tan Binh", "Tan Phu", "Binh Tan", "11", "10", "3", "1", "4", "5", "6", "7", "8"
]

DOMAINS = ["Đỏ", "Xanh lá", "Vàng", "Xanh dương"]

def format_assignment(assignment):
    if not assignment:
        return "{}"
    return "{" + ", ".join(f"{k}={v}" for k, v in assignment.items()) + "}"

def format_domain(domain):
    if not domain:
        return "rỗng"
    return "{" + ", ".join(domain) + "}"

