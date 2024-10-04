# acts = {}
import random
import json

y = []
X = []

with open("dialog_acts.dat", "r") as file:
    for line in file:
        act, sentence = line.split(' ', 1)

        X.append(sentence.strip().lower())
        y.append(act)
        # if act not in acts:
        #     acts[act] = []
        #
        # acts[act].append(sentence.strip().lower())


def word_in_sentence(rule, sentence):
    if ' ' in rule:
        words = rule.split(' ')
        n_words = len(words)
        n_words_attended = len(list(filter(lambda word: word_in_sentence(word, sentence) is True, words)))

        word_attendance = n_words_attended / n_words

        return word_attendance >= 1.0
    else:
        return rule in sentence.split(' ')


def check_sentence(sentence, rules):
    return any(word_in_sentence(rule, sentence) for rule in rules)


def is_bye(sentence):
    return check_sentence(sentence, ['goodbye', 'bye', 'stop', 'thats all'])


def is_affirm(sentence):
    return check_sentence(sentence, ['correct', 'yes', 'ye', 'yea', 'yeah', 'perfect', 'right', 'uh huh', 'uh yes', 'mmhm'])


def is_ack(sentence):
    return check_sentence(sentence, ['okay', 'kay', 'good', 'fine', 'that I will do', 'will take that one'])


def is_confirm(sentence):
    return check_sentence(sentence,['do they serve', 'do they have', 'does it serve', 'does it have', 'is it', 'is it in', 'is that', 'is this', 'is there', 'okay', 'uh', 'um'])


def is_deny(sentence):
    return check_sentence(sentence, ['change', 'dont', 'not', 'no', 'wrong'])


def is_hello(sentence):
    return check_sentence(sentence, ['hello', 'halo', 'hi'])


def is_repeat(sentence):
    return check_sentence(sentence, ['repeat', 'again', 'back'])


def is_reqalts(sentence):
    return check_sentence(sentence,['other', 'another', 'anything', 'any other', 'something else', 'how bout', 'how about','what about', 'next', 'are there', 'is there', 'what else'])


def is_negate(sentence):
    return check_sentence(sentence, ['no', 'not'])


def is_request(sentence):
    return check_sentence(sentence,['whats', 'what', 'where', 'could i have', 'may i have', 'can i get', 'telephone', 'phone number', 'phone', 'address', 'postal code', 'post code', 'postcode', 'price', 'location', 'area', 'type of food'])


def is_thankyou(sentence):
    return check_sentence(sentence, ['thank you', 'thanks', 'thank'])


def is_reqmore(sentence):
    return check_sentence(sentence, ['more'])


def is_restart(sentence):
    return check_sentence(sentence, ['restart', 'start over', 'reset', 'start again'])


def is_inform(sentence):
    return check_sentence(sentence, ['im looking for', 'i need a', 'i want a', 'restaurant', 'cheap', 'expensive', 'world', 'town', 'food', 'venetian', 'vegetarian', 'swiss', 'steakhouse', 'vegitarian', 'vietnam', 'moderate', 'moderately', 'afghan', 'spanish', 'international', 'scandinavian', 'german', 'creative', 'south', 'north', 'east', 'west', 'italian', 'hungarian', 'crossover', 'part of town', 'asian', 'caribbean', 'indian', 'leban', 'carraibean', 'center', 'area', 'vietnamese', 'japanese', 'cuban', 'chinese', 'mexican', 'basque', 'african', 'french', 'scottish', 'airatarin', 'aristrain', 'arotrian', 'airitran', 'gastropub', 'american', 'cantonese', 'thai', 'british', 'tuscan', 'anything', 'any', 'mediterranean', 'portuguese', 'european', 'turkish', 'australian', 'austria', 'austrian', 'barbecue', 'belgium', 'bistro', 'korean', 'brazilian', 'malaysian', 'cuban', 'unusual', 'russian', 'traditional', 'welsh', 'swedish', 'irish', 'greek', 'seafood', 'canape', 'canapes', 'catalan', 'catalanian', 'catalania', 'danish', 'doesnt matter', 'does not matter', 'dont care', 'jamaican', 'eritrean', 'signaporian', 'christmas', 'scandanavian', 'halal', 'moroccan', 'i do not care', 'i dont care', 'i dont mind', 'what ever', 'lebanese', 'venesian', 'romanian', 'steak house', 'chineese', 'singapore', 'singaporean', 'english', 'indonesian'])

def is_null(sentence):
    return check_sentence(sentence, ['unintelligible', 'uh', 'um', 'sil', 'noise', 'cough', 'sigh', 'inaudible', 'breathing', 'system', 'tv_noise'])

checkers = {
    "bye": is_bye,
    "affirm": is_affirm,
    "ack": is_ack,
    "confirm": is_confirm,
    "deny": is_deny,
    "hello": is_hello,
    "request": is_request,
    "repeat": is_repeat,
    "reqalts": is_reqalts,
    "restart": is_restart,
    "reqmore": is_reqmore,
    "negate": is_negate,
    "thankyou": is_thankyou,
    "inform": is_inform,
    "null": is_null,
}


def classify(sentence, checkers):
    for act, checker in checkers.items():
        if checker(sentence):
            return act

    return 'null'


with open('../../checking_order.json') as f:
    current_check_order = json.load(f)


## if you run just this file and don't import it, this is the code that will run
if __name__ == "__main__":
    print('(1) show individual act precision')
    print('(2) search for a better checking order')
    print('(3) test the classifier via a chat')
    print('')
    operation = int(input("Choose action: "))

    if operation not in [1,2,3]:
        print('Invalid')
        exit(1)

    if operation == 1:

        ### Test individual precision

        show_missing = input('You want to show missing sentences? (yes|no) ')
        show_missing = show_missing == 'yes'

        print()
        for act in checkers.keys():
            X_scoped = [sentence for a, sentence in zip(y, X) if a == act]
            accuracy = len(list(filter(lambda sentence: checkers[act](sentence), X_scoped))) / len(X_scoped)

            print(act, accuracy)

            if accuracy < 1.0:
                missed_sentences = [sentence for sentence in X_scoped if not checkers[act](sentence)]
                print()
                print('Missed sentences (' + str(len(missed_sentences)) + ')')

                if show_missing:
                    for sentence in missed_sentences:
                        print('- ' + sentence)

                print()

    elif operation == 2:

        ### Script that searches for better checking orders

        best_accuracy = 0.0

        tries = 0
        failure_threshold = int(input("Choose the failure threshold (overcome local optima): "))
        history = []

        print()
        while True:
            predict = [classify(x, dict(zip(current_check_order, [checkers[act] for act in current_check_order]))) for x in X]
            accuracy = len(list(filter(lambda y: y[0] == y[1], zip(y, predict)))) / len(predict)

            if accuracy > best_accuracy:
                best_accuracy = accuracy

                print('We achieved a better accuracy of ' + str(best_accuracy) + '! 🤌🏻')
                print('Automatically updated...')

                with open('checking_order_old.json', 'w', encoding='utf-8') as f:
                    json.dump(current_check_order, f, ensure_ascii=False, indent=4)
            else:
                tries += 1

                if tries >= failure_threshold:
                    for index1, index2 in reversed(history):
                        current_check_order[index1], current_check_order[index2] = current_check_order[index2], current_check_order[index1]

                    tries = 0
                    history = []

            index1 = random.randint(0, len(current_check_order)-1)
            index2 = random.randint(0, len(current_check_order)-1)

            history.append((index1, index2))

            current_check_order[index1], current_check_order[index2] = current_check_order[index2], current_check_order[index1]

    elif operation == 3:

        ### Test the sentence classifier with a chat

        print()
        while True:
            # Ask the user for input
            user_input = input("Ask me a question or type 'exit' to exit: ").lower()

            # Exit the loop if the user types 'bye'
            if user_input == 'exit':
                break

            # Process the user's input
            result = classify(user_input, dict(zip(current_check_order, [checkers[act] for act in current_check_order])))
            print(result)