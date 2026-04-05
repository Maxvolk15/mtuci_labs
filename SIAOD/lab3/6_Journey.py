stations = [120, 260, 410, 560, 730, 890, 1040, 1190, 1360, 1520, 1680, 1840, 2010, 2170, 2330, 2480, 2650, 2810, 2970, 3140, 3300, 3460, 3630, 3790, 3950, 4120, 4280, 4440, 4610, 4770, 4930, 5100, 5260, 5420, 5590, 5750, 5910, 6080, 6240, 6400, 6570, 6730, 6890, 7060, 7220, 7380, 7550, 7710, 7870, 8040, 8200, 8360, 8530, 8690, 8850, 9020, 9180, 9340, 9510, 9670, 9830, 10000, 10160, 10320]

full_distance = 10451
max_distance = 500

def min_refills(total_distance, max_run, stations):
    refills = []
    current_position = 0
    i = 0

    while current_position + max_run < total_distance:
        farthest = current_position

        while i < len(stations) and stations[i] <= current_position + max_run:
            farthest = stations[i]
            i += 1

        refills.append(farthest)
        current_position = farthest

    return refills

route = min_refills(full_distance, max_distance, stations)


print("Минимальное количество остановок:", len(route))
print("Выбранные заправки:", route)
print("Маршрут:")
print([0] + route + [full_distance])