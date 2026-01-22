from datetime import datetime

# -----------------------------
# Column aliases (schema map)
# -----------------------------
COLUMN_ALIASES = {
    "qty": "quantity",
    "quantity": "quantity",
    "price": "price",
    "product": "product",
    "date": "date",
}

def normalize_row(row: dict) -> dict:
    """
    Normalize CSV row:
    - strip spaces
    - lowercase
    - apply column aliases
    """
    normalized = {}

    for key, value in row.items():
        clean_key = key.strip().lower()
        canonical_key = COLUMN_ALIASES.get(clean_key, clean_key)
        normalized[canonical_key] = value

    return normalized

def validate_row(row: dict):
    """
    Returns:
        (is_valid: bool, reason: str)
    """
    try:
        datetime.strptime(row["date"], "%Y-%m-%d")
    except Exception:
        return False, "invalid_date"

    if not row.get("product", "").strip():
        return False, "empty_product"

    try:
        qty = int(row["quantity"])
        if qty <= 0:
            return False, "quantity_non_positive"
    except Exception:
        return False, "quantity_not_integer"

    try:
        price = float(row["price"])
        if price <= 0:
            return False, "price_non_positive"
    except Exception:
        return False, "price_not_number"

    return True, "ok"
