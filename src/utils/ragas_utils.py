"""
RAGAS evaluation utility functions for RAG pipeline assessment.

This module provides reusable functions for running RAGAS evaluations
on different retrieval chains and comparing their performance.
"""

from typing import List, Dict, Any, Optional
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness, answer_relevancy, context_precision, context_recall,
    answer_correctness, context_entity_recall
)
from src.utils.config import get_model_factory
import pandas as pd


def run_ragas_evaluation(evaluation_data: List[Dict[str, Any]], chain_name: str = "retriever") -> Optional[Dict[str, Any]]:
    """
    Run RAGAS evaluation on evaluation data and return results with summary statistics.
    
    Args:
        evaluation_data: List of evaluation data with RAGAS field names
        chain_name: Name of the chain being evaluated (for display purposes)
        
    Returns:
        Dictionary containing evaluation results and summary statistics, or None if error
    """
    
    print(f"\n{'='*80}")
    print(f"RAGAS EVALUATION RESULTS - {chain_name.upper()}")
    print(f"{'='*80}")
    
    # Convert to HuggingFace Dataset format for RAGAS
    print("Converting to RAGAS evaluation format...")
    eval_dataset = Dataset.from_list(evaluation_data)
    
    print(f"Evaluation dataset created with {len(eval_dataset)} samples")
    
    # Define metrics - enhanced for SRE use case
    metrics = [
        faithfulness,              # Measures factual consistency of generated answer
        answer_relevancy,         # Measures how relevant the answer is to the question  
        context_precision,        # Measures precision of retrieved contexts
        context_recall,           # Measures recall of retrieved contexts
        answer_correctness,       # Measures correctness against ground truth (SRE critical)
        context_entity_recall     # Measures recall of specific entities/commands (SRE critical)
    ]
    
    # Run evaluation
    print("\nRunning RAGAS evaluation metrics...")
    print("This may take a few minutes...")
    
    try:
        # Use a more capable model for evaluation (judge) while keeping cost-effective model for generation
        # Get judge LLM from model factory
        judge_llm = get_model_factory().get_judge_llm()
        
        result = evaluate(
            eval_dataset,
            metrics=metrics,
            llm=judge_llm,  # Use dedicated judge LLM
            embeddings=get_model_factory().get_embeddings()
        )
        
        print("✅ RAGAS evaluation completed successfully!")
        
        return {
            'result': result,
            'chain_name': chain_name,
            'eval_dataset': eval_dataset
        }
        
    except Exception as e:
        print(f"❌ Error during RAGAS evaluation: {e}")
        return None


def process_ragas_results(evaluation_results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Process and display RAGAS evaluation results with summary statistics.

    Args:
        evaluation_results: Raw results from run_ragas_evaluation

    Returns:
        Dictionary containing processed results and summary statistics, or None if error
    """
    if not evaluation_results:
        print("❌ No evaluation results to process")
        return None

    try:
        result = evaluation_results['result']
        chain_name = evaluation_results['chain_name']
        
        print(f"\n📊 PROCESSING RESULTS FOR {chain_name.upper()}")
        print("=" * 60)

        # Convert EvaluationResult to pandas DataFrame for analysis
        df = result.to_pandas()

        # Calculate summary statistics - only process actual RAGAS metrics
        actual_metrics = [
            'faithfulness', 'answer_relevancy', 'context_precision', 
            'context_recall', 'answer_correctness', 'context_entity_recall'
        ]
        
        summary_stats = {}
        for metric_name in actual_metrics:
            if metric_name in df.columns:
                values = df[metric_name].dropna()
                
                # Handle cases where values might be lists or complex types
                numeric_values = []
                for val in values:
                    if isinstance(val, (int, float)):
                        numeric_values.append(val)
                    elif isinstance(val, list) and len(val) > 0:
                        # If it's a list, try to extract the first numeric value
                        if isinstance(val[0], (int, float)):
                            numeric_values.append(val[0])
                    elif hasattr(val, 'item'):  # Handle numpy scalars
                        try:
                            numeric_values.append(val.item())
                        except:
                            pass
                
                if numeric_values:
                    numeric_series = pd.Series(numeric_values)
                    summary_stats[metric_name] = {
                        'mean': numeric_series.mean(),
                        'std': numeric_series.std(),
                        'min': numeric_series.min(),
                        'max': numeric_series.max()
                    }
                else:
                    # If no numeric values found, skip this metric
                    print(f"⚠️ Skipping metric {metric_name} - no numeric values found")
                    continue

        # Display results
        print("\n📊 SUMMARY METRICS TABLE:")
        print(f"{'Metric':<20} {'Mean Score':<12} {'Std Dev':<10} {'Min Score':<10} {'Max Score':<10}")
        print("-" * 70)

        for metric_name, stats in summary_stats.items():
            print(f"{metric_name:<20} {stats['mean'] if not pd.isna(stats['mean']) else 'N/A':<12.3f} {stats['std'] if not pd.isna(stats['std']) else 'N/A':<10.3f} {stats['min'] if not pd.isna(stats['min']) else 'N/A':<10.3f} {stats['max'] if not pd.isna(stats['max']) else 'N/A':<10.3f}")

        # Performance interpretation for SRE metrics
        print("\n📈 PERFORMANCE INTERPRETATION:")
        print("-" * 50)

        sre_metrics = [
            'faithfulness', 'answer_relevancy', 'context_precision', 'context_recall',
            'answer_correctness', 'context_entity_recall'
        ]

        for metric in sre_metrics:
            if metric in summary_stats:
                mean_score = summary_stats[metric]['mean']
                if not pd.isna(mean_score):
                    if mean_score >= 0.8:
                        performance = "🟢 Excellent"
                    elif mean_score >= 0.6:
                        performance = "🟡 Good"
                    elif mean_score >= 0.4:
                        performance = "🟠 Fair"
                    else:
                        performance = "🔴 Needs Improvement"
                else:
                    performance = "⚪ N/A (Evaluation incomplete)"

                # Add SRE-specific interpretation
                if metric == 'answer_correctness':
                    print(f"{metric.replace('_', ' ').title()}: {mean_score:.3f} - {performance} (Critical for production)")
                elif metric == 'context_entity_recall':
                    print(f"{metric.replace('_', ' ').title()}: {mean_score:.3f} - {performance} (Command/entity coverage)")
                else:
                    print(f"{metric.replace('_', ' ').title()}: {mean_score:.3f} - {performance}")
            else:
                print(f"{metric.replace('_', ' ').title()}: ⚪ N/A (Metric not evaluated)")

        print(f"\n📋 DETAILED RESULTS ({len(df)} samples):")
        print(df.to_string())

        return {
            'result': result,
            'summary_stats': summary_stats,
            'chain_name': chain_name,
            'dataframe': df
        }

    except Exception as e:
        print(f"❌ Error processing RAGAS results: {e}")
        import traceback
        traceback.print_exc()
        return None


def compare_retriever_performance(results_dict: Dict[str, Dict[str, Any]]) -> None:
    """
    Compare performance of multiple retrievers side by side.
    
    Args:
        results_dict: Dictionary with retriever names as keys and RAGAS results as values
    """
    if not results_dict:
        print("No results to compare")
        return
    
    print(f"\n{'='*100}")
    print("RETRIEVER PERFORMANCE COMPARISON")
    print(f"{'='*100}")
    
    # Get all metrics from the first result
    first_result = next(iter(results_dict.values()))
    metrics = list(first_result['summary_stats'].keys())
    
    # Create comparison table
    print(f"\n{'Metric':<25} {'Retriever':<20} {'Mean Score':<12} {'Performance':<15}")
    print("-" * 80)
    
    for metric in metrics:
        print(f"\n{metric.replace('_', ' ').title()}:")
        for retriever_name, result in results_dict.items():
            if metric in result['summary_stats']:
                mean_score = result['summary_stats'][metric]['mean']
                if mean_score >= 0.8:
                    performance = "🟢 Excellent"
                elif mean_score >= 0.6:
                    performance = "🟡 Good"
                elif mean_score >= 0.4:
                    performance = "🟠 Fair"
                else:
                    performance = "🔴 Needs Improvement"
                
                print(f"{'':<25} {retriever_name:<20} {mean_score:<12.3f} {performance:<15}")
    
    # Overall winner analysis
    print(f"\n🏆 OVERALL WINNER ANALYSIS:")
    print("-" * 50)
    
    retriever_scores = {}
    for retriever_name, result in results_dict.items():
        total_score = sum(result['summary_stats'][metric]['mean'] for metric in metrics)
        avg_score = total_score / len(metrics)
        retriever_scores[retriever_name] = avg_score
    
    sorted_retrievers = sorted(retriever_scores.items(), key=lambda x: x[1], reverse=True)
    
    for i, (retriever, score) in enumerate(sorted_retrievers, 1):
        if i == 1:
            print(f"🥇 {retriever}: {score:.3f} (Best Overall)")
        elif i == 2:
            print(f"🥈 {retriever}: {score:.3f}")
        elif i == 3:
            print(f"🥉 {retriever}: {score:.3f}")
        else:
            print(f"   {retriever}: {score:.3f}")
