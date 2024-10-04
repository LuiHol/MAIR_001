import pickle
import numpy as np
from sklearn.metrics import classification_report
from src.data.preprocess_data import test_x, test_y, acts, load_data
from src.models.baseline_models import baseline_model1_majority_class, baseline_model2_keyword_matching, majority_class

df = load_data()

def load_model(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded from {filename}")
    return model

def evaluate_model(model, test_x, test_y):
    predictions = model.predict(test_x)
    test_y_labels = np.argmax(test_y, axis=1)

    report = classification_report(test_y_labels, predictions, target_names=acts)

    return report

def evaluate_majority(df):
    majority_class = baseline_model1_majority_class()
    predictions = [majority_class] * len(df)
    true_labels = df['dialog_act']

    report = classification_report(true_labels, predictions, target_names=acts)
    return report

def evaluate_rule_based(df):
    predictions = [baseline_model2_keyword_matching(utterance) for utterance in df['utterance_content']]
    true_labels = df['dialog_act']

    report = classification_report(true_labels, predictions, target_names=acts)
    return report

def save_to_file(reports, filename):
    with open(filename, 'w') as f:
        for model, report in reports.items():
            f.write(f"Model: {model}\n")
            f.write(report)
            f.write("\n")
        print(f"Classification report saved to {filename}")

if __name__ == '__main__':
    nn_model = load_model('nn_model.pkl')
    dt_model = load_model('dt_model.pkl')

    reports = {}
    reports["NNmodel"] = evaluate_model(nn_model, test_x, test_y)
    reports["DTmodel"] = evaluate_model(dt_model, test_x, test_y)
    reports["Majority Baseline"] = evaluate_majority(df)
    reports["Rule Based"] = evaluate_rule_based(df)

    save_to_file(reports, filename='model_classifications.txt')