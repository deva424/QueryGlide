import json
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTENTS_PATH = PROJECT_ROOT / "data" / "intents.json"

# Seed for reproducible dataset generation
random.seed(42)

intent_templates = {
    "greeting": {
        "templates": [
            "{hi}",
            "{hi} {there}",
            "{hi} chatbot",
            "{hi} support team",
            "{good_day}",
            "{good_day} {there}",
            "is {anyone} available",
            "is {anyone} online",
            "can {anyone} help me",
            "can {anyone} assist me today",
            "hello customer service",
            "hey can I ask a question",
            "starting a chat",
            "need some help please",
            "active support here"
        ],
        "slots": {
            "hi": ["hi", "hello", "hey", "howdy", "greetings", "hiya", "yo"],
            "there": ["there", "friend", "bot", "team", "support", "assistant"],
            "good_day": ["good morning", "good afternoon", "good evening", "good day"],
            "anyone": ["anyone", "somebody", "an agent", "a rep", "a person"]
        },
        "responses": [
            "Hello! Welcome to Customer Support. How can I assist you today?",
            "Hi there! What can I help you with today?",
            "Greetings! Please let me know how I can support you."
        ]
    },
    "goodbye": {
        "templates": [
            "{bye}",
            "{bye} {thanks}",
            "{bye} for now",
            "{see_you}",
            "I am {leaving}",
            "that is {all}",
            "no more questions {thanks}",
            "I am finished here",
            "closing the chat",
            "have a {great_day}",
            "done with support",
            "talk to you later",
            "disconnecting chat",
            "exit chat now"
        ],
        "slots": {
            "bye": ["bye", "goodbye", "cya", "farewell", "bye bye", "signing off"],
            "thanks": ["thanks", "thank you", "cheers", "much appreciated", "many thanks"],
            "see_you": ["see you later", "catch you later", "talk soon", "until next time"],
            "leaving": ["leaving", "heading out", "done", "going", "offline"],
            "all": ["all I needed", "everything I wanted", "all set", "sufficient"],
            "great_day": ["great day", "wonderful afternoon", "good night", "nice weekend"]
        },
        "responses": [
            "Thank you for reaching out. Have a wonderful day!",
            "Goodbye! Let us know if you need anything else.",
            "Take care! Feel free to chat again if you run into any issues."
        ]
    },
    "order_tracking": {
        "templates": [
            "where is my {package}",
            "track my {package}",
            "when will my {package} arrive",
            "my {package} has not arrived yet",
            "check my {delivery} status",
            "status of order {id_num}",
            "where is order {id_num}",
            "tracking info for {package}",
            "has my {package} shipped",
            "can you locate my {package}",
            "delivery status update for {id_num}",
            "is order {id_num} delayed",
            "estimated delivery time for {package}",
            "check tracking for order {id_num}",
            "any update on package {id_num}"
        ],
        "slots": {
            "package": ["order", "package", "shipment", "item", "parcel", "delivery", "purchase"],
            "delivery": ["delivery", "shipping", "dispatch", "transit"],
            "id_num": ["12345", "987654", "AB-102", "#4432", "88219", "US-9921", "#99012"]
        },
        "responses": [
            "I can help you track that. Please provide your 8-digit Order Number.",
            "To check your shipment status, please enter your Order ID or tracking number.",
            "Let me look that up for you. Could you share your Order Reference number?"
        ]
    },
    "order_cancellation": {
        "templates": [
            "I want to cancel my {order}",
            "can I stop my {shipment}",
            "cancel order {id_num}",
            "how do I cancel {an_item}",
            "please cancel my recent {order}",
            "I bought the wrong {item} cancel it",
            "stop processing order {id_num}",
            "I changed my mind cancel my {order}",
            "cancel purchase {id_num}",
            "abort order shipment {id_num}",
            "need to revoke order {id_num}",
            "is it too late to cancel {order}",
            "terminate order {id_num}",
            "cancel my order immediately",
            "void purchase {id_num}"
        ],
        "slots": {
            "order": ["order", "purchase", "transaction", "checkout"],
            "shipment": ["shipment", "delivery", "dispatch", "package"],
            "an_item": ["an item", "a product", "my order", "this item", "my purchase"],
            "item": ["item", "product", "thing", "size", "color"],
            "id_num": ["12345", "987654", "AB-102", "#4432", "88219", "US-9921", "#99012"]
        },
        "responses": [
            "Orders can be cancelled within 30 minutes of placement. Please provide your Order ID so I can check if it is eligible.",
            "If your order hasn't shipped yet, I can cancel it for you. Please share your Order Number."
        ]
    },
    "refund_request": {
        "templates": [
            "I want a refund",
            "can I get my money back",
            "requesting a return and refund for {item}",
            "my {item} was {damaged}, I want my money returned",
            "how long do refunds take for {item}",
            "process a return for my {item}",
            "I need a refund for order {id_num}",
            "send my payment back for {item}",
            "damaged product refund request",
            "issue a money reimbursement",
            "return this broken {item}",
            "how do I initiate a refund",
            "where is my refund for {id_num}",
            "give me my cashback for return",
            "reimburse my order {id_num}"
        ],
        "slots": {
            "item": ["order", "package", "item", "product", "shoes", "shirt", "device"],
            "damaged": ["broken", "damaged", "faulty", "defective", "wrong size", "scratched"],
            "id_num": ["12345", "987654", "AB-102", "#4432", "88219", "US-9921", "#99012"]
        },
        "responses": [
            "To process a refund, please initiate a return through the 'My Orders' dashboard. Once processed, refunds take 3-5 business days to reflect in your account.",
            "We accept returns within 30 days of delivery. Once we receive the item back at our warehouse, your refund will be issued immediately."
        ]
    },
    "payment_issue": {
        "templates": [
            "my credit card was {failed}",
            "I was charged {multiple} times",
            "payment failed at checkout",
            "why did my transaction fail",
            "incorrect billing amount on {card}",
            "card payment error",
            "you double charged my account",
            "payment processing failed for order {id_num}",
            "checkout error with {card}",
            "billing system rejected my {card}",
            "debit card transaction declined",
            "money deducted but order not placed",
            "overcharged on my order {id_num}",
            "payment gateway issue",
            "why was my payment unsuccessful"
        ],
        "slots": {
            "failed": ["declined", "rejected", "failed", "denied", "canceled"],
            "multiple": ["twice", "two times", "multiple times", "double"],
            "card": ["credit card", "debit card", "Visa", "Mastercard", "PayPal"],
            "id_num": ["12345", "987654", "AB-102", "#4432", "88219", "US-9921", "#99012"]
        },
        "responses": [
            "I am sorry for the payment issue. Please verify your billing zip code and CVV code. If you were double-charged, our system automatically reverses pending duplicate charges within 24 hours.",
            "Payment failures usually happen due to bank security blocks or incorrect card details. Would you like to try an alternative payment method like PayPal?"
        ]
    },
    "account_security": {
        "templates": [
            "I forgot my password",
            "reset my password",
            "locked out of my account",
            "can't log into my profile",
            "change my email address",
            "help me unlock my profile",
            "password reset link not working",
            "update login credentials",
            "cannot access my account",
            "security issue with my login",
            "lost password for email",
            "how to reset my account pin",
            "unable to sign in",
            "account blocked due to invalid login",
            "send password recovery link"
        ],
        "slots": {},
        "responses": [
            "You can reset your password by clicking 'Forgot Password' on the login screen. We will send a secure reset link to your registered email address.",
            "For security reasons, account recovery links must be requested via the login page. Let me know if you do not receive the email within 5 minutes."
        ]
    },
    "agent_escalation": {
        "templates": [
            "I want to talk to a {human}",
            "speak to a real person",
            "connect me to an agent",
            "transfer me to customer service",
            "you are not helping, give me a representative",
            "let me speak to a supervisor",
            "need a real representative right now",
            "human support agent please",
            "transfer to live agent immediately",
            "I need human assistance",
            "stop bot response connect human",
            "escalate this to support team",
            "get me a manager",
            "chat with customer care representative",
            "pass me over to a real worker"
        ],
        "slots": {
            "human": ["human", "person", "agent", "representative", "specialist"]
        },
        "responses": [
            "I am transferring you to a live support representative right now. Please hold for a moment...",
            "Let me connect you with a member of our human support team to solve this complex issue. Hold on tightly!"
        ]
    }
}

def generate_patterns(template, slots):
    """Recursively replaces template keys with slot combinations."""
    results = [template]
    for key, values in slots.items():
        placeholder = "{" + key + "}"
        new_results = []
        for text in results:
            if placeholder in text:
                for val in values:
                    new_results.append(text.replace(placeholder, val))
            else:
                new_results.append(text)
        results = new_results
    return results

def generate_large_dataset(target_count_per_class=260):
    intents = []
    total_patterns_generated = 0
    
    for tag, config in intent_templates.items():
        patterns_set = set()
        
        # 1. Generate base patterns from templates
        for tmpl in config["templates"]:
            gen = generate_patterns(tmpl, config.get("slots", {}))
            patterns_set.update(gen)
            
        # 2. Add realistic variations (prefix/suffix additions) to reach exact target
        base_patterns = list(patterns_set)
        prefixes = ["", "hello, ", "please ", "can you ", "i need to ", "hey ", "urgently "]
        suffixes = ["", " please", " thanks", " right now", " as soon as possible", " help me"]
        
        idx = 0
        while len(patterns_set) < target_count_per_class:
            base = base_patterns[idx % len(base_patterns)]
            pref = random.choice(prefixes)
            suff = random.choice(suffixes)
            combo = f"{pref}{base}{suff}".strip()
            patterns_set.add(combo)
            idx += 1
            
        final_patterns = list(patterns_set)[:target_count_per_class]
        total_patterns_generated += len(final_patterns)
        
        intents.append({
            "tag": tag,
            "patterns": final_patterns,
            "responses": config["responses"]
        })

    # Add empty fallback intent
    intents.append({
        "tag": "fallback",
        "patterns": [],
        "responses": [
            "I am sorry, I did not quite catch that. Could you rephrase your question?",
            "I am still learning! Can you provide more details so I can assist you better?",
            "I am not sure I understand. Type 'agent' if you would like to speak to a human representative."
        ]
    })

    dataset = {"intents": intents}
    
    with open(INTENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
        
    print(f"🎉 Successfully generated 'intents.json' with {total_patterns_generated} total patterns!")

if __name__ == "__main__":
    generate_large_dataset(target_count_per_class=260)
