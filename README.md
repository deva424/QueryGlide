# QueryGlide

QueryGlide is an intent-based customer-support chatbot built with Streamlit and scikit-learn. It gives users a focused, conversational place to ask common support questions such as where an order is, how to request a refund, payment problems, account access, and contacting a human agent.

Instead of relying on a large language model, QueryGlide uses a lightweight traditional machine-learning pipeline. This makes its responses fast, predictable, and easy to train on a custom support dataset.

## What the app does

1. A visitor writes a support question or selects a suggested starting point.
2. The app cleans the message and sends it to the trained intent classifier.
3. The classifier assigns the most likely support topic and returns a confidence score.
4. If the score is above the chosen threshold, QueryGlide selects a response for that topic.
5. If confidence is too low, the app gives a safe fallback response and asks the visitor to rephrase.

The sidebar includes an Answer Sensitivity control. Raising it prioritizes more certain answers; lowering it allows the assistant to respond to a wider range of messages.

## Supported support topics

The included dataset covers these customer-service flows:

- Greetings and conversation closing
- Order tracking
- Order cancellation
- Returns and refund requests
- Payment and billing issues
- Account access and password recovery
- Escalation to a human support representative

## Machine-learning approach

The model is trained using a pipeline of:

- TF-IDF vectorization to convert text into numerical features
- A linear Support Vector Classifier to identify the intent
- Calibrated probabilities to provide a useful confidence score

Training uses five-fold cross-validation before fitting the final model on the complete dataset. The resulting classifier and response catalogue are saved as Joblib files in the models directory.

## Project structure

    QueryGlide/
    |-- app.py                    Streamlit application and user interface
    |-- README.md                 Project documentation
    |-- data/
    |   -- intents.json           Generated intent training dataset
    |-- models/
    |   |-- queryglide_model.pkl  Trained classifier pipeline
    |   -- responses_map.pkl      Intent-to-response mapping
    -- scripts/
        |-- generate_intents.py   Generates examples for each intent
        -- train_model.py         Evaluates, trains, and exports model files

## Requirements

Install the project dependencies:

    pip install streamlit scikit-learn joblib nltk

## Run the app

From the project root, start the Streamlit interface:

    streamlit run app.py

Streamlit will open the local application in your browser, usually at:

    http://localhost:8501

## Refresh or customize the model

To add a new support topic, update the intent templates and responses in scripts/generate_intents.py. Then regenerate the dataset and train a fresh model:

    python scripts/generate_intents.py
    python scripts/train_model.py

The training script replaces the files in models with the newly trained classifier and response map. Restart the Streamlit app after retraining so it loads the new assets.

## Notes

- Keep the data, models, and scripts folders together with app.py; their paths are resolved automatically from the project root.
- The app stores chat history only in the active Streamlit session. Starting a new conversation clears that session history.
- QueryGlide is suited to simple, well-defined support flows. Production deployments should add secure order lookups, authentication, analytics, live-agent handoff, and appropriate data-protection controls.
