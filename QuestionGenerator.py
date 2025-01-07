import json
from pathlib import Path


def create_sample_questions():
    """Create sample questions for testing"""
    categories = {
        "mathematical_numerical": [
            {"question": "What is 25 * 4?", "correct_answer": "100"},
            {"question": "What is the square root of 144?", "correct_answer": "12"}
        ],
        "mathematical_text": [
            {"question": "If John has 5 apples and gives 2 to Mary, how many does he have left?", 
             "correct_answer": "3"},
            {"question": "What is the next number in the sequence: 2, 4, 8, 16, ?", 
             "correct_answer": "32"}
        ],
        "logical_thinking": [
            {"question": "If all A are B, and all B are C, then are all A also C?", 
             "correct_answer": "Yes"},
            {"question": "If it's not sunny and it's not cloudy, what's the weather like?", 
             "correct_answer": "There must be an error in the premises"}
        ],
        "true_false": [
            {"question": "Is water composed of hydrogen and oxygen?", 
             "correct_answer": "True"},
            {"question": "Is the Earth flat?", 
             "correct_answer": "False"}
        ],
        "general_knowledge": [
            {"question": "What is the capital of France?", 
             "correct_answer": "Paris"},
            {"question": "Who wrote Romeo and Juliet?", 
             "correct_answer": "William Shakespeare"}
        ]
    }

    # Create questions directory
    questions_dir = Path("questions")
    questions_dir.mkdir(exist_ok=True)
    
    # Save each category to a JSON file
    for category, questions in categories.items():
        with open(questions_dir / f"{category}.json", "w") as f:
            json.dump(questions, f, indent=2)