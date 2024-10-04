from keyword_matching import inform_sentence_matching
from src.dialog_system.rule_based_system import classify, checkers, current_check_order

system_talks = {
    'hello': 'Hello there!',
    'ask_preference': 'What do you like to eat?',
    'food': 'What do you like to eat?',
    'area': 'From which area do you wish to have your meal from?',
    'price': 'What is the price range you are looking for?', # we need another formulation ??
}

confirm_talks = {
    'food': 'Would you like $ as food?',
    'area': 'Would you wish to have your meal from $?',
    'price': 'Are you looking for $ food?',
}

no_preferences_words = ['doesnt matter', 'does not matter', 'dont care', 'anything', 'any', 'i do not care', 'i dont care', 'i dont mind', 'what ever']

# Preference based on money:
money_based_preference_words = ['cheap', 'expensive', 'moderate', 'moderately']

# Preference based on location:
location_based_preference_words = ['town', 'south', 'north', 'east', 'west', 'part of town', 'center', 'area']

# Preference based on country:
country_based_preference_words = ['swiss', 'vietnam', 'afghan', 'spanish', 'scandinavian', 'german', 'italian', 'hungarian', 'asian', 'caribbean', 'indian', 'leban', 'carraibean','vietnamese', 'korean', 'russian', 'brazilian', 'malaysian', 'jamaican', 'eritrean', 'moroccan','scandanavian', 'signaporian',  'cuban', 'japanese', 'cuban', 'chinese', 'mexican', 'basque','african', 'french', 'scottish', 'airatarin', 'aristrain', 'arotrian', 'airitran', 'chineese', 'singapore', 'singaporean', 'english', 'indonesian''lebanese', 'venesian', 'romanian', 'welsh', 'swedish', 'irish', 'greek','catalan', 'catalanian', 'catalania', 'danish','american', 'cantonese', 'thai', 'british', 'tuscan', 'mediterranean', 'portuguese', 'european', 'turkish', 'australian', 'austria', 'austrian','belgium']

# Preference based on category:
category_based_preference_words = ['world', 'venetian', 'vegetarian', 'vegitarian', 'steakhouse', 'international', 'creative', 'crossover', 'gastropub','barbecue', 'bistro', 'unusual', 'traditional', 'seafood', 'canape', 'canapes', 'christmas', 'halal', 'steak house',]

inform_patterns = {
    'food': category_based_preference_words + country_based_preference_words,
    'area': location_based_preference_words,
    'price': money_based_preference_words,
}

### Test the sentence classifier with a chat

print()

variables = {
    'food': None,
    'area': None,
    'price': None,
}

print('System: ' + system_talks['hello'])

while True:
    if len(list(filter(lambda x: x is None, variables.values()))) == 0:
        print('Your done!')
        break

    variables_set = 0

    # Ask the user for input
    user_input = input("You: ").lower()

    # Exit the loop if the user types 'bye'
    if user_input == 'exit':
        break

    # Process the user's input
    act = classify(user_input.lower(), dict(zip(current_check_order, [checkers[act] for act in current_check_order]))) # do classification

    if act == 'inform':
        for variable, inform_pattern in inform_patterns.items():
            if variables[variable] is not None:
                continue

            score, value = inform_sentence_matching(inform_pattern, user_input)

            if value is None:
                continue

            print(score, value)

            if score == 0:
                variables[variable] = value
                variables_set += 1
            elif score > 0:
                print('System: ' + confirm_talks[variable].replace('$', value))
                confirm = input('You: ')

                if confirm == 'yes':
                    variables[variable] = value
                    variables_set += 1

        if variables_set == 0:
            print('System: I did not understand your input.')
    else:
        for variable, value in variables.items():
            if value is None:
                print('System: ' + system_talks[variable])
                break

print(variables)