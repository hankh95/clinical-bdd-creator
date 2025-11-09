import json
import os
from evaluation_framework import GuidelineEvaluator

def test_evaluation_mode():
    """Test the evaluation-only fidelity mode"""
    print('🧪 Testing Evaluation-Only Fidelity Mode')
    print('=' * 40)

    evaluator = GuidelineEvaluator()

    # Test with sample cardiology guideline
    sample_text = '''
    Atrial fibrillation treatment guidelines:
    For patients with atrial fibrillation, anticoagulation therapy is recommended.
    Treatment should include rate control or rhythm control strategies.
    Drug interactions must be monitored, especially with amiodarone.
    Diagnostic tests include ECG and echocardiography.
    Lifestyle modifications and patient education are important.
    Quality metrics should be tracked for anticoagulation control.
    '''

    print('📄 Sample Guideline Text:')
    print(sample_text[:200] + '...')
    print()

    # Run evaluation
    result = evaluator.evaluate_guideline(sample_text)

    print('📊 Evaluation Results:')
    print(f'   Fidelity: {result["fidelity"]}')
    print(f'   Total Scenarios: {result["total_scenarios"]}')
    print(f'   Coverage Score: {result["coverage_score"]:.2f}')
    print()

    print('🎯 Top 5 Category Matches:')
    sorted_matches = sorted(result['category_matches'].items(),
                          key=lambda x: x[1], reverse=True)
    for category, score in sorted_matches[:5]:
        print(f'   {category}: {score:.2f}')

    # Save results
    with open('test_evaluation_results.json', 'w') as f:
        json.dump(result, f, indent=2)

    print()
    print('✅ Evaluation test completed!')
    print('   Results saved to: test_evaluation_results.json')

    return result['coverage_score'] >= 0.1  # More realistic threshold for short sample

if __name__ == '__main__':
    success = test_evaluation_mode()
    exit(0 if success else 1)
