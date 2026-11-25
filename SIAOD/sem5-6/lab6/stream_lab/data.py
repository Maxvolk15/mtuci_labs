import hashlib
from random import Random

rng = Random(2026)
N = 12_000
paths = ["/search", "/catalog", "/profile", "/checkout", "/news"]
events = []

for i in range(N):
    if rng.random() < 0.40:
        user_num = rng.randrange(24)
    else:
        user_num = rng.randrange(24, 2024)
    duration = (rng.randint(30, 450)
                if rng.random() < 0.92
                else rng.randint(800, 3500))

    events.append({
        "event_id": f"evt_{i:05d}",
        "user_id": f"user_{user_num:04d}",
        "duration_ms": duration,
        "timestamp": i,
        "path": rng.choice(paths),
    })


def hash64(text):
    digest = hashlib.blake2b(
        str(text).encode("utf-8"), digest_size=8
    ).digest()
    return int.from_bytes(digest, "big")
