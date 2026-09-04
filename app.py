"""
SchemeWise: AI-powered Government Scheme Eligibility & Recommendation Platform
Main Flask Application
"""

from flask import Flask, render_template, jsonify, request
import json
from pathlib import Path
from services.matcher import MatchingEngine
from services.ai_service import AIService

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Load schemes data
def load_schemes():
    schemes_path = Path(__file__).parent / 'data' / 'schemes.json'
    with open(schemes_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Initialize services
schemes_data = load_schemes()
matcher = MatchingEngine(schemes_data)
ai_service = AIService()

@app.route('/')
def index():
    """Render the main homepage"""
    return render_template('index.html')

@app.route('/api/schemes')
def get_schemes():
    """Return all available schemes"""
    return jsonify({
        'status': 'success',
        'count': len(schemes_data),
        'schemes': schemes_data
    })

@app.route('/api/check-eligibility', methods=['POST'])
def check_eligibility():
    """
    Check eligibility for schemes based on user profile
    Expects JSON: user profile with name, age, state, income, etc.
    """
    try:
        user_profile = request.get_json()
        
        if not user_profile:
            return jsonify({
                'status': 'error',
                'message': 'No user profile provided'
            }), 400
        
        # Get matching schemes
        matches = matcher.find_matches(user_profile)
        
        # Get AI explanations for each match
        results = []
        for match in matches:
            explanation = ai_service.generate_explanation(
                user_profile=user_profile,
                scheme=match['scheme'],
                score=match['score'],
                reasons=match['reasons']
            )
            
            results.append({
                'scheme': match['scheme'],
                'score': match['score'],
                'match_level': match['match_level'],
                'reasons': match['reasons'],
                'explanation': explanation,
                'documents': match.get('documents', [])
            })
        
        return jsonify({
            'status': 'success',
            'profile': user_profile,
            'total_matches': len(results),
            'matches': results,
            'disclaimer': 'SchemeWise provides informational recommendations based on the information provided. This does not guarantee official eligibility. Always verify current requirements through the official source before applying.'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error processing eligibility check: {str(e)}'
        }), 500

@app.route('/api/ask', methods=['POST'])
def ask_schemewise():
    """
    AI-powered chatbot for answering questions about schemes
    Expects JSON: { question: "..." }
    """
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'status': 'error',
                'message': 'Please provide a question'
            }), 400
        
        # Get AI response
        response = ai_service.answer_question(question, schemes_data)
        
        return jsonify({
            'status': 'success',
            'question': question,
            'answer': response
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error processing question: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
