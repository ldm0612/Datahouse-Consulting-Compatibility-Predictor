import numpy as np
import json

input_file = #path of the input file#
output_file = #path of the desire output file#

### 1.Read in sample input file.

with open(input_file, 'r') as json_file:
    data = json.load(json_file)

team_members = data['team']
applicants = data['applicants']


### 2. Calculate team average for each attribute. 

# Create a list that stores the attribute scores for all team members
team_attributes= list(member["attributes"] for member in team_members )

# Create the list that contain the names of the attributes
attributes_list=list(team_attributes[1].keys())

# Create the list that contain the mean scores of the attributes
attribute_mean_dict={key: 0 for key in attributes_list}

# Sum up the scores stored in team_attributes previously
for member in team_attributes:
  for attribute, score in member.items():
    attribute_mean_dict[attribute] += score

# Divide the score by the number of team members
for attribute, score in attribute_mean_dict.items():
  attribute_mean_dict[attribute] = score / len(team_attributes)


### 3. Check for polarization for each attribute.

# Create a dictionary that stores the categories of each attribute, including:
#   1. Is this attribute we value the most or is it just good to have
#   2. Do we want to find new applicants that are similar or diverse in this attribute to our team members?
#   3. Are our current team members polarized in this attribute (False by default)
attribute_cat={
  'Endurance': ["Value the most", "Similar", False],
  'Intelligence': ["Value the most", "Similar", False],
  'SpicyFoodTolerance': ["Good to have", "Similar", False],
  'Leadership': ["Value the most", "Diverse", False],
  'Strength': ["Good to have", "Diverse", False],
  'Extroversion': ["Good to have", "Diverse", False]
  }

# This function checks whether our current team members are polarized in an attribute
def check_polar(attributes_cat):

  # If the difference in mean scores is more than 4, than we consider our team to be polarized in this attribute
  polarization_threshold=4

  for attribute in attributes_list:
    # Extract all the score for the attribute from our members
    team_score=[member[attribute] for member in team_attributes]

    # Rank the scores from high to low
    sorted_team_score=sorted(team_score, reverse=True)

    # Find the midpoint score, here we used the floor division
    midpoint = len(sorted_team_score) // 2

    # Finding the mean for the higher half and the lower half
    first_half_mean = np.mean(sorted_team_score[:midpoint])
    second_half_mean = np.mean(sorted_team_score[midpoint:])

    # If the difference between the two means is greater than our set threshold, we mark the attribute as polarized.
    if first_half_mean-second_half_mean > polarization_threshold:
      attributes_cat[attribute][2]=True

  return attributes_cat

# Update our attribute category dictionary
attribute_cat=check_polar(attribute_cat)


### 4. Computing the final score for each applicant

# Here, we use a simple linear interpolation to convert the raw score to the final score
# Our input raw score range from 0 to 10, the raw score comes from the difference between the applicant's score and the team's mean score
# How the output score is generated by the raw score is based on the category of the specific attribute.
# Our output score for "Value the most" attribute range from 0-0.8; output score for "Good to have" attributes range from 0-0.2
def linear_scaling(x, v_or_g, s_or_d, polarized):
    x1 = 0
    x2 = 10
    if v_or_g == "Value the most":
       y1= 0.8
    elif v_or_g == "Good to have":
      y1 = 0.2
    y2 = 0

    if (s_or_d == "Similar" and polarized == False) or (s_or_d == "Diverse" and polarized == True):
      score = y1+((y2-y1)/(x2-x1))*(x-x1)
    elif (s_or_d == "Similar" and polarized == True) or (s_or_d == "Diverse" and polarized == False):
      score = y1-(y1+((y2-y1)/(x2-x1))*(x-x1))
    else:
      print("Error")

    return round(score, 1)

scoredApplicants = []

for applicant in applicants:
  applicant_attributes = applicant["attributes"]

  # Initialize two list to store the scores for "Value the most" attributes and "Good to have" attributes separately
  v_scores=[]
  g_scores=[]

  for attribute, applicant_score in applicant_attributes.items():
    cat=attribute_cat[attribute]
    if cat[1]== "Similar":
      # Sum up the scores generated by our linear interpolation
      v_scores.append(linear_scaling(x=applicant_score, v_or_g=cat[0], s_or_d=cat[1], polarized=cat[2]))
    elif cat[1]== "Diverse":
      g_scores.append(linear_scaling(x=applicant_score, v_or_g=cat[0], s_or_d=cat[1], polarized=cat[2]))
    else:
      print("Error")
      break

  # The final score is the sum of the mean "Value the most" score and the mean "Good to have" score.
  # If the applicant have perfect scores in both fields, then their final score will be 0.8+0.2=1.
  final_score= round(np.mean(v_scores)+np.mean(g_scores), 1)
  scoredApplicants.append({"name" : applicant["name"], "score": final_score})
  output_dict={"scoredApplicants": scoredApplicants}

### 5. Output a JSON file
json_outcome=json.dumps(output_dict)
with open(output_file, 'w') as json_file:
    json_file.write(json_outcome)
