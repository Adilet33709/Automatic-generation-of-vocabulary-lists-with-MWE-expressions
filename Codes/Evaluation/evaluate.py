import pandas as pd
from Codes.Evaluation.functions import evaluate




## This function outputs Comprehension and study time values for a given vocabulary list in a form of a dictionary
## The function takes the following parameters:
## vocabulary: Specifies a name of excel sheet that contains vocabulary to be evaluated
## levels: Specifies which levels needs to be evaluated. Inputs list with names of levels.
## Y: Graduation level
## k: text comprehension parameter
x = evaluate(vocabulary="", levels=["KET", "PET", "FCE", "CAE", "CPE"], Y=80, k = 8598)
