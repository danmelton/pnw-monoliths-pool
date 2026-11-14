import csv
import io 


# story2: handle nested or uneven data  
def flatten(record, parent_key=""):
    flat = {}
    for key, value in record.items():

        if parent_key:
            new_key = f"{parent_key}.{key}"
        else:
            new_key = key
    
        # nested values, use recursive call, merge dictionaries with .update()
        if isinstance(value, dict):
            flat.update(flatten(value, new_key))
        # list value, combine with ';'
        elif isinstance(value, list):
            flat[new_key] = ";".join(str(val) for val in value)
        else:
            flat[new_key] = value
    return flat



# story1: convert JSON to CSV
def json_to_csv(data, columns=None):
    # flatten data
    flattened = [flatten(r) for r in data]

    # parse columns
    if columns:
        cols = list(columns)
    else:
        cols = []
        for record in flattened:
            for key in record:
                if key not in cols:
                    cols.append(key)

    # write headers/rows to in memory IO "file"
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=cols, restval="", extrasaction="ignore")
    writer.writeheader()
    for record in flattened:
        writer.writerow(record)
    return buffer.getvalue()



# story3: handle bad/unsafe data (RUSSELL)

# csv injection: excel/sheets run a cell as a formula if it starts with = + - or @
# so put a ' in front and it shows up as normal text instead
def make_safe(value):
    if isinstance(value, str):
        if len(value) > 0 and value[0] in ["=", "+", "-", "@"]:
            return "'" + value
        return value

    # nested objects and lists, go through each value
    if isinstance(value, dict):
        new_dict = {}
        for key in value:
            new_dict[key] = make_safe(value[key])
        return new_dict

    if isinstance(value, list):
        new_list = []
        for item in value:
            new_list.append(make_safe(item))
        return new_list

    # numbers, true/false, null stay the same
    return value



if __name__ == "__main__":
    
    print("=== UserStory1: basic functionality ===")
    test1 = [
        {"date": "2026-11-01", "exercise": "Squat", "sets": 3, "reps": 10},
        {"date": "2026-11-02", "exercise": "Bench Press", "sets": 4, "reps": 8}
    ]
    print(json_to_csv(test1))

    print("=== UserStory1: commas, quotes, newlines ===")
    test2 = [
        {"ip": "192.168.1.1", "hostname": "router, upstairs", "notes": 'runs "dnsmasq"'},
        {"ip": "192.168.1.3", "hostname": "laptop", "notes": "seen twice\nonce on wifi"}
    ]
    print(json_to_csv(test2))

    print("=== UserStory2: nested objects + lists ===")
    test3 = [
        {"date": "2026-11-01", "exercise": {"name": "Squat", "equipment": {"type": "barbell"}}, "sets": 3, "reps": [10, 8, 6]},
        {"date": "2026-11-02", "exercise": {"name": "Bench Press", "equipment": {"type": "dumbbell"}}, "sets": 4, "reps": [8, 8, 6, 6]}
    ]
    print(json_to_csv(test3))

    print("=== UserStory2: uneven keys ===")
    test4 = [
        {"date": "2026-11-01", "exercise": "Squat"},
        {"date": "2026-11-02", "notes": "felt strong"}
    ]
    print(json_to_csv(test4))

