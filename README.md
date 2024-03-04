# Datahouse-Consulting-Compatibility-Predictor
This is a predictor that predict compatibility between applicants and existing team members.

## Input
The predictor takes a json file as input. The json file should store a dictionary object that include keys "team" and "applicants".
Under "team" and "applicants", each individual should be stored as a dictionary object with keys "name" and "attributes".
Under the "attributes" key, the score for each of the following attributes should be stored: 'Endurance', 'Intelligence', 'Leadership', 'Strength', 'SpicyFoodTolerance', and 'Extroversion'.

## Output
The output will be a json file storing applicants' outcome compatibility score. Specifically, it will store a dictionary object with one key: "scoredApplicants". Under this key, the dictionary will store the list of applicants, with their respective name and compatibility score.

The compatibility score is generated considering the following three factors: 
  1. For each attribute, do we the team value it as crucial or just good to have?
  2. For each attribute, do we want new applicants to be similar to or different from our current team member?
  3. For each attribute, are our current team members polarized on this attribute?


