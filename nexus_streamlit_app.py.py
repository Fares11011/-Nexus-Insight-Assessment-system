# nexus_streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import json
import random
from typing import Dict, List, Any
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

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
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 2rem;
        color: #2e86ab;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .question-card {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .result-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .recommendation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .dimension-score {
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class NexusInsightAssessment:
    def __init__(self):
        self.dimensions = {
            'Psy': 'Psychological Metrics',
            'CT': 'Critical Thinking', 
            'LT': 'Logical Thinking',
            'LD': 'Leadership',
            'Cog': 'Cognitive Skills',
            'TR': 'Team Roles'
        }
        
        self.thresholds = {
            'Low': (0, 40),
            'Medium': (40, 70), 
            'High': (70, 100)
        }
        
        self.questions = self._create_innovative_questions()
        
    def _create_innovative_questions(self) -> List[Dict]:
        """Create innovative assessment questions with real-world scenarios"""
        questions = [
            {
                "id": 1,
                "text": "You're the young founder of an AI startup. After 6 months of launch, a major competitor copies your product and offers it at 50% lower price. Your team is demotivated. What do you do?",
                "type": "situational_judgment",
                "scenario_type": "startup_crisis",
                "options": [
                    {"text": "Rush to develop unique features and lower prices to compete", "weights": {"Psy": -3, "LD": 2, "CT": 1}},
                    {"text": "Host brainstorming session with team for creative solutions", "weights": {"LD": 4, "TR": 3, "Cog": 2}},
                    {"text": "Focus on different customer segment not served by competitor", "weights": {"CT": 4, "LD": 3, "Psy": 2}},
                    {"text": "Seek strategic partnership with larger company", "weights": {"TR": 4, "LD": 3, "CT": 2}}
                ],
                "creative_elements": ["Startup environment", "Fierce competition", "Creative problem-solving"],
                "dimensions": ["Psy", "LD", "CT", "TR"]
            },
            {
                "id": 2,
                "text": "An investor asks you to completely change your business model for funding. This conflicts with your core vision. How do you handle this dilemma?",
                "type": "ethical_dilemma", 
                "scenario_type": "investor_pressure",
                "options": [
                    {"text": "Reject the offer and maintain your vision", "weights": {"Psy": 4, "LD": 3, "CT": -2}},
                    {"text": "Accept with reservations and minor adjustments", "weights": {"TR": 3, "LD": 2, "Psy": 1}},
                    {"text": "Negotiate to find middle ground satisfying both parties", "weights": {"LD": 4, "CT": 3, "TR": 3}},
                    {"text": "Request time to think and consult mentors", "weights": {"CT": 4, "Psy": 3, "Cog": 2}}
                ],
                "creative_elements": ["Ethical dilemma", "Investor pressure", "Vision preservation"],
                "dimensions": ["Psy", "LD", "CT", "TR"]
            },
            {
                "id": 3,
                "text": "Your top performer is highly productive but creates team conflicts. Do you prioritize results or team harmony?",
                "type": "leadership_dilemma",
                "scenario_type": "team_management",
                "options": [
                    {"text": "Focus on results and manage conflicts separately", "weights": {"LD": 3, "Psy": -2, "TR": -3}},
                    {"text": "Coach the employee on teamwork while acknowledging contributions", "weights": {"LD": 4, "Psy": 3, "TR": 4}},
                    {"text": "Reassign to individual contributor role", "weights": {"TR": 3, "LD": 2, "CT": 2}},
                    {"text": "Implement team-building activities addressing the issue", "weights": {"TR": 4, "LD": 3, "Psy": 3}}
                ],
                "creative_elements": ["Performance vs harmony", "Leadership challenge", "Conflict resolution"],
                "dimensions": ["LD", "TR", "Psy", "CT"]
            },
            {
                "id": 4,
                "text": "As a manager in traditional manufacturing company, you need to lead digital transformation. 60% of employees resist change. What's your strategy?",
                "type": "change_management",
                "scenario_type": "digital_resistance", 
                "options": [
                    {"text": "Enforce change gradually with intensive training", "weights": {"LD": 3, "Psy": -2, "TR": 1}},
                    {"text": "Identify 'change champions' and make them transformation ambassadors", "weights": {"TR": 4, "LD": 4, "Psy": 3}},
                    {"text": "Start with small pilot project to demonstrate success", "weights": {"CT": 4, "LD": 3, "Cog": 2}},
                    {"text": "Redesign incentives to encourage voluntary adoption", "weights": {"LD": 4, "Psy": 3, "CT": 3}}
                ],
                "creative_elements": ["Digital transformation", "Change resistance", "Adoption strategy"],
                "dimensions": ["LD", "TR", "Psy", "CT"]
            },
            {
                "id": 5,
                "text": "AI implementation will replace 30% of manual jobs in your department. How do you lead this transition ethically?",
                "type": "ethical_leadership",
                "scenario_type": "ai_implementation",
                "options": [
                    {"text": "Implement quickly and offer severance packages", "weights": {"LD": 2, "Psy": -4, "CT": 1}},
                    {"text": "Create upskilling programs and gradual transition plan", "weights": {"LD": 5, "TR": 4, "Psy": 4}},
                    {"text": "Slow implementation and seek alternative roles", "weights": {"CT": 3, "LD": 3, "TR": 3}},
                    {"text": "Form employee committee to co-design transition", "weights": {"TR": 5, "LD": 4, "CT": 4}}
                ],
                "creative_elements": ["AI ethics", "Workforce transition", "Inclusive decision-making"],
                "dimensions": ["LD", "CT", "TR", "Psy"]
            },
            {
                "id": 6,
                "text": "Market research shows your product is becoming obsolete. Do you invest in incremental improvements or radical innovation?",
                "type": "strategic_decision",
                "scenario_type": "innovation_crossroads",
                "options": [
                    {"text": "Focus on improving existing product features", "weights": {"CT": 3, "LD": 2, "Psy": -2}},
                    {"text": "Allocate resources for breakthrough innovation", "weights": {"LD": 4, "CT": 4, "Cog": 3}},
                    {"text": "Pursue both paths with separate teams", "weights": {"TR": 4, "LD": 3, "CT": 3}},
                    {"text": "Acquire innovative startup instead of internal development", "weights": {"CT": 4, "LD": 3, "TR": 2}}
                ],
                "creative_elements": ["Innovation strategy", "Risk assessment", "Strategic thinking"],
                "dimensions": ["LD", "CT", "TR", "Cog"]
            },
            {
                "id": 7,
                "text": "Major data breach exposes customer information. Media is calling, stock price is dropping. What's your first response?",
                "type": "crisis_management",
                "scenario_type": "data_breach",
                "options": [
                    {"text": "Issue immediate public apology and transparency", "weights": {"LD": 4, "CT": 3, "Psy": 3}},
                    {"text": "First contain breach internally, then communicate", "weights": {"CT": 4, "LD": 3, "Cog": 3}},
                    {"text": "Blame technical issues and minimize responsibility", "weights": {"LD": -4, "Psy": -3, "CT": -2}},
                    {"text": "Activate crisis team and follow pre-established protocol", "weights": {"LD": 5, "CT": 4, "TR": 4}}
                ],
                "creative_elements": ["Crisis leadership", "Stakeholder management", "Quick decision-making"],
                "dimensions": ["LD", "CT", "Psy", "TR"]
            },
            {
                "id": 8,
                "text": "Expanding to new international market, you discover cultural practices conflicting with company values. How do you proceed?",
                "type": "cross_cultural",
                "scenario_type": "global_expansion",
                "options": [
                    {"text": "Adapt company practices to local culture", "weights": {"TR": 3, "LD": 2, "Psy": 2}},
                    {"text": "Maintain company values and educate local partners", "weights": {"LD": 4, "CT": 3, "Psy": 3}},
                    {"text": "Find compromise respecting both perspectives", "weights": {"CT": 4, "LD": 4, "TR": 3}},
                    {"text": "Reconsider market entry if values conflict irreconcilably", "weights": {"CT": 5, "LD": 3, "Psy": 4}}
                ],
                "creative_elements": ["Cultural intelligence", "Values-based leadership", "Global mindset"],
                "dimensions": ["LD", "CT", "Psy", "TR"]
            },
            {
                "id": 9,
                "text": "Metaverse technology could transform your industry in 5 years. Do you invest heavily now or wait for market maturity?",
                "type": "future_strategy",
                "scenario_type": "emerging_technology",
                "options": [
                    {"text": "Heavy investment to become early leader", "weights": {"LD": 4, "CT": 3, "Psy": 2}},
                    {"text": "Wait for clear ROI and proven use cases", "weights": {"CT": 4, "LD": 2, "Psy": 3}},
                    {"text": "Form strategic partnerships to share risk", "weights": {"TR": 4, "LD": 3, "CT": 3}},
                    {"text": "Create innovation lab for experimentation", "weights": {"Cog": 4, "LD": 3, "CT": 4}}
                ],
                "creative_elements": ["Future thinking", "Technology adoption", "Strategic foresight"],
                "dimensions": ["LD", "CT", "TR", "Cog"]
            },
            {
                "id": 10,
                "text": "Your company is accused of greenwashing. Environmental groups are protesting. How do you restore trust?",
                "type": "reputation_management",
                "scenario_type": "crisis_communication",
                "options": [
                    {"text": "Issue strong denial and defend current practices", "weights": {"LD": -3, "CT": -2, "Psy": -4}},
                    {"text": "Admit shortcomings and present concrete improvement plan", "weights": {"LD": 5, "CT": 4, "Psy": 4}},
                    {"text": "Hire PR firm to manage the narrative", "weights": {"CT": 2, "LD": 2, "TR": 1}},
                    {"text": "Engage with protesters and co-create sustainability goals", "weights": {"TR": 5, "LD": 4, "CT": 4}}
                ],
                "creative_elements": ["Reputation crisis", "Stakeholder engagement", "Authentic leadership"],
                "dimensions": ["LD", "CT", "TR", "Psy"]
            }
        ]
        return questions

    def calculate_dimension_scores(self, responses: Dict) -> Dict[str, float]:
        """Calculate scores using advanced algorithm"""
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
                max_possible = question_counts[dim] * 5
                min_possible = question_counts[dim] * -4
                
                if max_possible != min_possible:
                    normalized = ((raw_score - min_possible) / (max_possible - min_possible)) * 100
                    normalized_scores[dim] = max(0, min(100, normalized))
                else:
                    normalized_scores[dim] = 50
            else:
                normalized_scores[dim] = 0
        
        # Apply cross-dimension correlations
        normalized_scores = self._apply_cross_dimension_correlations(normalized_scores)
        
        return normalized_scores

    def _apply_cross_dimension_correlations(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Apply advanced correlations between dimensions"""
        adjusted_scores = scores.copy()
        
        if adjusted_scores['LD'] > 70:
            adjusted_scores['TR'] = min(100, adjusted_scores['TR'] * 1.1)
        
        if adjusted_scores['CT'] > 70:
            adjusted_scores['LD'] = min(100, adjusted_scores['LD'] * 1.08)
        
        if adjusted_scores['Psy'] > 70:
            adjusted_scores['Cog'] = min(100, adjusted_scores['Cog'] * 1.05)
        
        if adjusted_scores['LT'] > 70:
            adjusted_scores['CT'] = min(100, adjusted_scores['CT'] * 1.06)
        
        return adjusted_scores

    def generate_ai_coach_recommendations(self, scores: Dict[str, float]) -> List[Dict]:
        """Generate personalized AI Coach recommendations"""
        recommendations = []
        
        if scores['LD'] < 40:
            recommendations.append({
                "dimension": "LD",
                "priority": "high",
                "title": "Develop Leadership Skills",
                "description": "Leadership score indicates need for development in decision-making and team guidance.",
                "actions": [
                    "Enroll in strategic leadership course",
                    "Find leadership mentor",
                    "Practice leading small project teams"
                ]
            })
        
        if scores['CT'] < 40:
            recommendations.append({
                "dimension": "CT", 
                "priority": "high",
                "title": "Enhance Critical Thinking",
                "description": "Critical thinking skills need development for better analysis and decision-making.",
                "actions": [
                    "Read books on critical thinking",
                    "Practice analyzing complex case studies",
                    "Train on detecting cognitive biases"
                ]
            })
        
        if scores['Psy'] < 40:
            recommendations.append({
                "dimension": "Psy",
                "priority": "medium", 
                "title": "Build Psychological Resilience",
                "description": "Psychological resilience can be enhanced for better stress management.",
                "actions": [
                    "Practice mindfulness and meditation",
                    "Develop emotional intelligence skills",
                    "Learn stress management techniques"
                ]
            })

        if scores['TR'] < 40:
            recommendations.append({
                "dimension": "TR",
                "priority": "medium",
                "title": "Improve Team Collaboration",
                "description": "Team role effectiveness needs enhancement for better collaboration.",
                "actions": [
                    "Take team role assessment",
                    "Participate in team-building activities",
                    "Learn conflict resolution techniques"
                ]
            })
        
        return recommendations

    def create_executive_dashboard(self, scores: Dict[str, float], user_id: str) -> Dict:
        """Create comprehensive executive dashboard"""
        score_analysis = {}
        for dim, score in scores.items():
            if score < 40:
                level = "Low"
                color = "🔴"
            elif score < 70:
                level = "Medium" 
                color = "🟡"
            else:
                level = "High"
                color = "🟢"
            
            score_analysis[dim] = {
                "score": score,
                "level": level,
                "color": color,
                "description": f"{self.dimensions[dim]}: {level} ({score:.1f}/100)"
            }
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_3 = sorted_scores[:3]
        bottom_3 = sorted_scores[-3:]
        
        dashboard = {
            "user_id": user_id,
            "report_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "overall_score": np.mean(list(scores.values())),
            "dimension_scores": score_analysis,
            "top_strengths": [
                {
                    "dimension": dim,
                    "name": self.dimensions[dim],
                    "score": score,
                    "interpretation": self._get_interpretation(dim, score)
                } for dim, score in top_3
            ],
            "development_areas": [
                {
                    "dimension": dim, 
                    "name": self.dimensions[dim],
                    "score": score,
                    "recommendations": self._get_development_recommendations(dim, score)
                } for dim, score in bottom_3
            ],
            "leadership_style": self._analyze_leadership_style(scores),
            "innovation_potential": self._calculate_innovation_potential(scores)
        }
        
        return dashboard

    def _get_interpretation(self, dimension: str, score: float) -> str:
        interpretations = {
            'LD': {
                'low': 'Cautious leadership style, needs to develop confidence in decision-making',
                'medium': 'Balanced leader, can improve influence and guidance skills',
                'high': 'Inspiring leader with clear vision and ability to motivate teams'
            },
            'CT': {
                'low': 'Tends toward superficial acceptance, needs to develop critical analysis',
                'medium': 'Capable of analysis in familiar contexts, needs to broaden thinking scope',
                'high': 'Excellent analyst, detects biases and offers innovative problem solutions'
            },
            'Psy': {
                'low': 'Needs to enhance psychological resilience and stress management',
                'medium': 'Psychologically balanced, can improve handling change',
                'high': 'Psychologically resilient, quickly adapts to challenges and difficult conditions'
            }
        }
        
        level = 'low' if score < 40 else 'medium' if score < 70 else 'high'
        return interpretations.get(dimension, {}).get(level, 'Strong capabilities in this area')

    def _get_development_recommendations(self, dimension: str, score: float) -> List[str]:
        recommendations = {
            'LD': [
                'Situational Leadership workshops',
                'Decision-making training',
                'Influence and persuasion exercises'
            ],
            'CT': [
                'Critical thinking courses',
                'Case study analysis exercises',
                'Bias detection training'
            ],
            'Psy': [
                'Resilience enhancement programs',
                'Stress management training',
                'Emotional intelligence exercises'
            ]
        }
        return recommendations.get(dimension, ['Professional development programs'])

    def _analyze_leadership_style(self, scores: Dict[str, float]) -> str:
        if scores['LD'] > 70 and scores['CT'] > 60:
            return "Strategic Leader: Combines vision with precise analysis"
        elif scores['LD'] > 70 and scores['Psy'] > 70:
            return "Inspirational Leader: Focuses on motivating teams and building relationships"
        elif scores['CT'] > 70 and scores['LT'] > 70:
            return "Analytical Leader: Relies on data and logic in leadership"
        else:
            return "Balanced Leader: Combines multiple leadership approaches"

    def _calculate_innovation_potential(self, scores: Dict[str, float]) -> float:
        innovation_score = (
            scores['CT'] * 0.3 +
            scores['Psy'] * 0.3 + 
            scores['LD'] * 0.2 +
            scores['Cog'] * 0.2
        )
        return innovation_score

# Initialize the assessment system
@st.cache_resource
def get_assessment_system():
    return NexusInsightAssessment()

# Initialize session state
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
if 'dashboard' not in st.session_state:
    st.session_state.dashboard = {}
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

# Main app
def main():
    nia = get_assessment_system()
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150/1f77b4/ffffff?text=NIA", width=150)
        st.title("Nexus Insight Assessment")
        st.markdown("---")
        
        if not st.session_state.assessment_started:
            st.info("Start your assessment to discover your leadership potential and development areas.")
        elif st.session_state.assessment_started and not st.session_state.assessment_completed:
            progress = (st.session_state.current_question / len(nia.questions)) * 100
            st.progress(progress)
            st.write(f"Progress: {st.session_state.current_question}/{len(nia.questions)} questions")
        else:
            st.success("Assessment Completed!")
            st.write(f"Overall Score: {st.session_state.dashboard.get('overall_score', 0):.1f}/100")
        
        st.markdown("---")
        st.markdown("### Navigation")
        page = st.radio("Go to:", ["Home", "Assessment", "Results", "Improvement Plan"])
    
    # Page routing
    if page == "Home":
        show_home_page(nia)
    elif page == "Assessment":
        show_assessment_page(nia)
    elif page == "Results":
        show_results_page(nia)
    elif page == "Improvement Plan":
        show_improvement_page(nia)

def show_home_page(nia):
    """Display the home page with introduction"""
    st.markdown('<h1 class="main-header">🚀 Nexus Insight Assessment</h1>', unsafe_allow_html=True)
    st.markdown("### First-of-its-kind innovative corporate leadership assessment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🌟 Welcome to the Future of Leadership Assessment
        
        **Nexus Insight Assessment** is the first comprehensive system that combines:
        - **Real-world corporate scenarios**
        - **Advanced psychological metrics**
        - **AI-powered coaching recommendations**
        - **Executive-level insights**
        
        ### 📊 What You'll Discover
        
        **6 Core Dimensions of Leadership Excellence:**
        1. **Psychological Metrics** - Resilience, adaptability, emotional intelligence
        2. **Critical Thinking** - Analysis, bias detection, ethical reasoning
        3. **Logical Thinking** - Problem-solving, pattern recognition
        4. **Leadership** - Decision-making, influence, vision
        5. **Cognitive Skills** - Memory, attention, flexibility
        6. **Team Roles** - Collaboration, role understanding
        
        ### 🎯 How It Works
        
        1. **Complete 10 innovative scenarios** (15-20 minutes)
        2. **Receive instant comprehensive analysis**
        3. **Get personalized development plan**
        4. **Access AI coach recommendations**
        
        ### 🚀 Ready to Begin?
        """)
        
        if st.button("Start Your Assessment Journey", type="primary", use_container_width=True):
            st.session_state.assessment_started = True
            st.session_state.current_question = 0
            st.session_state.responses = {}
            st.session_state.assessment_completed = False
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 📈 Sample Insights
        
        **Leadership Styles:**
        - Strategic Leader
        - Inspirational Leader  
        - Analytical Leader
        - Balanced Leader
        
        **Innovation Potential:**
        - High creativity index
        - Problem-solving ability
        - Future thinking capacity
        
        **Growth Trajectory:**
        - Executive readiness
        - Development priorities
        - Career path insights
        """)

def show_assessment_page(nia):
    """Display the assessment questions"""
    st.markdown('<h1 class="main-header">📝 Leadership Assessment</h1>', unsafe_allow_html=True)
    
    if not st.session_state.assessment_started:
        st.warning("Please start the assessment from the Home page.")
        return
    
    if st.session_state.assessment_completed:
        st.success("Assessment completed! View your results in the Results section.")
        return
    
    # Get current question
    current_q = st.session_state.current_question
    total_questions = len(nia.questions)
    
    if current_q < total_questions:
        question = nia.questions[current_q]
        
        # Progress bar
        progress = (current_q / total_questions)
        st.progress(progress)
        st.write(f"Question {current_q + 1} of {total_questions}")
        
        # Display question
        st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f"### {question['text']}")
        st.markdown(f"*Scenario type: {question['scenario_type'].replace('_', ' ').title()}*")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display options
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
                # Save response
                option_index = [opt['text'] for opt in options].index(selected_option)
                st.session_state.responses[str(question['id'])] = {
                    "selected_option": option_index,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Move to next question or complete assessment
                if current_q + 1 < total_questions:
                    st.session_state.current_question += 1
                else:
                    st.session_state.assessment_completed = True
                    # Calculate scores
                    st.session_state.scores = nia.calculate_dimension_scores(st.session_state.responses)
                    st.session_state.recommendations = nia.generate_ai_coach_recommendations(st.session_state.scores)
                    st.session_state.dashboard = nia.create_executive_dashboard(
                        st.session_state.scores, 
                        "streamlit_user"
                    )
                st.rerun()
    
    else:
        st.session_state.assessment_completed = True
        st.rerun()

def show_results_page(nia):
    """Display assessment results and visualizations"""
    st.markdown('<h1 class="main-header">📊 Assessment Results</h1>', unsafe_allow_html=True)
    
    if not st.session_state.assessment_completed:
        st.warning("Please complete the assessment first to view results.")
        return
    
    scores = st.session_state.scores
    dashboard = st.session_state.dashboard
    
    # Overall score and key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Score", f"{dashboard['overall_score']:.1f}/100")
    
    with col2:
        st.metric("Leadership Style", dashboard['leadership_style'].split(":")[0])
    
    with col3:
        st.metric("Innovation Potential", f"{dashboard['innovation_potential']:.1f}/100")
    
    with col4:
        level = "High" if dashboard['overall_score'] > 70 else "Medium" if dashboard['overall_score'] > 40 else "Low"
        st.metric("Performance Level", level)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar chart
        dimensions = list(scores.keys())
        values = list(scores.values())
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=[nia.dimensions[d] for d in dimensions] + [nia.dimensions[dimensions[0]]],
            fill='toself',
            name='Competency Profile',
            line=dict(color='blue', width=2),
            fillcolor='rgba(30, 144, 255, 0.3)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=False,
            title="Competency Radar Profile",
            height=400
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        # Bar chart
        fig_bar = go.Figure()
        colors = ['red' if x < 40 else 'orange' if x < 70 else 'green' for x in values]
        
        fig_bar.add_trace(go.Bar(
            x=[nia.dimensions[d] for d in dimensions],
            y=values,
            marker_color=colors,
            text=[f"{v:.1f}" for v in values],
            textposition='auto',
        ))
        
        fig_bar.update_layout(
            title="Dimension Scores",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detailed results
    st.markdown("### 📈 Detailed Dimension Analysis")
    
    for dim, score_data in dashboard['dimension_scores'].items():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            score = score_data['score']
            if score < 40:
                color = "red"
            elif score < 70:
                color = "orange"
            else:
                color = "green"
            
            st.markdown(f"""
            <div class="dimension-score" style="background-color: {color}; color: white;">
                {score:.1f}/100
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.write(f"**{nia.dimensions[dim]}** - {score_data['level']}")
            st.write(nia._get_interpretation(dim, score))
        
        with col3:
            st.write(score_data['color'])
    
    # AI Coach Recommendations
    st.markdown("### 🤖 AI Coach Recommendations")
    
    for rec in st.session_state.recommendations:
        with st.expander(f"{rec['title']} - {rec['priority'].upper()} PRIORITY"):
            st.write(rec['description'])
            st.write("**Recommended Actions:**")
            for action in rec['actions']:
                st.write(f"- {action}")

def show_improvement_page(nia):
    """Display improvement plan and development suggestions"""
    st.markdown('<h1 class="main-header">📝 Personal Improvement Plan</h1>', unsafe_allow_html=True)
    
    if not st.session_state.assessment_completed:
        st.warning("Please complete the assessment first to view your improvement plan.")
        return
    
    st.markdown("""
    ### 🎯 Customized Development Framework
    
    Based on your assessment results, this section is designed for you to create 
    and track your personal development plan. Use the insights from your assessment 
    to set specific goals and action items.
    """)
    
    # Empty improvement plan template
    st.markdown("### 📋 Development Goals Template")
    
    with st.form("improvement_plan"):
        st.write("**Set your development goals for each dimension:**")
        
        for dim in nia.dimensions.keys():
            st.markdown(f"#### {nia.dimensions[dim]}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                goal = st.text_area(
                    f"Development goal for {nia.dimensions[dim]}",
                    placeholder=f"Example: Improve {nia.dimensions[dim].lower()} through specific actions...",
                    key=f"goal_{dim}"
                )
            
            with col2:
                actions = st.text_area(
                    f"Action items for {nia.dimensions[dim]}",
                    placeholder="List specific actions, timelines, and resources needed...",
                    key=f"actions_{dim}"
                )
        
        st.markdown("### 📅 Implementation Timeline")
        
        timeline_col1, timeline_col2, timeline_col3 = st.columns(3)
        
        with timeline_col1:
            st.write("**Short-term (1-3 months)**")
            short_term = st.text_area("Immediate actions", placeholder="Quick wins and initial steps...")
        
        with timeline_col2:
            st.write("**Medium-term (3-6 months)**")
            medium_term = st.text_area("Development projects", placeholder="Larger initiatives and skill building...")
        
        with timeline_col3:
            st.write("**Long-term (6-12 months)**")
            long_term = st.text_area("Career development", placeholder="Advanced skills and leadership growth...")
        
        submitted = st.form_submit_button("Save Improvement Plan")
        if submitted:
            st.success("Improvement plan saved! You can revisit this page to update your progress.")
    
    # Progress tracking
    st.markdown("### 📊 Progress Tracking")
    st.info("""
    **Track your development progress here:**
    - Update your goals regularly
    - Note achievements and challenges
    - Adjust your plan as needed
    - Seek feedback from mentors and peers
    """)
    
    progress_update = st.text_area(
        "Progress Notes and Updates",
        placeholder="Document your development journey, milestones achieved, and lessons learned...",
        height=150
    )
    
    if st.button("Save Progress Update"):
        if progress_update:
            st.success("Progress update saved!")
        else:
            st.warning("Please enter some progress notes before saving.")

if __name__ == "__main__":
    main()