import csv

TRACK_FILE = "M06/track.csv"

class Entry:
    def __init__(self, desc: str, time: int, tags: list[str]) -> None:
        self.desc = desc
        self.time = time
        self.tags = tags

    def __repr__(self) -> str:
        return f"Entry(desc={self.desc!r}, time={self.time!r}, tags={self.tags!r}"

def create_entry_from_dict(row: dict[str, str]) -> Entry:
    """Accepts a dictionary consisting of strings.

    Returns an Entry class with converted arguments(str, int and list[str])."""
    return Entry(
        desc=row["desc"],
        time=int(row["time"]),
        tags=row["tags"].split()
    )

def read_entry(filename: str) -> list[Entry]:
    """Accepts a filename as a string.

    Returns a list of gathered information from the file."""
    with open(filename) as stream:
        reader = csv.DictReader(stream)
        entries = [create_entry_from_dict(row) for row in reader]
    return entries

def existing_tags(entries: list[Entry]) -> set[str]:
    """Accepts a list of informations.

    Returns a set of all the tags."""
    tags = set(tag for entry in entries for tag in entry.tags)
    return tags
 
def tags_total_time(entries: list[Entry]) -> dict[str, int]:
    """Accepts a list of informations.
    
    Returns a dictonary consisting of the total time spend on a tag."""
    tag_time_dict = {}
    for entry in entries:
        for tag in entry.tags:
            if tag in existing_tags(entries):
                tag_time_dict[tag] = tag_time_dict.get(tag, 0) + entry.time 
    return tag_time_dict 

def print_report(entries: list[Entry]) -> None:
    """Accepts a list of informations.

    Prints separately each tag and its total time."""
    print("TOTAL_TIME  TAG")
    for tag, time in tags_total_time(entries).items():
        print(f"{time:10}  #{tag}")

def main() -> None:
    entries = read_entry(TRACK_FILE)
    print_report(entries)

if __name__ == "__main__":
    main()
