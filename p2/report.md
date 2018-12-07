# Introduction
In this project we were asked to develop an expert system in CLIPS to determine the illness probabilites of various patients. 
We were asked to use naive bayes algorithm to calculate the probabilities of the illnesses. I wasn't familiar with the CLIPS so I read the documentation first.
It was similar to prolog that we have used in some other course. The difference between them is prolog uses backward chaining and clips uses forward chaining to assert new facts.
# Languages & How to Run
I have used python to read the input files and construct the clips code to assert the facts to the knowledge base.

# Knowledge Base - Initial Facts
My knowledge base includes the following initial facts:

* (illness illness_name initial_probability)
* (symptom symptom_id illness_name saying_yes_probabilty_with_illness saying_yes_probabilty_without_illness)
* (patient-said patient_id symptom_id answer)

These were my initial facts that I have read from the input files via python. I have read the files via python and created the knowledge base via python. 
But all the inferences and other fact derivations are made by the   CLIPS code. I will explain the rules as we go along.
