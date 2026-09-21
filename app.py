"""
Student Performance Prediction - Modular Pipeline & Gradio Application
========================================================================
Author : Kishore Kumar
Colab  : https://colab.research.google.com/drive/1-b6Jf6io10mEnceh52oc64c1i2DpLHGD?usp=sharing

This script provides an end-to-end execution of the machine learning pipeline:
1. Ingestion & Preprocessing (Dynamic Encoding & Scaling)
2. Model Benchmarking (Linear Regression, Random Forest, XGBoost)
3. Model Selection & Feature Importance Analysis
4. Interactive Local Gradio Web Interface
"""

import os
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import gradio as gr


def run_pipeline(csv_path: str = "sample_data.csv", target_col: str = "Grade", share_ui: bool = False):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at: {csv_path}. Please provide a valid CSV file.")

    print(f"[1/4] Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"      Rows: {len(df)}, Columns: {len(df.columns)}")

    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not present in dataset.")

    # 1. Cleaning & Encoding
    print("[2/4] Preprocessing data (cleaning & encoding)...")
    df = df.dropna()

    label_encoders = {}
    for col in df.select_dtypes(include="object").columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    feature_names = df.drop(target_col, axis=1).columns.tolist()
    X = df.drop(target_col, axis=1)
    y = df[target_col]

    # Standardization
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train / Test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # 2. Model Training & Comparison
    print("[3/4] Training candidate regression models...")
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(random_state=42),
        "XGBoost": XGBRegressor(eval_metric="rmse", random_state=42)
    }

    results = {}
    preds = {}

    for name, m in models.items():
        m.fit(X_train, y_train)
        pred = m.predict(X_test)
        preds[name] = pred
        results[name] = r2_score(y_test, pred)

    results_df = pd.DataFrame(results.items(), columns=["Model", "Test R2"]).sort_values(
        by="Test R2", ascending=False
    )
    print("\n" + "=" * 45)
    print("           MODEL BENCHMARK RESULTS")
    print("=" * 45)
    for _, row in results_df.iterrows():
        print(f"  {row['Model']:<22} | Test R2: {row['Test R2']:>8.4f}")
    print("=" * 45)

    best_name = results_df.iloc[0]["Model"]
    best_model = models[best_name]
    best_pred = preds[best_name]
    best_r2 = r2_score(y_test, best_pred)
    best_mse = mean_squared_error(y_test, best_pred)

    print(f"\n[+] Selected Model : {best_name}")
    print(f"    R^2 Score      : {best_r2:.4f}")
    print(f"    MSE            : {best_mse:.4f}")

    # Feature Importance (Random Forest)
    rf = models["Random Forest"]
    importances = rf.feature_importances_
    imp_df = pd.DataFrame({"Feature": feature_names, "Importance": importances}).sort_values(
        by="Importance", ascending=False
    )
    print("\n[+] Top Predictive Features:")
    for _, row in imp_df.head(5).iterrows():
        print(f"    - {row['Feature']:<20}: {row['Importance']:.4f}")

    # 3. Gradio Interface Construction
    print("\n[4/4] Launching Gradio Web Interface...")

    def predict_grade(*args):
        input_dict = {}
        for idx, col in enumerate(feature_names):
            input_dict[col] = args[idx]

        row_df = pd.DataFrame([input_dict])

        for col in feature_names:
            if col in label_encoders:
                row_df[col] = label_encoders[col].transform(row_df[col])

        scaled_row = scaler.transform(row_df[feature_names])
        predicted_value = best_model.predict(scaled_row)
        return round(float(predicted_value[0]), 2)

    gradio_inputs = []
    for col in feature_names:
        if col in label_encoders:
            choices = label_encoders[col].classes_.tolist()
            gradio_inputs.append(gr.Dropdown(choices, label=col, value=choices[0]))
        elif col == "Weekly_Study_Hours":
            gradio_inputs.append(gr.Number(label=col, value=15))
        elif np.issubdtype(df[col].dtype, np.number):
            median_val = float(df[col].median())
            gradio_inputs.append(gr.Number(label=col, value=median_val))
        else:
            gradio_inputs.append(gr.Textbox(label=col, value=""))

    demo = gr.Interface(
        fn=predict_grade,
        inputs=gradio_inputs,
        outputs=gr.Number(label="Predicted Grade"),
        title="Student Performance Prediction System",
        description=(
            "Predict academic grades dynamically using the benchmarked Machine Learning model.\n\n"
            f"**Selected Model:** {best_name} | **Test R²:** {best_r2:.4f} | **MSE:** {best_mse:.4f}"
        ),
        theme="default"
    )

    demo.launch(share=share_ui)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Student Performance Prediction Pipeline & UI")
    parser.add_argument("--data", type=str, default="sample_data.csv", help="Path to student performance CSV")
    parser.add_argument("--target", type=str, default="Grade", help="Target column name to predict")
    parser.add_argument("--share", action="store_true", help="Generate public temporary Gradio link")
    args = parser.parse_args()

    run_pipeline(csv_path=args.data, target_col=args.target, share_ui=args.share)
