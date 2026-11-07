"""STEP 8 - Predictive analysis  (slides 10, 16).
Trains 4 classifiers with grid search, saves a results table, confusion matrix and accuracy chart."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from config import load_clean, DATA, OUT

df = load_clean()
X = pd.read_csv(DATA / "features.csv")
Y = df["Class"].to_numpy()

X = StandardScaler().fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
print("Train:", X_train.shape, "Test:", X_test.shape)

models = {
    "Logistic Regression": (LogisticRegression(max_iter=2000),
                            {"C": [0.01, 0.1, 1], "penalty": ["l2"], "solver": ["lbfgs"]}),
    "SVM": (SVC(), {"kernel": ["linear", "rbf", "sigmoid"], "C": np.logspace(-3, 3, 5),
                    "gamma": np.logspace(-3, 3, 5)}),
    "Decision Tree": (DecisionTreeClassifier(random_state=2),
                      {"criterion": ["gini", "entropy"], "max_depth": [2, 4, 6, 8, 10],
                       "min_samples_leaf": [1, 2, 4], "min_samples_split": [2, 5, 10]}),
    "KNN": (KNeighborsClassifier(), {"n_neighbors": list(range(1, 11)), "p": [1, 2]}),
}

results, fitted = {}, {}
for name, (est, grid) in models.items():
    gs = GridSearchCV(est, grid, cv=10).fit(X_train, Y_train)
    fitted[name] = gs
    results[name] = {"CV accuracy": gs.best_score_, "Test accuracy": gs.score(X_test, Y_test)}
    print(f"\n{name}\n  best params: {gs.best_params_}\n  CV accuracy: {gs.best_score_:.4f}"
          f"\n  Test accuracy: {results[name]['Test accuracy']:.4f}")

res = pd.DataFrame(results).T.round(4)
res.to_csv(OUT / "model_results.csv")
print("\n", res)

best = res["Test accuracy"].idxmax()
print(f"\nBEST MODEL: {best}  (test accuracy {res.loc[best, 'Test accuracy']:.4f})")

cm = confusion_matrix(Y_test, fitted[best].predict(X_test))
ConfusionMatrixDisplay(cm, display_labels=["did not land", "landed"]).plot(cmap="Blues")
plt.title(f"Confusion Matrix - {best}")
plt.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight"); plt.close()

ax = res["Test accuracy"].plot(kind="bar", figsize=(7, 4), color="#1F8A8A", ylim=(0, 1))
ax.set_title("Test accuracy by model"); ax.set_ylabel("Accuracy")
plt.xticks(rotation=20); plt.tight_layout()
plt.savefig(OUT / "model_accuracy.png", dpi=150); plt.close()
print("Saved model_results.csv, confusion_matrix.png, model_accuracy.png in", OUT)
