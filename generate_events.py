import json
import string
from random import randint, choice
from copy import deepcopy
from datetime import date, timedelta
from collections import defaultdict


def generate_random_date():
    return str(date.today() - timedelta(days=randint(22, 388)))


def generate_random_int(range_start, range_end):
    return str(randint(range_start, range_end))


def generate_event_id():
    return choice(string.ascii_lowercase) + "".join(
        choice(string.ascii_lowercase + string.digits) for _ in range(10))


def get_age(range_num):
    if range_num == 0:
        return generate_random_int(1, 4)
    if range_num == 1:
        return generate_random_int(5, 14)
    if range_num == 2:
        return generate_random_int(15, 99)


def generate_random_string():
    return "".join(choice(string.ascii_uppercase) for _ in range(6))


def get_base_event(program_name):
    return json.loads(open("base_events/" + program_name + ".json").read())["events"][0]


def get_config(program_name):
    return json.loads(open("config/" + program_name + ".json").read())


def populate_random_dv(data_values_config, data_values):
    if data_values_config[data_values["dataElement"]].startswith("int"):
        limit = int(data_values_config[data_values["dataElement"]].split()[1])
        data_values["value"] = generate_random_int(0, limit)
    elif data_values_config[data_values["dataElement"]] == "string":
        data_values["value"] = generate_random_string()
    elif data_values_config[data_values["dataElement"]] == "date":
        data_values["value"] = generate_random_date()


def populate_option_dv(data_values, data_values_config, next_option_pointer):
    all_options = data_values_config[data_values["dataElement"]]
    index = 0 if not next_option_pointer[data_values["dataElement"]] else next_option_pointer[
        data_values["dataElement"]]
    index %= len(all_options)
    data_values["value"] = all_options[index]
    next_option_pointer[data_values["dataElement"]] += 1


def generate_events(program_name):
    base_event = get_base_event(program_name)
    config = get_config(program_name)

    data_values_config = config["data_values_config"]
    metadata = config["metadata"]

    event_list = []
    next_option_pointer = defaultdict(int)

    for i in range(0, 3):
        for j in range(0, metadata["max_options"]):
            event = deepcopy(base_event)
            event_date = str(date.today() - timedelta(days=7))
            event["event"] = generate_event_id()
            event["eventDate"] = event_date + "T00:00:00"

            for data_values in event["dataValues"]:
                if metadata["age"] == data_values["dataElement"]:
                    data_values["value"] = get_age(i)
                elif type(data_values_config[data_values["dataElement"]]) == list:
                    populate_option_dv(data_values, data_values_config, next_option_pointer)
                elif data_values_config[data_values["dataElement"]] == "event_date":
                    data_values["value"] = event_date
                else:
                    populate_random_dv(data_values_config, data_values)

            event_list.append(event)

    with open('generated/' + program_name + '.json', 'w') as f:
        f.write(json.dumps({"events": event_list}))


def main():
    programs = ["ctc", "measles", "er", "icu"]
    for p in programs:
        generate_events(p)


if __name__ == "__main__":
    main()
