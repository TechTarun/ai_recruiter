"""
Here we will define the algorithm that will create the visualization using the parsed data
@params
1. job_requirement_object : Dictionary of all the requirements needed for the job
                            This may involves - 
                            * List of required skills
                            * Experience needed in each skill(future scope)
                            * Some other eligibility criteria(to be applied to filter out candidates)
2. candidate_parsed_data_json_list : List of JSON-format parsed data of candidates

@output
series = [
  {
    "name" : "skill 1",
    "data" : [] # list of scores of that skill for all candidates
  },
  {},
  {}
],
candidate_list = [] # list of names of all candidates
"""

# Imports
import textdistance
from preprocess_string import PreProcessor
from crawl_job_desc import get_job_desc
from resume_parser import *
from data import *
from utilities import stringify_parsed_resume_json

# Constants
JOB_URL = 'https://www.amazon.jobs/en/jobs/1227693/software-development-engineer-intern'

# Code
def check_similarity_score(job_desc, parsed_resume):
  # STEP 1 - PreProcess job description and parsed_resume to get clean token lists
  prep = PreProcessor()
  ## Preprocessing job description
  raw_tokens = prep.tokenize(job_desc)
  cleaned_tokens = prep.filter_out('total', raw_tokens)
  job_token_list = prep.downcase_to_set(cleaned_tokens)
  ## Preprocesing parsed resume
  raw_tokens = prep.tokenize(parsed_resume)
  cleaned_tokens = prep.filter_out('total', raw_tokens)
  resume_token_list = prep.downcase_to_set(cleaned_tokens)

  # STEP 2 - Get similarity between resume and job description (Needs analysis)
  ## Using Jaccard Index
  jacc_similarity_score = textdistance.jaccard.similarity(job_token_list, resume_token_list)
  print(jacc_similarity_score)
  ## Using Sorenson-Dice Coefficient
  sor_dice_similarity_score = textdistance.sorensen_dice.similarity(job_token_list, resume_token_list)
  print(sor_dice_similarity_score)
  ## Using Tversky Index
  tversky_similarity_score = textdistance.tversky.similarity(job_token_list, resume_token_list)
  print(tversky_similarity_score)
  ## Using Cosine Similarity
  cosine_similarity_score = textdistance.cosine.similarity(job_token_list, resume_token_list)
  print(cosine_similarity_score)
  print("=============")

def get_empty_skills_score_list(skills):
  skills_dict = {}
  for skill in skills:
    skills_dict[skill] = []
  return skills_dict

def format_output(skills_score_dict, skills):
  result = []
  for skill in skills:
    result.append({
      "name" : skill,
      "data" : skills_score_dict[skill]
    })
  return result

def create_visualization(parsed_resumes_list, job_skills):
  # TODO - ensure uniqueness of resume for an applicant for a job
  SKILLS_SCORE_DICT = get_empty_skills_score_list(job_skills)
  CANDIDATE_LIST = []
  for resume in parsed_resumes_list:
    CANDIDATE_LIST.append(resume["parsedData"]["parts"]["name"])
    resume_data = stringify_parsed_resume_json(resume)
    for skill in job_skills:
      SKILLS_SCORE_DICT[skill].append(resume_data.count(skill))

  result = format_output(SKILLS_SCORE_DICT, job_skills)
  return [result, CANDIDATE_LIST]

#
# main section
job_desc = get_job_desc(JOB_URL)
parsed_resumes = get_parsed_data()
for resume in parsed_resumes["data"]:
  resume_data = stringify_parsed_resume_json(resume)
  check_similarity_score(job_desc, resume_data)
# job_desc = read_docx_resume('jd1.docx')
#

