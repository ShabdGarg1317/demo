"""
SchemeWise Matching Engine
Implements weighted scoring algorithm to find matching government schemes
"""

class MatchingEngine:
    """
    Transparent weighted recommendation algorithm
    """
    
    def __init__(self, schemes_data):
        self.schemes = schemes_data
    
    def find_matches(self, user_profile):
        """
        Find matching schemes for a user profile.
        Returns top 5 schemes with scores and reasons.
        """
        scores = []
        
        for scheme in self.schemes:
            score, reasons = self._calculate_score(user_profile, scheme)
            if score >= 60:  # Minimum threshold
                scores.append({
                    'scheme': scheme,
                    'score': score,
                    'match_level': self._get_match_level(score),
                    'reasons': reasons
                })
        
        # Sort by score descending and return top 5
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:5]
    
    def _calculate_score(self, user_profile, scheme):
        """
        Calculate eligibility score using weighted criteria.
        Total: 100 points
        """
        score = 0
        reasons = []
        
        # State match (20 points)
        state_score, state_reason = self._check_state(user_profile, scheme)
        score += state_score
        if state_reason:
            reasons.append(state_reason)
        
        # Age match (15 points)
        age_score, age_reason = self._check_age(user_profile, scheme)
        score += age_score
        if age_reason:
            reasons.append(age_reason)
        
        # Income match (20 points)
        income_score, income_reason = self._check_income(user_profile, scheme)
        score += income_score
        if income_reason:
            reasons.append(income_reason)
        
        # Occupation match (15 points)
        occ_score, occ_reason = self._check_occupation(user_profile, scheme)
        score += occ_score
        if occ_reason:
            reasons.append(occ_reason)
        
        # Category match (10 points)
        cat_score, cat_reason = self._check_category(user_profile, scheme)
        score += cat_score
        if cat_reason:
            reasons.append(cat_reason)
        
        # Special status match (20 points)
        special_score, special_reason = self._check_special_status(user_profile, scheme)
        score += special_score
        if special_reason:
            reasons.extend(special_reason)
        
        return min(score, 100), reasons
    
    def _check_state(self, user_profile, scheme):
        """Check if user's state matches scheme's supported states (20 points)"""
        user_state = user_profile.get('state', '').strip()
        scheme_states = scheme.get('states', [])
        
        if not user_state or not scheme_states:
            return 0, None
        
        # Allow "All India" as a universal match
        if user_state in scheme_states or 'All India' in scheme_states:
            return 20, "✓ Your state is supported by this scheme"
        
        return 0, "✗ Your state may not be covered by this scheme"
    
    def _check_age(self, user_profile, scheme):
        """Check if user's age is within scheme's age range (15 points)"""
        try:
            user_age = int(user_profile.get('age', 0))
            min_age = scheme.get('min_age', 0)
            max_age = scheme.get('max_age', 100)
            
            if min_age <= user_age <= max_age:
                return 15, f"✓ Your age ({user_age} years) is within the eligible range"
            else:
                return 0, f"✗ Age requirement: {min_age}-{max_age} years"
        except:
            return 0, None
    
    def _check_income(self, user_profile, scheme):
        """Check if user's income is within scheme's limit (20 points)"""
        try:
            user_income = int(user_profile.get('annual_income', 0))
            max_income = scheme.get('max_income', float('inf'))
            
            if user_income <= max_income:
                return 20, "✓ Your income is within the listed threshold"
            else:
                return 0, f"✗ Income limit: ₹{max_income:,}"
        except:
            return 0, None
    
    def _check_occupation(self, user_profile, scheme):
        """Check if user's occupation matches scheme (15 points)"""
        user_occupation = user_profile.get('occupation', '').strip()
        scheme_occupations = scheme.get('occupations', [])
        
        if not user_occupation or not scheme_occupations:
            return 0, None
        
        if user_occupation in scheme_occupations:
            return 15, f"✓ Your occupation ({user_occupation}) matches the scheme"
        
        return 0, None
    
    def _check_category(self, user_profile, scheme):
        """Check if user's category matches scheme (10 points)"""
        user_category = user_profile.get('social_category', '').strip()
        scheme_categories = scheme.get('categories', [])
        
        if not user_category or not scheme_categories:
            return 0, None
        
        if user_category in scheme_categories:
            return 10, f"✓ Your social category ({user_category}) is eligible"
        
        return 0, None
    
    def _check_special_status(self, user_profile, scheme):
        """Check special status: student, farmer, disability, employment (20 points)"""
        reasons = []
        score = 0
        
        # Student check
        is_student = user_profile.get('is_student', False)
        scheme_requires_student = scheme.get('student_required', False)
        scheme_allows_student = 'Student' in scheme.get('employment_status', [])
        
        if scheme_requires_student and is_student:
            score += 5
            reasons.append("✓ Your student status matches the scheme")
        elif scheme_requires_student and not is_student:
            reasons.append("✗ This scheme requires student status")
        elif not scheme_requires_student and is_student and scheme_allows_student:
            score += 3
        
        # Farmer check
        is_farmer = user_profile.get('is_farmer', False)
        scheme_requires_farmer = scheme.get('farmer_required', False)
        
        if scheme_requires_farmer and is_farmer:
            score += 5
            reasons.append("✓ Your farmer status matches the scheme")
        elif scheme_requires_farmer and not is_farmer:
            reasons.append("✗ This scheme requires farmer status")
        
        # Disability check
        has_disability = user_profile.get('has_disability', False)
        scheme_requires_disability = scheme.get('disability_required', False)
        
        if scheme_requires_disability and has_disability:
            score += 5
            reasons.append("✓ This scheme supports persons with disabilities")
        elif scheme_requires_disability and not has_disability:
            reasons.append("✗ This scheme is specifically for persons with disabilities")
        
        # Employment status check
        employment_status = user_profile.get('employment_status', '').strip()
        scheme_employment = scheme.get('employment_status', [])
        
        if employment_status and scheme_employment:
            if employment_status in scheme_employment:
                score += 5
                reasons.append(f"✓ Your employment status ({employment_status}) matches")
        
        return score, reasons
    
    def _get_match_level(self, score):
        """Classify the match level based on score"""
        if score >= 90:
            return "Excellent Match"
        elif score >= 75:
            return "Strong Match"
        elif score >= 60:
            return "Potential Match"
        else:
            return "Low Match"
