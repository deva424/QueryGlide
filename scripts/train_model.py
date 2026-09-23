import json
import re
from pathlib import Path
import nltk
from nltk.stem import PorterStemmer
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import classification_report

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "intents.json"
MODEL_DIR = PROJECT_ROOT / "models"

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
stemmer = PorterStemmer()

def clean_and_stem(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = nltk.word_tokenize(text)
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    return " ".join(stemmed_tokens)

def load_and_prepare_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    X = []
    y = []
    responses_map = {}
    
    for intent in data['intents']:
        tag = intent['tag']
        responses_map[tag] = intent['responses']
        
        for pattern in intent['patterns']:
            X.append(clean_and_stem(pattern))
            y.append(tag)
            
    return X, y, responses_map

def train_model():
    print("⏳ Loading intents dataset...")
    X, y, responses_map = load_and_prepare_data(DATA_PATH)
    print(f"📊 Dataset loaded successfully. Total training patterns: {len(X)}")
    
    # 1. FIX DEPRECATION WARNING: Use CalibratedClassifierCV around SVC for probabilities
    base_svc = SVC(kernel='linear', C=10.0, random_state=42)
    calibrated_svc = CalibratedClassifierCV(estimator=base_svc, ensemble=False)
    
    bot_pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(ngram_range=(1, 2), use_idf=True, min_df=1)),
        ('classifier', calibrated_svc)
    ])
    
    # 2. FIX ACCURACY OVERFITTING: Evaluate using Stratified Cross-Validation on unseen folds
    print("\n🔍 Evaluating Model with 5-Fold Stratified Cross-Validation:")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_predictions = cross_val_predict(bot_pipeline, X, y, cv=cv)
    print(classification_report(y, cv_predictions, zero_division=0))
    
    # Fit final model on all data for deployment export
    print("🤖 Training final model on full dataset...")
    bot_pipeline.fit(X, y)
    
    print("💾 Exporting pristine model artifacts to disk...")
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(bot_pipeline, MODEL_DIR / "queryglide_model.pkl")
    joblib.dump(responses_map, MODEL_DIR / "responses_map.pkl")
    print("✅ Success! 'queryglide_model.pkl' and 'responses_map.pkl' are synchronized.")

if __name__ == "__main__":
    train_model()
