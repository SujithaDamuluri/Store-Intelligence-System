import json

def load_events():

    events = []

    try:
        with open(
            "data/events/generated_events.jsonl",
            "r"
        ) as f:

            for line in f:
                events.append(
                    json.loads(line)
                )

    except FileNotFoundError:
        pass

    return events