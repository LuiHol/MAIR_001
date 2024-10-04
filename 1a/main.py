from src import preprocess_data, trainNNModel, trainDecisionTree
from src import baseline_model1_majority_class, baseline_model2_keyword_matching


def test_baseline1():
    print("\nbaseline_model1 testing:")
    user_input = input("Please input utterance (input 'exit' to exit):")
    while user_input.lower() != 'exit':
        print("result:", baseline_model1_majority_class(user_input))
        user_input = input("Please input utterance (input 'exit' to exit):")
    return 0

def test_baseline2():
    print("\nbaseline_model2 testing:")
    user_input = input("Please input utterance (input 'exit' to exit):")
    while user_input.lower() != 'exit':
        print("result:", baseline_model2_keyword_matching(user_input))
        user_input = input("Please input utterance (input 'exit' to exit):")

def test_ML_models():
    train_x, train_y, test_x, test_y = preprocess_data()
    nn_model = trainNNModel(train_x, train_y, test_x, test_y)
    tree_model = trainDecisionTree(train_x, train_y, test_x, test_y)

if __name__ == '__main__':
    test_baseline1()
    test_baseline2()
    test_ML_models()

# Neural Network Test loss, Test accuracy: [0.08314337581396103, 0.9783063530921936]
# Decision Tree Test Accuracy: 0.9814427600627287
# Decision Tree Classification Report:
#               precision    recall  f1-score   support
#
#       negate       1.00      1.00      1.00        69
#       affirm       0.99      1.00      1.00       180
#     thankyou       1.00      1.00      1.00       474
#      reqalts       0.97      0.97      0.97       279
#        hello       1.00      1.00      1.00        14
#      request       0.99      1.00      0.99       972
#      restart       1.00      0.50      0.67         2
#       repeat       1.00      0.67      0.80         3
#          bye       0.97      1.00      0.99        35
#       inform       0.99      0.98      0.98      1532
#      reqmore       1.00      1.00      1.00         1
#          ack       0.67      0.80      0.73         5
#         null       0.90      0.95      0.92       232
#         deny       0.86      1.00      0.92         6
#      confirm       0.82      0.82      0.82        22
#
#     accuracy                           0.98      3826
#    macro avg       0.94      0.91      0.92      3826
# weighted avg       0.98      0.98      0.98      3826
