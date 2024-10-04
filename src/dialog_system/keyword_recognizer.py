from typing import Tuple, Any

from Levenshtein import distance
import math
import re

min_score = 3

# No preference:
no_preferences_words = ['doesn\'t matter', 'does not matter', 'dont care', 'anything', 'any', 'i do not care',
                        'i don\'t care', 'i don\'t mind', 'what ever']

# Preference based on money:
money_based_preference_words = ['cheap', 'expensive', 'moderate', 'moderately']
price_regex_set = [
    {
        'regex': '.*(?:price|price range)(.*)',
        'post_variable': True,
        'preferences': no_preferences_words,
        'replacement': 'any'
    },
]

# Preference based on area:
area_based_preference_words = ['town', 'south', 'north', 'east', 'west', 'part of town', 'center', 'area']
area_regex_set = [
    {
        'regex': '.*(?:in the)(.*)',
        'post_variable': True,
        'preferences': area_based_preference_words
    },
    {
        'regex': '.*(?:area|location|where)(.*)',
        'post_variable': True,
        'preferences': no_preferences_words,
        'replacement': 'any'
    },
]

# Preference based on country:
country_based_preference_words = [
    'swiss', 'vietnam', 'afghan', 'spanish', 'scandinavian', 'german', 'italian',
    'hungarian', 'asian', 'caribbean', 'indian', 'lebanese', 'vietnamese', 'korean',
    'russian', 'brazilian', 'malaysian', 'jamaican', 'eritrean', 'moroccan',
    'singaporean', 'cuban', 'japanese', 'chinese', 'mexican', 'basque', 'african',
    'french', 'scottish', 'venetian', 'singapore', 'english', 'indonesian', 'romanian',
    'welsh', 'swedish', 'irish', 'greek', 'catalan', 'danish', 'american', 'cantonese',
    'thai', 'british', 'tuscan', 'mediterranean', 'portuguese', 'european', 'turkish',
    'australian', 'austria', 'austrian', 'belgium', 'polish', 'ukrainian', 'filipino',
    'ethiopian', 'syrian', 'egyptian', 'israeli', 'argentinian', 'peruvian', 'pakistani',
    'bangladeshi', 'burmese', 'kenyan', 'nigerian', 'south african',
    'canadian', 'colombian', 'venezuelan', 'nepalese', 'cambodian', 'mongolian', 'taiwanese',
    'sudanese', 'persian', 'kurdish', 'georgian', 'armenian', 'lithuanian', 'latvian',
    'croatian', 'serbian', 'slovenian', 'slovakian', 'czech',
    'algerian', 'tunisian', 'dutch', 'finnish', 'norwegian', 'icelandic', 'hawaiian', 'new zealand'
]

# Preference based on category:
category_based_preference_words = [
    'world', 'venetian', 'vegetarian', 'steakhouse', 'international', 'creative', 'crossover',
    'gastropub', 'barbecue', 'bistro', 'unusual', 'traditional', 'seafood', 'canape', 'christmas', 'halal'
]

food_regex_set = [
    {
        'regex': '(.*)(?:food|restaurant).*',
        'post_variable': False,
        'preferences': category_based_preference_words + country_based_preference_words
    },
    {
        'regex': '.*(?:food|restaurant|what)(.*)',
        'post_variable': True,
        'preferences': no_preferences_words,
        'replacement': 'any'
    },
]


def extract_keywords(utterance, current_preference) -> tuple[dict, dict]:
    """Extracts keywords found in the given utterance"""
    found_preferences = {
        "food": None,
        "pricerange": None,
        "area": None,
    }

    scores = {
        "food": None,
        "pricerange": None,
        "area": None,
    }

    utterance = utterance.lower()

    find_variable_by_regex(
        utterance,
        'food',
        food_regex_set,
        found_preferences,
        scores
    )

    find_variable_by_regex(
        utterance,
        'area',
        area_regex_set,
        found_preferences,
        scores
    )

    find_variable_by_regex(
        utterance,
        'pricerange',
        price_regex_set,
        found_preferences,
        scores
    )

    # global found_preferences
    line_split = utterance.split(" ")

    for word in line_split:
        if len(line_split) == 1:
            if find_variable_by_levenstein(word, 'food',
                                           category_based_preference_words + country_based_preference_words,
                                           found_preferences, scores):
                continue

        if len(line_split) == 1:
            if find_variable_by_levenstein(word, 'area', area_based_preference_words, found_preferences, scores):
                continue

        if find_variable_by_levenstein(word, 'pricerange', money_based_preference_words, found_preferences, scores):
            continue

    if len([preference for preference in found_preferences.values() if preference is not None]) == 0:
        if len([preference for preference in no_preferences_words if
                re.sub(r'[^A-Za-z\s]', '', preference) in re.sub(r'[^A-Za-z\s]', '', utterance)]) > 0:
            for key, value in current_preference.items():
                if value is None:
                    found_preferences[key] = 'any'
                    scores[key] = 0

    return scores, found_preferences


def find_variable_by_regex(utterance, name, regex_set, found_preferences, scores):
    for config in regex_set:
        results = re.search(config['regex'], utterance)
        if results is None:
            continue

        val = results.group(1).strip()

        grouped_by_word_count = {}
        for word in config['preferences']:
            word_count = len(word.split(' '))
            if word_count not in grouped_by_word_count.keys():
                grouped_by_word_count[word_count] = []

            grouped_by_word_count[word_count].append(word)

        for word_count, words in grouped_by_word_count.items():
            if config['post_variable']:
                query = val.split(' ')[0:word_count]
            else:
                query = val.split(' ')[-word_count:]

            found_keyword, score = find_closest_preference(' '.join(query), words)

            if found_keyword is not None and score < min(scores[name] if isinstance(scores[name], int) else math.inf,
                                                         min_score):
                if 'replacement' in config:
                    found_preferences[name] = config['replacement']
                else:
                    found_preferences[name] = found_keyword

                scores[name] = score

                continue


def find_variable_by_levenstein(word, name, preference_words, found_preferences, scores):
    if found_preferences[name] is None:
        found_keyword, score = find_closest_preference(word, preference_words)
        if found_keyword is not None and score < min(scores[name] if isinstance(scores[name], int) else math.inf,
                                                     min_score):
            found_preferences[name] = found_keyword
            scores[name] = score

            return True

    return False


def find_closest_preference(word, preferences) -> tuple[None | str, int]:
    """A function that finds the keyword closest to the matched word"""
    lowest_score = min_score
    found_keyword = None

    for preference in preferences:
        dist = distance(word, preference)

        if dist < lowest_score:
            found_keyword = preference
            lowest_score = dist

        if lowest_score == 0:
            break

    return found_keyword, lowest_score


def find_detail_keyword(utterance):
    """Finds what detail the user requested to get from the restaurant"""
    # utt_split = utterance.split(" ")
    m1 = re.search(r"(postcode)", utterance)
    m2 = re.search(r"(address)", utterance)
    m3 = re.search(r"(phone)", utterance)
    found = []
    if m1 is not None:
        found.append(m1.group(1))
    if m2 is not None:
        found.append(m2.group(1))
    if m3 is not None:
        found.append(m3.group(1))

    return found


if __name__ == "__main__":
    find_detail_keyword("phone number and address please")

    while True:
        print(extract_keywords(input('Test me: ')))
    # print(distance("east", "want"))