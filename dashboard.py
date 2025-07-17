import streamlit as st

def show_dashboard():
    # Custom CSS for the exact design
    st.markdown("""
    <style>
    .main-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 2rem;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .hero-section {
        text-align: center;
        padding: 3rem 0;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
    }
    
    .stats-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stats-text {
        font-size: 1.1rem;
        color: white;
        font-weight: 500;
    }
    
    .review-section {
        text-align: center;
        padding: 2rem 0;
    }
    
    .review-title {
        font-size: 2.5rem;
        color: white;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    
    .review-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
    }
    
    .review-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .review-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .review-card:hover {
        transform: translateY(-5px);
    }
    
    .review-card-title {
        font-size: 1.5rem;
        color: white;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    .review-card-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 1rem;
    }
    
    .stars {
        color: #ffd700;
        font-size: 1.2rem;
        margin: 0.5rem 0;
    }
    
    .review-count {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
    }
    
    .btn-primary {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .btn-secondary {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 0.8rem 2rem;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }
    
    .icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Hide Streamlit elements */
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        margin-top: -80px;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="card">
        <div class="hero-section">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 2rem;">
                <div style="background: #ff6b6b; padding: 1rem; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.5rem;">🎯</span>
                </div>
                <span style="color: white; font-size: 1.2rem; font-weight: 500;">II Tuitions Mock Test Generator</span>
            </div>
            <h1 class="hero-title">Mock Tests/Quiz/Puzzles Generator</h1>
            <p class="hero-subtitle">Generate practice tests, quizzes, and puzzles for comprehensive learning</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create Test Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Create Test", key="create_test_btn", help="Create a new mock test", type="primary"):
            st.session_state.current_page = 'create_test'
            st.rerun()
    
    # Stats Section
    st.markdown("""
    <div class="card">
        <div class="stats-container">
            <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">📊</span>
                <span class="stats-text">3,675 tests generated</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Review Section
    st.markdown("""
    <div class="card">
        <div class="review-section">
            <h2 class="review-title">
                <span>⭐</span>
                <span>Review</span>
            </h2>
            <p class="review-subtitle">Review your progress, results, and get feedback from teachers and parents</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # View Reviews Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("View Reviews", key="view_reviews_btn", help="View all reviews and feedback"):
            st.info("Reviews section coming soon!")
    
    # Review Cards
    st.markdown("""
    <div class="review-cards">
        <div class="review-card">
            <div class="icon">👨‍🏫</div>
            <h3 class="review-card-title">Teacher Review</h3>
            <p class="review-card-subtitle">Get feedback from educators</p>
            <div class="stars">⭐⭐⭐⭐⭐</div>
            <p class="review-count">124 reviews</p>
        </div>
        
        <div class="review-card">
            <div class="icon">👨‍👩‍👧‍👦</div>
            <h3 class="review-card-title">Parent Review</h3>
            <p class="review-card-subtitle">Parental feedback & support</p>
            <div class="stars">⭐⭐⭐⭐⭐</div>
            <p class="review-count">89 reviews</p>
        </div>
        
        <div class="review-card">
            <div class="icon">👨‍🏫</div>
            <h3 class="review-card-title">Teacher Review</h3>
            <p class="review-card-subtitle">Academic performance insights</p>
            <div class="stars">⭐⭐⭐⭐⭐</div>
            <p class="review-count">156 reviews</p>
        </div>
        
        <div class="review-card">
            <div class="icon">👨‍👩‍👧‍👦</div>
            <h3 class="review-card-title">Parent Review</h3>
            <p class="review-card-subtitle">Progress tracking & guidance</p>
            <div class="stars">⭐⭐⭐⭐⭐</div>
            <p class="review-count">201 reviews</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
