import json
from pathlib import Path


def create_sample_questions():
    """Create sample questions for testing"""
    categories = {
        "mathematical_numerical": [
            {"question": "What is 25 * 4?", "correct_answer": "100"}
        ]
    }

    # Create questions directory
    questions_dir = Path("questions")
    questions_dir.mkdir(exist_ok=True)
    
    # Save each category to a JSON file
    for category, questions in categories.items():
        with open(questions_dir / f"{category}.json", "w") as f:
            json.dump(questions, f, indent=2)