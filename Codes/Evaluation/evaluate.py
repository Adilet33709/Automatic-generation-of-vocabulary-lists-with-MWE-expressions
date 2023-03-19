import pandas as pd
from Codes.Evaluation.functions import evaluate




## Get Comprehension and study time results for a given vocabulary list in a form of a dictionary
## Write vocabulary name
x = evaluate(vocabulary="", Levels=["KET", "PET", "FCE", "CAE", "CPE"], Y=80, k = 8598)
print(x)