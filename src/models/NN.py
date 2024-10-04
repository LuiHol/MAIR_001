## feed forward Neural Network using Keras
import random
import numpy as np
import keras
from keras import layers
from keras.utils import to_categorical

model = None
TRAINING_RATIO = 0.85 # training ratio

bow_vocab = []
data_preproc = []
train_y, train_x, test_y, test_x = [], [], [], []
# one-hot encode the dialog acts
acts = [
    "negate",
    "affirm",
    "thankyou",
    "reqalts",
    "hello",
    "request",
    "restart",
    "repeat",
    "bye",
    "inform",
    "reqmore",
    "ack",
    "null",
    "deny",
    "confirm"
]
# preprocessing
def preprocessing():
    """Preprocessing the data"""
    print("preprocessing")
    with open("../data/dialog_acts.txt", "r") as file:
        data_raw = file.readlines()


    for line in data_raw:
        # remove "\n", set everything to lowercase and separate the label from the utterance
        line_proc = line.strip().lower().split(" ", 1)

        # get the bow representation of the line by 
        # splitting on the space and counting occurrences of each word
        line_split = line_proc[1].split(" ")
        line_bow = {}
        for word in line_split:
            if word not in line_bow.keys():
                line_bow[word] = 1
            else:
                line_bow[word] += 1

            # alter the global bow vocabulary
            if word not in bow_vocab:
                bow_vocab.append(word)

        data_preproc.append([line_proc[0], line_bow])



    # assign a vector to each of the utterances which corresponds to 
    # how many times each word of the bow vocabulary are in the utterance
    # add 1 index to accomodate for unknown words
    emptyline = [0] * (len(bow_vocab) + 1)
    for i, line in enumerate(data_preproc):
        # loop through each utterance
        for word, count in line[1].items():
            word_index = bow_vocab.index(word)
            emptyline[word_index] = count


        data_preproc[i] = (acts.index(line[0]), emptyline)

        # reset the empty line
        emptyline = [0] * (len(bow_vocab) + 1)



    # time for training
    # shuffle the data
    # random.seed(1)
    # random.shuffle(data_preproc)
    train = data_preproc[:int(TRAINING_RATIO * len(data_preproc))]
    test = data_preproc[int(TRAINING_RATIO * len(data_preproc)):]

    global train_y, train_x, test_x, test_y
    train_y, train_x = list(zip(*train))
    train_x = np.array(train_x)
    train_y = to_categorical(np.array(train_y), num_classes=15)

    test_y, test_x = list(zip(*test))
    test_x = np.array(test_x)
    test_y = to_categorical(np.array(test_y), num_classes=15)
    print("end of preprocessing")

def trainModel():
    print("training model")
    # feed forward neural network
    global model

    # model = keras.Sequential()
    # model.add(keras.Input(shape=(len(bow_vocab),)))
    # model.add(layers.Dense(100, activation="relu", name="layer1"))
    # model.add(layers.Dense(100, activation="relu", name="layer2"))
    # model.add(layers.Dense(len(acts), activation="softmax", name="output"))

    model = keras.Sequential(
        [
            keras.Input(shape=(len(bow_vocab) + 1,)),
            layers.Dense(100, activation="relu", name="layer1"),
            layers.Dense(100, activation="relu", name="layer2"),
            layers.Dense(len(acts), activation="softmax", name="output"),
        ]
    )


    # Compile the model
    model.compile(
        optimizer=keras.optimizers.RMSprop(),  # Optimizer
        # Loss function to minimize
        loss=keras.losses.CategoricalCrossentropy(),
        # List of metrics to monitor
        metrics=[keras.metrics.CategoricalAccuracy(), keras.metrics.F1Score(), keras.metrics.Recall(), keras.metrics.Precision()],
    )

    # model.summary()
    print(len(train_x), len(train_y))
    print("Fit model on training data")
    history = model.fit(
        train_x,
        train_y,
        batch_size=64,
        epochs=2
    )


    print("Evaluate on test data")
    results = model.evaluate(test_x, test_y, batch_size=128)
    print("test loss, test acc:", results)
    print("done training model")

    return model

    # test loss, test acc: [0.08156711608171463, 0.9775221943855286]

def utteranceToBOW(utterance):
    line_split = utterance.split(" ")

    line_bow = {}
    for word in line_split:
        if word not in line_bow.keys():
            line_bow[word] = 1
        else:
            line_bow[word] += 1

    emptyline = [0] * (len(bow_vocab) + 1)


    for word, count in line_bow.items():
        # there needs to be some check here for words that are not in the vocab.
        # maybe there needs to be a final index which basically counts the unkown words
        if word in bow_vocab:
            word_index = bow_vocab.index(word)
            emptyline[word_index] = count
        else:
            # add one to the unknown word index
            emptyline[-1] += 1
            # print("unknown word")
    return np.array(emptyline)


def predictDialogAct(utterance) -> str:
    if model is not None:
        # get the bag of words of the utterance to 
        utt_bow = utteranceToBOW(utterance)
        # print(len(utt_bow))

        return acts[np.argmax(model(utt_bow.reshape((1, -1))))]
    return "There is no model..."



## if you run just this file and don't import it, this is the code that will run
if __name__ == "__main__":
    preprocessing()

    trainModel()