"""
SchemeWise AI Service
Provides AI-powered explanations with optional OpenAI integration and local fallback
"""

import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """
    Handles AI-powered explanations for scheme matches and questions.
    Supports optional OpenAI API integration with local fallback.
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '').strip()
        self.use_ai = bool(self.api_key and self.api_key != 'your_api_key_here')
        
        if self.use_ai:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                self.use_ai = False
    
    def generate_explanation(self, user_profile, scheme, score, reasons):
        """
        Generate a natural language explanation for why this scheme matches.
        
        Args:
            user_profile: User's profile data
            scheme: Scheme information
            score: Matching score (0-100)
            reasons: List of matching reasons
        
        Returns:
            Natural language explanation string
        """
        try:
            if self.use_ai:
                return self._explain_with_ai(user_profile, scheme, score, reasons)
        except Exception as e:
            print(f"AI explanation failed: {e}. Falling back to local explanation.")
        
        return self._explain_locally(user_profile, scheme, score, reasons)
    
    def _explain_with_ai(self, user_profile, scheme, score, reasons):
        """Generate explanation using OpenAI API"""
        try:
            prompt = f"""Based on the following government scheme and user profile, provide a brief, 
friendly explanation (2-3 sentences) of why this scheme is a good match. Be encouraging but honest.

User Profile:
- Name: {user_profile.get('name', 'Applicant')}
- Age: {user_profile.get('age', 'Not specified')}
- State: {user_profile.get('state', 'Not specified')}
- Annual Income: ₹{user_profile.get('annual_income', 0):,}
- Occupation: {user_profile.get('occupation', 'Not specified')}
- Student: {user_profile.get('is_student', False)}
- Farmer: {user_profile.get('is_farmer', False)}

Scheme: {scheme.get('name', 'Untitled')}
Category: {scheme.get('category', 'General')}
Match Score: {score}%
Why you matched: {'; '.join(reasons) if reasons else 'See scheme details'}

Scheme Benefits: {scheme.get('benefits', 'Various benefits')}

Generate a warm, encouraging explanation that emphasizes the matched criteria and what the applicant can expect."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful government scheme advisor. Provide clear, encouraging explanations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise e
    
    def _explain_locally(self, user_profile, scheme, score, reasons):
        """Generate explanation using local template-based system"""
        name = user_profile.get('name', 'Applicant')
        scheme_name = scheme.get('name', 'This scheme')
        benefits = scheme.get('benefits', 'various benefits')
        
        # Build explanation based on match quality
        if score >= 90:
            base = f"Excellent news, {name}! You're a strong match for {scheme_name}."
        elif score >= 75:
            base = f"Good news, {name}! You appear to be well-suited for {scheme_name}."
        else:
            base = f"{scheme_name} may be worth exploring for you, {name}."
        
        # Add reason-based explanation
        if reasons:
            # Pick the top 2-3 most relevant reasons
            key_reasons = reasons[:3]
            reason_text = " ".join(key_reasons)
            explanation = f"{base} {reason_text} This scheme offers {benefits}."
        else:
            explanation = f"{base} This scheme provides {benefits} to eligible applicants like you."
        
        # Add disclaimer
        disclaimer = " Remember to verify the latest requirements on the official portal before applying."
        
        return explanation + disclaimer
    
    def answer_question(self, question, schemes_data):
        """
        Answer questions about government schemes using RAG approach.
        
        1. Retrieve relevant schemes from the dataset
        2. Use AI (if available) or local templates to generate answer
        """
        
        # Step 1: Retrieve relevant schemes
        relevant_schemes = self._retrieve_relevant_schemes(question, schemes_data)
        
        # Step 2: Generate answer
        if self.use_ai:
            try:
                return self._answer_with_ai(question, relevant_schemes)
            except Exception as e:
                print(f"AI answer failed: {e}. Using local answer.")
        
        return self._answer_locally(question, relevant_schemes)
    
    def _retrieve_relevant_schemes(self, question, schemes_data):
        """
        Simple keyword-based retrieval for relevant schemes.
        Returns top 3-5 schemes most likely to answer the question.
        """
        question_lower = question.lower()
        
        # Define keyword-to-category mappings
        keywords = {
            'education': ['Education', 'Scholarship'],
            'student': ['Education', 'Scholarship'],
            'scholarship': ['Education', 'Scholarship'],
            'agriculture': ['Agriculture', 'Farmer'],
            'farmer': ['Agriculture', 'Farmer'],
            'farm': ['Agriculture', 'Farmer'],
            'employment': ['Employment', 'Skill Development'],
            'job': ['Employment', 'Skill Development'],
            'skill': ['Skill Development'],
            'women': ['Women Empowerment'],
            'health': ['Healthcare'],
            'medical': ['Healthcare'],
            'senior': ['Senior Citizens'],
            'elderly': ['Senior Citizens'],
            'disability': ['Disability Support'],
            'disabled': ['Disability Support'],
            'housing': ['Housing'],
            'home': ['Housing'],
            'business': ['Entrepreneurship'],
            'startup': ['Entrepreneurship'],
            'rural': ['Rural Development'],
        }
        
        # Find matching categories
        relevant_categories = set()
        for keyword, categories in keywords.items():
            if keyword in question_lower:
                relevant_categories.update(categories)
        
        # Filter schemes by category
        matching_schemes = []
        if relevant_categories:
            for scheme in schemes_data:
                if scheme.get('category', '') in relevant_categories:
                    matching_schemes.append(scheme)
        
        # If no specific category match, return top schemes
        if not matching_schemes:
            matching_schemes = schemes_data[:5]
        
        # Return top results
        return matching_schemes[:5]
    
    def _answer_with_ai(self, question, relevant_schemes):
        """Answer question using OpenAI API with retrieved schemes"""
        try:
            schemes_context = "\n".join([
                f"- {s['name']} ({s['category']}): {s['description']}"
                for s in relevant_schemes
            ])
            
            prompt = f"""You are a helpful government scheme advisor. 
Based on the following schemes, answer this question concisely in 2-3 sentences:

Question: {question}

Available Schemes:
{schemes_context}

Provide a helpful answer that references specific schemes when relevant. 
Do NOT invent information. Only use the provided scheme data."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful government scheme advisor. Provide accurate information based only on provided data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise e
    
    def _answer_locally(self, question, relevant_schemes):
        """Answer question using local template system"""
        question_lower = question.lower()
        
        # Common question patterns and answers
        if any(word in question_lower for word in ['which', 'what', 'list']):
            if 'student' in question_lower or 'education' in question_lower:
                schemes = [s for s in relevant_schemes if s.get('category') in ['Education', 'Scholarship']]
                if schemes:
                    scheme_list = ", ".join([s['name'] for s in schemes[:3]])
                    return f"For students, we have schemes like {scheme_list}. Each offers unique benefits and eligibility criteria. Visit their official portals for detailed information."
            
            if 'farmer' in question_lower or 'agriculture' in question_lower:
                schemes = [s for s in relevant_schemes if s.get('category') in ['Agriculture', 'Farmer']]
                if schemes:
                    scheme_list = ", ".join([s['name'] for s in schemes[:3]])
                    return f"For farmers, consider schemes such as {scheme_list}. Check the official government website for current eligibility and application timelines."
            
            if 'women' in question_lower:
                schemes = [s for s in relevant_schemes if 'Women' in s.get('category', '')]
                if schemes:
                    scheme_list = ", ".join([s['name'] for s in schemes[:3]])
                    return f"Women-focused schemes include {scheme_list}. Visit the issuing ministry's website to check if you're eligible."
        
        if 'document' in question_lower or 'requirement' in question_lower:
            if relevant_schemes:
                docs = []
                for scheme in relevant_schemes[:2]:
                    docs.extend(scheme.get('documents', []))
                if docs:
                    doc_list = ", ".join(list(set(docs))[:5])
                    return f"Common documents needed include {doc_list}. The specific requirements depend on the scheme you're applying for. Check the scheme details for a complete list."
        
        if 'apply' in question_lower or 'application' in question_lower:
            return "Most government schemes have specific application portals. Visit the official government website, fill the application form, upload required documents, and submit. Processing times vary by scheme."
        
        # Default answer
        if relevant_schemes:
            scheme_names = ", ".join([s['name'] for s in relevant_schemes[:3]])
            return f"Based on your question, schemes like {scheme_names} might be relevant. For detailed information, visit the official government portals and check current eligibility criteria."
        
        return "Thank you for your question. Please visit the official government scheme portals for accurate, up-to-date information about eligibility and application processes."
