# app.py
import streamlit as st
import pandas as pd
import numpy as np
import json
import random
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Nexus Insight Assessment",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2e86ab;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .question-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .result-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 0.8rem;
    }
    .recommendation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

class NexusInsightAssessment:
    def __init__(self):
        self.dimensions = {
            'Psy': 'Psychological Metrics',
            'CT': 'Critical Thinking', 
            'LD': 'Leadership',
            'Cog': 'Cognitive Skills',
            'TR': 'Team Roles'
        }
        
        self.questions = self._create_questions()
        
    def _create_questions(self):
        """Create assessment questions"""
        return [
            {
                "id": 1,
                "text": "You're the young founder of an AI startup. After 6 months of launch, a major competitor copies your product and offers it at 50% lower price. Your team is demotivated. What do you do?",
                "type": "situational_judgment",
                "options": [
                    {"text": "Rush to develop unique features and lower prices", "weights": {"Psy": -2, "LD": 2, "CT": 1}},
                    {"text": "Host brainstorming session for creative solutions", "weights": {"LD": 3, "TR": 3, "Cog": 2}},
                    {"text": "Focus on different customer segment", "weights": {"CT": 3, "LD": 2, "Psy": 2}},
                    {"text": "Seek strategic partnership", "weights": {"TR": 3, "LD": 2, "CT": 2}}
                ]
            },
            {
                "id": 2,
                "text": "An investor asks you to completely change your business model for funding. This conflicts with your core vision. How do you handle this?",
                "type": "ethical_dilemma", 
                "options": [
                    {"text": "Reject the offer and maintain your vision", "weights": {"Psy": 3, "LD": 2, "CT": -1}},
                    {"text": "Accept with minor adjustments", "weights": {"TR": 2, "LD": 1, "Psy": 1}},
                    {"text": "Negotiate to find middle ground", "weights": {"LD": 3, "CT": 2, "TR": 2}},
                    {"text": "Request time to consult mentors", "weights": {"CT": 3, "Psy": 2, "Cog": 1}}
                ]
            },
            {
                "id": 3,
                "text": "Your top performer is highly productive but creates team conflicts. Do you prioritize results or team harmony?",
                "type": "leadership_dilemma",
                "options": [
                    {"text": "Focus on results and manage conflicts separately", "weights": {"LD": 2, "Psy": -1, "TR": -2}},
                    {"text": "Coach the employee on teamwork", "weights": {"LD": 3, "Psy": 2, "TR": 3}},
                    {"text": "Reassign to individual contributor role", "weights": {"TR": 2, "LD": 1, "CT": 1}},
                    {"text": "Implement team-building activities", "weights": {"TR": 3, "LD": 2, "Psy": 2}}
                ]
            },
            {
                "id": 4,
                "text": "As a manager, you need to lead digital transformation. 60% of employees resist change. What's your strategy?",
                "type": "change_management", 
                "options": [
                    {"text": "Enforce change gradually with training", "weights": {"LD": 2, "Psy": -1, "TR": 1}},
                    {"text": "Identify 'change champions' as ambassadors", "weights": {"TR": 3, "LD": 3, "Psy": 2}},
                    {"text": "Start with small pilot project", "weights": {"CT": 3, "LD": 2, "Cog": 1}},
                    {"text": "Redesign incentives for adoption", "weights": {"LD": 3, "Psy": 2, "CT": 2}}
                ]
            },
            {
                "id": 5,
                "text": "AI implementation will replace 30% of manual jobs. How do you lead this transition ethically?",
                "type": "ethical_leadership",
                "options": [
                    {"text": "Implement quickly with severance packages", "weights": {"LD": 1, "Psy": -3, "CT": 1}},
                    {"text": "Create upskilling programs", "weights": {"LD": 4, "TR": 3, "Psy": 3}},
                    {"text": "Slow implementation and seek alternatives", "weights": {"CT": 2, "LD": 2, "TR": 2}},
                    {"text": "Form employee committee to co-design", "weights": {"TR": 4, "LD": 3, "CT": 3}}
                ]
            },
            {
                "id": 6,
                "text": "Market research shows your product is becoming obsolete. Do you invest in improvements or innovation?",
                "type": "strategic_decision",
                "options": [
                    {"text": "Focus on improving existing features", "weights": {"CT": 2, "LD": 1, "Psy": -1}},
                    {"text": "Allocate resources for breakthrough innovation", "weights": {"LD": 3, "CT": 3, "Cog": 2}},
                    {"text": "Pursue both paths with separate teams", "weights": {"TR": 3, "LD": 2, "CT": 2}},
                    {"text": "Acquire innovative startup", "weights": {"CT": 3, "LD": 2, "TR": 1}}
                ]
            },
            {
                "id": 7,
                "text": "Major data breach exposes customer information. Media is calling. What's your first response?",
                "type": "crisis_management",
                "options": [
                    {"text": "Issue immediate public apology", "weights": {"LD": 3, "CT": 2, "Psy": 2}},
                    {"text": "First contain breach, then communicate", "weights": {"CT": 3, "LD": 2, "Cog": 2}},
                    {"text": "Blame technical issues", "weights": {"LD": -3, "Psy": -2, "CT": -1}},
                    {"text": "Activate crisis team protocol", "weights": {"LD": 4, "CT": 3, "TR": 3}}
                ]
            },
            {
                "id": 8,
                "text": "Expanding to new international market, you discover cultural practices conflicting with company values. How do you proceed?",
                "type": "cross_cultural",
                "options": [
                    {"text": "Adapt company practices to local culture", "weights": {"TR": 2, "LD": 1, "Psy": 1}},
                    {"text": "Maintain company values and educate", "weights": {"LD": 3, "CT": 2, "Psy": 2}},
                    {"text": "Find compromise respecting both", "weights": {"CT": 3, "LD": 3, "TR": 2}},
                    {"text": "Reconsider market entry", "weights": {"CT": 4, "LD": 2, "Psy": 3}}
                ]
            },
            {
                "id": 9,
                "text": "New technology could transform your industry in 5 years. Do you invest now or wait?",
                "type": "future_strategy",
                "options": [
                    {"text": "Heavy investment to become early leader", "weights": {"LD": 3, "CT": 2, "Psy": 1}},
                    {"text": "Wait for clear ROI and proven use cases", "weights": {"CT": 3, "LD": 1, "Psy": 2}},
                    {"text": "Form strategic partnerships to share risk", "weights": {"TR": 3, "LD": 2, "CT": 2}},
                    {"text": "Create innovation lab for experimentation", "weights": {"Cog": 3, "LD": 2, "CT": 3}}
                ]
            },
            {
                "id": 10,
                "text": "Your company is accused of greenwashing. Environmental groups are protesting. How do you restore trust?",
                "type": "reputation_management",
                "options": [
                    {"text": "Issue strong denial", "weights": {"LD": -2, "CT": -1, "Psy": -3}},
                    {"text": "Admit shortcomings and present plan", "weights": {"LD": 4, "CT": 3, "Psy": 3}},
                    {"text": "Hire PR firm to manage narrative", "weights": {"CT": 1, "LD": 1, "TR": 1}},
                    {"text": "Engage with protesters co-create goals", "weights": {"TR": 4, "LD": 3, "CT": 3}}
                ]
            }
        ]

    def calculate_scores(self, responses):
        """Calculate dimension scores"""
        dimension_totals = {dim: 0 for dim in self.dimensions.keys()}
        question_counts = {dim: 0 for dim in self.dimensions.keys()}
        
        for q_id, response in responses.items():
            question = next((q for q in self.questions if q["id"] == int(q_id)), None)
            if question and "selected_option" in response:
                option_index = response["selected_option"]
                if 0 <= option_index < len(question["options"]):
                    selected_option = question["options"][option_index]
                    
                    for dim, weight in selected_option["weights"].items():
                        dimension_totals[dim] += weight
                        question_counts[dim] += 1
        
        # Normalize scores to 0-100 scale
        normalized_scores = {}
        for dim in self.dimensions.keys():
            if question_counts[dim] > 0:
                raw_score = dimension_totals[dim]
                max_possible = question_counts[dim] * 4
                min_possible = question_counts[dim] * -3
                
                if max_possible != min_possible:
                    normalized = ((raw_score - min_possible) / (max_possible - min_possible)) * 100
                    normalized_scores[dim] = max(0, min(100, normalized))
                else:
                    normalized_scores[dim] = 50
            else:
                normalized_scores[dim] = 0
        
        return normalized_scores

    def get_recommendations(self, scores):
        """Get development recommendations"""
        recommendations = []
        
        if scores.get('LD', 0) < 40:
            recommendations.append({
                "dimension": "LD",
                "title": "Develop Leadership Skills",
                "description": "Focus on decision-making and team guidance.",
                "actions": ["Leadership course", "Find mentor", "Lead small projects"]
            })
        
        if scores.get('CT', 0) < 40:
            recommendations.append({
                "dimension": "CT", 
                "title": "Enhance Critical Thinking",
                "description": "Improve analysis and decision-making skills.",
                "actions": ["Critical thinking books", "Case studies", "Bias training"]
            })
        
        if scores.get('Psy', 0) < 40:
            recommendations.append({
                "dimension": "Psy",
                "title": "Build Resilience", 
                "description": "Enhance stress management and adaptability.",
                "actions": ["Mindfulness practice", "Emotional intelligence", "Stress management"]
            })

        if scores.get('TR', 0) < 40:
            recommendations.append({
                "dimension": "TR",
                "title": "Improve Team Collaboration",
                "description": "Enhance team role effectiveness.",
                "actions": ["Team assessment", "Team-building", "Conflict resolution"]
            })
        
        return recommendations

# Initialize session state
def init_session_state():
    if 'assessment_started' not in st.session_state:
        st.session_state.assessment_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'assessment_completed' not in st.session_state:
        st.session_state.assessment_completed = False
    if 'scores' not in st.session_state:
        st.session_state.scores = {}
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []

def main():
    init_session_state()
    nia = NexusInsightAssessment()
    
    # Sidebar
    with st.sidebar:
        st.title("Nexus Insight")
        st.markdown("---")
        
        if not st.session_state.assessment_started:
            st.info("Start assessment to discover your potential.")
        elif st.session_state.assessment_started and not st.session_state.assessment_completed:
            progress = (st.session_state.current_question / len(nia.questions)) * 100
            st.progress(progress / 100)
            st.write(f"Progress: {st.session_state.current_question}/{len(nia.questions)}")
        else:
            st.success("Assessment Completed!")
            if st.session_state.scores:
                st.write(f"Score: {np.mean(list(st.session_state.scores.values())):.1f}/100")
        
        st.markdown("---")
        page = st.radio("Navigation", ["Home", "Assessment", "Results", "Improvement Plan"])
    
    # Page routing
    if page == "Home":
        show_home_page(nia)
    elif page == "Assessment":
        show_assessment_page(nia)
    elif page == "Results":
        show_results_page(nia)
    elif page == "Improvement Plan":
        show_improvement_page()

def show_home_page(nia):
    """Home page"""
    st.markdown('<h1 class="main-header">🚀 Nexus Insight Assessment</h1>', unsafe_allow_html=True)
    st.markdown("### Innovative Corporate Leadership Assessment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🌟 Discover Your Leadership Potential
        
        **Comprehensive assessment covering:**
        - **Psychological Metrics** - Resilience & adaptability
        - **Critical Thinking** - Analysis & decision-making  
        - **Leadership** - Influence & vision
        - **Cognitive Skills** - Mental agility
        - **Team Roles** - Collaboration
        
        ### 🎯 How It Works
        1. **10 real-world scenarios** (10-15 minutes)
        2. **Instant comprehensive analysis**
        3. **Personalized development plan**
        4. **AI-powered recommendations**
        """)
        
        if st.button("Start Assessment", type="primary", use_container_width=True):
            st.session_state.assessment_started = True
            st.session_state.current_question = 0
            st.session_state.responses = {}
            st.session_state.assessment_completed = False
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 📈 Assessment Features
        
        **Real-world Scenarios:**
        - Startup challenges
        - Ethical dilemmas
        - Crisis management
        - Team leadership
        
        **Advanced Analytics:**
        - Multi-dimensional scoring
        - Personalized insights
        - Development roadmap
        - Progress tracking
        """)

def show_assessment_page(nia):
    """Assessment page"""
    st.markdown('<h1 class="main-header">📝 Leadership Assessment</h1>', unsafe_allow_html=True)
    
    if not st.session_state.assessment_started:
        st.warning("Please start the assessment from the Home page.")
        return
    
    if st.session_state.assessment_completed:
        st.success("Assessment completed! View your results.")
        return
    
    current_q = st.session_state.current_question
    total_questions = len(nia.questions)
    
    if current_q < total_questions:
        question = nia.questions[current_q]
        
        # Progress
        progress = (current_q / total_questions)
        st.progress(progress)
        st.write(f"Question {current_q + 1} of {total_questions}")
        
        # Question
        st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f"**{question['text']}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Options
        options = question['options']
        selected_option = st.radio(
            "Choose your response:",
            options=[opt['text'] for opt in options],
            key=f"q_{question['id']}"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("← Previous", disabled=current_q == 0):
                st.session_state.current_question -= 1
                st.rerun()
        
        with col2:
            if st.button("Next →", type="primary"):
                option_index = [opt['text'] for opt in options].index(selected_option)
                st.session_state.responses[str(question['id'])] = {
                    "selected_option": option_index
                }
                
                if current_q + 1 < total_questions:
                    st.session_state.current_question += 1
                else:
                    st.session_state.assessment_completed = True
                    st.session_state.scores = nia.calculate_scores(st.session_state.responses)
                    st.session_state.recommendations = nia.get_recommendations(st.session_state.scores)
                st.rerun()

def show_results_page(nia):
    """Results page"""
    st.markdown('<h1 class="main-header">📊 Assessment Results</h1>', unsafe_allow_html=True)
    
    if not st.session_state.assessment_completed:
        st.warning("Please complete the assessment first.")
        return
    
    scores = st.session_state.scores
    
    # Overall metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        overall = np.mean(list(scores.values())) if scores else 0
        st.metric("Overall Score", f"{overall:.1f}/100")
    
    with col2:
        high_scores = len([s for s in scores.values() if s > 70])
        st.metric("Strong Areas", high_scores)
    
    with col3:
        low_scores = len([s for s in scores.values() if s < 40])
        st.metric("Development Areas", low_scores)
    
    st.markdown("---")
    
    # Scores
    st.markdown("### 📈 Dimension Scores")
    
    for dim, score in scores.items():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if score < 40:
                color = "red"
                level = "Low"
            elif score < 70:
                color = "orange" 
                level = "Medium"
            else:
                color = "green"
                level = "High"
            
            st.markdown(f"""
            <div style="background-color: {color}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                <strong>{score:.1f}/100</strong><br>{level}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.write(f"**{nia.dimensions[dim]}**")
            progress = score / 100
            st.progress(progress)
    
    # Recommendations
    if st.session_state.recommendations:
        st.markdown("### 🤖 Development Recommendations")
        
        for rec in st.session_state.recommendations:
            with st.expander(f"🎯 {rec['title']}"):
                st.write(rec['description'])
                st.write("**Suggested Actions:**")
                for action in rec['actions']:
                    st.write(f"- {action}")

def show_improvement_page():
    """Improvement plan page"""
    st.markdown('<h1 class="main-header">📝 Personal Improvement Plan</h1>', unsafe_allow_html=True)
    
    if not st.session_state.assessment_completed:
        st.warning("Complete assessment to create your improvement plan.")
        return
    
    st.markdown("""
    ### 🎯 Custom Development Framework
    
    Based on your assessment results, create your personalized development plan.
    Set specific goals and track your progress.
    """)
    
    # Development goals form
    with st.form("improvement_plan"):
        st.markdown("### 📋 Development Goals")
        
        goals = st.text_area(
            "What are your main development goals?",
            placeholder="Example: Improve leadership decision-making, enhance team collaboration skills...",
            height=100
        )
        
        st.markdown("### 🛠️ Action Plan")
        
        actions = st.text_area(
            "What specific actions will you take?",
            placeholder="Example: Attend leadership workshop, practice conflict resolution, read books on critical thinking...",
            height=100
        )
        
        st.markdown("### 📅 Timeline")
        
        timeline = st.select_slider(
            "Implementation timeline",
            options=["1-3 months", "3-6 months", "6-12 months", "12+ months"]
        )
        
        submitted = st.form_submit_button("Save Improvement Plan")
        if submitted:
            st.success("Improvement plan saved! You can update it anytime.")
    
    # Progress tracking
    st.markdown("### 📊 Progress Tracking")
    
    progress_update = st.text_area(
        "Progress notes and updates",
        placeholder="Document your achievements, challenges, and learnings...",
        height=120
    )
    
    if st.button("Save Progress Update"):
        if progress_update.strip():
            st.success("Progress update saved!")
        else:
            st.warning("Please enter some progress notes.")

if __name__ == "__main__":
    main()
