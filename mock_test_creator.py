import streamlit as st
import json
import requests
import re
from datetime import datetime
import os

# Configure page
st.set_page_config(
    page_title="II Tuitions Mock Test Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    .stats-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
    .review-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-top: 2rem;
    }
    .review-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    .form-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
    }
    .test-paper {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
    .question-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .error-message {
        color: #dc3545;
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-message {
        color: #155724;
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
CLAUDE_API_KEY = ""
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

# Add these imports for PDF generation
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Enhanced Subject mapping with curriculum standards
def get_subjects_by_board():
    return {
        "CBSE": {
            1: ["Mathematics", "English", "Hindi", "EVS"],
            2: ["Mathematics", "English", "Hindi", "EVS"],
            3: ["Mathematics", "English", "Hindi", "EVS", "Computer Science"],
            4: ["Mathematics", "English", "Hindi", "EVS", "Computer Science"],
            5: ["Mathematics", "English", "Hindi", "EVS", "Computer Science"],
            6: ["Mathematics", "English", "Hindi", "Science", "Social Science", "Sanskrit"],
            7: ["Mathematics", "English", "Hindi", "Science", "Social Science", "Sanskrit"],
            8: ["Mathematics", "English", "Hindi", "Science", "Social Science", "Sanskrit"],
            9: ["Mathematics", "English", "Hindi", "Science", "Social Science", "Sanskrit", "Computer Science"],
            10: ["Mathematics", "English", "Hindi", "Science", "Social Science", "Sanskrit", "Computer Science"],
            11: ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Computer Science", "Economics", "Business Studies"],
            12: ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Computer Science", "Economics", "Business Studies"]
        },
        "ICSE": {
            1: ["Mathematics", "English", "Hindi", "EVS"],
            2: ["Mathematics", "English", "Hindi", "EVS"],
            3: ["Mathematics", "English", "Hindi", "EVS", "Computer Applications"],
            4: ["Mathematics", "English", "Hindi", "EVS", "Computer Applications"],
            5: ["Mathematics", "English", "Hindi", "EVS", "Computer Applications"],
            6: ["Mathematics", "English", "Hindi", "Physics", "Chemistry", "Biology", "History", "Geography"],
            7: ["Mathematics", "English", "Hindi", "Physics", "Chemistry", "Biology", "History", "Geography"],
            8: ["Mathematics", "English", "Hindi", "Physics", "Chemistry", "Biology", "History", "Geography"],
            9: ["Mathematics", "English", "Hindi", "Physics", "Chemistry", "Biology", "History", "Geography", "Computer Applications"],
            10: ["Mathematics", "English", "Hindi", "Physics", "Chemistry", "Biology", "History", "Geography", "Computer Applications"],
            11: ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Computer Science", "Economics", "Commerce"],
            12: ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Computer Science", "Economics", "Commerce"]
        },
        "IB": {
            1: ["Mathematics", "English", "Science", "Social Studies"],
            2: ["Mathematics", "English", "Science", "Social Studies"],
            3: ["Mathematics", "English", "Science", "Social Studies"],
            4: ["Mathematics", "English", "Science", "Social Studies"],
            5: ["Mathematics", "English", "Science", "Social Studies"],
            6: ["Mathematics", "English", "Science", "Social Studies", "Arts"],
            7: ["Mathematics", "English", "Science", "Social Studies", "Arts"],
            8: ["Mathematics", "English", "Science", "Social Studies", "Arts"],
            9: ["Mathematics", "English", "Science", "Social Studies", "Arts", "Computer Science"],
            10: ["Mathematics", "English", "Science", "Social Studies", "Arts", "Computer Science"],
            11: ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Economics", "Business Management"],
            12: ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Economics", "Business Management"]
        },
        "Cambridge IGCSE": {
            1: ["Mathematics", "English", "Science", "Social Studies"],
            2: ["Mathematics", "English", "Science", "Social Studies"],
            3: ["Mathematics", "English", "Science", "Social Studies"],
            4: ["Mathematics", "English", "Science", "Social Studies"],
            5: ["Mathematics", "English", "Science", "Social Studies"],
            6: ["Mathematics", "English", "Science", "Social Studies", "ICT"],
            7: ["Mathematics", "English", "Science", "Social Studies", "ICT"],
            8: ["Mathematics", "English", "Science", "Social Studies", "ICT"],
            9: ["Mathematics", "English", "Physics", "Chemistry", "Biology", "Computer Science", "Economics"],
            10: ["Mathematics", "English", "Physics", "Chemistry", "Biology", "Computer Science", "Economics"],
            11: ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Computer Science", "Economics"],
            12: ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Computer Science", "Economics"]
        },
        "State Board": {
            1: ["Mathematics", "English", "Mother Tongue", "EVS"],
            2: ["Mathematics", "English", "Mother Tongue", "EVS"],
            3: ["Mathematics", "English", "Mother Tongue", "EVS", "Computer Science"],
            4: ["Mathematics", "English", "Mother Tongue", "EVS", "Computer Science"],
            5: ["Mathematics", "English", "Mother Tongue", "EVS", "Computer Science"],
            6: ["Mathematics", "English", "Mother Tongue", "Science", "Social Science"],
            7: ["Mathematics", "English", "Mother Tongue", "Science", "Social Science"],
            8: ["Mathematics", "English", "Mother Tongue", "Science", "Social Science"],
            9: ["Mathematics", "English", "Mother Tongue", "Science", "Social Science", "Computer Science"],
            10: ["Mathematics", "English", "Mother Tongue", "Science", "Social Science", "Computer Science"],
            11: ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Computer Science", "Economics"],
            12: ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Computer Science", "Economics"]
        }
    }

def get_curriculum_specific_content(board, grade, subject):
    """Get curriculum-specific content mapping for realistic question generation"""
    curriculum_map = {
        "CBSE": {
            "Mathematics": {
                1: ["Numbers 1-100", "Addition", "Subtraction", "Shapes", "Patterns"],
                2: ["Numbers 1-1000", "Place Value", "Addition & Subtraction", "Multiplication tables", "Time"],
                3: ["Numbers up to 10000", "Multiplication", "Division", "Fractions", "Measurement"],
                4: ["Large Numbers", "Operations", "Factors & Multiples", "Fractions", "Decimals", "Geometry"],
                5: ["Number System", "Operations", "LCM & HCF", "Fractions & Decimals", "Percentage", "Area & Perimeter"],
                6: ["Integers", "Fractions & Decimals", "Basic Algebra", "Ratio & Proportion", "Geometry", "Mensuration"],
                7: ["Integers", "Fractions & Decimals", "Simple Equations", "Lines & Angles", "Triangles", "Percentage"],
                8: ["Rational Numbers", "Linear Equations", "Quadrilaterals", "Mensuration", "Exponents", "Comparing Quantities"],
                9: ["Number Systems", "Polynomials", "Coordinate Geometry", "Linear Equations", "Triangles", "Statistics"],
                10: ["Real Numbers", "Polynomials", "Linear Equations", "Quadratic Equations", "Arithmetic Progressions", "Coordinate Geometry", "Triangles", "Circles", "Statistics", "Probability"],
                11: ["Sets", "Relations & Functions", "Trigonometry", "Complex Numbers", "Linear Inequalities", "Permutations & Combinations", "Binomial Theorem", "Sequences & Series", "Coordinate Geometry", "Limits & Derivatives", "Statistics", "Probability"],
                12: ["Relations & Functions", "Inverse Trigonometry", "Matrices", "Determinants", "Continuity & Differentiability", "Applications of Derivatives", "Integrals", "Applications of Integrals", "Differential Equations", "Vector Algebra", "3D Geometry", "Linear Programming", "Probability"]
            },
            "Science": {
                6: ["Food", "Components of Food", "Fiber to Fabric", "Sorting Materials", "Separation of Substances", "Changes Around Us", "Living Organisms", "Body Movements", "Living & Non-living", "Motion & Distance", "Light", "Electricity"],
                7: ["Nutrition in Plants", "Nutrition in Animals", "Fiber to Fabric", "Heat", "Acids & Bases", "Physical & Chemical Changes", "Weather & Climate", "Winds & Storms", "Soil", "Respiration", "Transportation", "Reproduction", "Motion & Time", "Electric Current", "Light", "Water"],
                8: ["Crop Production", "Microorganisms", "Synthetic Fibers", "Materials", "Coal & Petroleum", "Combustion & Flame", "Conservation of Plants & Animals", "Cell Structure", "Reproduction", "Reaching Adolescence", "Force & Pressure", "Friction", "Sound", "Chemical Effects of Electric Current", "Natural Phenomena", "Light", "Stars & Solar System", "Pollution of Air & Water"],
                9: ["Matter", "Is Matter Pure", "Atoms & Molecules", "Atomic Structure", "Fundamental Unit of Life", "Tissues", "Diversity in Living Organisms", "Motion", "Force & Laws of Motion", "Gravitation", "Work & Energy", "Sound", "Natural Resources"],
                10: ["Chemical Reactions", "Acids & Bases", "Metals & Non-metals", "Carbon & Compounds", "Periodic Classification", "Life Processes", "Control & Coordination", "Reproduction", "Heredity & Evolution", "Light", "Human Eye", "Electricity", "Magnetic Effects", "Natural Resource Management"]
            }
        }
    }
    
    return curriculum_map.get(board, {}).get(subject, {}).get(grade, [])

def test_claude_api():
    """Test Claude API connection"""
    try:
        if not CLAUDE_API_KEY or CLAUDE_API_KEY == "REPLACE_WITH_YOUR_API_KEY":
            return False, "API key not configured"
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "Test"}]
        }
        
        response = requests.post(CLAUDE_API_URL, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            return True, "API connection successful"
        elif response.status_code == 401:
            return False, f"API Authentication failed - check your API key"
        elif response.status_code == 429:
            return False, f"API rate limit exceeded - try again later"
        else:
            try:
                error_detail = response.json()
                return False, f"API Error {response.status_code}: {error_detail.get('error', {}).get('message', 'Unknown error')}"
            except:
                return False, f"API Error: {response.status_code}"
            
    except Exception as e:
        return False, f"Connection Error: {str(e)}"

def verify_api_key():
    """Verify API key with details"""
    st.write("🔍 **API Key Verification:**")
    
    if not CLAUDE_API_KEY or CLAUDE_API_KEY == "REPLACE_WITH_YOUR_API_KEY":
        st.error("❌ API key not configured")
        return False
    
    if not CLAUDE_API_KEY.startswith("sk-ant-api03-"):
        st.error("❌ Invalid API key format")
        return False
    
    st.success("✅ API key format is correct")
    
    # Test connection
    working, message = test_claude_api()
    if working:
        st.success(f"✅ {message}")
    else:
        st.error(f"❌ {message}")
    
    return working

def generate_questions(board, grade, subject, topic, paper_type, include_answers_on_screen):
    """Generate real exam-style questions using Claude AI"""
    
    # Determine counts based on paper type
    if paper_type == "Paper 1 (25 MCQs)":
        mcq_count = 25
        short_count = 0
    elif paper_type == "Paper 2 (23 Mixed)":
        mcq_count = 15
        short_count = 8
    else:  # Paper 3 (more than 25)
        mcq_count = 30
        short_count = 0
    
    # Get curriculum-specific content
    curriculum_topics = get_curriculum_specific_content(board, grade, subject)
    curriculum_context = ", ".join(curriculum_topics) if curriculum_topics else f"{subject} topics for Grade {grade}"
    
    # Simple prompt - let Claude generate real difficult questions
    prompt = f"""Create a challenging {board} Grade {grade} {subject} test on "{topic}".

Generate {mcq_count} difficult multiple choice questions about {topic}.
Generate {short_count} challenging short answer questions about {topic}.

Requirements:
- Create REAL exam questions with actual content about {topic}
- Make questions challenging and difficult level
- Each MCQ has 4 options (A, B, C, D) with one correct answer
- Use actual facts, calculations, formulas related to {topic}
- No generic descriptions - create specific questions
- Test deep understanding of {topic} concepts
- Make questions that would appear in competitive exams

Return in JSON format:
{{
    "test_info": {{
        "board": "{board}",
        "grade": {grade},
        "subject": "{subject}",
        "topic": "{topic}",
        "paper_type": "{paper_type}",
        "total_questions": {mcq_count + short_count},
        "show_answers_on_screen": {str(include_answers_on_screen).lower()}
    }},
    "questions": [
        {{
            "question_number": 1,
            "type": "mcq",
            "question": "Real challenging question about {topic}",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "correct_answer": "A",
            "explanation": "Explanation"
        }}
    ]
}}"""

    try:
        if not CLAUDE_API_KEY or CLAUDE_API_KEY == "REPLACE_WITH_YOUR_API_KEY":
            st.error("❌ API key not configured")
            return None
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(CLAUDE_API_URL, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result['content'][0]['text']
            
            # Clean and extract JSON
            content = content.strip()
            
            if '```json' in content:
                start = content.find('```json') + 7
                end = content.find('```', start)
                if end != -1:
                    content = content[start:end]
            elif '```' in content:
                start = content.find('```') + 3
                end = content.find('```', start)
                if end != -1:
                    content = content[start:end]
            
            content = content.strip()
            
            try:
                test_data = json.loads(content)
                
                # Ensure test_info has required fields
                if 'test_info' in test_data:
                    test_data['test_info']['show_answers_on_screen'] = include_answers_on_screen
                
                return test_data
                
            except json.JSONDecodeError:
                st.error("❌ Could not parse AI response. Try again.")
                return None
            
        elif response.status_code == 401:
            st.error("❌ API Authentication failed. Check your API key.")
            return None
        elif response.status_code == 429:
            st.error("❌ API rate limit exceeded. Please wait and try again.")
            return None
        else:
            st.error(f"❌ API Error {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"❌ Request failed: {str(e)}")
        return None

def get_enhanced_subject_keywords():
    """Enhanced keywords for topic validation with curriculum focus"""
    return {
        "Mathematics": [
            "number", "numbers", "addition", "subtraction", "multiplication", "division", "counting",
            "algebra", "geometry", "calculus", "arithmetic", "trigonometry", "statistics", "probability",
            "equation", "equations", "function", "functions", "graph", "graphs", "formula", "formulas",
            "fraction", "fractions", "decimal", "decimals", "percentage", "percentages", "ratio", "ratios", "proportion",
            "linear", "quadratic", "polynomial", "polynomials", "derivative", "derivatives", "integral", "integrals",
            "limit", "limits", "theorem", "theorems", "proof", "proofs", "expression", "expressions", 
            "variable", "variables", "constant", "constants", "coefficient", "coefficients",
            "angle", "angles", "triangle", "triangles", "circle", "circles", "square", "squares", 
            "rectangle", "rectangles", "polygon", "polygons", "volume", "area", "perimeter",
            "coordinate", "coordinates", "slope", "parallel", "perpendicular",
            "matrix", "matrices", "determinant", "determinants", "vector", "vectors",
            "hypothesis", "hypothesis testing", "correlation", "regression", "mean", "median", "mode",
            "deviation", "variance", "binomial", "normal", "distribution",
            "measurement", "time", "money", "profit", "loss", "interest",
            "speed", "distance", "rate", "work", "pattern", "patterns", "sequence", "sequences"
        ],
        
        "Science": [
            "matter", "energy", "force", "motion", "gravity", "friction", "pressure", "temperature",
            "heat", "light", "sound", "electricity", "magnetism", "wave", "waves", "radiation",
            "physics", "velocity", "acceleration", "momentum", "power", "work", "machine", "machines",
            "lever", "pulley", "inclined", "current", "voltage", "resistance", "circuit", "circuits",
            "electromagnetic", "quantum", "atomic", "nuclear", "optics", "mechanics", "thermodynamics",
            "chemistry", "atom", "atoms", "molecule", "molecules", "element", "elements", "compound", "compounds",
            "reaction", "reactions", "acid", "acids", "base", "bases", "salt", "salts", "pH",
            "carbon", "organic", "inorganic", "periodic", "table", "bond", "bonds", "electron", "electrons",
            "proton", "protons", "neutron", "neutrons", "ion", "ions", "catalyst", "catalysts",
            "solution", "solutions", "mixture", "mixtures", "oxidation", "reduction", "combustion",
            "biology", "cell", "cells", "tissue", "tissues", "organ", "organs", "system", "systems",
            "photosynthesis", "respiration", "digestion", "circulation", "reproduction", "evolution",
            "genetics", "DNA", "RNA", "gene", "genes", "protein", "proteins", "enzyme", "enzymes",
            "hormone", "hormones", "plant", "plants", "animal", "animals", "bacteria", "virus", "viruses",
            "ecosystem", "ecosystems", "biodiversity", "adaptation", "mutation", "mutations",
            "inheritance", "classification", "taxonomy", "metabolism", "homeostasis", "immunity",
            "experiment", "experiments", "hypothesis", "observation", "data", "analysis", "conclusion",
            "theory", "theories", "law", "laws", "research", "investigation", "method", "procedure"
        ],
        
        "Physics": [
            "motion", "force", "forces", "energy", "electricity", "magnetism", "light", "sound", "heat", 
            "wave", "waves", "particle", "particles", "atom", "atoms", "quantum", "relativity", "mechanics", 
            "thermodynamics", "optics", "acoustics", "velocity", "acceleration", "momentum", "friction", 
            "gravity", "gravitational", "pressure", "temperature", "current", "voltage", "resistance", 
            "circuit", "circuits", "electromagnetic", "radiation", "nuclear", "radioactive", "radioactivity",
            "hypothesis", "experiment", "theory", "law", "measurement", "units", "vectors", "scalars"
        ],
        
        "Chemistry": [
            "atom", "atoms", "molecule", "molecules", "element", "elements", "compound", "compounds", 
            "reaction", "reactions", "acid", "acids", "base", "bases", "salt", "salts", "carbon", 
            "organic", "inorganic", "periodic", "bond", "bonds", "electron", "electrons", "proton", "protons", 
            "neutron", "neutrons", "catalyst", "catalysts", "solution", "solutions", "mixture", "mixtures", 
            "oxidation", "reduction", "pH", "molarity", "valency", "isotope", "isotopes", "chemical", 
            "formula", "formulas", "equation", "equations", "precipitate", "crystallization", "distillation",
            "hypothesis", "experiment", "laboratory", "test", "analysis", "synthesis"
        ],
        
        "Biology": [
            "cell", "cells", "tissue", "tissues", "organ", "organs", "system", "systems", 
            "photosynthesis", "respiration", "digestion", "circulation", "reproduction", "evolution",
            "genetics", "DNA", "RNA", "gene", "genes", "protein", "proteins", "enzyme", "enzymes",
            "hormone", "hormones", "plant", "plants", "animal", "animals", "bacteria", "virus", "viruses",
            "ecosystem", "ecosystems", "biodiversity", "adaptation", "mutation", "mutations",
            "inheritance", "classification", "taxonomy", "metabolism", "homeostasis", "immunity",
            "mitosis", "meiosis", "species", "population", "community", "food", "chain", "web",
            "hypothesis", "experiment", "observation", "microscope", "specimen", "culture"
        ],
        
        "English": [
            "grammar", "literature", "writing", "reading", "comprehension", "vocabulary", "poetry",
            "prose", "novel", "novels", "story", "stories", "essay", "essays", "paragraph", "paragraphs", 
            "sentence", "sentences", "word", "words", "letter", "letters", "phonics", "spelling", 
            "punctuation", "tense", "tenses", "noun", "nouns", "verb", "verbs", "adjective", "adjectives", 
            "adverb", "adverbs", "preposition", "prepositions", "conjunction", "conjunctions", 
            "metaphor", "metaphors", "simile", "similes", "alliteration", "rhyme", "rhythm", "theme", "themes", 
            "plot", "character", "characters", "dialogue", "setting", "conflict", "resolution",
            "article", "articles", "report", "reports", "summary", "analysis", "interpretation"
        ],
        
        "Hindi": [
            "व्याकरण", "साहित्य", "कविता", "गद्य", "उपन्यास", "कहानी", "निबंध", "अनुच्छेद",
            "वाक्य", "शब्द", "अक्षर", "वर्ण", "संज्ञा", "सर्वनाम", "विशेषण", "क्रिया",
            "काल", "वचन", "लिंग", "छंद", "अलंकार", "रस", "भाव", "संवाद", "चरित्र",
            "गद्यांश", "पद्यांश", "व्याख्या", "भावार्थ", "संदेश", "शिक्षा", "नैतिकता"
        ],
        
        "Social Science": [
            "history", "geography", "civics", "economics", "politics", "government", "society", "culture",
            "civilization", "civilizations", "war", "wars", "independence", "freedom", "constitution", 
            "democracy", "republic", "monarchy", "empire", "empires", "map", "maps", "climate", "weather",
            "population", "resources", "agriculture", "industry", "industries", "trade", "commerce", 
            "market", "markets", "money", "currency", "taxation", "budget", "development",
            "ancient", "medieval", "modern", "contemporary", "revolution", "revolutions"
        ],
        
        "History": [
            "ancient", "medieval", "modern", "contemporary", "war", "wars", "battle", "battles",
            "independence", "freedom", "civilization", "civilizations", "empire", "empires",
            "king", "kings", "queen", "queens", "ruler", "rulers", "dynasty", "dynasties",
            "revolution", "revolutions", "culture", "cultures", "heritage", "monument", "monuments",
            "archaeology", "archaeological", "colonialism", "nationalism", "democracy", "republic",
            "constitution", "treaty", "treaties", "timeline", "chronology", "period", "periods",
            "historical", "primary", "secondary", "source", "sources", "evidence"
        ],
        
        "Geography": [
            "map", "maps", "continent", "continents", "country", "countries", "state", "states",
            "city", "cities", "river", "rivers", "mountain", "mountains", "ocean", "oceans",
            "climate", "weather", "population", "resources", "agriculture", "industry", "industries",
            "trade", "transport", "transportation", "latitude", "longitude", "equator", "hemisphere",
            "hemispheres", "topography", "erosion", "watershed", "physical", "human", "economic",
            "political", "natural", "environment", "environmental", "region", "regions"
        ],
        
        "Computer Science": [
            "programming", "algorithm", "algorithms", "data", "structure", "structures", "software", 
            "hardware", "internet", "network", "networks", "database", "databases", "coding", 
            "python", "java", "javascript", "html", "css", "computer", "computers", "technology",
            "binary", "loop", "loops", "function", "functions", "variable", "variables", "array", "arrays",
            "debugging", "cybersecurity", "artificial", "intelligence", "machine", "learning",
            "input", "output", "processing", "logic", "conditional", "iteration", "recursion"
        ],
        
        "Economics": [
            "money", "market", "markets", "trade", "business", "profit", "loss", "demand", "supply",
            "price", "prices", "inflation", "economy", "economic", "finance", "financial", "bank", "banks",
            "investment", "investments", "budget", "budgets", "income", "expenditure", "taxation", "taxes",
            "GDP", "employment", "unemployment", "poverty", "development", "globalization", "production",
            "consumption", "distribution", "resources", "scarcity", "opportunity", "cost"
        ],
        
        "EVS": [
            "environment", "environmental", "nature", "natural", "pollution", "conservation", "wildlife",
            "forest", "forests", "water", "air", "soil", "plant", "plants", "animal", "animals",
            "ecosystem", "ecosystems", "biodiversity", "climate", "weather", "resource", "resources",
            "renewable", "sustainable", "sustainability", "recycling", "global", "warming", "deforestation",
            "endangered", "habitat", "habitats", "food", "chain", "web", "energy", "solar", "wind"
        ],
        
        "Sanskrit": [
            "संस्कृत", "श्लोक", "मंत्र", "व्याकरण", "धातु", "प्रत्यय", "उपसर्ग", "संधि",
            "छंद", "काव्य", "नाटक", "गीता", "वेद", "उपनिषद", "पुराण", "रामायण", "महाभारत",
            "संस्कृति", "धर्म", "दर्शन", "योग", "तप", "त्याग", "सेवा", "अहिंसा"
        ]
    }

def check_topic_relevance(topic, subject):
    """Enhanced topic relevance checking with better curriculum matching"""
    if not topic or not subject:
        return True, []
    
    keywords_dict = get_enhanced_subject_keywords()
    
    # Safe string operations
    topic_clean = str(topic).lower().strip()
    subject_keywords = keywords_dict.get(subject, [])
    
    # Check for direct matches or partial matches
    matches = False
    matched_keywords = []
    
    for keyword in subject_keywords:
        keyword_clean = str(keyword).lower()
        # Check if keyword is in topic or topic is in keyword (both ways)
        if keyword_clean in topic_clean or topic_clean in keyword_clean:
            matches = True
            matched_keywords.append(keyword)
    
    # Additional check for Science subject (covers Physics, Chemistry, Biology)
    if not matches and subject == "Science":
        for science_subject in ["Physics", "Chemistry", "Biology"]:
            if science_subject in keywords_dict:
                for keyword in keywords_dict[science_subject]:
                    keyword_clean = str(keyword).lower()
                    if keyword_clean in topic_clean or topic_clean in keyword_clean:
                        matches = True
                        matched_keywords.append(keyword)
                        break
                if matches:
                    break
    
    # Special cases for mathematical concepts
    if not matches and subject == "Mathematics":
        math_concepts = ["hypothesis", "data", "analysis", "statistics", "probability", "graph", "chart"]
        for concept in math_concepts:
            if concept in topic_clean:
                matches = True
                matched_keywords.append(concept)
                break
    
    return matches, subject_keywords

def display_generated_test(test_data):
    """Display the generated test in a formatted way"""
    if not test_data:
        st.error("No test data to display")
        return
    
    test_info = test_data.get('test_info', {})
    questions = test_data.get('questions', [])
    show_answers_on_screen = test_info.get('show_answers_on_screen', False)
    difficulty_level = test_info.get('difficulty_level', f"Grade {test_info.get('grade', '')} Level")
    
    # Test header with II Tuition branding
    st.markdown(f"""
    <div class="test-paper">
        <h1 style="text-align: center; color: #667eea; margin-bottom: 0.5rem; font-size: 2.5rem;">
            🎓 II Tuition Mock Test Generated
        </h1>
        <h2 style="text-align: center; color: #333; margin-bottom: 1rem; font-size: 1.8rem;">
            {test_info.get('subject', 'Subject')} Mock Test
        </h2>
        <div style="text-align: center; margin-bottom: 1rem; color: #2e7d32; font-size: 18px; font-weight: bold;">
            📚 Difficulty Level: {difficulty_level} 📚
        </div>
        <div style="text-align: center; margin-bottom: 1.5rem; font-size: 16px; background: #f8f9fa; padding: 15px; border-radius: 10px;">
            <strong>Board:</strong> {test_info.get('board', 'N/A')} | 
            <strong>Grade:</strong> {test_info.get('grade', 'N/A')} | 
            <strong>Topic:</strong> {test_info.get('topic', 'N/A')}
        </div>
        <div style="text-align: center; margin-bottom: 2rem; color: #666; font-size: 14px;">
            <strong>Paper Type:</strong> {test_info.get('paper_type', 'N/A')} | 
            <strong>Total Questions:</strong> {test_info.get('total_questions', len(questions))}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions section
    st.markdown("### 📋 Instructions:")
    st.markdown("""
    <div style="background: #e8f5e8; border: 1px solid #4caf50; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h4 style="color: #2e7d32; margin-bottom: 10px;">📖 Test Guidelines</h4>
        <p style="color: #2e7d32; margin-bottom: 0;">This test is designed according to your curriculum standards. Read questions carefully and choose the best answers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    instructions_col1, instructions_col2 = st.columns(2)
    
    with instructions_col1:
        st.markdown("""
        - Read all questions carefully before answering
        - For multiple choice questions, select the best option
        - Take your time to understand each question
        """)
    
    with instructions_col2:
        st.markdown("""
        - Show all working for calculation problems
        - Write clearly for descriptive answers
        - Manage your time effectively
        """)
    
    st.markdown("---")
    
    # Questions display
    for i, question in enumerate(questions, 1):
        question_difficulty = question.get('difficulty', difficulty_level)
        
        st.markdown(f"""
        <div class="question-container">
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">Question {i}</h4>
            <div style="color: #2e7d32; font-size: 12px; font-weight: bold; margin-bottom: 1rem;">
                📚 {question_difficulty}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**{question.get('question', 'Question text missing')}**")
        
        if question.get('type') == 'mcq' and 'options' in question:
            options = question['options']
            for option_key, option_text in options.items():
                st.write(f"**{option_key})** {option_text}")
            
            # Only show correct answer if "Show Answers on Screen" was checked
            if show_answers_on_screen and 'correct_answer' in question and question['correct_answer']:
                st.success(f"**Correct Answer: {question['correct_answer']}**")
                # Show explanation if available
                if 'explanation' in question and question['explanation']:
                    st.info(f"**Explanation:** {question['explanation']}")
        
        elif question.get('type') == 'short_answer':
            st.write("**[Short Answer Question - Write your detailed answer below]**")
            # Only show sample answer if "Show Answers on Screen" was checked
            if show_answers_on_screen and 'sample_answer' in question and question['sample_answer']:
                st.info(f"**Sample Answer:** {question['sample_answer']}")
        
        st.markdown("---")

def get_available_subjects(board, grade):
    """Get available subjects for board and grade"""
    subjects_data = get_subjects_by_board()
    board_data = subjects_data.get(board, {})
    return board_data.get(grade, [])

def create_questions_pdf(test_data, filename="questions.pdf"):
    """Create PDF with questions only"""
    if not PDF_AVAILABLE:
        st.error("PDF generation not available. Please install reportlab: pip install reportlab")
        return None
    
    try:
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # II Tuition Title style
        tuitions_title_style = ParagraphStyle(
            'TuitionsTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=10,
            alignment=1,  # Center
            textColor=colors.darkblue
        )
        
        # Subject title style
        subject_title_style = ParagraphStyle(
            'SubjectTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=1,  # Center
            textColor=colors.darkblue
        )
        
        # Question style
        question_style = ParagraphStyle(
            'QuestionStyle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            leftIndent=20
        )
        
        test_info = test_data.get('test_info', {})
        questions = test_data.get('questions', [])
        
        # II Tuition Header
        story.append(Paragraph("🎓 II Tuition Mock Test Generated", tuitions_title_style))
        story.append(Paragraph(f"{test_info.get('subject', 'Subject')} Mock Test", subject_title_style))
        story.append(Paragraph(f"Board: {test_info.get('board', 'N/A')} | Grade: {test_info.get('grade', 'N/A')} | Topic: {test_info.get('topic', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"Paper Type: {test_info.get('paper_type', 'N/A')} | Total Questions: {test_info.get('total_questions', len(questions))}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Instructions
        story.append(Paragraph("Instructions:", styles['Heading2']))
        story.append(Paragraph("• Read all questions carefully", styles['Normal']))
        story.append(Paragraph("• Choose the best answer for multiple choice questions", styles['Normal']))
        story.append(Paragraph("• Write clearly for descriptive answers", styles['Normal']))
        story.append(Paragraph("• Manage your time effectively", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Questions
        for i, question in enumerate(questions, 1):
            story.append(Paragraph(f"<b>Question {i}:</b> {question.get('question', '')}", question_style))
            
            if question.get('type') == 'mcq' and 'options' in question:
                options = question['options']
                for option_key, option_text in options.items():
                    story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;<b>{option_key})</b> {option_text}", styles['Normal']))
            
            story.append(Spacer(1, 15))
        
        doc.build(story)
        return filename
        
    except Exception as e:
        st.error(f"Error creating PDF: {str(e)}")
        return None

def create_answers_pdf(test_data, filename="answers.pdf"):
    """Create PDF with answers only"""
    if not PDF_AVAILABLE:
        st.error("PDF generation not available. Please install reportlab: pip install reportlab")
        return None
    
    try:
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # II Tuition Title style
        tuitions_title_style = ParagraphStyle(
            'TuitionsTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=10,
            alignment=1,  # Center
            textColor=colors.darkgreen
        )
        
        # Subject title style
        subject_title_style = ParagraphStyle(
            'SubjectTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=1,  # Center
            textColor=colors.darkgreen
        )
        
        test_info = test_data.get('test_info', {})
        questions = test_data.get('questions', [])
        
        # II Tuition Header
        story.append(Paragraph("🎓 II Tuition Mock Test Generated", tuitions_title_style))
        story.append(Paragraph(f"{test_info.get('subject', 'Subject')} Mock Test - Answer Key", subject_title_style))
        story.append(Paragraph(f"Board: {test_info.get('board', 'N/A')} | Grade: {test_info.get('grade', 'N/A')} | Topic: {test_info.get('topic', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"Paper Type: {test_info.get('paper_type', 'N/A')} | Total Questions: {test_info.get('total_questions', len(questions))}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Answers
        for i, question in enumerate(questions, 1):
            story.append(Paragraph(f"<b>Question {i}:</b> {question.get('question', '')}", styles['Normal']))
            
            # Show the question options first (for MCQs)
            if question.get('type') == 'mcq' and 'options' in question:
                options = question['options']
                for option_key, option_text in options.items():
                    story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;<b>{option_key})</b> {option_text}", styles['Normal']))
            
            # Show the correct answer
            if 'correct_answer' in question and question['correct_answer']:
                story.append(Paragraph(f"<b>Correct Answer:</b> {question['correct_answer']}", styles['Normal']))
            elif 'sample_answer' in question and question['sample_answer']:
                story.append(Paragraph(f"<b>Sample Answer:</b> {question['sample_answer']}", styles['Normal']))
            elif 'answer' in question and question['answer']:
                story.append(Paragraph(f"<b>Answer:</b> {question['answer']}", styles['Normal']))
            else:
                story.append(Paragraph("<b>Answer:</b> Answer not generated (test created without answers)", styles['Normal']))
            
            # Show explanation if available
            if 'explanation' in question and question['explanation']:
                story.append(Paragraph(f"<b>Explanation:</b> {question['explanation']}", styles['Normal']))
            
            story.append(Spacer(1, 15))
        
        doc.build(story)
        return filename
        
    except Exception as e:
        st.error(f"Error creating PDF: {str(e)}")
        return None

def show_mock_test_creator():
    """Main application function with improved form logic"""
    
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    if 'generated_test' not in st.session_state:
        st.session_state.generated_test = None
    
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'board': '',
            'grade': 0,
            'subject': '',
            'topic': ''
        }
    
    # Home Page
    if st.session_state.current_page == 'home':
        # API Status
        with st.expander("🔧 API Configuration Status"):
            if CLAUDE_API_KEY and CLAUDE_API_KEY != "REPLACE_WITH_YOUR_API_KEY":
                st.success("✅ Claude API Key is configured")
            else:
                st.error("❌ Claude API Key not configured")
        
        # Header
        st.markdown("""
        <div class="main-header">
            <div class="hero-title">🎯 II Tuitions Mock Test Generator</div>
            <div class="hero-subtitle">Generate realistic practice tests based on curriculum standards</div>
            <div class="stats-container">📊 3,675 curriculum-based tests generated</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create Test Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Create Test", use_container_width=True):
                st.session_state.current_page = 'create_test'
                st.rerun()
        
        # Review Section
        st.markdown("""
        <div class="review-section">
            <h2 style="text-align: center; margin-bottom: 2rem;">⭐ Review</h2>
            <p style="text-align: center; margin-bottom: 2rem;">Review your progress, results, and get feedback from teachers and parents</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Review Cards
        cols = st.columns(4)
        review_data = [
            ("👨‍🏫 Teacher Review", "Get feedback from educators", "124 reviews"),
            ("👨‍👩‍👧‍👦 Parent Review", "Parental feedback & support", "89 reviews"),
            ("👨‍🏫 Teacher Review", "Academic performance insights", "156 reviews"),
            ("👨‍👩‍👧‍👦 Parent Review", "Progress tracking & guidance", "201 reviews")
        ]
        
        for i, (title, desc, count) in enumerate(review_data):
            with cols[i]:
                st.markdown(f"""
                <div class="review-card">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                    <div style="color: #FFD700;">⭐⭐⭐⭐⭐</div>
                    <p>{count}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # View Reviews Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("View Reviews", use_container_width=True)
    
    # Create Test Page with improved form management
    elif st.session_state.current_page == 'create_test':
        st.markdown("""
        <div class="form-container">
            <h1 style="text-align: center; margin-bottom: 2rem;">🎯 Curriculum-Based Mock Test Generator</h1>
            <p style="text-align: center; margin-bottom: 2rem;">Generate realistic practice tests aligned with your curriculum standards</p>
        </div>
        """, unsafe_allow_html=True)
        
        # API Test Section (outside form for immediate testing)
        st.markdown("### 🔍 Claude AI Configuration Test")
        
        # Show API key status
        st.write("**Current API Key Status:**")
        if CLAUDE_API_KEY and CLAUDE_API_KEY != "REPLACE_WITH_YOUR_API_KEY":
            key_preview = CLAUDE_API_KEY[:15] + "..." + CLAUDE_API_KEY[-8:]
            st.success(f"✅ API Key configured: {key_preview}")
        else:
            st.error("❌ API Key not configured")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Test Claude API Connection"):
                with st.spinner("Testing API connection..."):
                    working, message = test_claude_api()
                    if working:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
                        if "401" in message:
                            st.info("🔧 **Troubleshooting Tips:**")
                            st.info("1. Check if your API key is correct")
                            st.info("2. Verify you have Claude API credits remaining")
                            st.info("3. Make sure the API key hasn't expired")
                            st.info("4. Try generating a new API key from Anthropic Console")
        
        with col2:
            if st.button("📋 Detailed API Verification"):
                verify_api_key()
        
        st.markdown("---")
        
        # Main Form with improved state management
        # Board selection (always available)
        st.subheader("1️⃣ Select Board")
        board_options = ["Select Board", "CBSE", "ICSE", "IB", "Cambridge IGCSE", "State Board"]
        selected_board = st.selectbox(
            "Choose your education board", 
            board_options, 
            index=0,
            key="board_select",
            help="Choose from major education boards"
        )
        
        # Update session state
        if selected_board != "Select Board":
            st.session_state.form_data['board'] = selected_board
            board = selected_board
        else:
            st.session_state.form_data['board'] = ''
            board = ''
        
        # Grade selection (available after board selection)
        st.subheader("2️⃣ Select Grade")
        if board:
            grade_options = ["Select Grade"] + [f"Grade {i}" for i in range(1, 13)]
            selected_grade = st.selectbox(
                "Choose your grade level", 
                grade_options, 
                index=0,
                key=f"grade_select_{board}",
                help="Select your current grade (1-12)"
            )
            
            # Update session state
            if selected_grade != "Select Grade":
                # Safely extract grade number
                try:
                    grade_text = str(selected_grade)
                    if "Grade" in grade_text:
                        grade_num = int(grade_text.replace("Grade ", ""))
                    else:
                        grade_num = int(grade_text)
                    st.session_state.form_data['grade'] = grade_num
                    grade = grade_num
                except (ValueError, AttributeError):
                    grade = 0
            else:
                st.session_state.form_data['grade'] = 0
                grade = 0
        else:
            st.selectbox(
                "Choose your grade level", 
                ["Please select Board first"], 
                disabled=True,
                key="grade_disabled",
                help="Please select a Board first"
            )
            grade = 0
        
        # Subject selection (available after board and grade selection)
        st.subheader("3️⃣ Select Subject")
        if board and grade > 0:
            available_subjects = get_available_subjects(board, grade)
            
            if available_subjects:
                subject_options = ["Select Subject"] + available_subjects
                selected_subject = st.selectbox(
                    "Choose your subject", 
                    subject_options, 
                    index=0,
                    key=f"subject_select_{board}_{grade}",
                    help=f"Available subjects for {board} Grade {grade}"
                )
                
                # Update session state
                if selected_subject != "Select Subject":
                    st.session_state.form_data['subject'] = selected_subject
                    subject = selected_subject
                    st.success(f"✅ Selected: {subject} for {board} Grade {grade}")
                else:
                    st.session_state.form_data['subject'] = ''
                    subject = ''
            else:
                st.error(f"❌ No subjects available for {board} Grade {grade}")
                st.selectbox(
                    "Choose your subject", 
                    ["No subjects available"], 
                    disabled=True, 
                    key=f"subject_disabled_{board}_{grade}",
                    help="Please select a valid board and grade combination"
                )
                subject = ''
        else:
            if not board and grade == 0:
                help_text = "Please select Board and Grade first"
            elif not board:
                help_text = "Please select a Board first"
            else:
                help_text = "Please select a Grade first"
            
            st.selectbox(
                "Choose your subject", 
                [help_text], 
                disabled=True, 
                key=f"subject_placeholder_{board}_{grade}",
                help=help_text
            )
            subject = ''
        
        # Topic input (available after subject selection)
        st.subheader("4️⃣ Enter Topic")
        if subject:
            topic_input = st.text_input(
                "Enter your topic here...", 
                placeholder=f"e.g., Photosynthesis, Algebra, World War II (for {subject})", 
                key=f"topic_input_{subject}",
                help=f"Enter a topic related to {subject}"
            )
            
            # Update session state
            if topic_input:
                topic = topic_input.strip()
                st.session_state.form_data['topic'] = topic
            else:
                topic = ''
                st.session_state.form_data['topic'] = ''
        else:
            st.text_input(
                "Enter your topic here...", 
                placeholder="Please select a subject first", 
                disabled=True,
                key="topic_disabled",
                help="Please select a subject first to enter a topic"
            )
            topic = ''
        
        # Topic validation (only if topic is entered)
        topic_valid = True
        topic_error_message = ""
        
        if topic and subject:
            is_relevant, keywords = check_topic_relevance(topic, subject)
            if not is_relevant:
                topic_valid = False
                topic_error_message = f"Topic '{topic}' doesn't seem to match {subject}"
                st.error(f"⚠️ {topic_error_message}")
                
                # Show suggestions
                if keywords:
                    st.info(f"💡 Try topics related to {subject}:")
                    
                    # Display keywords safely
                    col1, col2 = st.columns(2)
                    keywords_count = len(keywords)
                    mid_point = keywords_count // 2
                    
                    with col1:
                        st.write("**Suggestions:**")
                        for i in range(min(mid_point, 8)):
                            if i < len(keywords):
                                keyword = str(keywords[i])
                                st.write(f"• {keyword.title()}")
                    
                    with col2:
                        st.write("**More topics:**")
                        start_idx = mid_point
                        for i in range(start_idx, min(start_idx + 8, len(keywords))):
                            if i < len(keywords):
                                keyword = str(keywords[i])
                                st.write(f"• {keyword.title()}")
            else:
                st.success(f"✅ Topic '{topic}' is relevant to {subject}")
        elif topic and not subject:
            st.warning("⚠️ Please select a subject first to validate your topic")
            topic_valid = False
        
        # Current selections summary
        if board or grade or subject or topic:
            st.markdown("---")
            st.markdown("### 📋 Current Selections:")
            
            summary_col1, summary_col2 = st.columns(2)
            with summary_col1:
                if board:
                    st.write(f"**Board:** {board}")
                if grade > 0:
                    st.write(f"**Grade:** {grade}")
            with summary_col2:
                if subject:
                    st.write(f"**Subject:** {subject}")
                if topic:
                    st.write(f"**Topic:** {topic}")
        
        # Paper Type and Options
        st.markdown("---")
        st.subheader("5️⃣ Test Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Paper Type:**")
            paper_type = st.radio("Select Paper Type", [
                "Paper 1 (25 MCQs)",
                "Paper 2 (23 Mixed)",
                "Paper 3 (more than 25)"
            ], key="paper_type_radio")
        
        with col2:
            st.write("**Questions Format:**")
            if paper_type == "Paper 1 (25 MCQs)":
                st.info("✅ 25 Multiple Choice Questions")
            elif paper_type == "Paper 2 (23 Mixed)":
                st.info("✅ 15 MCQs + 8 Short Answer Questions")
            else:
                st.info("✅ 30+ Multiple Choice Questions")
        
        # Include Answers option
        include_answers = st.checkbox(
            "✓ Show Answers on Screen", 
            value=False, 
            help="Check this to display answers on screen after generating the test. Answers will always be available in the downloadable Answer PDF regardless of this setting."
        )
        
        # Enhanced validation with detailed feedback
        st.markdown("---")
        st.markdown("### 📋 Validation Summary")
        
        validation_results = []
        
        # Board validation
        if board:
            validation_results.append(("✅ Board", f"Selected: {board}", "success"))
        else:
            validation_results.append(("❌ Board", "Please select a board", "error"))
        
        # Grade validation
        if grade > 0:
            validation_results.append(("✅ Grade", f"Selected: Grade {grade}", "success"))
        else:
            validation_results.append(("❌ Grade", "Please select a grade", "error"))
        
        # Subject validation
        if subject:
            validation_results.append(("✅ Subject", f"Selected: {subject}", "success"))
        else:
            if board and grade > 0:
                validation_results.append(("❌ Subject", "Please select a subject", "error"))
            else:
                validation_results.append(("⚠️ Subject", "Select board and grade first", "warning"))
        
        # Topic validation
        if topic:
            if topic_valid:
                validation_results.append(("✅ Topic", f"'{topic}' is valid for {subject}", "success"))
            else:
                validation_results.append(("❌ Topic", topic_error_message, "error"))
        else:
            if subject:
                validation_results.append(("❌ Topic", "Please enter a topic", "error"))
            else:
                validation_results.append(("⚠️ Topic", "Select subject first", "warning"))
        
        # Display validation results
        validation_col1, validation_col2 = st.columns(2)
        
        with validation_col1:
            for i in range(0, len(validation_results), 2):
                status, message, msg_type = validation_results[i]
                if msg_type == "success":
                    st.success(f"{status}: {message}")
                elif msg_type == "error":
                    st.error(f"{status}: {message}")
                else:
                    st.warning(f"{status}: {message}")
        
        with validation_col2:
            for i in range(1, len(validation_results), 2):
                if i < len(validation_results):
                    status, message, msg_type = validation_results[i]
                    if msg_type == "success":
                        st.success(f"{status}: {message}")
                    elif msg_type == "error":
                        st.error(f"{status}: {message}")
                    else:
                        st.warning(f"{status}: {message}")
        
        # Check if all validations pass
        valid_count = sum(1 for result in validation_results if result[0].startswith("✅"))
        all_valid = (valid_count == 4)  # Need all 4 validations to pass
        
        if all_valid:
            st.success("🎉 All validations passed! Ready to create curriculum-based mock test.")
            st.info("💡 **Note:** Questions will be generated according to your curriculum standards with realistic difficulty level.")
        
        # Submit button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            create_btn = st.button("🚀 CREATE CURRICULUM-BASED MOCK TEST", use_container_width=True)
            
            if create_btn:
                if not all_valid:
                    st.error("❌ Please fix validation errors before creating the test")
                    st.warning("⚠️ Make sure to complete all required fields: Board, Grade, Subject, and Topic")
                else:
                    with st.spinner("🤖 Generating curriculum-specific questions with answers..."):
                        test_data = generate_questions(board, grade, subject, topic, paper_type, include_answers)
                        
                        if test_data:
                            st.success("✅ Curriculum-based test generated successfully!")
                            st.balloons()
                            st.session_state.generated_test = test_data
                            st.session_state.current_page = 'test_display'
                            st.rerun()
                        else:
                            st.error("❌ Failed to generate test. Please check your API connection and try again.")
                            st.info("💡 Try testing the API connection first, then regenerate the test.")
        
        # Navigation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.current_page = 'home'
                st.rerun()
    
    # Test Display Page
    elif st.session_state.current_page == 'test_display':
        if st.session_state.generated_test:
            test_data = st.session_state.generated_test
            
            # Header buttons with PDF download functionality
            col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
            
            with col1:
                if st.button("← Back to Create Test"):
                    st.session_state.current_page = 'create_test'
                    st.rerun()
            
            with col2:
                if st.button("🏠 Home"):
                    st.session_state.current_page = 'home'
                    st.rerun()
            
            with col3:
                if st.button("📄 Save Questions PDF"):
                    if PDF_AVAILABLE:
                        with st.spinner("Generating questions PDF..."):
                            questions_pdf = create_questions_pdf(test_data, "questions.pdf")
                            if questions_pdf:
                                with open(questions_pdf, "rb") as pdf_file:
                                    st.download_button(
                                        label="⬇️ Download Questions PDF",
                                        data=pdf_file.read(),
                                        file_name=f"mock_test_questions_{test_data['test_info']['subject']}_grade_{test_data['test_info']['grade']}.pdf",
                                        mime="application/pdf"
                                    )
                    else:
                        st.error("PDF generation not available. Please install reportlab: pip install reportlab")
            
            with col4:
                if st.button("📝 Save Answers PDF"):
                    if PDF_AVAILABLE:
                        with st.spinner("Generating answers PDF..."):
                            answers_pdf = create_answers_pdf(test_data, "answers.pdf")
                            if answers_pdf:
                                with open(answers_pdf, "rb") as pdf_file:
                                    st.download_button(
                                        label="⬇️ Download Answers PDF",
                                        data=pdf_file.read(),
                                        file_name=f"mock_test_answers_{test_data['test_info']['subject']}_grade_{test_data['test_info']['grade']}.pdf",
                                        mime="application/pdf"
                                    )
                    else:
                        st.error("PDF generation not available. Please install reportlab: pip install reportlab")
            
            with col5:
                st.button("📤 Share Test")
            
            with col6:
                if st.button("🔄 Generate New"):
                    st.session_state.current_page = 'create_test'
                    st.rerun()
            
            # PDF Installation Notice
            if not PDF_AVAILABLE:
                st.warning("📋 **PDF functionality requires additional package.** Run: `pip install reportlab` to enable PDF downloads.")
            
            # Display the generated test
            display_generated_test(test_data)
            
        else:
            st.warning("No test generated yet. Please create a test first.")
            if st.button("← Back to Create Test"):
                st.session_state.current_page = 'create_test'
                st.rerun()

if __name__ == "__main__":
    show_mock_test_creator()
