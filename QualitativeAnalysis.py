from textblob import TextBlob
from collections import defaultdict
import numpy as np
from typing import List, Dict, Any
import pandas as pd
import json
from pathlib import Path
import re
from scipy.stats import entropy
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import nltk

class QualitativeAnalysis:
    def __init__(self, base_prompt: str = None):
        """
        Initialize the qualitative analysis component with enhanced metrics.
        """
        # Download required NLTK data
        try:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('averaged_perceptron_tagger')
        except:
            print("Warning: NLTK data download failed. Some features may be limited.")
            
        self.response_characteristics = {
            "creativity": self._analyze_creativity,
            "complexity": self._analyze_complexity,
            "sentiment": self._analyze_sentiment,
            "mathematical_rigor": self._analyze_mathematical_rigor
        }
        
        self.base_prompt = base_prompt or """
        Solve this problem: {question}
        
        Rules:
        - Explain your thinking process
        - Show your work
        - Discuss any assumptions
        - Mention alternative approaches if applicable
        - Indicate confidence level in your solution
        """
        
        # Mathematical terms and symbols for domain-specific analysis
        self.math_terms = {
            'basic': set(['sum', 'difference', 'product', 'quotient', 'equals']),
            'intermediate': set(['derivative', 'integral', 'function', 'polynomial', 'equation']),
            'advanced': set(['theorem', 'proof', 'lemma', 'corollary', 'axiom'])
        }
        
        self.math_symbols = {
            'basic': set(['+-*/=']),
            'intermediate': set(['∑∫≠≈≤≥']),
            'advanced': set(['∏∆∇∀∃'])
        }
    
    def _calculate_text_entropy(self, text: str) -> float:
        """
        Calculate the Shannon entropy of text as a measure of complexity.
        """
        if not text:
            return 0.0
        
        # Count character frequencies
        freq_dict = defaultdict(int)
        for char in text:
            freq_dict[char] += 1
            
        # Calculate probabilities
        length = len(text)
        probabilities = [count/length for count in freq_dict.values()]
        
        return entropy(probabilities)
    
    def _analyze_creativity(self, response: str) -> Dict[str, Any]:
        """
        Enhanced creativity analysis with additional metrics.
        """
        # Previous metrics
        approach_indicators = ["alternatively", "another way", "we could also", "different approach"]
        unique_approaches = sum(1 for indicator in approach_indicators if indicator.lower() in response.lower())
        
        # New metrics
        words = word_tokenize(response)
        pos_tags = nltk.pos_tag(words)
        
        # Analyze variety in sentence structure
        sentences = TextBlob(response).sentences
        sentence_lengths = [len(str(sentence).split()) for sentence in sentences]
        length_variety = np.std(sentence_lengths) if sentence_lengths else 0
        
        # Calculate linguistic diversity
        unique_word_ratio = len(set(words)) / len(words) if words else 0
        
        # Analyze metaphorical language
        metaphor_indicators = ["like", "as", "similar to", "metaphorically"]
        metaphor_count = sum(1 for indicator in metaphor_indicators if indicator.lower() in response.lower())
        
        return {
            "unique_approaches": unique_approaches,
            "sentence_variety": length_variety,
            "linguistic_diversity": unique_word_ratio,
            "metaphor_usage": metaphor_count,
            "creativity_score": (
                unique_approaches * 0.3 +
                min(length_variety / 10, 1) * 0.2 +
                unique_word_ratio * 0.3 +
                min(metaphor_count / 3, 1) * 0.2
            )
        }
    
    def _analyze_complexity(self, response: str) -> Dict[str, Any]:
        """
        Enhanced complexity analysis with advanced metrics.
        """
        words = word_tokenize(response)
        pos_tags = nltk.pos_tag(words)
        
        # Lexical density
        content_words = [word for word, tag in pos_tags if tag.startswith(('N', 'V', 'J', 'R'))]
        lexical_density = len(content_words) / len(words) if words else 0
        
        # Syntactic complexity
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # Information entropy
        text_entropy = self._calculate_text_entropy(response)
        
        # Technical language analysis
        technical_patterns = [
            r'\b[A-Z][a-z]+ (theorem|law|principle)\b',
            r'\b\w+tion\b',
            r'\b\w+ism\b',
            r'\b\w+ology\b'
        ]
        technical_terms = sum(len(re.findall(pattern, response)) for pattern in technical_patterns)
        
        return {
            "lexical_density": lexical_density,
            "avg_word_length": avg_word_length,
            "information_entropy": text_entropy,
            "technical_term_count": technical_terms,
            "complexity_score": (
                lexical_density * 0.3 +
                (avg_word_length / 10) * 0.2 +
                (text_entropy / 5) * 0.3 +
                min(technical_terms / 5, 1) * 0.2
            )
        }
    
    def _analyze_sentiment(self, response: str) -> Dict[str, Any]:
        """
        Analyze sentiment and confidence levels in responses.
        """
        # Overall sentiment analysis
        blob = TextBlob(response)
        sentiment = blob.sentiment
        
        # Confidence indicators
        confidence_boosters = ["certainly", "definitely", "clearly", "obviously", "without doubt"]
        confidence_hedges = ["perhaps", "maybe", "might", "could", "possibly"]
        
        confidence_score = (
            sum(1 for word in confidence_boosters if word in response.lower()) -
            sum(1 for word in confidence_hedges if word in response.lower())
        )
        
        # Analyze certainty in mathematical statements
        certainty_patterns = [
            r'\b(proves?|shows?|demonstrates?)\b',
            r'\b(therefore|thus|hence)\b',
            r'\b(must|always|never)\b'
        ]
        certainty_count = sum(len(re.findall(pattern, response, re.IGNORECASE)) for pattern in certainty_patterns)
        
        return {
            "polarity": sentiment.polarity,
            "subjectivity": sentiment.subjectivity,
            "confidence_level": min(max(confidence_score / 3, -1), 1),
            "certainty_indicators": certainty_count,
            "sentiment_score": (
                (sentiment.polarity + 1) * 0.3 +  # Normalize to 0-1
                (1 - sentiment.subjectivity) * 0.3 +  # Prefer objective statements
                (confidence_score / 5 + 1) * 0.2 +  # Normalize to 0-1
                min(certainty_count / 5, 1) * 0.2
            )
        }
    
    def _analyze_mathematical_rigor(self, response: str) -> Dict[str, Any]:
        """
        Analyze mathematical reasoning and rigor.
        """
        # Count mathematical symbols by complexity level
        symbol_counts = {
            level: sum(1 for symbol in symbols for char in response if char in symbol)
            for level, symbols in self.math_symbols.items()
        }
        
        # Count mathematical terms by complexity level
        term_counts = {
            level: sum(1 for term in terms if term in response.lower())
            for level, terms in self.math_terms.items()
        }
        
        # Analyze logical structure
        logical_patterns = {
            'if_then': len(re.findall(r'\bif\b.*\bthen\b', response, re.IGNORECASE)),
            'because': len(re.findall(r'\bbecause\b', response, re.IGNORECASE)),
            'therefore': len(re.findall(r'\btherefore\b|\bhence\b|\bthus\b', response, re.IGNORECASE))
        }
        
        # Check for step-by-step solutions
        step_indicators = len(re.findall(r'\b(step|first|second|third|finally)\b', response, re.IGNORECASE))
        
        # Calculate overall mathematical complexity score
        math_complexity = (
            sum(symbol_counts.values()) * 0.3 +
            sum(term_counts.values()) * 0.3 +
            sum(logical_patterns.values()) * 0.2 +
            step_indicators * 0.2
        )
        
        return {
            "symbol_usage": symbol_counts,
            "term_usage": term_counts,
            "logical_structure": logical_patterns,
            "solution_steps": step_indicators,
            "math_rigor_score": min(math_complexity / 10, 1)  # Normalize to 0-1
        }

    def analyze_response(self, response: str, responses_at_temp: List[str] = None) -> Dict[str, Any]:
        """
        Perform comprehensive qualitative analysis on a single response.
        """
        analysis = {}
        
        # Individual response characteristics
        for characteristic, analyzer in self.response_characteristics.items():
            if characteristic != "style_consistency":
                analysis[characteristic] = analyzer(response)
        
        # Style consistency (if multiple responses provided)
        if responses_at_temp:
            analysis["style_consistency"] = self._analyze_style_consistency(responses_at_temp)
            
        return analysis

    def generate_qualitative_report(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate a comprehensive qualitative analysis report with enhanced metrics.
        """
        qualitative_results = []
        
        for temp in results_df['temperature'].unique():
            temp_responses = results_df[results_df['temperature'] == temp]
            responses_list = temp_responses['response'].tolist()
            
            # Aggregate analyses for this temperature
            aggregated_analysis = defaultdict(list)
            
            for response in responses_list:
                analysis = self.analyze_response(response, responses_list)
                
                for characteristic, metrics in analysis.items():
                    if isinstance(metrics, dict):
                        for metric_name, value in metrics.items():
                            if isinstance(value, (int, float)):
                                aggregated_analysis[f"{characteristic}_{metric_name}"].append(value)
                            elif isinstance(value, dict):
                                for sub_name, sub_value in value.items():
                                    aggregated_analysis[f"{characteristic}_{metric_name}_{sub_name}"].append(sub_value)
            
            # Calculate averages and add temperature
            averaged_analysis = {
                key: np.mean(values) for key, values in aggregated_analysis.items()
            }
            averaged_analysis['temperature'] = temp
            qualitative_results.append(averaged_analysis)
        
        return pd.DataFrame(qualitative_results)

    def _generate_analysis_visualizations(self, analysis_df: pd.DataFrame, output_dir: Path, category: str):
        """
        Generate enhanced visualizations for the qualitative analysis results.
        """
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        plt.style.use('seaborn')
        
        # 1. Overall Scores Comparison
        plt.figure(figsize=(12, 6))
        score_columns = [col for col in analysis_df.columns if col.endswith('_score')]
        for col in score_columns:
            plt.plot(analysis_df['temperature'], analysis_df[col], marker='o', label=col.replace('_score', ''))
        plt.xlabel('Temperature')
        plt.ylabel('Score')
        plt.title(f'Quality Metrics vs Temperature - {category}')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_dir / f"{category}_quality_metrics.png")
        plt.close()
        
        # 2. Mathematical Rigor Analysis
        plt.figure(figsize=(12, 6))
        math_columns = [col for col in analysis_df.columns if col.startswith('mathematical_rigor_')]
        for col in math_columns:
            plt.plot(analysis_df['temperature'], analysis_df[col], marker='o', label=col.replace('mathematical_rigor_', ''))
        plt.xlabel('Temperature')
        plt.ylabel('Score')
        plt.title(f'Mathematical Rigor Analysis - {category}')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_dir / f"{category}_math_rigor.png")
        plt.close()
        
        # 3. Sentiment and Confidence Analysis
        plt.figure(figsize=(12, 6))
        sentiment_columns = [col for col in analysis_df.columns if col.startswith('sentiment_')]
        for col in sentiment_columns:
            plt.plot(analysis_df['temperature'], analysis_df[col], marker='o', label=col.replace('sentiment_', ''))
        plt.xlabel('Temperature')
        plt.ylabel('Score')
        plt.title(f'Sentiment and Confidence Analysis - {category}')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_dir / f"{category}_sentiment.png")
        plt.close()

    def save_analysis(self, analysis_df: pd.DataFrame, output_dir: Path, category: str):
        """
        Save the enhanced qualitative analysis results and visualizations.
        """
        output_dir.mkdir(exist_ok=True)
        
        # Save detailed CSV
        analysis_df.to_csv(output_dir / f"{category}_qualitative_analysis.csv", index=False)
        
        # Generate summary statistics
        summary_stats = analysis_df.describe()
        summary_stats.to_csv(output_dir / f"{category}_summary_statistics.csv")
        
        # Generate visualizations
        self._generate_analysis_visualizations(analysis_df, output_dir, category)
    
