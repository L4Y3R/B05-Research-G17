from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import pandas as pd
import json
from typing import List, Dict
import time
from pathlib import Path
import asyncio
from langchain.callbacks import get_openai_callback

class TemperatureStudy:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperatures: List[float] = None):
        """
        Initialize the study with model configuration and temperature range.
        
        Args:
            model_name: The name of the LLM to use
            temperatures: List of temperature values to test
        """
        self.model_name = model_name
        self.temperatures = temperatures or [round(t * 0.1, 1) for t in range(11)]  # 0.0 to 1.0
        self.results_dir = Path("temperature_study_results")
        self.results_dir.mkdir(exist_ok=True)
        
    def load_questions(self, category: str) -> List[Dict]:
        """
        Load questions from JSON files organized by category.
        Expected format: [{"question": "...", "correct_answer": "..."}]
        """
        question_file = Path(f"questions/{category}.json")
        with open(question_file, 'r') as f:
            return json.load(f)

    async def run_temperature_test(self, question: str, temperature: float) -> Dict:
        """
        Run a single test with a specific temperature setting.
        """
        chat = ChatOpenAI(
            model_name=self.model_name,
            temperature=temperature
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Provide direct answers without explanation."),
            ("human", "{question}")
        ])
        
        # Track token usage and response time
        start_time = time.time()
        with get_openai_callback() as cb:
            chain = prompt | chat
            response = await chain.ainvoke({"question": question})
            
        return {
            "temperature": temperature,
            "response": response.content,
            "prompt_tokens": cb.prompt_tokens,
            "completion_tokens": cb.completion_tokens,
            "total_tokens": cb.total_tokens,
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
                    
                    # Add delay to respect API rate limits
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"Error processing question: {question} at temp {temp}: {str(e)}")
        
        # Save results for this category
        df = pd.DataFrame(results)
        df.to_csv(self.results_dir / f"{category}_results.csv", index=False)
        return df

    async def run_study(self):
        """
        Run the complete study across all categories.
        """
        categories = [
            "mathematical_numerical",
            "mathematical_text",
            "logical_thinking",
            "true_false",
            "general_knowledge"
        ]
        
        all_results = []
        for category in categories:
            print(f"Processing category: {category}")
            results = await self.process_category(category)
            all_results.append(results)
            
        # Combine all results
        final_df = pd.concat(all_results)
        final_df.to_csv(self.results_dir / "complete_results.csv", index=False)
        return final_df

    def analyze_results(self, results_df: pd.DataFrame):
        """
        Analyze the results of the study.
        """
        # Group by category and temperature
        analysis = results_df.groupby(['category', 'temperature']).agg({
            'response_time': ['mean', 'std'],
            'total_tokens': ['mean', 'std'],
        }).round(3)
        
        # Calculate response consistency
        return analysis
