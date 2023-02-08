
def parse_seconds(seconds: int):
    hours = int(seconds // 3600)
    minutes = int((seconds - (hours * 3600)) // 60)
    return hours, minutes
