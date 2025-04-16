import asyncio
from pathlib import Path
from QuestionGenerator import create_sample_questions
from General_Knowledge_Test import TemperatureStudy

async def test_connection():
    """Test the API connection with a simple query"""
    try:
        study = TemperatureStudy()
        result = await study.run_temperature_test("Say hello", 0.0)
        print("API Connection Test Successful!")
        return True
    except Exception as e:
        print("API Connection Test Failed!")
        print("Error:", str(e))
        return False

async def main():

    # First test the connection
    if not await test_connection():
        print("Exiting due to connection test failure")
        return
        
    # Create sample questions if they don't exist
    if not Path("questions").exists():
        create_sample_questions()
    
    # Run the study
    study = TemperatureStudy()
    results = await study.run_study()

if __name__ == "__main__":
    asyncio.run(main())