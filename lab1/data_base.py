import string
import random
from attraction import Attraction


class DateBase:
    length_of_text1 = 100
    length_of_text2 = 200

    attraction_to_information = dict()
    attraction_to_feedback = dict()

    @staticmethod
    def get_information(attraction: Attraction):
        if attraction in DateBase.attraction_to_information:
            return DateBase.attraction_to_information[attraction]

        if attraction.date_of_building <= 1000:
            information = ''.join(random.choices(string.ascii_uppercase + string.digits, k=DateBase.length_of_text1))
            DateBase.attraction_to_information[attraction] = information
            return information

        information = ''.join(random.choices(string.ascii_uppercase + string.digits, k=DateBase.length_of_text2))
        DateBase.attraction_to_information[attraction] = information
        return information

    @staticmethod
    def feedback_publication(attraction: Attraction, text: str):
        DateBase.attraction_to_feedback[attraction] = text
