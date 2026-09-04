// ======================
// SCHEMEWISE JAVASCRIPT
// ======================

// Global state
let currentStep = 1;
const totalSteps = 3;
let currentMatches = [];
let allMatches = [];
let userProfile = null;

// DOM Elements
const form = document.getElementById('eligibilityForm');
const nextBtn = document.getElementById('nextBtn');
const backBtn = document.getElementById('backBtn');
const checkEligibilityBtn = document.getElementById('checkEligibilityBtn');
const heroCheckBtn = document.getElementById('heroCheckBtn');
const demoBtnHero = document.getElementById('demoBtnHero');
const resultsSection = document.getElementById('resultsSection');
const eligibilitySection = document.querySelector('.eligibility-form-section');
const schemeModal = document.getElementById('schemeModal');
const modalClose = document.getElementById('modalClose');
const loadingOverlay = document.getElementById('loadingOverlay');
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
const navLink = document.querySelectorAll('.nav-link');

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    setupFormSteps();
    setupChatbot();
});

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    nextBtn.addEventListener('click', handleNextStep);
    backBtn.addEventListener('click', handleBackStep);
    checkEligibilityBtn.addEventListener('click', scrollToForm);
    heroCheckBtn.addEventListener('click', scrollToForm);
    demoBtnHero.addEventListener('click', loadDemoProfile);
    form.addEventListener('submit', handleFormSubmit);
    modalClose.addEventListener('click', closeModal);
    schemeModal.addEventListener('click', function(e) {
        if (e.target === schemeModal) closeModal();
    });
    
    // Close modal on Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeModal();
    });
    
    // Hamburger menu
    hamburger.addEventListener('click', toggleMobileMenu);
    navLink.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.classList.remove('active');
        });
    });
    
    // Filter and sort listeners
    document.getElementById('categoryFilter')?.addEventListener('change', filterResults);
    document.getElementById('scoreFilter')?.addEventListener('change', filterResults);
    document.getElementById('sortFilter')?.addEventListener('change', filterResults);
}

// ===== MOBILE MENU =====
function toggleMobileMenu() {
    navLinks.classList.toggle('active');
}

// ===== FORM STEP HANDLING =====
function setupFormSteps() {
    // Initialize step dots
    updateStepIndicator();
}

function handleNextStep(e) {
    e.preventDefault();
    
    // Validate current step
    if (!validateStep(currentStep)) {
        alert('Please fill all required fields correctly.');
        return;
    }
    
    if (currentStep < totalSteps) {
        currentStep++;
        updateFormDisplay();
    } else {
        // Submit form
        handleFormSubmit(e);
    }
}

function handleBackStep(e) {
    e.preventDefault();
    if (currentStep > 1) {
        currentStep--;
        updateFormDisplay();
    }
}

function validateStep(step) {
    const formElements = document.querySelectorAll(`.form-step[data-step="${step}"] [required]`);
    let isValid = true;
    
    formElements.forEach(element => {
        if (!element.value || element.value.trim() === '') {
            isValid = false;
            element.focus();
            element.style.borderColor = '#ef4444';
        } else {
            element.style.borderColor = '';
        }
    });
    
    return isValid;
}

function updateFormDisplay() {
    // Hide all steps
    document.querySelectorAll('.form-step').forEach(step => {
        step.classList.remove('active');
    });
    
    // Show current step
    document.querySelector(`.form-step[data-step="${currentStep}"]`).classList.add('active');
    
    // Update buttons
    backBtn.style.display = currentStep > 1 ? 'block' : 'none';
    nextBtn.textContent = currentStep === totalSteps ? 'Find My Schemes' : 'Continue →';
    
    // Update step indicator
    updateStepIndicator();
    
    // Scroll to form
    form.scrollIntoView({ behavior: 'smooth' });
}

function updateStepIndicator() {
    document.querySelectorAll('.step-dot').forEach((dot, index) => {
        if (index + 1 <= currentStep) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
}

// ===== FORM SUBMISSION =====
function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!validateStep(currentStep)) {
        alert('Please fill all required fields.');
        return;
    }
    
    // Collect form data
    userProfile = getFormData();
    
    // Show loading and fetch results
    showLoading();
    checkEligibility(userProfile);
}

function getFormData() {
    const formData = new FormData(form);
    const profile = {};
    
    formData.forEach((value, key) => {
        if (key === 'is_student' || key === 'is_farmer' || key === 'has_disability') {
            profile[key] = value === 'true';
        } else if (key === 'annual_income' || key === 'age') {
            profile[key] = parseInt(value);
        } else {
            profile[key] = value;
        }
    });
    
    return profile;
}

// ===== DEMO PROFILE =====
function loadDemoProfile() {
    const demoProfile = {
        name: 'Demo User',
        age: 21,
        gender: 'Male',
        state: 'Rajasthan',
        district: 'Jaipur',
        annual_income: 250000,
        occupation: 'Student',
        employment_status: 'Student',
        education: 'Undergraduate',
        social_category: 'OBC',
        is_student: true,
        is_farmer: false,
        has_disability: false
    };
    
    populateForm(demoProfile);
    currentStep = 1;
    updateFormDisplay();
    scrollToForm();
}

function populateForm(profile) {
    document.getElementById('fullName').value = profile.name;
    document.getElementById('age').value = profile.age;
    document.getElementById('gender').value = profile.gender;
    document.getElementById('state').value = profile.state;
    document.getElementById('district').value = profile.district;
    document.getElementById('income').value = profile.annual_income;
    document.getElementById('occupation').value = profile.occupation;
    document.getElementById('employment').value = profile.employment_status;
    document.getElementById('education').value = profile.education;
    document.getElementById('category').value = profile.social_category;
    
    // Set radio buttons
    document.querySelector(`input[name="is_student"][value="${profile.is_student}"]`).checked = true;
    document.querySelector(`input[name="is_farmer"][value="${profile.is_farmer}"]`).checked = true;
    document.querySelector(`input[name="has_disability"][value="${profile.has_disability}"]`).checked = true;
}

function scrollToForm() {
    eligibilitySection.scrollIntoView({ behavior: 'smooth' });
    currentStep = 1;
    updateFormDisplay();
}

// ===== API CALLS =====
async function checkEligibility(profile) {
    try {
        const response = await fetch('/api/check-eligibility', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(profile)
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.status === 'success') {
            allMatches = data.matches;
            displayResults(data);
        } else {
            alert('Error: ' + (data.message || 'Could not process your request'));
        }
    } catch (error) {
        hideLoading();
        alert('Error: ' + error.message);
        console.error('Error:', error);
    }
}

// ===== RESULTS DISPLAY =====
function displayResults(data) {
    // Update profile summary
    document.getElementById('summaryName').textContent = data.profile.name;
    document.getElementById('summaryAge').textContent = data.profile.age + ' years';
    document.getElementById('summaryState').textContent = data.profile.state;
    document.getElementById('summaryIncome').textContent = '₹' + data.profile.annual_income.toLocaleString();
    document.getElementById('summaryOccupation').textContent = data.profile.occupation;
    document.getElementById('summaryCategory').textContent = data.profile.social_category;
    document.getElementById('matchCount').textContent = data.total_matches;
    
    // Populate category filter
    const categories = [...new Set(data.matches.map(m => m.scheme.category))];
    const categorySelect = document.getElementById('categoryFilter');
    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        categorySelect.appendChild(option);
    });
    
    currentMatches = data.matches;
    renderSchemeCards(data.matches);
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function renderSchemeCards(matches) {
    const container = document.getElementById('schemesContainer');
    container.innerHTML = '';
    
    if (matches.length === 0) {
        container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #64748b;">No matching schemes found. Try adjusting your profile information.</p>';
        return;
    }
    
    matches.forEach(match => {
        const card = createSchemeCard(match);
        container.appendChild(card);
    });
}

function createSchemeCard(match) {
    const card = document.createElement('div');
    card.className = 'scheme-card';
    
    const scheme = match.scheme;
    const score = match.score;
    const matchLevel = match.match_level;
    const reasons = match.reasons.slice(0, 3); // Top 3 reasons
    
    card.innerHTML = `
        <div class="scheme-header">
            <span class="scheme-category">${scheme.category}</span>
        </div>
        <h3>${scheme.name}</h3>
        <p class="scheme-description">${scheme.description}</p>
        
        <div class="match-score-section">
            <div class="match-score-circle">${score}%</div>
            <div class="match-info-text">
                <h4>Match Score</h4>
                <div class="match-level">${matchLevel}</div>
            </div>
        </div>
        
        <div class="scheme-reasons">
            <strong>Why you matched:</strong>
            <ul>
                ${reasons.map(r => `<li>${r}</li>`).join('')}
            </ul>
        </div>
        
        <div class="scheme-buttons">
            <button class="view-details-btn" onclick="openSchemeModal(${currentMatches.indexOf(match)})">View Details</button>
            <button class="check-source-btn" onclick="alert('Visit the official government portal for the latest information')">Check Source</button>
        </div>
    `;
    
    return card;
}

// ===== MODAL HANDLING =====
function openSchemeModal(index) {
    const match = currentMatches[index];
    const scheme = match.scheme;
    const score = match.score;
    const matchLevel = match.match_level;
    const reasons = match.reasons;
    const explanation = match.explanation;
    
    // Update modal content
    document.getElementById('modalSchemeName').textContent = scheme.name;
    document.getElementById('modalCategory').textContent = scheme.category;
    document.getElementById('modalDescription').textContent = scheme.description;
    document.getElementById('modalScore').textContent = score + '%';
    document.getElementById('modalMatchLevel').textContent = matchLevel;
    document.getElementById('modalExplanation').textContent = explanation;
    document.getElementById('modalBenefits').textContent = scheme.benefits;
    
    // Update reasons
    const reasonsList = document.getElementById('modalReasons');
    reasonsList.innerHTML = '';
    reasons.forEach(reason => {
        const li = document.createElement('li');
        li.textContent = reason;
        reasonsList.appendChild(li);
    });
    
    // Update documents
    const documentsList = document.getElementById('modalDocuments');
    documentsList.innerHTML = '';
    scheme.documents.forEach(doc => {
        const li = document.createElement('li');
        li.textContent = doc;
        documentsList.appendChild(li);
    });
    
    // Update steps
    const stepsList = document.getElementById('modalSteps');
    stepsList.innerHTML = '';
    scheme.application_steps.forEach(step => {
        const li = document.createElement('li');
        li.textContent = step;
        stepsList.appendChild(li);
    });
    
    // Update progress circle
    const percentage = score;
    const circumference = 2 * Math.PI * 45;
    const offset = circumference - (percentage / 100) * circumference;
    const progressCircle = document.getElementById('progressCircle');
    if (progressCircle) {
        progressCircle.style.strokeDashoffset = offset;
    }
    
    // Show modal
    schemeModal.classList.add('active');
}

function closeModal() {
    schemeModal.classList.remove('active');
}

// ===== FILTERING AND SORTING =====
function filterResults() {
    const categoryFilter = document.getElementById('categoryFilter').value;
    const scoreFilter = parseInt(document.getElementById('scoreFilter').value);
    const sortFilter = document.getElementById('sortFilter').value;
    
    let filtered = allMatches.filter(match => {
        const categoryMatch = !categoryFilter || match.scheme.category === categoryFilter;
        const scoreMatch = match.score >= scoreFilter;
        return categoryMatch && scoreMatch;
    });
    
    // Sort
    if (sortFilter === 'score') {
        filtered.sort((a, b) => b.score - a.score);
    } else if (sortFilter === 'name') {
        filtered.sort((a, b) => a.scheme.name.localeCompare(b.scheme.name));
    }
    
    currentMatches = filtered;
    renderSchemeCards(filtered);
}

// ===== LOADING STATE =====
function showLoading() {
    loadingOverlay.style.display = 'flex';
    const messages = [
        'Analyzing your profile...',
        'Checking eligibility factors...',
        'Finding relevant schemes...',
        'Preparing your personalized results...'
    ];
    
    let msgIndex = 0;
    const msgElement = document.getElementById('loadingMessage');
    
    const interval = setInterval(() => {
        msgIndex++;
        if (msgIndex < messages.length) {
            msgElement.textContent = messages[msgIndex];
        } else {
            clearInterval(interval);
        }
    }, 1500);
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// ===== CHATBOT =====
function setupChatbot() {
    const chatInput = document.getElementById('chatInput');
    const chatSendBtn = document.getElementById('chatSendBtn');
    
    if (!chatInput || !chatSendBtn) return;
    
    chatSendBtn.addEventListener('click', sendChat);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendChat();
        }
    });
}

function askQuestion(question) {
    const chatInput = document.getElementById('chatInput');
    chatInput.value = question;
    sendChat();
}

async function sendChat() {
    const chatInput = document.getElementById('chatInput');
    const question = chatInput.value.trim();
    
    if (!question) return;
    
    // Add user message
    addChatMessage(question, 'user');
    chatInput.value = '';
    
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            addChatMessage(data.answer, 'bot');
        } else {
            addChatMessage('Sorry, I could not process your question. Please try again.', 'bot');
        }
    } catch (error) {
        console.error('Error:', error);
        addChatMessage('Sorry, there was an error. Please try again.', 'bot');
    }
}

function addChatMessage(text, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const p = document.createElement('p');
    p.textContent = text;
    messageDiv.appendChild(p);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ===== UTILITY FUNCTIONS =====
function formatCurrency(amount) {
    return '₹' + amount.toLocaleString('en-IN');
}

// Add some polish with scroll animations
document.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.75) {
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }
    });
});
