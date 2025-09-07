import os
import json
import time
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# Smart model selection based on task complexity
MODELS = {
    "gemini-2.0-flash-exp": "Fast, creative responses",
    "gemini-1.5-flash": "Balanced performance",
    "gemini-1.5-pro": "Complex reasoning",
    "gemini-2.0-flash": "Latest model, best overall"
}

if API_KEY:
    genai.configure(api_key=API_KEY)

class SmartGeminiClient:
    """Advanced Gemini client with intelligent prompting and response formatting."""
    
    def __init__(self):
        self.conversation_history = []
        self.model_usage_stats = {}
        self.response_templates = self._load_response_templates()
        
    def _load_response_templates(self) -> Dict[str, str]:
        """Load professional response templates for different use cases."""
        return {
            "startup_idea": """
**🚀 STARTUP IDEA ANALYSIS**

**Core Concept:**
{concept}

**Market Opportunity:**
- **TAM:** {tam}
- **Target Market:** {target_market}
- **Problem Solved:** {problem}

**Business Model:**
- **Revenue Streams:** {revenue}
- **Key Partners:** {partners}
- **Competitive Advantage:** {advantage}

**Execution Strategy:**
1. {step1}
2. {step2}
3. {step3}

**Risk Assessment:**
⚠️ {risks}

**Next Steps:**
✅ {next_steps}
            """,
            
            "market_research": """
**📊 MARKET RESEARCH REPORT**

**Executive Summary:**
{summary}

**Market Size & Growth:**
- **Total Addressable Market (TAM):** {tam}
- **Serviceable Addressable Market (SAM):** {sam}
- **Growth Rate:** {growth_rate}
- **Market Trends:** {trends}

**Competitive Landscape:**
| Competitor | Market Share | Strengths | Weaknesses |
|------------|-------------|-----------|------------|
{competitors_table}

**Customer Segments:**
{segments}

**Strategic Recommendations:**
1. **Immediate Actions:** {immediate}
2. **Medium-term Strategy:** {medium}
3. **Long-term Vision:** {long_term}

**Risk Factors:**
⚠️ {risks}

**Success Metrics:**
📈 {metrics}
            """,
            
            "business_model": """
**🏢 BUSINESS MODEL CANVAS**

**Key Partners:**
{partners}

**Key Activities:**
{activities}

**Value Propositions:**
{value_props}

**Customer Relationships:**
{relationships}

**Customer Segments:**
{segments}

**Key Resources:**
{resources}

**Channels:**
{channels}

**Cost Structure:**
{costs}

**Revenue Streams:**
{revenue}

**Business Model Type:** {model_type}
**Competitive Moat:** {moat}
            """,
            
            "financial_forecast": """
**💰 FINANCIAL PROJECTION**

**Revenue Forecast:**
{revenue_forecast}

**Key Assumptions:**
- **Growth Rate:** {growth_rate}
- **Customer Acquisition Cost:** {cac}
- **Lifetime Value:** {ltv}
- **Churn Rate:** {churn}

**Financial Metrics:**
| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
{metrics_table}

**Break-even Analysis:**
{break_even}

**Funding Requirements:**
{funding}

**Risk Factors:**
⚠️ {risks}

**Recommendations:**
✅ {recommendations}
            """,
            
            "swot_analysis": """
**🔍 SWOT & RISK ANALYSIS**

**Strengths:**
{strengths}

**Weaknesses:**
{weaknesses}

**Opportunities:**
{opportunities}

**Threats:**
{threats}

**Strategic Risks:**
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
{risks_table}

**Action Items:**
1. **High Priority:** {high_priority}
2. **Medium Priority:** {medium_priority}
3. **Low Priority:** {low_priority}

**Success Indicators:**
📊 {indicators}
            """,
            
            "pitch_refinement": """
**🎯 INVESTOR PITCH**

**Problem Statement:**
{problem}

**Solution:**
{solution}

**Market Opportunity:**
{market}

**Business Model:**
{model}

**Traction & Metrics:**
{traction}

**Competitive Advantage:**
{advantage}

**Team:**
{team}

**Financials:**
{financials}

**Ask:**
{ask}

**Call to Action:**
{cta}
            """,
            
            "investor_qa": """
**💼 INVESTOR Q&A SIMULATION**

**Your Pitch:**
{pitch}

**Potential Questions:**
{q1}
{q2}
{q3}
{q4}
{q5}

**Recommended Responses:**
{r1}
{r2}
{r3}
{r4}
{r5}

**Preparation Tips:**
💡 {tips}

**Red Flags to Address:**
⚠️ {red_flags}

**Success Metrics:**
📈 {success_metrics}
            """,
            
            "branding_kit": """
**🎨 BRANDING KIT**

**Company Name Options:**
{names}

**Taglines:**
{taglines}

**Brand Positioning:**
{positioning}

**Visual Identity:**
- **Primary Color:** {primary_color}
- **Secondary Color:** {secondary_color}
- **Typography:** {typography}
- **Logo Concept:** {logo_concept}

**Brand Voice:**
{voice}

**Messaging Framework:**
{framework}

**Brand Guidelines:**
{guidelines}
            """
        }
    
    def _select_optimal_model(self, task_type: str, complexity: str = "medium") -> str:
        """Intelligently select the best model for the task."""
        if complexity == "high" and "gemini-1.5-pro" in MODELS:
            return "gemini-1.5-pro"
        elif complexity == "fast" and "gemini-2.0-flash-exp" in MODELS:
            return "gemini-2.0-flash-exp"
        else:
            return "gemini-2.0-flash"
    
    def _create_smart_prompt(self, task_type: str, user_input: str, context: Dict = None) -> str:
        """Create intelligent, context-aware prompts."""
        
        base_prompts = {
            "startup_idea": f"""
You are an expert startup consultant with 15+ years of experience in venture capital and entrepreneurship. 
Analyze the following keywords/domain: "{user_input}"

Generate 5 innovative startup ideas with the following structure:
1. **Core Concept** - One sentence description
2. **Market Opportunity** - TAM, target market, problem solved
3. **Business Model** - Revenue streams, key partners, competitive advantage
4. **Execution Strategy** - 3 concrete steps
5. **Risk Assessment** - Main challenges
6. **Next Steps** - Immediate actions

Make each idea:
- Innovative and disruptive
- Financially viable
- Scalable globally
- Technology-enabled
- Address real market pain points

Format the response in a professional, investor-ready structure with clear sections and bullet points.
            """,
            
            "market_research": f"""
You are a senior market research analyst at a top-tier consulting firm.
Conduct comprehensive market research for: "{user_input}"

Provide analysis covering:
1. **Executive Summary** - Key findings
2. **Market Size & Growth** - TAM, SAM, growth rates, trends
3. **Competitive Landscape** - Top 5 competitors with analysis
4. **Customer Segments** - Detailed segmentation
5. **Strategic Recommendations** - Immediate, medium-term, long-term
6. **Risk Factors** - Market, competitive, regulatory risks
7. **Success Metrics** - KPIs to track

Use data-driven insights and provide specific, actionable recommendations.
Format with professional tables, bullet points, and clear sections.
            """,
            
            "business_model": f"""
You are a business model expert and startup advisor.
Create a comprehensive Business Model Canvas for: "{user_input}"

Structure the response with these 9 building blocks:
1. **Key Partners** - Strategic alliances, suppliers
2. **Key Activities** - Core operations, value creation
3. **Value Propositions** - Customer benefits, differentiation
4. **Customer Relationships** - How to acquire and retain customers
5. **Customer Segments** - Target markets, personas
6. **Key Resources** - Human, financial, physical, intellectual
7. **Channels** - Distribution, communication channels
8. **Cost Structure** - Fixed and variable costs
9. **Revenue Streams** - Pricing models, revenue sources

Add insights on:
- Business model type (SaaS, Marketplace, etc.)
- Competitive moat
- Scalability factors

Format with clear sections, bullet points, and professional structure.
            """,
            
            "financial_forecast": f"""
You are a CFO and financial advisor for startups.
Analyze the financial projection: Initial Revenue: ${context.get('initial', 1000)}, Growth Rate: {context.get('growth', 10)}%, Months: {context.get('months', 12)}

Provide comprehensive financial analysis:
1. **Revenue Forecast** - Detailed projection analysis
2. **Key Assumptions** - Growth drivers, market factors
3. **Financial Metrics** - Unit economics, profitability
4. **Break-even Analysis** - Timeline and requirements
5. **Funding Requirements** - Capital needs and timing
6. **Risk Factors** - Financial risks and mitigations
7. **Recommendations** - Strategic financial advice

Include specific numbers, percentages, and actionable insights.
Format with professional tables and clear financial metrics.
            """,
            
            "swot_analysis": f"""
You are a strategic management consultant.
Conduct a comprehensive SWOT analysis for: "{user_input}"

Provide detailed analysis in these areas:

**Strengths:**
- Internal capabilities and advantages
- Unique resources and competencies

**Weaknesses:**
- Internal limitations and gaps
- Areas needing improvement

**Opportunities:**
- External factors to leverage
- Market trends and possibilities

**Threats:**
- External challenges and risks
- Competitive and market threats

**Strategic Risks:**
- Probability and impact assessment
- Mitigation strategies

**Action Items:**
- Prioritized recommendations
- Implementation timeline

Format with clear sections, risk matrices, and actionable insights.
            """,
            
            "pitch_refinement": f"""
You are a pitch coach who has helped 100+ startups raise over $2B in funding.
Refine this pitch for investors: "{user_input}"

Transform it into a compelling investor pitch with:
1. **Problem Statement** - Clear pain point
2. **Solution** - Your unique approach
3. **Market Opportunity** - Size and growth
4. **Business Model** - How you make money
5. **Traction & Metrics** - Key performance indicators
6. **Competitive Advantage** - Your moat
7. **Team** - Key personnel and expertise
8. **Financials** - Revenue, growth, projections
9. **Ask** - Specific funding request
10. **Call to Action** - Next steps

Make it:
- Concise and impactful
- Data-driven
- Investor-focused
- Professional and polished

Format with clear sections and bullet points for easy reading.
            """,
            
            "investor_qa": f"""
You are a venture capital partner with 20+ years of experience.
Simulate investor questions for this startup: "{user_input}"

Generate {context.get('rounds', 5)} challenging questions covering:
- Market validation
- Competitive positioning
- Financial projections
- Team capabilities
- Execution risks
- Scalability concerns

For each question, provide:
- The question (skeptical but fair)
- Recommended response approach
- Key points to emphasize
- Potential follow-up questions

Include:
- Preparation tips
- Red flags to address
- Success metrics for the Q&A

Format with clear Q&A structure and professional insights.
            """,
            
            "branding_kit": f"""
You are a senior brand strategist at a top branding agency.
Create a comprehensive branding kit for: "{user_input}"

Generate:

**Company Names (6 options):**
- Creative and memorable
- Domain availability considered
- Cultural sensitivity checked

**Taglines (3 options):**
- Compelling and concise
- Brand promise focused
- Different from competitors

**Brand Positioning:**
- Core value proposition
- Target audience
- Competitive differentiation

**Visual Identity:**
- Color palette recommendations
- Typography suggestions
- Logo concept direction

**Brand Voice:**
- Personality traits
- Communication style
- Tone guidelines

**Messaging Framework:**
- Key messages
- Value propositions
- Brand story

Format with professional structure and clear brand guidelines.
            """
        }
        
        return base_prompts.get(task_type, user_input)
    
    def _format_response(self, task_type: str, raw_response: str, context: Dict = None) -> str:
        """Format raw AI response into professional, structured output."""
        
        # Clean and structure the response
        response = raw_response.strip()
        
        # Add professional formatting based on task type
        if task_type == "startup_idea":
            if "**" not in response:  # If not already formatted
                response = self._format_startup_ideas(response)
        elif task_type == "market_research":
            if "**" not in response:
                response = self._format_market_research(response)
        elif task_type == "business_model":
            if "**" not in response:
                response = self._format_business_model(response)
        elif task_type == "financial_forecast":
            if "**" not in response:
                response = self._format_financial_forecast(response, context)
        elif task_type == "swot_analysis":
            if "**" not in response:
                response = self._format_swot_analysis(response)
        elif task_type == "pitch_refinement":
            if "**" not in response:
                response = self._format_pitch_refinement(response)
        elif task_type == "investor_qa":
            if "**" not in response:
                response = self._format_investor_qa(response, context)
        elif task_type == "branding_kit":
            if "**" not in response:
                response = self._format_branding_kit(response)
        
        return response
    
    def _format_startup_ideas(self, response: str) -> str:
        """Format startup ideas into professional structure."""
        ideas = response.split('\n\n') if '\n\n' in response else [response]
        formatted = "**🚀 STARTUP IDEA ANALYSIS**\n\n"
        
        for i, idea in enumerate(ideas[:5], 1):
            formatted += f"**Idea {i}:**\n{idea.strip()}\n\n"
            if i < 5:
                formatted += "---\n\n"
        
        return formatted
    
    def _format_market_research(self, response: str) -> str:
        """Format market research into professional structure."""
        return f"**📊 MARKET RESEARCH REPORT**\n\n{response}"
    
    def _format_business_model(self, response: str) -> str:
        """Format business model into professional structure."""
        return f"**🏢 BUSINESS MODEL CANVAS**\n\n{response}"
    
    def _format_financial_forecast(self, response: str, context: Dict) -> str:
        """Format financial forecast into professional structure."""
        return f"**💰 FINANCIAL PROJECTION**\n\n{response}"
    
    def _format_swot_analysis(self, response: str) -> str:
        """Format SWOT analysis into professional structure."""
        return f"**🔍 SWOT & RISK ANALYSIS**\n\n{response}"
    
    def _format_pitch_refinement(self, response: str) -> str:
        """Format pitch refinement into professional structure."""
        return f"**🎯 INVESTOR PITCH**\n\n{response}"
    
    def _format_investor_qa(self, response: str, context: Dict) -> str:
        """Format investor Q&A into professional structure."""
        return f"**💼 INVESTOR Q&A SIMULATION**\n\n{response}"
    
    def _format_branding_kit(self, response: str) -> str:
        """Format branding kit into professional structure."""
        return f"**🎨 BRANDING KIT**\n\n{response}"
    
    def ask_gemini(self, prompt: str, task_type: str = "general", context: Dict = None, complexity: str = "medium") -> str:
        """
        Smart Gemini query with intelligent prompting and response formatting.
        
        Args:
            prompt: User input
            task_type: Type of task (startup_idea, market_research, etc.)
            context: Additional context for the task
            complexity: Task complexity (low, medium, high)
        """
        try:
            # Select optimal model
            model_name = self._select_optimal_model(task_type, complexity)
            
            # Create intelligent prompt
            smart_prompt = self._create_smart_prompt(task_type, prompt, context)
            
            # Add conversation context if available
            if self.conversation_history:
                context_prompt = f"Previous context: {self.conversation_history[-3:]}\n\n"
                smart_prompt = context_prompt + smart_prompt
            
            # Generate response
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(smart_prompt)
            
            # Extract text
            raw_response = response.text if hasattr(response, "text") else str(response)
            
            # Format response professionally
            formatted_response = self._format_response(task_type, raw_response, context)
            
            # Update conversation history
            self.conversation_history.append({
                "task_type": task_type,
                "prompt": prompt,
                "response": formatted_response,
                "timestamp": time.time()
            })
            
            # Update model usage stats
            self.model_usage_stats[model_name] = self.model_usage_stats.get(model_name, 0) + 1
            
            return formatted_response
            
        except Exception as e:
            error_msg = f"**❌ ERROR**\n\nAn error occurred while processing your request: {str(e)}\n\nPlease try again or contact support if the issue persists."
            return error_msg
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics and performance metrics."""
        return {
            "total_requests": len(self.conversation_history),
            "model_usage": self.model_usage_stats,
            "recent_tasks": [conv["task_type"] for conv in self.conversation_history[-5:]],
            "average_response_length": sum(len(conv["response"]) for conv in self.conversation_history) / max(len(self.conversation_history), 1)
        }

# Global smart client instance
smart_client = SmartGeminiClient()

def ask_gemini(prompt: str, task_type: str = "general", context: Dict = None, complexity: str = "medium") -> str:
    """
    Enhanced Gemini query function with smart prompting and formatting.
    
    Args:
        prompt: User input
        task_type: Type of task for intelligent prompting
        context: Additional context
        complexity: Task complexity level
    """
    return smart_client.ask_gemini(prompt, task_type, context, complexity)

def get_ai_stats() -> Dict[str, Any]:
    """Get AI usage statistics and performance metrics."""
    return smart_client.get_usage_stats()
