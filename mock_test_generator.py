import streamlit as st

def show_mock_test_generator():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        margin: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    h1, h2, h3 {
        color: white;
    }
    .stButton > button {
        background: linear-gradient(45deg, #6c5ce7, #a29bfe);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: bold;
    }
    .info-container {
        background: rgba(33, 150, 243, 0.2);
        border: 1px solid #2196f3;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main container
    with st.container():
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Header
        st.title("📊 Mock Test Generator Results")
        
        # Info container
        st.markdown('<div class="info-container">', unsafe_allow_html=True)
        st.markdown("### 🎯 Test Generation Complete!")
        st.info("This page shows the generated test results and analytics.")
        st.markdown("**Features coming soon:**")
        st.markdown("- Test performance analytics")
        st.markdown("- Student progress tracking")
        st.markdown("- Detailed score reports")
        st.markdown("- Question-wise analysis")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Back button
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_mock_test_generator()
