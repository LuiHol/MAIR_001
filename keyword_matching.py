from Levenshtein import distance
import math


#inform grouped:

# No preference:
no_preferences_words = ['doesnt matter', 'does not matter', 'dont care', 'anything', 'any', 'i do not care', 'i dont care', 'i dont mind', 'what ever']

# Preference based on money:
money_based_preference_words = ['cheap', 'expensive', 'moderate', 'moderately']

# Preference based on location:
location_based_preference_words = ['town', 'south', 'north', 'east', 'west', 'part of town', 'center', 'area']

# Preference based on country:
country_based_preference_words = ['swiss', 'vietnam', 'afghan', 'spanish', 'scandinavian', 'german', 'italian', 'hungarian', 'asian', 'caribbean', 'indian', 'leban', 'carraibean','vietnamese', 'korean', 'russian', 'brazilian', 'malaysian', 'jamaican', 'eritrean', 'moroccan','scandanavian', 'signaporian',  'cuban', 'japanese', 'cuban', 'chinese', 'mexican', 'basque','african', 'french', 'scottish', 'airatarin', 'aristrain', 'arotrian', 'airitran', 'chineese', 'singapore', 'singaporean', 'english', 'indonesian''lebanese', 'venesian', 'romanian', 'welsh', 'swedish', 'irish', 'greek','catalan', 'catalanian', 'catalania', 'danish','american', 'cantonese', 'thai', 'british', 'tuscan', 'mediterranean', 'portuguese', 'european', 'turkish', 'australian', 'austria', 'austrian','belgium']

# Preference based on category:
category_based_preference_words = ['world', 'venetian', 'vegetarian', 'vegitarian', 'steakhouse', 'international', 'creative', 'crossover', 'gastropub','barbecue', 'bistro', 'unusual', 'traditional', 'seafood', 'canape', 'canapes', 'christmas', 'halal', 'steak house',]

preferences_groups = {
    'no_preference': no_preferences_words,
    'country': country_based_preference_words,
    'category': category_based_preference_words,
}

def inform_sentence_matching(pattern, sentance, min_score=3):
    lowest_score = math.inf
    lowest_match = None

    sentance = ''.join(e for e in sentance.lower().strip() if e.isalnum() or e == ' ')

    for word in sentance.split(' '):
        score, match = inform_word_matching(pattern, word, min_score)

        if score < lowest_score:
            lowest_score = score
            lowest_match = match

    return (lowest_score, lowest_match)

def inform_word_matching(pattern, word, min_score=3):
    lowest_score = min_score
    lowest_match = None

    for preference in pattern:
        score = distance(word, preference)
        if score < lowest_score:
            lowest_score = score
            lowest_match = preference

    return lowest_score, lowest_match
