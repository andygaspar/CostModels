

def get_haul(length: float) -> str:
    if length <= 1500:
        return "ShortHaul"
    if length <= 3500:
        return "MediumHaul"
    return "LongHaul"
