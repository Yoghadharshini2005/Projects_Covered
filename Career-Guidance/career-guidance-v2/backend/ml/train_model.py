"""
train_model.py - Train Random Forest + compare models
Run: python backend/ml/train_model.py  (from project root)
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib, os, json

BASE    = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA    = os.path.join(BASE, 'dataset', 'career_guidance_dataset_500.csv')
ML_DIR  = os.path.dirname(os.path.abspath(__file__))
MODEL   = os.path.join(ML_DIR, 'career_model.pkl')
LE_PATH = os.path.join(ML_DIR, 'career_model_le.pkl')
META    = os.path.join(ML_DIR, 'model_meta.json')

FEATURES = [
    'cgpa','math_score','physics_score','cs_score','logical_reasoning',
    'python_skill','java_skill','webdev_skill','sql_skill','dsa_skill',
    'ml_knowledge','cloud_skill','design_skill','communication',
    'leadership','creativity','problem_solving',
    'projects_count','internship','certifications','years_experience',
    'ai_interest','cyber_interest','cloud_interest',
    'web_interest','design_interest','business_interest'
]

def train():
    print("="*55)
    print("  AI Career Guidance - Model Training")
    print("="*55)
    df = pd.read_csv(DATA)
    print(f"\n[+] Dataset: {df.shape}")
    print(df['career'].value_counts().to_string())

    X = df[FEATURES].values
    le = LabelEncoder()
    y = le.fit_transform(df['career'])
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    candidates = {
        'RandomForest':       RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
        'GradientBoosting':   GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, random_state=42),
        'DecisionTree':       DecisionTreeClassifier(max_depth=12, random_state=42),
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
    }

    print("\n[+] Comparing models:")
    best_acc, best_name, best_model = 0, '', None
    for name, m in candidates.items():
        cv = cross_val_score(m, X, y, cv=5).mean()
        m.fit(X_tr, y_tr)
        acc = accuracy_score(y_te, m.predict(X_te))
        print(f"    {name:<25} CV={cv:.3f}  Test={acc:.3f}")
        if acc > best_acc:
            best_acc, best_name, best_model = acc, name, m

    print(f"\n[+] Best: {best_name} ({best_acc:.3f})")
    print(classification_report(y_te, best_model.predict(X_te), target_names=le.classes_))

    if hasattr(best_model, 'feature_importances_'):
        fi = sorted(zip(FEATURES, best_model.feature_importances_), key=lambda x: -x[1])
        print("[+] Top 10 features:")
        for f, v in fi[:10]:
            print(f"    {f:<28} {'#'*int(v*60)} {v:.4f}")

    joblib.dump(best_model, MODEL)
    joblib.dump(le, LE_PATH)
    meta = {'features': FEATURES, 'classes': list(le.classes_),
            'best_model': best_name, 'accuracy': round(best_acc, 4)}
    with open(META, 'w') as f:
        json.dump(meta, f, indent=2)
    print(f"\n[+] Saved: {MODEL}")
    print(f"[+] Meta:  {META}")
    return best_acc

if __name__ == '__main__':
    train()
