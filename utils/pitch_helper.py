from .gemini_client import ask_gemini

def generate_pitch(startup_name: str, idea: str, market: str):
    """Generates a pitch deck outline."""
    prompt = f"""
You are a world-class startup mentor. 
Generate a 7-slide pitch deck for a startup.

Startup: {startup_name}
Idea: {idea}
Target Market: {market}

Slides needed:
1. Problem
2. Solution
3. Market Opportunity
4. Business Model
5. Competitive Advantage
6. Financials
7. Team & Ask

Return in markdown.
"""
    return ask_gemini(prompt)
