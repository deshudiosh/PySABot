from pathlib import Path

def create():
    used = list(Path("./proxies/used").iterdir())
    fresh = list(Path("./proxies/fresh").iterdir())

    names = [str(elem.name) for elem in used+fresh]

    with open("./proxies/cleaned.txt") as f:
        lines = f.readlines()

        duplicates = 0
        added = 0

        for line in lines:
            name = line.replace(":", "-").rstrip("\n")

            if name in names:
                duplicates += 1
                continue

            filepath = "{}{}".format("./proxies/", name)
            open(filepath, "w+")

            added += 1

        print("Duplicate proxies found:", duplicates)
        print("Created new proxy files:", added)


if __name__ == "__main__":
    create()