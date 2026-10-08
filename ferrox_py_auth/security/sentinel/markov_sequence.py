from typing import List, Dict

class MarkovSequenceDetector:
    """
    Analyzes sequences of events/requests to detect anomalous or bot-like behavior
    using Markov chains.
    """
    def __init__(self, transition_matrix: Dict[str, Dict[str, float]]):
        self.transition_matrix = transition_matrix
        
    def score_sequence(self, sequence: List[str]) -> float:
        """
        Calculates the probability of a given sequence of actions.
        A very low score indicates highly anomalous behavior (potential attack).
        """
        if len(sequence) < 2:
            return 1.0
            
        probability = 1.0
        for i in range(len(sequence) - 1):
            current_state = sequence[i]
            next_state = sequence[i + 1]
            
            transitions = self.transition_matrix.get(current_state, {})
            transition_prob = transitions.get(next_state, 0.01) # Default low probability for unseen transitions
            probability *= transition_prob
            
        return probability
        
    def is_anomalous(self, sequence: List[str], threshold: float = 0.001) -> bool:
        return self.score_sequence(sequence) < threshold
