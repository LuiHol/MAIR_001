import pickle
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from src.data.preprocess_data import train_x, train_y

def trainNNModel(train_x, train_y, filename):
    print("Training Neural Network Model (MLPClassifier)...")

    nn_model = MLPClassifier(hidden_layer_sizes=(100, 100), activation='relu', solver='adam', max_iter=200, random_state=42)
    nn_model.fit(train_x, np.argmax(train_y, axis=1))

    with open(filename, 'wb') as f:
        pickle.dump(nn_model, f)
    print(f"NN_model saved to {filename}")


def trainDecisionTree(train_x, train_y, filename):
    print("Training Decision Tree Model...")

    dt_clf = DecisionTreeClassifier(random_state=42)
    dt_clf.fit(train_x, np.argmax(train_y, axis=1))

    with open(filename, 'wb') as f:
        pickle.dump(dt_clf, f)
    print(f"Decision Tree model saved to {filename}")

if __name__ == '__main__':
    trainNNModel(train_x, train_y, filename='nn_model.pkl')
    trainDecisionTree(train_x, train_y, filename='dt_model.pkl')
