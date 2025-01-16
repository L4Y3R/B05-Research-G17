from langchain_fireworks import Fireworks 
from langchain.prompts import PromptTemplate
import pandas as pd
import json
from typing import List, Dict
import time
from pathlib import Path
import asyncio
import os
from dotenv import load_dotenv

class TemperatureStudy:
    def __init__(
        self, 
        model_name: str = "accounts/fireworks/models/llama-v3p1-8b-instruct",
        temperatures: List[float] = None
    ):
        """
        Initialize the study with Fireworks model configuration and temperature range.
        """
        load_dotenv()
        self.model_name = model_name
        self.temperatures = temperatures or [round(t * 0.1, 1) for t in range(11)]
        self.results_dir = Path("temperature_study_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Validate API key
        if not os.getenv("FIREWORKS_API_KEY"):
            raise ValueError("FIREWORKS_API_KEY not found in environment variables")
        
    def load_questions(self, category: str) -> List[Dict]:
        """
        Load questions from JSON files organized by category.
        """
        question_file = Path(f"questions/{category}.json")
        with open(question_file, 'r') as f:
            return json.load(f)
    
    def clean_response(self, text: str) -> str:
        """Clean the model response to keep only the first line."""
        # Split the text into lines and take the first one
        first_line = text.split('\n', 1)[0]
        
        # Remove extra quotes and clean up whitespace
        first_line = first_line.replace('"""', '').replace('```', '').strip()
        
        return first_line


    async def run_temperature_test(self, question: str, temperature: float) -> Dict:
        """
        Run a single test with a specific temperature setting using Fireworks.
        """
        llm = Fireworks(
            model=self.model_name,
            fireworks_api_key=os.getenv("FIREWORKS_API_KEY"),
            temperature=temperature
        )
        
        prompt = PromptTemplate(
            template="""State whether these statements are either True or False {question}

                Rules:
                - Provide ONLY "True" or "False" as the answer
                - No explanations
                - Only one word is allowed as the answer

                Your response:""",
            input_variables=["question"]
        )
        
        start_time = time.time()
        try:
            response = await llm.agenerate([prompt.format(question=question)])
            response_text = self.clean_response(response.generations[0][0].text)
            
            result = {
                "temperature": temperature,
                "response": response_text,
                "response_time": round(time.time() - start_time, 3)
            }
            
            # Print real-time results in a clear format
            print(f"\nTest Results for Temperature {temperature}:")
            print(f"Question: {question}")
            print(f"Response: {response_text}")
            print(f"Response Time: {result['response_time']} seconds")
            print("-" * 50)
            
            return result
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return {
                "temperature": temperature,
                "response": f"Error: {str(e)}",
                "response_time": time.time() - start_time
            }

    async def process_category(self, category: str):
        """
        Process all questions in a category across all temperature settings.
        """
        questions = self.load_questions(category)
        results = []
        
        for question_data in questions:
            question = question_data["question"]
            correct_answer = question_data["correct_answer"]
            
            for temp in self.temperatures:
                try:
                    result = await self.run_temperature_test(question, temp)
                    result.update({
                        "question": question,
                        "correct_answer": correct_answer,
                        "category": category
                    })
                    results.append(result)
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"Error processing question: {question} at temp {temp}: {str(e)}")
        
        df = pd.DataFrame(results)
        df.to_csv(self.results_dir / f"{category}_results.csv", index=False)
        return df

    async def run_study(self):
        """
        Run the complete study across all categories.
        """
        categories = [
            "true_false"
        ]
        
        all_results = []
        for category in categories:
            print(f"Processing category: {category}")
            results = await self.process_category(category)
            all_results.append(results)
            
        final_df = pd.concat(all_results)
        return final_df
    
    def analyze_results(self, results_df: pd.DataFrame):
        """
        Analyze the results of the temperature study to understand how temperature affects model responses.
        
        Args:
            results_df (pd.DataFrame): DataFrame containing all the study results
            
        Returns:
            tuple: (analysis DataFrame, consistency DataFrame) containing statistical analysis
        """
        # Basic statistical analysis of response times and other metrics
        analysis = results_df.groupby(['category', 'temperature']).agg({
            'response_time': ['mean', 'std']
        }).round(3)
        
        # Analyze response consistency by counting unique responses for each question
        def calculate_response_similarity(group):
            # Count unique responses for each question at each temperature
            responses = group['response'].tolist()
            return len(set(responses))
        
        # Group responses by category and temperature to analyze consistency
        consistency = (results_df.groupby(['category', 'temperature'])
                      .apply(calculate_response_similarity)
                      .reset_index(name='unique_responses'))
        
        # Add percentage of correct answers if possible
        if 'correct_answer' in results_df.columns:
            def calculate_accuracy(group):
                return (group['response'].str.strip().str.lower() == 
                       group['correct_answer'].str.strip().str.lower()).mean() * 100
                
            accuracy = (results_df.groupby(['category', 'temperature'])
                       .apply(calculate_accuracy)
                       .reset_index(name='accuracy_percentage'))
            
            # Merge accuracy with consistency
            consistency = consistency.merge(accuracy, on=['category', 'temperature'])
        
        return analysis, consistency