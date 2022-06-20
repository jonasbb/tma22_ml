import numpy as np
import pandas as pd
from typing import List
from scipy.stats import entropy
from sklearn.base import BaseEstimator

from . import SamplingMethod


class CommitteeDisagreementSampling(SamplingMethod):
    @staticmethod
    def select_batch(pool: pd.DataFrame, nr_samples: int, committee: List[BaseEstimator], **kwargs) -> list:
        
        vote_proba = []
        for member in committee:
            vote_proba.append(member.predict_proba(pool))
        vote_proba = np.array(vote_proba)

        consensus_proba = np.mean(vote_proba, axis=0)

        learner_KL_div = np.empty_like(consensus_proba)
        for i in range(len(consensus_proba)):
            for j in range(consensus_proba.shape[1]):
                learner_KL_div[i, j] = entropy(vote_proba[j, i], qk=consensus_proba[i])

        max_disagreement = pd.Series(np.max(learner_KL_div, axis=1), index=pool.index)
        return max_disagreement.sort_values(ascending=False)[:nr_samples].index
