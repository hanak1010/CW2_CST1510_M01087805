import os
from google import genai

def get_gemini_client():
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    api_key=os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)
    
# Keywords to indicate user is asking about dataset 
KEYWORDS = [
    "incident", "cyber", "attack", "threat", "severity", "status", "date",
    "ticket", "priority", "category", "issue", "dataset", "data", "table", "value" , "analysis", "performance", "resolution", "average", "trends", "summarize", "IT", "service" , "support" 
] 

# Define AI persona according to user role and dashboard
ROLE_PERSONAS = {
    "admin":
        "You are a Cybersecurity and IT Executive Advisor. Your goal is to provide high-level, strategic, and concise summaries suitable for executive review. You focus on organizational risk, resource allocation, and strategic direction, using the data provided to justify business decisions.",
    "analyst":
        "You are a Multi-Domain Intelligence Platform Analyst. Your goal is to perform deep dives, statistical analysis, trend identification, and find hidden patterns in the data provided. Your tone is technical, methodical, and insightful, specializing in data correlation across IT, Cyber, and datasets metadata datasets.",
    "user":
        "You are an Operational Support Assistant. Your goal is to provide clear, simple, and direct answers to help with day-to-day data lookups and understanding dashboard content. You act as a guide to the data available."
}

DASBOARD_PERSONAS ={
    "cyber_incidents":
        "You specialize in cyber threat intelligence, incidents trends, and attack pattern analysis.",
    "datasets":
        "You specialize in dataset summarizaion, exploring metadata, and deriving insights from tabular data.",
    "it_tickets":
        "You specialize in IT ticket diagnostics, priority analysis, SLA behavior, and workload efficiency."
}
    

def ask_gemini(user_input:str, user_role: str, dashboard_type: str, df=None):

    client =get_gemini_client()
    lower = user_input.lower()

    # Persona Selection
    role_persona = ROLE_PERSONAS.get(user_role, ROLE_PERSONAS["user"])
    dashboard_persona = DASBOARD_PERSONAS.get(dashboard_type, "")
    persona = role_persona + " " + dashboard_persona

    if df is not None and any(word in lower for word in KEYWORDS):
        dataset_text = df.to_string()

        prompt = f"""
{persona}

You are answering a question based ONLY on the dataset below. 
If the answer cannot be found in the dataset, say:
"I can only answer based on the dashboard dataset."

Dataset:
{dataset_text}

User question: {user_input}
"""

    else:
        prompt = f"""
{persona}
The user asked a general question. Answer normally.

Question: {user_input}
"""
    response = client.models.generate_content(
        model="models/gemini-2.5-flash", contents=prompt
    )

    return response.text