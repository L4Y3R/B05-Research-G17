import json
from pathlib import Path


def create_sample_questions():
    """Create sample questions for testing"""
    categories = {
        "mathematical_numerical": [
            {"question": "What is 25 * 4?", "correct_answer": "100"}
        ],
        "mathematical_text": [
            {"question": "What is twenty five multiplied by four?", "correct_answer": "Hundred"}
        ],
        "true_false": [
            {"question": "Is sun rotating around the earth", "correct_answer": "False"}
        ],
        "logical": [
            {"question": "Is joe mama fat", "correct_answer": "False"}
        ],
        "general_knowledge": [
            {"question": "Is Dubai a country", "correct_answer": "Dubai is a city"}
        ]

    }

    # Create questions directory
    questions_dir = Path("questions")
    questions_dir.mkdir(exist_ok=True)
    
    # Save each category to a JSON file
    for category, questions in categories.items():
        with open(questions_dir / f"{category}.json", "w") as f:
            json.dump(questions, f, indent=2)