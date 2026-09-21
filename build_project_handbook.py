from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether, HRFlowable
)

OUT = "output/pdf/Student_Performance_Prediction_Project_Handbook.pdf"

NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#1D70B8")
TEAL = colors.HexColor("#0B7285")
PALE = colors.HexColor("#EAF4FB")
INK = colors.HexColor("#243B53")
MUTED = colors.HexColor("#627D98")
GREEN = colors.HexColor("#E7F5EC")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleX", parent=styles["Title"], fontName="Helvetica-Bold",
                          fontSize=27, leading=32, textColor=NAVY, spaceAfter=12))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], fontName="Helvetica",
                          fontSize=12, leading=18, textColor=MUTED, spaceAfter=18))
styles.add(ParagraphStyle(name="H1X", parent=styles["Heading1"], fontName="Helvetica-Bold",
                          fontSize=18, leading=22, textColor=NAVY, spaceBefore=7, spaceAfter=9))
styles.add(ParagraphStyle(name="H2X", parent=styles["Heading2"], fontName="Helvetica-Bold",
                          fontSize=12, leading=15, textColor=TEAL, spaceBefore=9, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyX", parent=styles["BodyText"], fontName="Helvetica",
                          fontSize=9.4, leading=14, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName="Helvetica",
                          fontSize=8.1, leading=11, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontName="Helvetica-Bold",
                          fontSize=10, leading=14, textColor=NAVY, spaceAfter=0))
styles.add(ParagraphStyle(name="Quote", parent=styles["BodyText"], fontName="Helvetica-Oblique",
                          fontSize=10.3, leading=15, textColor=INK, leftIndent=12, rightIndent=12, spaceAfter=7))

def P(text, style="BodyX"):
    return Paragraph(text, styles[style])

def table(rows, widths, header=True):
    data = [[P(cell, "Small" if r else "Callout") for cell in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmds = [
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#C9D8E5")),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]
    if header:
        cmds += [("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), colors.white)]
    for i in range(1 if header else 0, len(rows)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0,i), (-1,i), colors.HexColor("#F7FAFC")))
    t.setStyle(TableStyle(cmds))
    return t

def callout(title, text):
    t = Table([[P(title, "Callout")], [P(text, "BodyX")]], colWidths=[17.2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PALE),
        ("BOX", (0,0), (-1,-1), 0.6, colors.HexColor("#8DB9D8")),
        ("LINEBEFORE", (0,0), (0,-1), 4, BLUE),
        ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    return t

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#C9D8E5")); canvas.line(1.55*cm, 1.25*cm, 19.45*cm, 1.25*cm)
    canvas.setFont("Helvetica", 7.8); canvas.setFillColor(MUTED)
    canvas.drawString(1.55*cm, 0.82*cm, "Student Performance Prediction | Project Handbook")
    canvas.drawRightString(19.45*cm, 0.82*cm, f"Page {doc.page}")
    canvas.restoreState()

story = []
story += [Spacer(1, 1.3*cm), P("STUDENT PERFORMANCE", "TitleX"), P("PREDICTION", "TitleX"),
          HRFlowable(width="100%", thickness=2.2, color=BLUE, spaceBefore=2, spaceAfter=14),
          P("Project handbook for learning, viva preparation, technical discussion, and self-introduction", "Subtitle")]
story += [callout("Project in one sentence", "A machine-learning regression project that learns from a student-performance CSV, compares three regression models, selects the model with the best test R-squared score, and exposes it through a Gradio prediction interface."), Spacer(1, 14)]
story += [P("What this handbook is based on", "H2X"),
          P("This document is grounded in the submitted notebook <b>STUDENT_PERFORMANCE.ipynb</b>. It distinguishes what was actually implemented from reasonable future improvements, so you can explain the project accurately."),
          P("Notebook scope: data is uploaded in Google Colab, processed in memory, evaluated on one train/test split, then served through a temporary public Gradio link. The uploaded CSV itself and the trained model file are not stored in the project folder."),
          Spacer(1, 12), P("Quick facts", "H2X"),
          table([
              ["Area", "Implemented project choice"],
              ["Problem type", "Supervised machine learning - regression"],
              ["Prediction target", "Grade"],
              ["Selection metric", "Test R-squared (R2)"],
              ["Reported best model", "Random Forest Regressor"],
              ["Reported test performance", "R2 = 0.1269; MSE = 4.7610"],
              ["User interface", "Gradio web interface"],
              ["Execution environment", "Google Colab"],
          ], [4.5*cm, 12.7*cm]), PageBreak()]

story += [P("1. Project story and problem framing", "H1X"),
          P("The project answers a practical question: <b>given the available information about a student, what grade is the model likely to predict?</b> Rather than assigning a fixed rule, the system learns patterns from historical rows in a CSV file."),
          P("Each row represents one student record. The column named <b>Grade</b> is the output to predict. Every other column becomes an input feature. The notebook does not hard-code the full list of input columns; it discovers them from the uploaded dataset. One feature explicitly handled in the UI is <b>Weekly_Study_Hours</b>."),
          P("Why regression?", "H2X"),
          P("The project predicts a numeric grade, so it uses regression algorithms. If the goal were only categories such as pass/fail or low/medium/high performance, it would instead be a classification project."),
          P("End-to-end workflow", "H2X"),
          table([
              ["Stage", "What happens", "Why it matters"],
              ["1. Upload", "A CSV is uploaded in Colab and read with pandas.", "Brings project data into the notebook."],
              ["2. Clean", "Rows containing missing values are removed with dropna().", "Ensures training code receives complete rows."],
              ["3. Encode", "Every text/object column is converted to integer labels with LabelEncoder.", "Regression models require numeric input."],
              ["4. Define data", "X = all columns except Grade; y = Grade.", "Separates predictors from the answer."],
              ["5. Scale", "StandardScaler is fitted to X and transforms X.", "Puts numeric features on a comparable scale."],
              ["6. Split", "80% train / 20% test, random_state=42.", "Holds out data for evaluation."],
              ["7. Train", "Three models fit the same training partition.", "Enables fair comparison."],
              ["8. Evaluate", "Predictions on test data are scored with R2; MSE is reported for the selected model.", "Measures generalization on held-out rows."],
              ["9. Serve", "The selected model is called from a Gradio interface.", "Lets a user enter a new student profile."],
          ], [2.3*cm, 8.2*cm, 6.7*cm]), PageBreak()]

story += [P("2. Data preparation and feature handling", "H1X"),
          P("The data-processing pipeline is simple and dynamic: it adapts to the columns in the uploaded CSV, provided that a <b>Grade</b> column exists."),
          P("Implemented transformations", "H2X"),
          table([
              ["Operation", "Code-level behavior", "How to explain it"],
              ["Missing values", "df.dropna()", "I removed incomplete records instead of imputing values."],
              ["Categorical data", "One LabelEncoder per object-type column", "I transformed text categories into numeric codes and kept the encoders for later UI input conversion."],
              ["Feature / target split", "X = df.drop('Grade'); y = df['Grade']", "Grade is never used as an input feature."],
              ["Scaling", "StandardScaler on X", "I standardized input features before the train/test split in the notebook."],
              ["Data split", "train_test_split(test_size=0.2, random_state=42)", "I reserve 20% of rows for testing and fix the random seed for repeatability."],
          ], [3.3*cm, 7.3*cm, 6.6*cm]),
          Spacer(1, 8), callout("Important technical note for a strong explanation", "The current notebook fits StandardScaler on the full feature dataset before the train/test split. That lets information from the test distribution influence scaling, which is called data leakage. A stronger version would split first, fit the scaler only on X_train, and then transform X_train and X_test. This does not invalidate the prototype, but it is an important limitation to acknowledge."),
          P("Encoding details", "H2X"),
          P("LabelEncoder assigns an integer code to each category in a text column. The notebook saves each encoder in a dictionary, then uses the same encoder during prediction. This consistency is essential: the UI must use exactly the mappings learned during training."),
          P("Caution: label encoding gives categories a numeric order that may not be meaningful. Tree models can often work with it, but for linear regression, one-hot encoding is usually more appropriate for nominal categories. Unknown categories submitted later will cause LabelEncoder.transform() to fail unless handling is added."), PageBreak()]

story += [P("3. Models, selection, and evaluation", "H1X"),
          P("All three models train on the same training set and predict the same held-out test set. The project selects the highest R2 score as the best model."),
          table([
              ["Model", "What it learns", "Why it was included"],
              ["Linear Regression", "A linear relationship between features and Grade.", "A simple baseline that is fast and interpretable."],
              ["Random Forest Regressor", "An ensemble of decision trees; averages their predictions.", "Can capture non-linear patterns and feature interactions."],
              ["XGBRegressor", "Gradient-boosted decision trees trained sequentially to correct earlier errors.", "A powerful boosting-based alternative; configured with eval_metric='rmse'."],
          ], [4.1*cm, 7.4*cm, 5.7*cm]),
          P("Observed evaluation results", "H2X"),
          table([
              ["Model", "Test R2", "Interpretation"],
              ["Linear Regression", "-0.072443", "Worse than simply predicting the test-set mean."],
              ["Random Forest", "0.126913", "Highest R2 among the three; selected by the notebook."],
              ["XGBoost", "-0.110290", "Worse than the mean baseline on this split."],
          ], [4.8*cm, 3.1*cm, 9.3*cm]),
          P("Final reported metrics for the selected model", "H2X"),
          table([["Metric", "Value", "Meaning"], ["R2", "0.1269128216310509", "The model explains about 12.7% of variance on this test split."], ["MSE", "4.760972413793104", "Average squared prediction error; lower is better, but its scale is grade-squared units."]], [3*cm, 5.2*cm, 9*cm]),
          callout("Honest conclusion", "Random Forest is the best of the implemented candidates, but the R2 is low. The model is a working baseline, not a highly accurate production predictor. The likely next steps are better data quality, more informative features, cross-validation, tuning, and leakage-safe preprocessing."), PageBreak()]

story += [P("4. Model interpretation and application module", "H1X"),
          P("Feature importance", "H2X"),
          P("After comparison, the notebook separately trains a new RandomForestRegressor and reads its feature_importances_. It makes a bar chart ranking the input columns by how much they helped reduce impurity across that forest's trees. This is a useful global importance view, not a statement that one feature causes a grade."),
          P("One implementation nuance: the feature-importance forest is newly trained with default randomness, rather than reusing best_model. It will usually be similar, but its importance values are not guaranteed to match the selected Random Forest exactly. For a polished version, set random_state and reuse or persist the selected model."),
          P("Gradio prediction module", "H2X"),
          table([
              ["Module behavior", "Implementation"],
              ["Dynamic fields", "The interface creates an input component for every feature column except Grade."],
              ["Categorical inputs", "Dropdown choices come from the saved LabelEncoder classes."],
              ["Study-hours input", "Weekly_Study_Hours is displayed as a numeric field."],
              ["Other inputs", "All remaining features are displayed as text boxes in the notebook."],
              ["Prediction path", "Inputs -> one-row DataFrame -> categorical encoding -> StandardScaler transform -> best_model.predict() -> numeric predicted grade."],
              ["Deployment", "iface.launch(share=True) creates a temporary public Gradio share URL from Colab."],
          ], [5.6*cm, 11.6*cm]),
          P("What to mention if asked about deployment", "H2X"),
          P("This is a prototype deployment. The notebook launches Gradio directly from Colab and uses a temporary share URL. It does not save the model, scaler, encoders, or feature schema to disk. For persistent deployment, save those assets together and host the app on a stable service such as Hugging Face Spaces or a cloud platform."), PageBreak()]

story += [P("5. Tools and technologies", "H1X"),
          table([
              ["Technology", "Role in this project"],
              ["Python", "Programming language for data processing, modelling, evaluation, visualization, and application logic."],
              ["Google Colab", "Notebook environment; receives the uploaded CSV through google.colab.files."],
              ["pandas", "Loads the CSV and manages tabular data / prediction rows."],
              ["NumPy", "Imported for numerical work (not directly used in the shown notebook logic)."],
              ["scikit-learn", "train_test_split, LabelEncoder, StandardScaler, LinearRegression, RandomForestRegressor, R2, and MSE."],
              ["XGBoost", "XGBRegressor candidate model."],
              ["Matplotlib", "Creates figure containers for plots."],
              ["Seaborn", "Builds the model-comparison and feature-importance bar charts."],
              ["Gradio", "Builds the browser-based grade prediction interface."],
          ], [4.1*cm, 13.1*cm]),
          P("Architecture in words", "H2X"),
          P("CSV data feeds the preparation layer. The prepared data is split into training and test partitions. Three model candidates are trained and scored. The highest-R2 model becomes the prediction model. The user interface applies the saved encoding and scaling steps before sending new inputs to that model."),
          callout("Reproducibility status", "The train/test split uses random_state=42, but RandomForestRegressor and XGBRegressor are instantiated without a random_state. Exact model results may change between runs. Set random_state on both models and record package versions for reproducible experiments."), PageBreak()]

story += [P("6. How to explain the project", "H1X"),
          P("30-second self-introduction version", "H2X"),
          P("My project is a Student Performance Prediction system built with Python and machine learning. I use a CSV dataset where Grade is the target variable. I clean missing records, encode categorical values, standardize features, and compare Linear Regression, Random Forest, and XGBoost. On my held-out test split, Random Forest performed best with an R2 of about 0.127 and an MSE of about 4.76. I also built a Gradio interface so a user can enter student details and get a predicted grade."),
          P("One-minute walkthrough", "H2X"),
          P("The goal is to estimate a student's numeric grade from the other columns in the dataset. First, I upload the CSV in Google Colab and remove rows with missing data. Since machine-learning models need numbers, I label-encode text columns and retain those encoders for the application. I separate Grade as y and use every other column as X. Then I standardize the features, use an 80/20 split, and train three regressors. I compare them using R2 on the test set and choose the model with the best R2. Random Forest won on this dataset split. I show a feature-importance chart for Random Forest, and Gradio converts user inputs using the same preprocessing before returning the predicted grade. The result is a complete prototype, though I would improve it with leakage-safe preprocessing, cross-validation, tuning, and model persistence."),
          P("Common viva / interview questions", "H2X"),
          table([
              ["Question", "Concise answer"],
              ["Why did you use regression?", "Grade is treated as a numeric continuous target, so regression predicts its value directly."],
              ["Why compare models?", "Different algorithms capture patterns differently. Comparison on the same test split gives an evidence-based choice."],
              ["Why was Random Forest selected?", "It achieved the highest test R2 among Linear Regression, Random Forest, and XGBoost in this run."],
              ["What does negative R2 mean?", "It means the model performed worse than predicting the average target value for every test row."],
              ["What does MSE measure?", "It averages squared differences between actual and predicted grades; smaller values indicate lower error."],
              ["What is feature importance?", "It is a Random Forest estimate of which inputs most helped split the data; it indicates association, not causation."],
              ["What is the main limitation?", "Low R2 and a preprocessing leakage risk from scaling before splitting; this is a baseline prototype."],
          ], [6.2*cm, 10.9*cm]), PageBreak()]

story += [P("7. Improvement roadmap and accurate boundaries", "H1X"),
          P("Recommended next iteration", "H2X"),
          table([
              ["Priority", "Improvement", "Benefit"],
              ["High", "Split before fitting preprocessing; use a Pipeline.", "Prevents data leakage and makes inference consistent."],
              ["High", "Add random_state to Random Forest and XGBoost; save package versions.", "Makes results repeatable."],
              ["High", "Use cross-validation and report mean / spread of R2, MAE, RMSE.", "Avoids relying on one lucky or unlucky split."],
              ["High", "Persist model, scaler, encoders, and ordered feature list with joblib.", "Creates a reliable reusable application artifact."],
              ["Medium", "Use ColumnTransformer and OneHotEncoder for nominal categories.", "Improves handling of text features, especially for linear models."],
              ["Medium", "Tune hyperparameters using GridSearchCV or RandomizedSearchCV.", "May improve generalization."],
              ["Medium", "Add input validation and unknown-category handling in Gradio.", "Prevents user-input failures."],
              ["Medium", "Add MAE and RMSE alongside MSE.", "Provides errors in more interpretable grade units."],
          ], [2.2*cm, 8.8*cm, 6.1*cm]),
          P("Do not overclaim", "H2X"),
          P("The submitted notebook does <b>not</b> show the original CSV contents, dataset size, exact feature list, data source, or permanently saved model artifacts. It also does not show hyperparameter tuning, cross-validation, fairness testing, or production hosting. Describe those only as future work unless you add and verify them."),
          P("Final takeaway", "H2X"),
          P("This project demonstrates the full beginner-to-intermediate ML workflow: dataset ingestion, cleaning, categorical handling, scaling, regression-model comparison, metric-based selection, feature-importance visualization, and a usable prediction interface. Its central lesson is not that the current model is highly accurate; it is that you can build, evaluate, and honestly improve an end-to-end prediction system."),
          Spacer(1, 14),
          Table([[P("Prepared from the project notebook on 04 Sep 2026", "Small")]], colWidths=[17.2*cm], style=TableStyle([("BACKGROUND", (0,0), (-1,-1), GREEN), ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#9AC7A6")), ("LEFTPADDING", (0,0), (-1,-1), 9), ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7)]))]

doc = SimpleDocTemplate(OUT, pagesize=A4, rightMargin=1.55*cm, leftMargin=1.55*cm, topMargin=1.45*cm, bottomMargin=1.65*cm, title="Student Performance Prediction - Project Handbook", author="Project documentation generated from submitted notebook")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
