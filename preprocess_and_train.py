import os
import pandas as pd
import numpy as np
import cv2
import pickle
import time
from skimage.feature import graycomatrix, graycoprops
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Create models directory
os.makedirs("models", exist_ok=True)

# -------------------------------------------------------------------------
# Step 1: Preprocess and Downsample Financial Transactions (Paysim)
# -------------------------------------------------------------------------
print("--- Step 1: Processing Financial Transaction Dataset ---")
financial_csv = "Synthetic_Financial_datasets_log.csv"
small_financial_csv = "Synthetic_Financial_datasets_small.csv"

if os.path.exists(financial_csv):
    print(f"Reading {financial_csv} for downsampling...")
    # Load columns in chunks or filter
    chunk_size = 500000
    fraud_rows = []
    non_fraud_rows = []
    
    # Read in chunks to keep memory usage low
    for chunk in pd.read_csv(financial_csv, chunksize=chunk_size):
        fraud = chunk[chunk['isFraud'] == 1]
        non_fraud = chunk[chunk['isFraud'] == 0]
        
        fraud_rows.append(fraud)
        # Randomly sample non-fraud from each chunk to maintain speed
        sampled_non_fraud = non_fraud.sample(n=min(len(non_fraud), 4000), random_state=42)
        non_fraud_rows.append(sampled_non_fraud)
        
    df_fraud = pd.concat(fraud_rows, ignore_index=True)
    df_non_fraud = pd.concat(non_fraud_rows, ignore_index=True)
    
    # Final downsampling
    df_non_fraud_sampled = df_non_fraud.sample(n=min(len(df_non_fraud), 50000), random_state=42)
    df_small = pd.concat([df_fraud, df_non_fraud_sampled], ignore_index=True)
    
    df_small.to_csv(small_financial_csv, index=False)
    print(f"Downsampled financial dataset saved to {small_financial_csv} (Rows: {len(df_small)}, Fraud: {len(df_fraud)})")
else:
    print(f"WARNING: {financial_csv} not found in workspace!")

# -------------------------------------------------------------------------
# Step 2: Train Counterfeit Currency Classification Model
# -------------------------------------------------------------------------
print("\n--- Step 2: Training Counterfeit Currency Classifier ---")
currency_dir = "indian currency"

def extract_currency_features(img_path):
    image = cv2.imread(img_path)
    if image is None:
        return None
    # Resize to standard size
    image_resized = cv2.resize(image, (128, 128))
    
    # 1. Color channel statistics
    img_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
    r_mean, r_std = np.mean(img_rgb[:,:,0]), np.std(img_rgb[:,:,0])
    g_mean, g_std = np.mean(img_rgb[:,:,1]), np.std(img_rgb[:,:,1])
    b_mean, b_std = np.mean(img_rgb[:,:,2]), np.std(img_rgb[:,:,2])
    
    # 2. Texture features using Gray Level Co-occurrence Matrix (GLCM)
    gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    glcm = graycomatrix(gray, distances=[1, 3], angles=[0, np.pi/4], levels=256, symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast').mean()
    energy = graycoprops(glcm, 'energy').mean()
    homogeneity = graycoprops(glcm, 'homogeneity').mean()
    correlation = graycoprops(glcm, 'correlation').mean()
    
    # 3. Structural features (Edges)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.mean(edges > 0)
    
    return [r_mean, r_std, g_mean, g_std, b_mean, b_std, contrast, energy, homogeneity, correlation, edge_density]

if os.path.exists(currency_dir):
    X_currency = []
    y_currency = []
    
    subdirs = os.listdir(currency_dir)
    print(f"Found subdirectories: {subdirs}")
    
    for subdir in subdirs:
        subdir_path = os.path.join(currency_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue
            
        # Determine if class is REAL or FAKE
        label = "FAKE" if "fake" in subdir.lower() else "REAL"
        print(f"Processing folder '{subdir}' classified as class '{label}'...")
        
        files = os.listdir(subdir_path)
        for f in files:
            if not f.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            img_path = os.path.join(subdir_path, f)
            features = extract_currency_features(img_path)
            if features is not None:
                X_currency.append(features)
                y_currency.append(label)
                
    if len(X_currency) > 0:
        X_currency = np.array(X_currency)
        y_currency = np.array(y_currency)
        
        # Split and scale
        X_train, X_test, y_train, y_test = train_test_split(X_currency, y_currency, test_size=0.2, random_state=42, stratify=y_currency)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train Random Forest Classifier
        rf_currency = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_currency.fit(X_train_scaled, y_train)
        
        preds = rf_currency.predict(X_test_scaled)
        acc = accuracy_score(y_test, preds)
        print(f"Currency Classifier Trained. Test Accuracy: {acc:.4f}")
        print(classification_report(y_test, preds))
        
        # Save model and scaler
        with open("models/currency_model.pkl", "wb") as f_out:
            pickle.dump(rf_currency, f_out)
        with open("models/currency_scaler.pkl", "wb") as f_out:
            pickle.dump(scaler, f_out)
        print("Serialized currency model and scaler to models/ directory.")
    else:
        print("ERROR: No images processed successfully!")
else:
    print(f"WARNING: Directory '{currency_dir}' not found!")

# -------------------------------------------------------------------------
# Step 3: Train NLP Scam Call Classifier (Digital Arrest)
# -------------------------------------------------------------------------
print("\n--- Step 3: Training NLP Scam Transcript Classifier ---")
text_csv = "composite_test.csv"

if os.path.exists(text_csv):
    print(f"Loading {text_csv}...")
    df_text = pd.read_csv(text_csv, encoding='utf-8')
    df_text = df_text.dropna(subset=['text', 'label'])
    
    # Convert label to int if string
    df_text['label'] = df_text['label'].astype(int)
    
    X_train_t, X_test_t, y_train_t, y_test_t = train_test_split(df_text['text'], df_text['label'], test_size=0.2, random_state=42, stratify=df_text['label'])
    
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train_t)
    X_test_vec = vectorizer.transform(X_test_t)
    
    # Train Logistic Regression
    lr_text = LogisticRegression(max_iter=1000, random_state=42)
    lr_text.fit(X_train_vec, y_train_t)
    
    preds_t = lr_text.predict(X_test_vec)
    acc_t = accuracy_score(y_test_t, preds_t)
    print(f"Text Classifier Trained. Test Accuracy: {acc_t:.4f}")
    print(classification_report(y_test_t, preds_t))
    
    # Save vectorizer and model
    with open("models/scam_vectorizer.pkl", "wb") as f_out:
        pickle.dump(vectorizer, f_out)
    with open("models/scam_model.pkl", "wb") as f_out:
        pickle.dump(lr_text, f_out)
    print("Serialized text classification model and vectorizer to models/ directory.")
else:
    print(f"WARNING: {text_csv} not found in workspace!")

print("\n--- Model Training Pipeline Completed Successfully ---")
