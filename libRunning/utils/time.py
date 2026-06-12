
def to_sec(duration: str) -> int:
    parts: list[str] = duration.split(":")
    if len(parts) != 2:
        raise ValueError(f"Wrong value: {duration}")
    return (60 * int(parts[0])) + int(parts[1])


def to_time(sec: int) -> str:
    mins: int = sec // 60
    secs = sec % 60
    ssecs = str(secs).zfill(2)
    return f"{mins}:{ssecs}"
