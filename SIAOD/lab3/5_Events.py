import ast

days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def to_minutes(t):
    return t[0] * 60 + t[1]


def format_time(t):
    return f"{t[0]:02d}:{t[1]:02d}"


def load_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read().strip()

    var_name, data_part = text.split("=", 1)
    var_name = var_name.strip()
    data_part = data_part.strip()

    events = ast.literal_eval(data_part)
    return events


def greedy_schedule(events):
    selected_events = []
    schedule_by_day = {}

    for day in days_order:
        day_events = [event for event in events if event[1] == day]

        day_events.sort(key=lambda event: to_minutes(event[3]))

        chosen_for_day = []
        current_end = to_minutes((8, 0))

        for event in day_events:
            title, event_day, start, end, description = event
            start_minutes = to_minutes(start)
            end_minutes = to_minutes(end)

            if start_minutes < to_minutes((8, 0)):
                continue
            if end_minutes > to_minutes((18, 0)):
                continue

            if start_minutes >= current_end:
                chosen_for_day.append(event)
                current_end = end_minutes

        if chosen_for_day:
            schedule_by_day[day] = chosen_for_day
            selected_events.extend(chosen_for_day)

    return selected_events, schedule_by_day


events = load_from_file("works.txt")

selected_events, schedule_by_day = greedy_schedule(events)
max_events_count = len(selected_events)

print("Итоговое количество выбранных мероприятий:", max_events_count)
print()

for day in days_order:
    if day in schedule_by_day:
        print(f"День: {day}")
        for event in schedule_by_day[day]:
            title, event_day, start, end, description = event
            print("Время начала:", format_time(start))
            print("Время окончания:", format_time(end))
            print("Название:", title)
            print("Описание:", description)
            print()
        print("-" * 50)