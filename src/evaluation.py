from sklearn.metrics import accuracy_score, classification_report

def evaluate_models(models_dict, X_test, y_test):
    results = {}

    for name, model in models_dict.items():
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        report = classification_report(y_test, preds, output_dict=True)
        results[name] = {
            "accuracy": acc,
            "classification_report": report
        }

    return results
