## EXP 8: Facade for NLP-Based Customer Support Routing

### AIM
To implement the Facade Design Pattern for a multi-layered Natural Language Processing (NLP) framework that simplifies automated customer support routing through a single unified interface.

### ALGORITHM
1. Start the program.
2. Create the NLP subsystem classes: TextPreprocessor, IntentDetector, SentimentAnalyzer, TicketRouter
3. Create the CustomerSupportFacade class to coordinate all subsystem operations.
4. Accept the customer query as input.
5. Preprocess the input text.
6. Detect the customer's intent.
7. Analyze the sentiment of the query.
8. Route the query to the appropriate support department.
9. Display the customer query, detected intent, sentiment, and assigned department.
10. Stop the program.

### PROGRAM
```python
class TextPreprocessor:
    def process(self, text):
        return text.lower().strip()


class IntentDetector:
    KEYWORDS = {
        "refund":  "Refund Request",
        "payment": "Billing Issue",
        "login":   "Technical Support",
    }

    def detect(self, text):
        for keyword, intent in self.KEYWORDS.items():
            if keyword in text:
                return intent
        return "General Inquiry"


class SentimentAnalyzer:
    NEGATIVE = ["bad", "angry", "issue", "problem", "not working"]

    def analyze(self, text):
        if any(word in text for word in self.NEGATIVE):
            return "Negative"
        return "Neutral"


class TicketRouter:
    ROUTES = {
        "Refund Request":    "Finance Team",
        "Billing Issue":     "Accounts Team",
        "Technical Support": "IT Support Team",
    }

    def route(self, intent):
        return self.ROUTES.get(intent, "Customer Service Team")


class CustomerSupportFacade:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.detector = IntentDetector()
        self.analyzer = SentimentAnalyzer()
        self.router = TicketRouter()

    def handle_query(self, query):
        text = self.preprocessor.process(query)
        intent = self.detector.detect(text)
        sentiment = self.analyzer.analyze(text)
        department = self.router.route(intent)

        print("\n--- Routing Details ---")
        print("Customer Query :", query)
        print("Intent         :", intent)
        print("Sentiment      :", sentiment)
        print("Route To       :", department)


support = CustomerSupportFacade()
support.handle_query(input("Enter customer query: "))
```

### OUTPUT
```text
Enter customer query: My payment has an issue and I am angry.

--- Routing Details ---
Customer Query : My payment has an issue and I am angry.
Intent         : Billing Issue
Sentiment      : Negative
Route To       : Accounts Team
```

### RESULT
Thus, the Facade Design Pattern was successfully implemented to simplify a multi-layered NLP framework, enabling efficient processing and routing of customer support queries through a single unified interface.
