import os
import urllib.request
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

os.makedirs("models", exist_ok=True)

# URL of a popular public Phishing Email Dataset on GitHub (Tf-Idf friendly)
DATASET_URL = "https://raw.githubusercontent.com/subhamm/Phishing-Email-Detection/master/phishing_email.csv"
DATASET_PATH = "phishing_email_downloaded.csv"

print("Attempting to download public phishing email dataset...")
try:
    urllib.request.urlretrieve(DATASET_URL, DATASET_PATH)
    print("Download successful!")
    df = pd.read_csv(DATASET_PATH)
    # The dataset typically has columns: 'Email Text' and 'Email Type'
    # 'Email Type' contains values like 'Safe Email' and 'Phishing Email'
    df = df.dropna(subset=['Email Text', 'Email Type'])
    df['label'] = df['Email Type'].apply(lambda x: 1 if 'phishing' in str(x).lower() else 0)
    texts = df['Email Text'].values
    labels = df['label'].values
except Exception as e:
    print(f"Online download failed or timed out ({e}). Generating high-quality backup training dataset...")
    # High-quality synthetic/backup dataset to ensure the classifier trains instantly
    backup_data = []
    # Phishing email patterns
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
    # Safe email patterns
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
        
    df = pd.DataFrame(backup_data)
    texts = df['text'].values
    labels = df['label'].values

print(f"Total dataset samples for training: {len(texts)}")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42, stratify=labels)

# TF-IDF Vectorizer
print("Training TF-IDF Vectorizer...")
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Classifier
print("Training Logistic Regression Phishing Classifier...")
clf = LogisticRegression(max_iter=500)
clf.fit(X_train_vec, y_train)

# Evaluate
y_pred = clf.predict(X_test_vec)
acc = accuracy_score(y_test, y_pred)
print(f"Model test accuracy: {acc * 100:.2f}%")
print(classification_report(y_test, y_pred))

# Save models
with open("models/phishing_model.pkl", "wb") as f:
    pickle.dump(clf, f)
with open("models/phishing_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Saved models successfully to models/ directory!")
