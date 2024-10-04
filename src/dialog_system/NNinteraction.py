# Dialog handler
import pandas as pd
import os
import MachineLearning.NN as nn
from src.dialog_system import keyword_recognizer as kr


### TODO
# we need to make sure to ask for clarification when there are mutliple preferences being given.

class Dialog:
    """Dialog class"""

    def __init__(self):  # add the cmd args

        # what does the state need to represent and contain?
        # what turn it is; previous answers and responses; what dialog act occurred

        self.current_preferences = {
            "food": None,
            "pricerange": None,
            "area": None,
        }
        self.not_confirmed_preferences = {
            "food": None,
            "pricerange": None,
            "area": None,
        }
        self.unknowns = {
            "food": True,
            "pricerange": True,
            "area": True,
        }
        self.preference_text = {
            "food": 'food',
            "pricerange": 'price range',
            "area": 'area',
        }

        self.stages = {
            1: ['hello', 'inform'],
            2: ['inform'],
            3: ['inform'],
            4: ['affirm', 'negate'],
            5: ['affirm', 'negate', 'reqalts'],
            6: ['inform'],
            7: ['reqalts', 'negate', 'deny', 'inform', 'confirm'],
            99: ['inform', 'bye'],
        }

        self.exit_flag = False
        self.ask_unknown = False
        self.unknown_preferences = []

        self.found_restaurants = pd.DataFrame()
        self.current_reccomendation_index = -1

        self.restaurant_info = pd.read_csv("./restaurant_info.csv")

    def interact(self, stage=1):
        """The main while loop for handling user interactions"""
        while not self.exit_flag:
            utterance = self.input()

            if utterance == "exit":
                self.say('Have a great day!')

                return False

            dialog_act = nn.predictDialogAct(utterance)

            stage, reply = self.process_dialog_act(dialog_act, utterance, stage)
            print(self.current_preferences)
            self.say(reply)

    def retrieve_restaurant(self):
        """Retrieve the information of restaurants matching the found preferences"""
        result_df = self.restaurant_info

        for key, value in self.current_preferences.items():
            if value != "any" and value is not None:
                result_df = result_df.loc[self.restaurant_info[key] == value]

        # print(result_df)
        self.found_restaurants = result_df

    def recommend_restaurant(self):
        """Recommend restaurants based on the found restaurants"""
        self.current_reccomendation_index += 1
        rec = self.found_restaurants.iloc[self.current_reccomendation_index]
        # print(rec)

        print(f"{rec["restaurantname"]} serves {rec["food"]} food and is in the {rec["area"]} part of town")

    def retrieve_restaurant_detail(self, keys):
        """Retrieves a detail of the current recommended restaurant like phone number or location"""
        details = []
        for key in keys:
            details.append(self.found_restaurants.iloc[self.current_reccomendation_index][key])

        return details

    def process_dialog_act(self, dialog_act, utterance, stage) -> tuple[int, str]:
        """
        This is where the structure of the flow diagram can
        be used to determine what to do with the dialog act and utterance
        """

        print('Act:' + dialog_act)
        if type(dialog_act) is list:
            dialog_act = dialog_act[0]

        print('Stage: ' + str(stage))
        if dialog_act not in self.stages[stage]:
            return stage, 'Sorry, I did not understand you.'

        # using match-case-return structures
        match dialog_act:
            case "inform":
                ## we need to make sure to ask for clarification when there are conflicting preferences
                scores, found_preferences = kr.extract_keywords(utterance, self.current_preferences)

                if len([preference for preference in found_preferences.values() if preference is not None]) == 0:
                    return stage, 'Sorry, I did not understand you.'

                preferences_changed = []
                for key, val in found_preferences.items():
                    if self.current_preferences[key] is not None and val is not None:
                        self.not_confirmed_preferences[key] = found_preferences[key]
                        preferences_changed.append(key)

                preferences_misspelled = []
                for key, value in self.current_preferences.items():
                    if value is None and found_preferences[key] is not None:
                        if scores[key] > 0:
                            self.not_confirmed_preferences[key] = found_preferences[key]
                            preferences_misspelled.append(key)
                        else:
                            self.current_preferences[key] = found_preferences[key]

                needs_to_confirm_misspelled_preference = len(preferences_misspelled) > 0
                needs_to_confirm_changed_preference = len(preferences_changed) > 0

                if needs_to_confirm_misspelled_preference or needs_to_confirm_changed_preference:
                    reply = []

                    if needs_to_confirm_misspelled_preference:
                        reply.append('Can you confirm that you would like ' + ' and '.join(
                            [self.preference_text[key] + ' to ' + found_preferences[key] for key in
                             preferences_misspelled]) + '?')

                    if needs_to_confirm_changed_preference:
                        reply.append('Ok. Would you like to change the ' + ' and '.join(
                            [self.preference_text[key] + ' to ' + found_preferences[key] for key in
                             preferences_changed]) + '?')

                    return 4, ' '.join(reply)

                return self.control()

            case "negate":
                self.reset_not_confirmed_preferences()

                return self.control()

            case "affirm":
                # this means the user is

                if len(list(filter(lambda x: x is not None, self.not_confirmed_preferences.values()))) > 0:
                    for key, value in self.not_confirmed_preferences.items():
                        if value is not None:
                            self.current_preferences[key] = value

                    self.reset_not_confirmed_preferences()

                return self.control()

            case "thankyou":
                # close the program
                return 99, "No problem! Can I help you further?"
            case "reqalts":
                # recommend alternatives; maybe ask for affirmation
                self.recommend_restaurant()

                return stage, ""
            case "hello":
                # user says hello
                return stage, "Hello back pal."
            case "request":
                # answer request by getting info from csv
                # extract the specific detail
                # voeg een methode toe aan kr zodat deze ook de keywords kan vinden voor de specifieke details
                # self.retrieve_restaurant_detail()
                found_details = kr.find_detail_keyword(utterance)
                if len(found_details) == 0:
                    print("something went wrong, what information would you like to retrieve from the restaurant?")
                else:
                    rest_details = self.retrieve_restaurant_detail(found_details)
                    print(f"Ok i found the following details on the restaurant: {rest_details[0]}")
                return ""
            case "restart":
                # restart from the beginning
                # can this be done by just calling the __init__() function? or do each of the variables need to be redefined
                self.__init__()
                return stage, ""
            case "repeat":
                # ask something that has not been answered before
                return stage, ""
            case "bye":
                # close
                self.exit_flag = True

                return stage, "Oke. Have a great day!"
            case "reqmore":
                # not a clue
                return stage, ""
            case "ack":
                # not a clue
                return stage, ""
            case "null":
                # ignore, maybe repeat what system said in the previous turn
                return stage, "I did not understand that, how can I help?"
            case "deny":
                # idk, ask for clarification
                return stage, ""
            case "confirm":
                # The user wants to confirm a specific detail about the restaurant we recommended

                return stage, ""
            case _:  # base case; is this necessary if the above list of acts is exhaustive?
                return stage, ""

    def control(self):
        unknown_preferences = [key for key, preference in self.current_preferences.items() if preference is None]

        if len(unknown_preferences) > 0:
            return 3, 'Oke. Do you have any preferences for the ' + ' and '.join(
                [self.preference_text[key] for key in unknown_preferences]) + '?'

        self.retrieve_restaurant()

        if self.found_restaurants.empty:
            return 6, 'There are no restaurants found unfortunately. Please change your preferences.'

        self.recommend_restaurant()

        return 5, 'Here are some restaurants that I can recommend you! Do you have additional requirements?'

    def reset_not_confirmed_preferences(self):
        self.not_confirmed_preferences = dict(
            zip(self.current_preferences.keys(), [None] * len(self.current_preferences.keys())))

    def input(self):
        return input("Say something: ")

    def say(self, text=''):
        print('System: ' + text)


if __name__ == "__main__":
    nn.preprocessing()
    nn.try_load_model()
    os.system("clear")
    d = Dialog()
    d.interact()