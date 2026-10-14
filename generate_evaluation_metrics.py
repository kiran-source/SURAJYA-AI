import os
import pickle
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from skimage.feature import graycomatrix, graycoprops
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    roc_curve, 
    auc, 
    precision_recall_curve, 
    average_precision_score
)

# Create directory to save evaluation metrics
EVAL_DIR = "model_evaluation"
os.makedirs(EVAL_DIR, exist_ok=True)
print(f"Creating evaluation outputs in folder: '{EVAL_DIR}/'")

# Helper function to plot and save Confusion Matrix Heatmap
def save_confusion_matrix_plot(cm, labels, title, filename):
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=labels, yticklabels=labels,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')
    
    # Loop over data dimensions and create text annotations.
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black",
                    fontsize=12, fontweight='bold')
    
    fig.tight_layout()
    plt.savefig(os.path.join(EVAL_DIR, filename), dpi=300)
    plt.close()

# Helper function to plot and save ROC Curve
def save_roc_curve_plot(y_true, y_score, title, filename):
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc="lower right")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(EVAL_DIR, filename), dpi=300)
    plt.close()

# Helper function to plot and save Precision-Recall Curve
def save_precision_recall_plot(y_true, y_score, title, filename):
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    avg_precision = average_precision_score(y_true, y_score)
    
    plt.figure(figsize=(6, 5))
    plt.step(recall, precision, where='post', color='green', lw=2, label=f'AP = {avg_precision:.4f}')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.05])
    plt.title(title)
    plt.legend(loc="lower left")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(EVAL_DIR, filename), dpi=300)
    plt.close()


# -------------------------------------------------------------------------
# Evaluation 1: Counterfeit Currency Note Classifier (Random Forest)
# -------------------------------------------------------------------------
print("\n--- Running Evaluation for Counterfeit Currency Classifier ---")
currency_dir = "indian currency"

def extract_currency_features(img_path):
    image = cv2.imread(img_path)
    if image is None:
        return None
    image_resized = cv2.resize(image, (128, 128))
    
    img_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
    r_mean, r_std = np.mean(img_rgb[:,:,0]), np.std(img_rgb[:,:,0])
    g_mean, g_std = np.mean(img_rgb[:,:,1]), np.std(img_rgb[:,:,1])
    b_mean, b_std = np.mean(img_rgb[:,:,2]), np.std(img_rgb[:,:,2])
    
    gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    glcm = graycomatrix(gray, distances=[1, 3], angles=[0, np.pi/4], levels=256, symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast').mean()
    energy = graycoprops(glcm, 'energy').mean()
    homogeneity = graycoprops(glcm, 'homogeneity').mean()
    correlation = graycoprops(glcm, 'correlation').mean()
    
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.mean(edges > 0)
    
    return [r_mean, r_std, g_mean, g_std, b_mean, b_std, contrast, energy, homogeneity, correlation, edge_density]

if os.path.exists(currency_dir):
    X_currency = []
    y_currency = []
    
    for subdir in os.listdir(currency_dir):
        subdir_path = os.path.join(currency_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue
        label = "FAKE" if "fake" in subdir.lower() else "REAL"
        
        for f in os.listdir(subdir_path):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                features = extract_currency_features(os.path.join(subdir_path, f))
                if features is not None:
                    X_currency.append(features)
                    y_currency.append(label) # Save as strings: 'REAL' or 'FAKE'
                    
    if X_currency:
        X_currency = np.array(X_currency)
        y_currency = np.array(y_currency)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_currency, y_currency, test_size=0.2, random_state=42, stratify=y_currency
        )
        
        # Load active model and scaler to compute correct test metrics
        try:
            with open("models/currency_model.pkl", "rb") as f_model:
                rf_model = pickle.load(f_model)
            with open("models/currency_scaler.pkl", "rb") as f_scaler:
                scaler = pickle.load(f_scaler)
                
            X_test_scaled = scaler.transform(X_test)
            preds = rf_model.predict(X_test_scaled)
            
            # Identify class index for 'REAL' (should be index 1 if classes_ are ['FAKE', 'REAL'])
            real_class_idx = 1
            if list(rf_model.classes_)[0] == "REAL":
                real_class_idx = 0
            probs = rf_model.predict_proba(X_test_scaled)[:, real_class_idx]
            
            # Save classification report txt
            with open(os.path.join(EVAL_DIR, "currency_report.txt"), "w") as f_rep:
                f_rep.write(classification_report(y_test, preds))
                
            cm = confusion_matrix(y_test, preds, labels=["FAKE", "REAL"])
            save_confusion_matrix_plot(cm, ["FAKE", "REAL"], "Counterfeit Note Confusion Matrix", "currency_confusion_matrix.png")
            
            # Convert y_test to binary for ROC/PR plotting
            y_test_binary = np.where(y_test == "REAL", 1, 0)
            save_roc_curve_plot(y_test_binary, probs, "ROC Curve: Counterfeit Currency note verification", "currency_roc_curve.png")
            save_precision_recall_plot(y_test_binary, probs, "Precision-Recall Curve: Counterfeit note verification", "currency_precision_recall_curve.png")
            print("Successfully generated all currency note evaluation matrices and saved plots!")
        except Exception as e:
            print(f"Error evaluating currency note model: {e}")
else:
    print(f"WARNING: '{currency_dir}' directory not found to run live validation.")


# -------------------------------------------------------------------------
# Evaluation 2: Digital Arrest Call Scam Classifier (Logistic Regression)
# -------------------------------------------------------------------------
print("\n--- Running Evaluation for Digital Arrest Scam Classifier ---")
text_csv = "composite_test.csv"

if os.path.exists(text_csv):
    df_text = pd.read_csv(text_csv, encoding='utf-8')
    df_text = df_text.dropna(subset=['text', 'label'])
    df_text['label'] = df_text['label'].astype(int)
    
    X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(
        df_text['text'], df_text['label'], test_size=0.2, random_state=42, stratify=df_text['label']
    )
    
    try:
        with open("models/scam_model.pkl", "rb") as f_model:
            lr_model = pickle.load(f_model)
        with open("models/scam_vectorizer.pkl", "rb") as f_vec:
            vectorizer = pickle.load(f_vec)
            
        X_test_vec = vectorizer.transform(X_test_t)
        preds_t = lr_model.predict(X_test_vec)
        probs_t = lr_model.predict_proba(X_test_vec)[:, 1]
        
        # Save report
        with open(os.path.join(EVAL_DIR, "scam_report.txt"), "w") as f_rep:
            f_rep.write(classification_report(y_test_t, preds_t, target_names=["SAFE", "SCAM"]))
            
        cm_t = confusion_matrix(y_test_t, preds_t)
        save_confusion_matrix_plot(cm_t, ["SAFE", "SCAM"], "Digital Arrest Call Confusion Matrix", "scam_confusion_matrix.png")
        save_roc_curve_plot(y_test_t, probs_t, "ROC Curve: Digital Arrest Call Scam Classifier", "scam_roc_curve.png")
        save_precision_recall_plot(y_test_t, probs_t, "Precision-Recall Curve: Call Scam Classifier", "scam_precision_recall_curve.png")
        print("Successfully generated all Digital Arrest call evaluation matrices and saved plots!")
    except Exception as e:
        print(f"Error evaluating text scam model: {e}")
else:
    print(f"WARNING: '{text_csv}' not found to run validation.")


# -------------------------------------------------------------------------
# Evaluation 3: Phishing Email Classifier (Logistic Regression)
# -------------------------------------------------------------------------
print("\n--- Running Evaluation for Phishing Email Classifier ---")
phish_csv = "phishing_email_downloaded.csv"

if not os.path.exists(phish_csv):
    # Recreate the backup dataset used in training to compute evaluation splits
    backup_data = []
    phishing_samples = [
        "Dear customer, your bank account has been locked. Verify netbanking credentials at http://fakebank-verify.info.",
        "URGENT: Income Tax Refund Approved. Click link to verify your PAN and card details.",
        "Congratulations! You won Rs. 1,00,000 lottery cash prize. Submit bank statement to claim now.",
        "Your Netflix subscription has expired. Update credit card immediately on http://netflx-renew.com.",
        "Official notice from CBI: MDMA drugs package found on your Aadhar card. Pay verification fees.",
        "Dear User, your password expires in 2 hours. Click here to confirm your credentials.",
        "You have received a secure document from HR. Enter corporate active directory logins to view.",
        "Immediate refund approval: Credit of Rs. 4,500 pending. Complete registration on http://refunds-direct.com.",
        "Dear employee, click here to access the updated 2026 salary compensation sheets.",
        "ALERT: Suspicious transaction of Rs. 45,000 on your card. Verify transactions here http://verify-alerts.com."
    ] * 20
    safe_samples = [
        "Hi, here is the monthly project progress update report for your review.",
        "Your HDFC monthly bank statement is now ready to download via netbanking.",
        "Confirming our meeting scheduled for tomorrow afternoon at 3:00 PM.",
        "Thank you for your order on Amazon. Your package will arrive by Thursday.",
        "Hi Team, please find attached the slide deck from today's brainstorming session.",
        "Your utility electricity bill has been paid successfully. Receipt is attached.",
        "Here are the notes and action items from our weekly paired programming standup.",
        "Welcome to HDFC bank. Please find our standard security newsletter enclosed.",
        "Hi, let's schedule a catch-up call next week to discuss marketing plans.",
        "Hi Mom, I will be visiting this weekend. See you soon!"
    ] * 20
    for txt in phishing_samples:
        backup_data.append({"text": txt, "label": 1})
    for txt in safe_samples:
        backup_data.append({"text": txt, "label": 0})
    df_phish = pd.DataFrame(backup_data)
else:
    df_phish = pd.read_csv(phish_csv)
    df_phish = df_phish.dropna(subset=['Email Text', 'Email Type'])
    df_phish['label'] = df_phish['Email Type'].apply(lambda x: 1 if 'phishing' in str(x).lower() else 0)
    df_phish = df_phish.rename(columns={'Email Text': 'text'})

X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    df_phish['text'], df_phish['label'], test_size=0.2, random_state=42, stratify=df_phish['label']
)

try:
    with open("models/phishing_model.pkl", "rb") as f_model:
        phish_model = pickle.load(f_model)
    with open("models/phishing_vectorizer.pkl", "rb") as f_vec:
        phish_vectorizer = pickle.load(f_vec)
        
    X_test_vec = phish_vectorizer.transform(X_test_p)
    preds_p = phish_model.predict(X_test_vec)
    probs_p = phish_model.predict_proba(X_test_vec)[:, 1]
    
    # Save report
    with open(os.path.join(EVAL_DIR, "phishing_report.txt"), "w") as f_rep:
        f_rep.write(classification_report(y_test_p, preds_p, target_names=["SAFE", "PHISHING"]))
        
    cm_p = confusion_matrix(y_test_p, preds_p)
    save_confusion_matrix_plot(cm_p, ["SAFE", "PHISHING"], "Phishing Email Confusion Matrix", "phishing_confusion_matrix.png")
    save_roc_curve_plot(y_test_p, probs_p, "ROC Curve: Phishing Email Classifier", "phishing_roc_curve.png")
    save_precision_recall_plot(y_test_p, probs_p, "Precision-Recall Curve: Phishing Email Classifier", "phishing_precision_recall_curve.png")
    print("Successfully generated all Phishing Email evaluation matrices and saved plots!")
except Exception as e:
    print(f"Error evaluating phishing email model: {e}")

print(f"\nAll model evaluation graphics and documents saved inside folder: '{os.path.abspath(EVAL_DIR)}/'")
