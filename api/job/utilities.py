import datetime as dt
from api.models import *

def get_hashed_id(id, model):
  if model == "job":
    return "JOB_{id}".format(id=hex(id))
  elif model == "application":
    return "APP_{id}".format(id=hex(id))

def get_unhashed_id(hashed_id):
  return int(hashed_id.split("_")[1], 16)

def lowercase_array(array):
  lowered_array = [ele.lower() for ele in array]
  return lowered_array

def check_if_exists_or_add_new(skill):
  try:
    skill_obj = Skill.objects.get(skill=skill)
  except:
    skill_obj = Skill(skill=skill)
    skill_obj.save()
  return skill_obj

def get_candidates_count(job):
  return len(list(Job_Candidate_Map.objects.filter(job=job)))

def rollback(obj_array):
  for obj in obj_array:
    obj.delete()

def commit(obj_array):
  for obj in obj_array:
    obj.save()

def get_string_time(time):
  return dt.datetime.strftime(time, "%d/%m/%Y")

def get_job_skills(job):
  map_obj_array = list(Job_Skill_Map.objects.filter(job=job))
  skills = [obj.skill.skill for obj in map_obj_array]
  return skills
  
def get_eligibility_dict(eligibility_str):
  eligibility = dict()
  if eligibility_str is not None:
    eligibility_list = eligibility_str.split("&")
    eligibility_list.pop(-1)
    for criteria_str in eligibility_list:
      criteria = criteria_str.split("=>")
      eligibility[criteria[0]] = criteria[1]
  return eligibility

def get_series_data_list_from_str(series_data_str):
  """
  @params : series_data_str 
  @param_structure : "skill1=>12,23,11&skill2=>23,34,45&"

  @return : series_data_list
  @return structure : [
    {
      "name" : "skill1",
      "data" : [12, 23, 11]
    }
  ]
  """
  series_data_list = []
  series_data_str_list = series_data_str.split("&")
  series_data_str_list.pop(-1) # remove last empty string
  for substr in series_data_str_list:
    substr_list = substr.split("=>")
    series_data_list.append({
      "name" : substr_list[0],
      "data" : substr_list[1].split(",")
    })
  return series_data_list

def convert_series_data_list_to_str(series_data_list):
  """
  @params : series_data_list
  @params structure : [
    {
      "name" : "skill1",
      "data" : [12, 23, 11]
    }
  ]

  @return : series_data_str 
  @return structure : "skill1=>12,23,11&skill2=>23,34,45&"
  """
  series_data_str = ""
  for series_hash in series_data_list:
    series_data_str += "{skill}=>{score_str}".format(
      skill=series_hash["name"], 
      score_str=",".join(series_hash["data"])
    )
  return series_data_str

def stringify_parsed_resume_json(resume):
  skills = resume["parsedData"]["parts"]["skills"]
  projects = resume["parsedData"]["parts"]["projects"]
  education = resume["parsedData"]["parts"]["education"]
  try:
    experience = resume["parsedData"]["parts"]["experience"]
  except:
    experience = ""
  resume_data = "{0} {1} {2} {3}".format(skills, projects, experience, education)
  return resume_data

def get_job_candidates(job):
  candidate_list = list(Job_Candidate_Map.objects.filter(job=job))
  candidate_data = []
  for candidate in candidate_list:
    candidate_data.append({
      "id" : candidate.id,
      "name" : candidate.name,
      "email" : candidate.email
    })
  return candidate_data

def interview_questions():
  return [
    "Question 1",
    "Question 2",
    "Questions 3",
    "Question 4",
    "Questions 5"
  ]