from geolocation import read_voivodeships, read_places_from_single_voivodeship, read_single_medal_data
from libs import create_xlsx_file

all_medals = []


def main():
    voivodeships = read_voivodeships()
    for voivodeship in voivodeships:
        places, voivodeship_name = read_places_from_single_voivodeship(voivodeship)
        for place in places:
            medal_data = read_single_medal_data(place, voivodeship_name)
            print(f"Processed data: {medal_data}")
            all_medals.append(medal_data)
    create_xlsx_file(all_medals)


def fast():
    voivodeships = read_voivodeships()
    places, voivodeship_name = read_places_from_single_voivodeship(voivodeships[1])
    medal_data1 = read_single_medal_data(places[0], voivodeship_name)
    medal_data2 = read_single_medal_data(places[1], voivodeship_name)
    medal_data3 = read_single_medal_data(places[2], voivodeship_name)
    all_medals.append(medal_data1)
    all_medals.append(medal_data2)
    all_medals.append(medal_data3)
    create_xlsx_file(all_medals)

main()
# fast()