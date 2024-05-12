from geo_coordinate import GeoCoordinate
from path import Path
from geo_map import GeoMap
from attraction import Attraction
from electronic_guide import ElectronicGuide
from photo import Photo


def create_geo_coordinate():
    print("Enter geographical latitude")
    geo_latitude = float(input())

    print("Enter geographical longitude")
    geo_longitude = float(input())

    return GeoCoordinate(geo_latitude, geo_longitude)


def create_attraction():
    print("Enter the name of the attraction: ")
    namings = input()

    print("Enter geographical coordinates:\n")
    geo_coordinate = create_geo_coordinate()

    print("Enter date building ")
    date_of_building = input()

    return Attraction(namings, geo_coordinate, int(date_of_building))


def create_photo():
    print("Enter attraction on this photo:\n")
    attractions = create_attraction()

    print("Enter height for photo: ")
    height = int(input())

    print("Enter width for photo: ")
    width = int(input())

    print("Enter beautiful level for photo: ")
    beautiful_level = int(input())
    return Photo(attractions, height, width, beautiful_level)


def create_path():
    print("Enter the start coordinate:\n")
    start_coordinate = create_geo_coordinate()

    print("Enter the finish coordinate:\n")
    finish_coordinate = create_geo_coordinate()

    return Path(start_coordinate, finish_coordinate)


def create_geographic_map():
    naming_to_attraction = dict()

    print("Enter count attractions:")
    count = int(input())

    for i in range(0, count, 1):
        print("Enter attraction:\n")
        attractions = create_attraction()
        naming_to_attraction[attractions.naming] = attractions

    return GeoMap(naming_to_attraction)


def create_electronic_guide():
    list_of_attractions = list()

    print("Enter count attraction: ")
    count = int(input())

    for i in range(0, count, 1):
        print("Enter attraction:\n")
        attractions = create_attraction()
        list_of_attraction.append(attractions)

    print("Enter your current coordinate:\n")
    current_coordinate = create_geo_coordinate()

    return ElectronicGuide(list_of_attractions, current_coordinate)


if __name__ == "__main__":
    geographic_map = GeoMap
    electronic_guide = ElectronicGuide

    list_of_photo = list()
    list_of_attraction = list()
    list_of_path = list()

    while True:
        print("1 Photo\n")
        print(" 1.2) Create photo\n")
        print(" 1.1) Show all photo\n")
        print("2 Attraction\n")
        print(" 2.1) Create attraction\n")
        print(" 2.2) Show all attraction\n")
        print("3 Path\n")
        print(" 3.1) Create path\n")
        print(" 3.2) Show all path\n")
        print("4 Geographic map\n")
        print(" 4.1) Create geographic map\n")
        print(" 4.2) Add information in geographic map\n")
        print(" 4.3) Remove information in geographic map\n")
        print("5 Electronic guide\n")
        print(" 5.1) Create electronic guide")
        print(" 5.2) Browsing photo\n")
        print(" 5.3) Get path\n")
        print(" 5.4) Movement\n")
        print(" 5.5) Get information\n")
        print(" 5.6) Feedback publication\n")
        print("6) End\n")

        operation1 = int(input())

        if operation1 == 1:
            operation2 = int(input())

            if operation2 == 1:
                list_of_photo.append(create_photo())
            elif operation2 == 2:
                for photo in list_of_photo:
                    print("Attraction naming on this photo: " + photo.attraction.naming + "\n")
                    print("Beautiful level " + str(photo.beautiful_level) + "\n\n")

        elif operation1 == 2:
            operation2 = int(input())

            if operation2 == 1:
                list_of_attraction.append(create_attraction())
            elif operation2 == 2:
                for attraction in list_of_attraction:
                    print("Attraction naming: " + attraction.naming + "\n")
                    print("Date of building: " + str(attraction.date_of_building) + "\n\n")
        elif operation1 == 3:
            operation2 = int(input())

            if operation2 == 1:
                list_of_path.append(create_path())
            elif operation2 == 2:
                for path in list_of_path:
                    print("Start coordinate: " + str(path.coordinate_start.geo_latitude) +
                          str(path.coordinate_start.geo_longitude) + "\n")
                    print("Finish coordinate: " + str(path.coordinate_finish.geo_latitude) +
                          str(path.coordinate_finish.geo_longitude) + "\n\n")

        elif operation1 == 4:
            operation2 = int(input())

            if operation2 == 1:
                geographic_map = create_geographic_map()
            elif operation2 == 2:
                geographic_map.add_attraction(create_attraction())
            elif operation2 == 3:
                geographic_map.remove_attraction(create_attraction())

        elif operation1 == 5:
            operation2 = int(input())

            if operation2 == 1:
                electronic_guide = create_electronic_guide()
            elif operation2 == 2:
                print("Enter naming attraction: ")
                naming = input()
                photo = electronic_guide.browsing_photo(naming)
                print("Height: " + str(photo.height) + "\n")
                print("Width: " + str(photo.width) + "\n")
                print("Beautiful level:" + str(photo.beautiful_level) + "\n\n")
            elif operation2 == 3:
                print("Enter naming start attraction: ")
                naming_start = input()
                print("Enter naming finish attraction: ")
                naming_finish = input()

                path = electronic_guide.get_path(naming_start, naming_finish)

                print("Start coordinate: " + str(path.coordinate_start.geo_latitude) +
                      str(path.coordinate_start.geo_longitude) + "\n")
                print("Finish coordinate: " + str(path.coordinate_finish.geo_latitude) +
                      str(path.coordinate_finish.geo_longitude) + "\n\n")
            elif operation2 == 4:
                print("Enter next attraction naming: ")
                next_naming = input()
                electronic_guide.movement(next_naming)
            elif operation2 == 5:
                print("Enter attraction naming: ")
                naming = input()
                print(electronic_guide.get_information(naming))
            elif operation2 == 6:
                print("Enter your publication: ")
                text = input()
                electronic_guide.feedback_publication(text)

        elif operation1 == 6:
            break
        else:
            print("Incorrect input")
