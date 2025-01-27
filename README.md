# Problem Statement: Leveraging LLM/GenAI to Build a Flask-based Intelligent FAQ Assistant

## Objective
Develop a Flask web application that integrates a Large Language Model (LLM) to create an intelligent FAQ assistant. This assistant will dynamically answer user queries based on pre-loaded knowledge (e.g., company policies, product documentation, or customer service FAQs). The solution should also include a mechanism for updating the knowledge base and logging user interactions for analysis.

## Key Features

### Knowledge Base Integration:

Pre-load the assistant with a structured or unstructured text knowledge base (e.g., JSON, Markdown, or TXT files).
Allow for periodic updates to the knowledge base.
### Dynamic Query Handling:

Use an LLM (e.g., OpenAI's GPT models) to process and generate responses based on the context provided by the user queries.

### Flask Application Features:

**Frontend:** Create a simple web interface with a query input box and response display area. (Optional)
API Endpoint: Expose a /ask POST endpoint to accept queries programmatically.

**Admin Features:** Provide an admin interface to update the knowledge base and view logs. (Over API or Frontend)


### Interaction Logging:

Log all user queries and responses to a database (e.g., MongoDB) for future analysis and improvement.

### Fallback Mechanism:

Handle instances where the LLM cannot provide a clear answer by giving a polite fallback response or suggesting related topics.


## How to Submit Solution

Drop an Email on hr@polynomial.ai and prakhar.k+hiring@polynomial.ai with below things

1. Github Repository link
2. Proper documentation of the solution
3. Recorded video session of usage