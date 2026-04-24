import unittest
from unittest.mock import Mock
from app.models.base import Scorer
from app.models.baseline_scorer import BaselineScorer
from app.models.types import ScorerOutput


class TestScorerInterface(unittest.TestCase):
    
    def test_scorer_is_abstract(self):
        """Test that Scorer is an abstract base class"""
        self.assertTrue(Scorer.__abstractmethods__)
        
    def test_baseline_scorer_conforms_to_interface(self):
        """Test that BaselineScorer implements the Scorer interface"""
        scorer = BaselineScorer()
        
        # Test that it has the required method
        self.assertTrue(hasattr(scorer, 'score'))
        
        # Test that it can be called
        result = scorer.score({'test': 'data'})
        
        # Test that it returns the expected type
        self.assertIsInstance(result, dict)
        self.assertIn('score', result)
        self.assertIn('confidence', result)
        self.assertIn('explanation', result)
        
        # Test that the values are of expected types
        self.assertIsInstance(result['score'], float)
        self.assertIsInstance(result['confidence'], (float, type(None)))
        self.assertIsInstance(result['explanation'], (str, type(None)))


class TestBaselineScorer(unittest.TestCase):
    
    def test_baseline_scorer_returns_valid_output(self):
        """Test that BaselineScorer returns valid output"""
        scorer = BaselineScorer()
        
        # Test with different inputs
        test_inputs = [
            'test_string',
            42,
            {'key': 'value'},
            [1, 2, 3]
        ]
        
        for test_input in test_inputs:
            with self.subTest(input=test_input):
                result = scorer.score(test_input)
                
                # Verify the structure
                self.assertIsInstance(result, ScorerOutput)
                self.assertIsInstance(result['score'], float)
                self.assertGreaterEqual(result['score'], 0.0)
                self.assertLessEqual(result['score'], 1.0)
                self.assertIsInstance(result['confidence'], (float, type(None)))
                self.assertIsInstance(result['explanation'], (str, type(None)))

if __name__ == '__main__':
    unittest.main()
