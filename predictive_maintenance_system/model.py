"""
=============================================================
 Predictive Maintenance System - Model Training Script
=============================================================
 Author: Final Year Engineering Project
 Description:
   - Generates synthetic sensor data (temperature, vibration,
     pressure, rpm)
   - Trains XGBoost + Logistic Regression classifiers
   - Evaluates models with accuracy, confusion matrix, etc.
   - Saves trained model to disk using joblib
=============================================================
"""

import os
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, confusion_matrix,
    classification_report, roc_auc_score
)
from xgboost import XGBClassifier
import joblib

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. GENERATE SYNTHETIC SENSOR DATASET
# ─────────────────────────────────────────────

def generate_dataset(n_samples=3000, save_path='dataset/sensor_data.csv'):
    """
    Creates realistic synthetic sensor data for 3 machine conditions:
      0 = Healthy  → normal operating range
      1 = Warning  → slightly elevated readings
      2 = Failure  → critical readings
    """
    np.random.seed(42)
    n_each = n_samples // 3

    def make_samples(n, label,
                     temp_range, vib_range, pres_range, rpm_range,
                     noise=1.0):
        temp      = np.random.uniform(*temp_range, n) + np.random.normal(0, noise*2, n)
        vibration = np.random.uniform(*vib_range,  n) + np.random.normal(0, noise*0.5, n)
        pressure  = np.random.uniform(*pres_range, n) + np.random.normal(0, noise*1.5, n)
        rpm       = np.random.uniform(*rpm_range,  n) + np.random.normal(0, noise*20,  n)
        labels    = np.full(n, label)
        return np.column_stack([temp, vibration, pressure, rpm, labels])

    healthy = make_samples(n_each, 0,
                           temp_range=(40, 65),
                           vib_range=(0.1, 0.5),
                           pres_range=(90, 110),
                           rpm_range=(1400, 1600))

    warning = make_samples(n_each, 1,
                           temp_range=(65, 85),
                           vib_range=(0.5, 1.2),
                           pres_range=(75, 95),
                           rpm_range=(1200, 1450),
                           noise=2.0)

    failure = make_samples(n_each, 2,
                           temp_range=(85, 120),
                           vib_range=(1.2, 3.0),
                           pres_range=(50, 78),
                           rpm_range=(800, 1200),
                           noise=3.0)

    data = np.vstack([healthy, warning, failure])
    np.random.shuffle(data)

    df = pd.DataFrame(data, columns=[
        'temperature', 'vibration', 'pressure', 'rpm', 'label'
    ])
    df['label'] = df['label'].astype(int)

    # Clip to realistic bounds
    df['temperature'] = df['temperature'].clip(20, 140)
    df['vibration']   = df['vibration'].clip(0.0, 5.0)
    df['pressure']    = df['pressure'].clip(30, 130)
    df['rpm']         = df['rpm'].clip(500, 2000)

    # Intentionally inject ~2% missing values for realism
    for col in ['temperature', 'vibration', 'pressure', 'rpm']:
        mask = np.random.rand(len(df)) < 0.02
        df.loc[mask, col] = np.nan

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"[✓] Dataset saved → {save_path}  ({len(df)} rows)")
    return df


# ─────────────────────────────────────────────
# 2. DATA PREPROCESSING
# ─────────────────────────────────────────────

def preprocess(df):
    """
    Cleans and prepares the dataset:
      - Fills missing values with column median
      - Scales features using StandardScaler
      - Returns train/test splits + fitted scaler
    """
    print(f"\n[→] Missing values before cleaning:\n{df.isnull().sum()}")

    # Fill missing values with column median (robust to outliers)
    for col in ['temperature', 'vibration', 'pressure', 'rpm']:
        df[col] = df[col].fillna(df[col].median())

    print(f"[✓] Missing values after cleaning:\n{df.isnull().sum()}")

    X = df[['temperature', 'vibration', 'pressure', 'rpm']].values
    y = df['label'].values

    # Normalise features (mean=0, std=1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\n[✓] Train samples: {len(X_train)} | Test samples: {len(X_test)}")
    return X_train, X_test, y_train, y_test, scaler


# ─────────────────────────────────────────────
# 3. TRAIN MODELS
# ─────────────────────────────────────────────

def train_models(X_train, y_train):
    """Trains XGBoost and Logistic Regression models."""

    # ── XGBoost (main model) ──────────────────
    xgb_model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric='mlogloss',
        random_state=42
    )
    xgb_model.fit(X_train, y_train)
    print("[✓] XGBoost trained")

    # ── Logistic Regression (baseline) ───────
    lr_model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )
    lr_model.fit(X_train, y_train)
    print("[✓] Logistic Regression trained")

    return xgb_model, lr_model


# ─────────────────────────────────────────────
# 4. EVALUATE MODELS
# ─────────────────────────────────────────────

def evaluate(model, X_test, y_test, name="Model"):
    """Prints accuracy, classification report, and confusion matrix."""
    y_pred = model.predict(X_test)
    acc    = accuracy_score(y_test, y_pred)

    print(f"\n{'='*50}")
    print(f" {name} — Evaluation Report")
    print(f"{'='*50}")
    print(f" Accuracy : {acc*100:.2f}%")
    print(f"\n{classification_report(y_test, y_pred, target_names=['Healthy','Warning','Failure'])}")

    return acc, y_pred


# ─────────────────────────────────────────────
# 5. VISUALISE & SAVE PLOTS
# ─────────────────────────────────────────────

def save_plots(df, xgb_model, X_test, y_test, y_pred_xgb, y_pred_lr):
    """Generates and saves all visualisation plots."""
    os.makedirs('static/img', exist_ok=True)

    label_map  = {0: 'Healthy', 1: 'Warning', 2: 'Failure'}
    colors_map = {'Healthy': '#22c55e', 'Warning': '#f59e0b', 'Failure': '#ef4444'}
    df['condition'] = df['label'].map(label_map)

    # ── Plot 1: Temperature vs Condition ─────
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    for cond, grp in df.groupby('condition'):
        ax.hist(grp['temperature'], bins=40, alpha=0.75,
                label=cond, color=colors_map[cond], edgecolor='none')
    ax.set_xlabel('Temperature (°C)', color='#cbd5e1')
    ax.set_ylabel('Count', color='#cbd5e1')
    ax.set_title('Temperature Distribution by Machine Condition', color='white', fontsize=13)
    ax.tick_params(colors='#94a3b8')
    ax.legend(facecolor='#1e293b', labelcolor='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#334155')
    plt.tight_layout()
    plt.savefig('static/img/temperature_dist.png', dpi=100, bbox_inches='tight')
    plt.close()

    # ── Plot 2: Vibration Trends ──────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    sample = df.sample(300, random_state=1).sort_index()
    c_list = [colors_map[c] for c in sample['condition']]
    ax.scatter(range(len(sample)), sample['vibration'],
               c=c_list, s=25, alpha=0.8)
    ax.set_xlabel('Sample Index', color='#cbd5e1')
    ax.set_ylabel('Vibration (g)', color='#cbd5e1')
    ax.set_title('Vibration Trends (Sample)', color='white', fontsize=13)
    ax.tick_params(colors='#94a3b8')
    for spine in ax.spines.values():
        spine.set_edgecolor('#334155')
    from matplotlib.patches import Patch
    legend_elements = [Patch(fc=colors_map[c], label=c) for c in ['Healthy','Warning','Failure']]
    ax.legend(handles=legend_elements, facecolor='#1e293b', labelcolor='white')
    plt.tight_layout()
    plt.savefig('static/img/vibration_trends.png', dpi=100, bbox_inches='tight')
    plt.close()

    # ── Plot 3: Confusion Matrix (XGBoost) ───
    cm = confusion_matrix(y_test, y_pred_xgb)
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    sns.heatmap(cm, annot=True, fmt='d',
                xticklabels=['Healthy','Warning','Failure'],
                yticklabels=['Healthy','Warning','Failure'],
                cmap='Blues', ax=ax,
                linewidths=0.5, linecolor='#334155')
    ax.set_xlabel('Predicted', color='#cbd5e1')
    ax.set_ylabel('Actual', color='#cbd5e1')
    ax.set_title('XGBoost — Confusion Matrix', color='white', fontsize=13)
    ax.tick_params(colors='#cbd5e1')
    plt.tight_layout()
    plt.savefig('static/img/confusion_matrix.png', dpi=100, bbox_inches='tight')
    plt.close()

    # ── Plot 4: Feature Importance ────────────
    feat_names = ['Temperature', 'Vibration', 'Pressure', 'RPM']
    importance = xgb_model.feature_importances_
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    bars = ax.barh(feat_names, importance,
                   color=['#38bdf8','#818cf8','#34d399','#fb923c'])
    ax.set_xlabel('Importance Score', color='#cbd5e1')
    ax.set_title('XGBoost Feature Importance', color='white', fontsize=13)
    ax.tick_params(colors='#94a3b8')
    for spine in ax.spines.values():
        spine.set_edgecolor('#334155')
    for bar, val in zip(bars, importance):
        ax.text(val + 0.005, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center', color='white', fontsize=9)
    plt.tight_layout()
    plt.savefig('static/img/feature_importance.png', dpi=100, bbox_inches='tight')
    plt.close()

    # ── Plot 5: Model Accuracy Comparison ────
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    accs_xgb = accuracy_score(y_test, y_pred_xgb) * 100
    accs_lr  = accuracy_score(y_test, y_pred_lr)  * 100
    bars = ax.bar(['XGBoost', 'Logistic Reg.'], [accs_xgb, accs_lr],
                  color=['#38bdf8', '#818cf8'], width=0.4)
    ax.set_ylim(0, 105)
    ax.set_ylabel('Accuracy (%)', color='#cbd5e1')
    ax.set_title('Model Accuracy Comparison', color='white', fontsize=13)
    ax.tick_params(colors='#94a3b8')
    for spine in ax.spines.values():
        spine.set_edgecolor('#334155')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{bar.get_height():.1f}%', ha='center', color='white', fontsize=11)
    plt.tight_layout()
    plt.savefig('static/img/model_comparison.png', dpi=100, bbox_inches='tight')
    plt.close()

    print("[✓] All plots saved → static/img/")


# ─────────────────────────────────────────────
# 6. SAVE MODEL + SCALER + METRICS
# ─────────────────────────────────────────────

def save_artifacts(xgb_model, scaler, metrics):
    os.makedirs('saved_model', exist_ok=True)
    joblib.dump(xgb_model, 'saved_model/xgb_model.pkl')
    joblib.dump(scaler,    'saved_model/scaler.pkl')
    with open('saved_model/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    print("[✓] Model, scaler & metrics saved → saved_model/")


# ─────────────────────────────────────────────
# 7. MAIN ENTRY POINT
# ─────────────────────────────────────────────

def main():
    print("\n" + "="*55)
    print("  Predictive Maintenance System — Model Training")
    print("="*55)

    # Step 1 – Generate / load data
    csv_path = 'dataset/sensor_data.csv'
    if os.path.exists(csv_path):
        print(f"[→] Loading existing dataset from {csv_path}")
        df = pd.read_csv(csv_path)
    else:
        df = generate_dataset(n_samples=3000, save_path=csv_path)

    print(f"\n[→] Dataset shape : {df.shape}")
    print(f"[→] Class distribution:\n{df['label'].value_counts()}")

    # Step 2 – Preprocess
    X_train, X_test, y_train, y_test, scaler = preprocess(df.copy())

    # Step 3 – Train
    xgb_model, lr_model = train_models(X_train, y_train)

    # Step 4 – Evaluate
    acc_xgb, y_pred_xgb = evaluate(xgb_model, X_test, y_test, "XGBoost")
    acc_lr,  y_pred_lr  = evaluate(lr_model,  X_test, y_test, "Logistic Regression")

    # Step 5 – Plots
    save_plots(df, xgb_model, X_test, y_test, y_pred_xgb, y_pred_lr)

    # Step 6 – Save artifacts
    metrics = {
        'xgb_accuracy':  round(float(acc_xgb), 4),
        'lr_accuracy':   round(float(acc_lr),  4),
        'train_samples': int(len(X_train)),
        'test_samples':  int(len(X_test)),
        'features':      ['temperature', 'vibration', 'pressure', 'rpm'],
        'classes':       ['Healthy', 'Warning', 'Failure']
    }
    save_artifacts(xgb_model, scaler, metrics)

    print(f"\n{'='*55}")
    print(f"  ✓ XGBoost Accuracy        : {acc_xgb*100:.2f}%")
    print(f"  ✓ Logistic Reg. Accuracy  : {acc_lr*100:.2f}%")
    print(f"  ✓ Training complete! Run app.py to start the server.")
    print(f"{'='*55}\n")


if __name__ == '__main__':
    main()
