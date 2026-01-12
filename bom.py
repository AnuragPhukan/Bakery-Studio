from typing import Dict, List


BOM_PER_UNIT: Dict[str, Dict[str, object]] = {
    "cupcakes": {
        "materials": [
            {"name": "flour", "unit": "kg", "qty": 0.08},
            {"name": "sugar", "unit": "kg", "qty": 0.06},
            {"name": "butter", "unit": "kg", "qty": 0.04},
            {"name": "eggs", "unit": "each", "qty": 0.5},
            {"name": "milk", "unit": "L", "qty": 0.05},
            {"name": "vanilla", "unit": "ml", "qty": 1.0},
            {"name": "baking_powder", "unit": "kg", "qty": 0.001},
        ],
        "labor_hours": 0.05,
    },
    "cake": {
        "materials": [
            {"name": "flour", "unit": "kg", "qty": 0.50},
            {"name": "sugar", "unit": "kg", "qty": 0.40},
            {"name": "butter", "unit": "kg", "qty": 0.30},
            {"name": "eggs", "unit": "each", "qty": 4.0},
            {"name": "milk", "unit": "L", "qty": 0.20},
            {"name": "cocoa", "unit": "kg", "qty": 0.05},
            {"name": "vanilla", "unit": "ml", "qty": 5.0},
            {"name": "baking_powder", "unit": "kg", "qty": 0.005},
        ],
        "labor_hours": 0.80,
    },
    "pastry_box": {
        "materials": [
            {"name": "flour", "unit": "kg", "qty": 0.40},
            {"name": "butter", "unit": "kg", "qty": 0.35},
            {"name": "sugar", "unit": "kg", "qty": 0.10},
            {"name": "eggs", "unit": "each", "qty": 1.0},
            {"name": "milk", "unit": "L", "qty": 0.10},
            {"name": "salt", "unit": "kg", "qty": 0.002},
            {"name": "yeast", "unit": "kg", "qty": 0.005},
        ],
        "labor_hours": 0.60,
    },
}


def list_job_types() -> List[str]:
    return list(BOM_PER_UNIT.keys())


def scale_bom(job_type: str, quantity: int) -> Dict[str, object]:
    if job_type not in BOM_PER_UNIT:
        raise ValueError("Unknown job_type")
    if quantity <= 0:
        raise ValueError("quantity must be > 0")
    per_unit = BOM_PER_UNIT[job_type]
    scaled_materials = []
    for material in per_unit["materials"]:
        scaled_qty = material["qty"] * quantity
        if material["unit"] in ("kg", "L"):
            scaled_qty = round(scaled_qty, 3)
        elif material["unit"] == "ml":
            scaled_qty = round(scaled_qty, 1)
        else:
            scaled_qty = round(scaled_qty, 1)
        scaled_materials.append(
            {"name": material["name"], "unit": material["unit"], "qty": scaled_qty}
        )
    labor = round(per_unit["labor_hours"] * quantity, 3)
    return {
        "job_type": job_type,
        "quantity": quantity,
        "materials": scaled_materials,
        "labor_hours": labor,
    }
