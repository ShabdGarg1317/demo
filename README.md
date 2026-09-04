# SchemeWise

**AI-powered Government Scheme Eligibility & Recommendation Platform**

SchemeWise helps users discover government schemes relevant to their profile through an intuitive interface powered by intelligent matching algorithms and optional AI explanations.

---

## 🎯 Features

✅ **Personalized Scheme Matching** - Compare your profile against multiple government schemes  
✅ **Transparent Scoring** - Understand why you matched with each scheme  
✅ **Multi-step Form** - Easy-to-follow eligibility questionnaire  
✅ **Rich Scheme Information** - Benefits, documents, and application steps  
✅ **Demo Profile** - Try the platform instantly with sample data  
✅ **Smart Filters** - Filter by category, score, and sort results  
✅ **AI Assistant** - Ask questions about schemes (optional OpenAI integration)  
✅ **Mobile Friendly** - Fully responsive design  
✅ **No API Required** - Works perfectly without OpenAI API key  

---

## 🏗️ Architecture

```
SchemeWise/
├── app.py                    # Flask application & API routes
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
│
├── data/
│   └── schemes.json          # Sample government scheme data
│
├── services/
│   ├── __init__.py
│   ├── matcher.py            # Matching engine with weighted scoring
│   └── ai_service.py         # AI explanations & chatbot (optional OpenAI)
│
├── templates/
│   └── index.html            # Main application UI
│
└── static/
    ├── style.css             # Premium styling with animations
    └── script.js             # Frontend logic & interactivity
```

---

## 📋 Folder Structure

### Backend
- **app.py** - Main Flask application with 4 core routes:
  - `GET /` - Renders homepage
  - `GET /api/schemes` - Returns all schemes
  - `POST /api/check-eligibility` - Processes user profile and returns matches
  - `POST /api/ask` - AI-powered chatbot endpoint

### Services
- **matcher.py** - Matching engine implementing weighted scoring algorithm:
  - State match (20 points)
  - Age match (15 points)
  - Income match (20 points)
  - Occupation match (15 points)
  - Category match (10 points)
  - Special status (20 points)
  
- **ai_service.py** - AI integration layer:
  - Optional OpenAI API integration
  - Local fallback explanations
  - RAG-based chatbot for scheme questions

### Frontend
- **HTML** - Semantic structure with multiple sections
- **CSS** - Modern premium styling with animations and transitions
- **JavaScript** - Complex interactive features with no framework dependencies

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Setup
```bash
# Navigate to the project folder
cd SchemeWise

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment (Optional)
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key (optional)
# OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

If you don't have an OpenAI API key, the application will automatically use local explanations.

### Step 4: Run the Application
```bash
python app.py
```

The application will start at `http://127.0.0.1:5000`

---

## 💻 Using the Platform

### 1. **Landing Page**
- View the hero section with key information
- See statistics and how it works
- Click "Check Eligibility" or "Try Demo Profile"

### 2. **Try Demo Profile**
- Automatically fills the form with sample data
- Edit any field before submitting
- Demonstrates full functionality instantly

### 3. **Eligibility Form**
- **Step 1**: Basic information (name, age, gender, state, district)
- **Step 2**: Financial & professional (income, occupation, employment, education)
- **Step 3**: Eligibility factors (category, student/farmer/disability status)
- Click "Find My Schemes" to process

### 4. **Results**
- View your profile summary
- See all matching schemes ranked by score
- Filter by category or minimum score
- Sort by best match or alphabetically

### 5. **Scheme Details**
- Click "View Details" to see full information
- Match percentage with visual indicator
- Why you matched with detailed reasons
- AI-generated explanation
- Benefits, required documents, and application steps

### 6. **Ask SchemeWise**
- Ask questions about government schemes
- Chatbot searches scheme database
- AI-powered responses (or local templates)
- Suggested questions available

---

## 🔧 The Matching Engine

The matching algorithm uses **transparent weighted scoring** to rank schemes:

```
Score Calculation:
├── State Match (20 points)
├── Age Match (15 points)
├── Income Match (20 points)
├── Occupation Match (15 points)
├── Category Match (10 points)
└── Special Status - Student/Farmer/Disability/Employment (20 points)

Match Classification:
├── 90-100: Excellent Match
├── 75-89: Strong Match
├── 60-74: Potential Match
└── <60: Not recommended
```

### How It Works
1. **Input Validation** - Checks user profile data
2. **Eligibility Scoring** - Calculates match score for each scheme
3. **Ranking** - Sorts schemes by score (highest first)
4. **Explanation Generation** - Creates human-readable reasons
5. **Result Display** - Shows top 5 matches with details

---

## 🤖 AI Integration

### With OpenAI API
If `OPENAI_API_KEY` environment variable is set:
- Generates natural language explanations for each scheme match
- Provides intelligent answers to scheme-related questions
- Uses retrieved scheme data to ensure accuracy

### Without API Key
If no API key provided:
- Uses local template-based explanations
- Provides keyword-based chatbot responses
- **All features remain fully functional**

### Graceful Fallback
- If API call fails, automatically uses local explanations
- User never sees API errors
- Transparent switching between AI and local modes

---

## 📊 Sample Data

The `data/schemes.json` file contains **15 sample government schemes** across categories:

- ✏️ **Education** - Student scholarships and loans
- 🌾 **Agriculture** - Farmer support and subsidies
- 👩 **Women Empowerment** - Entrepreneurship and business support
- 💼 **Skill Development** - Vocational training programs
- 🏥 **Healthcare** - Health coverage and support
- 🏠 **Housing** - Affordable housing schemes
- 💼 **Employment** - Job placement and wage support
- ♿ **Disability** - Support for persons with disabilities
- 👴 **Senior Citizens** - Pension and social security
- 🚀 **Entrepreneurship** - Startup funding and support
- 🏘️ **Rural Development** - Community development programs
- 🌱 **Environment** - Green energy and sustainability

All schemes are clearly marked as **DEMO SCHEMES** for demonstration purposes.

---

## 🔐 Important Disclaimer

⚠️ **This is a demonstration platform.** 

- SchemeWise provides informational recommendations based on user input
- **This does NOT guarantee official eligibility**
- Always verify the latest official eligibility criteria before applying
- Information is based on the scheme database provided
- Application processes and benefits may have changed
- **Always consult official government portals for authoritative information**

---

## 🛠️ How to Add More Schemes

1. Open `data/schemes.json`
2. Add a new scheme object following this structure:

```json
{
  "id": "scheme_unique_id",
  "name": "Scheme Name",
  "category": "Category",
  "description": "Brief description",
  "states": ["State1", "State2", "All India"],
  "min_age": 18,
  "max_age": 65,
  "max_income": 500000,
  "occupations": ["Occupation1", "Occupation2"],
  "categories": ["OBC", "SC", "ST", "General"],
  "student_required": false,
  "farmer_required": false,
  "disability_required": false,
  "employment_status": ["Employed", "Self-Employed"],
  "education_levels": ["Undergraduate", "Postgraduate"],
  "benefits": "Description of benefits",
  "documents": ["Document1", "Document2"],
  "application_steps": ["Step 1", "Step 2", "Step 3"],
  "application_url": "#"
}
```

3. Save the file
4. Restart the Flask application
5. New schemes will appear automatically

---

## 💬 Chatbot Functionality

### Question Processing
1. User enters a question
2. System retrieves relevant schemes using keyword matching
3. AI or local system generates answer using retrieved schemes only
4. Never invents information - only uses provided scheme data

### Example Questions
- "Which schemes are for students?"
- "What documents do I need?"
- "Are there schemes for farmers?"
- "Tell me about women entrepreneurship programs"

---

## 📱 Responsive Design

The platform is fully responsive:
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

Optimized for all screen sizes with touch-friendly interface.

---

## ⚡ Performance Optimization

- Minimal dependencies (only Flask and python-dotenv required)
- No heavy frontend frameworks
- Vanilla JavaScript for interactivity
- Efficient CSS with animations
- Quick API response times
- Local fallback for all AI features

---

## 🐛 Troubleshooting

### Issue: Flask won't start
**Solution:** Ensure Python 3.8+ and all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: API returns 404
**Solution:** Ensure you're accessing `http://127.0.0.1:5000/` (not `/api/` without full path)

### Issue: No results found
**Solution:** 
- Check your income level - it may exceed scheme maximums
- Try the demo profile for guaranteed matches
- Verify form data was properly submitted

### Issue: AI explanations not working
**Solution:** 
- Check if `OPENAI_API_KEY` is set correctly in `.env`
- Ensure API key is valid and has quota
- Platform automatically falls back to local explanations
- This is not an error - it's by design

---

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application with routing & API endpoints |
| `matcher.py` | Weighted scoring algorithm for scheme matching |
| `ai_service.py` | AI explanations & chatbot with optional OpenAI |
| `schemes.json` | Database of sample government schemes |
| `index.html` | Complete HTML structure with all sections |
| `style.css` | Premium styling with animations & responsiveness |
| `script.js` | Interactive features, form handling, API calls |
| `requirements.txt` | Python package dependencies |
| `.env.example` | Template for environment variables |
| `.gitignore` | Files to ignore in version control |

---

## 🔄 Workflow Summary

```
User Visits Homepage
    ↓
Fills Eligibility Form (3 steps)
    ↓
Clicks "Find My Schemes"
    ↓
Flask receives POST request to /api/check-eligibility
    ↓
Matching engine calculates scores
    ↓
AI service generates explanations
    ↓
Results returned as JSON
    ↓
Frontend displays results with filtering/sorting
    ↓
User can view details or ask questions
    ↓
Chatbot uses scheme data to answer questions
```

---

## 🎓 Key Technical Features

- ✅ No database required (JSON file-based)
- ✅ No external CDNs (all CSS/JS local)
- ✅ No npm/webpack (pure vanilla JavaScript)
- ✅ Optional AI (graceful degradation)
- ✅ Full error handling
- ✅ Mobile responsive
- ✅ Accessible HTML/CSS
- ✅ Clean, documented code

---

## 📜 License

This is a demonstration project for educational purposes.

---

## 🙋 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the console for error messages
3. Ensure all files are in correct locations
4. Verify environment setup

---

**Built for the hackathon. Simple. Elegant. Effective.**

*Government Support, Simplified.*
