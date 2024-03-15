from feasibilityGPT4 import feasibility_score
from noveltyGPT4 import novelty_score
from validityGPT4 import validity_score

def get_validation(description):
    score = validity_score(description)
    if score == 0: 
        return "no" 
    else: 
        return "yes"


def get_novelty(description):
    score = novelty_score(description)
    return score

def get_feasibility(description):
    score = feasibility_score(description)
    return score 

def check_scores(description):
    valid=get_validation(description)
    novelty=get_novelty(description)
    feasibility=get_feasibility(description)
    return ("valid = " + str(valid) + " | Novelty Score = " + str(novelty) + " | Feasibility Score = " +  str(feasibility))

# description = "A washing machine that is engineered to reuse water used my collecting it and filtering the water to remove impurtities and bacteria using UV and charcoal filters"
# print(check_scores(description))

# description = "A washing machine that uses nuclear power to run"
# print(check_scores(description))
