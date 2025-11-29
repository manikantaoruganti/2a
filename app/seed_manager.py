DATA_PATH = "/data/seed.txt"


def write_seed(hex_seed: str):
    with open(DATA_PATH, "w") as f:
        f.write(hex_seed)


def read_seed() -> str:
    with open(DATA_PATH, "r") as f:
        return f.read().strip()
