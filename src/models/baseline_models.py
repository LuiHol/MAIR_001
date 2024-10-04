from src.data.preprocess_data import load_data
from src import DIALOG_ACTS_FILE

df = load_data(DIALOG_ACTS_FILE)

unique_dialog_acts = df['dialog_act'].unique()
majority_class = unique_dialog_acts[0]

def baseline_model1_majority_class():
    return majority_class

# baseline_model2:
keywords = {
    'inform': ['im looking for', 'i need a', 'i want a', 'restaurant', 'cheap', 'expensive', 'world', 'town', 'food', 'venetian', 'vegetarian', 'swiss', 'steakhouse', 'vegitarian', 'vietnam', 'moderate', 'moderately', 'afghan', 'spanish', 'international', 'scandinavian', 'german', 'creative', 'south', 'north', 'east', 'west', 'italian', 'hungarian', 'crossover', 'part of town', 'asian', 'caribbean', 'indian', 'leban', 'carraibean', 'center', 'area', 'vietnamese', 'japanese', 'cuban', 'chinese', 'mexican', 'basque', 'african', 'french', 'scottish', 'airatarin', 'aristrain', 'arotrian', 'airitran', 'gastropub', 'american', 'cantonese', 'thai', 'british', 'tuscan', 'anything', 'any', 'mediterranean', 'portuguese', 'european', 'turkish', 'australian', 'austria', 'austrian', 'barbecue', 'belgium', 'bistro', 'korean', 'brazilian', 'malaysian', 'cuban', 'unusual', 'russian', 'traditional', 'welsh', 'swedish', 'irish', 'greek', 'seafood', 'canape', 'canapes', 'catalan', 'catalanian', 'catalania', 'danish', 'doesnt matter', 'does not matter', 'dont care', 'jamaican', 'eritrean', 'signaporian', 'christmas', 'scandanavian', 'halal', 'moroccan', 'i do not care', 'i dont care', 'i dont mind', 'what ever', 'lebanese', 'venesian', 'romanian', 'steak house', 'chineese', 'singapore', 'singaporean', 'english', 'indonesian'],
    'confirm': ['do they serve', 'do they have', 'does it serve', 'does it have', 'is it', 'is it in', 'is that', 'is this', 'is there', 'okay', 'uh', 'um'],
    'affirm': ['correct', 'yes', 'ye', 'yea', 'yeah', 'perfect', 'right', 'uh huh', 'uh yes', 'mmhm'],
    'request': ['whats', 'what', 'where', 'could i have', 'may i have', 'can i get', 'telephone', 'phone number', 'phone', 'address', 'postal code', 'post code', 'postcode', 'price', 'location', 'area', 'type of food'],
    'thankyou': ['thank you', 'thanks', 'thank'],
    'null': ['unintelligible', 'uh', 'um', 'sil', 'noise', 'cough', 'sigh', 'inaudible', 'breathing', 'system', 'tv_noise'],
    'bye': ['goodbye', 'bye', 'stop', 'thats all'],
    'reqalts': ['other', 'another', 'anything', 'any other', 'something else', 'how bout', 'how about','what about', 'next', 'are there', 'is there', 'what else'],
    'negate': ['no', 'not'],
    'hello': ['hello', 'halo', 'hi'],
    'repeat': ['repeat', 'again', 'back'],
    'ack': ['okay', 'kay', 'good', 'fine', 'that I will do', 'will take that one'],
    'restart': ['restart', 'start over', 'reset', 'start again'],
    'deny': ['change', 'dont', 'not', 'no', 'wrong'],
    'reqmore': ['more'],
}

def baseline_model2_keyword_matching(utterance):
    utterance_lower = utterance.lower()
    for dialog_act, words in keywords.items():
        for word in words:
            if word in utterance_lower:
                return dialog_act
    return majority_class

