from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
import os
import datetime as dt
from api.models import *
from api.job.utilities import *
from api.job.visualization import *

class Index(APIView):
  def post(self, request):
    obj_array = list()
    params = request.data
    hr_id = get_unhashed_id(params['id'])
    skills_array = lowercase_array(params.get('skills'))
    # add eligibility to job object if present
    eligibility = ""
    if params["eligibility"] is not None:
      for (k, v) in params["eligibility"].items():
        eligibility += "{0}=>{1}&".format(k, v)
    try:
      hr = HR.objects.get(id=hr_id)
      company = hr.company
      job = Job(
        profile=params.get('profile'),
        description=params.get('description'),
        qualifications='<>'.join(params.get('qualifications')),
        hr_posted=hr,
        company=company,
        eligibility=eligibility
      )
      obj_array.append(job)
      for skill in skills_array:
        skill_obj = check_if_exists_or_add_new(skill)
        map_obj = Job_Skill_Map(job=job, skill=skill_obj)
        obj_array.append(map_obj)
      commit(obj_array)
      return Response({
        "status" : HTTP_201_CREATED,
        "message" : "Job posted",
        "data" : {
          "id" : get_hashed_id(job.id, "job")
        }
      })
    except:
      rollback(obj_array)
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "Some error occured"
      })

  def get(self, request, **kwargs):
    params = kwargs
    j_id = get_unhashed_id(params["id"])
    try:
      job = Job.objects.get(id=j_id)
      return Response({
        "status" : HTTP_200_OK,
        "data" : {
          "profile" : job.profile,
          "company" : job.company.name,
          "hr" : job.hr_posted.name,
          "description" : job.description,
          "qualifications" : job.qualifications.split('<>'),
          "posted_on" : get_string_time(job.posted_on),
          "eligibility" : get_eligibility_dict(job.eligibility),
          "candidates_count" : get_candidates_count(job),
          "candidates_applied" : get_job_candidates(job),
          "skills" : get_job_skills(job)
        }
      })
    except:
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "job not found"
      })

  def delete(self, request):
    params = request.data
    j_id = int(params.get("id").split("_")[1], 16)
    try:
      job = Job.objects.get(id=j_id)
      job.delete()
      return Response({
        "status" : HTTP_200_OK,
        "message" : "Job deleted"
      })
    except:
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "Job not found or cannot be deleted"
      })

  def put(self, request):
    params = request.data
    j_id = int(params.get("id").split("_")[1], 16)
    try:
      job = Job.objects.get(id=j_id)
      job.description = params.get('description')
      job.qualifications = '<>'.join(params.get('qualifications'))
      job.save()
      return Response({
        "status" : HTTP_200_OK,
        "message" : "Job data updated"
      })
    except:
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "Job not found or cannot be updated"
      })

class All(APIView):
  def get(self, request):
    job_list = list()
    jobs = list(Job.objects.all())
    for job in jobs:
      job_list.append({
        "id" : "JOB_{id}".format(id=hex(job.id)),
        "profile" : job.profile,
        "description" : job.description,
        "qualifications" : job.qualifications,
        "company" : job.company.name,
        "posted_on" : job.posted_on,
        "eligibility" : get_eligibility_dict(job.eligibility),
        "candidates_applied" : get_candidates_count(job)
      })
    return Response({
      "status" : HTTP_200_OK,
      "data" : job_list
    })

class Filter(APIView):
  def post(self, request):
    params = request.data
    hr_email = params["email"]
    hr = HR.objects.get(email=hr_email)
    jobs = list(Job.objects.filter(hr_posted=hr))
    job_list = list()
    for job in jobs:
      job_list.append({
        "id" : get_hashed_id(job.id, "job"),
        "profile" : job.profile,
        "description" : job.description,
        "qualifications" : job.qualifications,
        "posted_on" : job.posted_on,
        "eligibility" : get_eligibility_dict(job.eligibility),
        "candidates_applied" : get_candidates_count(job)
      })
    hr_details = {
      "id" : "HR_{id}".format(id=hex(hr.id)),
      "name" : hr.name
    }
    return Response({
      "data" : {
        "hr" : hr_details,
        "jobs" : job_list
      }
    })

class Visualization(APIView):
  # this method will return data for creating visualization
  def get(self, request, **kwargs):
    job_id = get_unhashed_id(kwargs["id"])
    job_vis = JobVisualizer.objects.get(id=job_id)
    series_data = get_series_data_list_from_str(job_vis.series_data)
    candidate_list = job_vis.candidate_list.split("&")
    return Response({
      "data" : {
        "series" : series_data,
        "candidates" : candidate_list
      }
    })
    
  # this method will update the visualization and then return data for creating visualization
  def post(self, request):
    params = request.data
    job_id = get_unhashed_id(params["id"])
    job = Job.objects.get(id=job_id)
    skill_obj_list = list(Job_Skill_Map.objects.filter(job=job))
    job_skills = [skill_obj.skill for skills_obj in skill_obj_list]
    parsed_resumes = api_call(parsed_resumes_fetch_api, job_id)
    series_data, candidate_list = create_visualization(parsed_resumes["data"], job_skills)
    job_vis = JobVisualizer(
      job=job, 
      series_data=convert_series_data_list_to_str(series_data), 
      candidate_list="&".join(candidate_list)
    )
    job_vis.save()
    return Response({
      "message" : "Visualization updated",
      "data" : {
        "series" : series_data,
        "candidates" : candidate_list
      }
    })

class Interview(APIView):
  def post(self, request):
    params = request.data
    app_id = params["id"]
    application = Job_Candidate_Map(id=app_id)
    interview_answers = InterviewAnswer(
      belong_to=application, 
      ans1=params["ans1"], 
      ans2=params["ans2"], 
      ans3=params["ans3"], 
      ans4=params["ans4"], 
      ans5=params["ans5"])
    interview_answers.save()
    return Response({
      "status" : HTTP_200_OK,
      "message" : "Answers saved successfully..."
    })

  def get(self, request, **kwargs):
    params = kwargs
    return Response({
      "data" : interview_questions()
    })

class EvaluatePersonality(APIView):
  def post(self, request):
    # calls for evaluation of a new candidate
    pass

  def get(self, request, **kwargs):
    # returns personality evaluation of a candidate
    params = request.data
    app_id = params["id"]
    application = Job_Candidate_Map(id=app_id)

class Apply(APIView):
  parser_classes = (MultiPartParser,)
  BASE_PATH = "api/job/tmp/"

  def save_to_disk(self, resume, filepath):
    with open(filepath, "wb+") as destination:
      for chunk in resume.chunks():
        destination.write(chunk)

  def post(self, request):
    params = request.data
    files = request.FILES

    # take params and create new application
    cand_id = params["cand_id"]
    job_id = get_unhashed_id(params["job_id"])
    candidate = Candidate.objects.get(id=cand_id)
    job = Job.objects.get(id=job_id)
    new_application = Job_Candidate_Map(job=job, candidate=candidate)
    new_application.save()

    # take resume, save it, parse it, remove it
    resume = files["resume"]
    filename = resume.name
    filepath = self.BASE_PATH + filename
    self.save_to_disk(resume, filepath)
    response_code = parse_resume(filepath, get_hashed_id(new_application.id, "application"))
    os.remove(filepath)
    if response_code == 503:
      new_application.delete()
      return Response({
        "status" : HTTP_503_SERVICE_UNAVAILABLE,
        "message" : "Try again in sometime..."
      })

    # add new event
    event = ProgressEvent(belong_to=new_application, key=0)
    event.save()

    # return response
    return Response({
      "status" : HTTP_200_OK,
      "message" : "Application saved...",
      "data" : {
        "id" : get_hashed_id(new_application.id, "application")
      }
    })
