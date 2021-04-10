from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from api.models import *
import datetime as dt

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
  
class Index(APIView):
  def post(self, request):
    obj_array = list()
    params = request.data
    c_id = int(params.get('c_id').split("_")[1], 16)
    hr_id = int(params.get('hr_id').split("_")[1], 16)
    skills_array = lowercase_array(params.get('skills'))
    try:
      company = Company.objects.get(id=c_id)
      hr = HR.objects.get(id=hr_id)
      job = Job(
        profile=params.get('profile'),
        description=params.get('description'),
        qualifications='<>'.join(params.get('qualifications')),
        hr_posted=hr,
        company=company,
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
          "id" : "JOB_{id}".format(id=hex(job.id))
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
    j_id = int(params["id"].split("_")[1], 16)
    # try:
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
        "candidates_applied" : get_candidates_count(job),
        "skills" : get_job_skills(job)
      }
    })
    # except:
    #   return Response({
    #     "status" : HTTP_400_BAD_REQUEST,
    #     "message" : "job not found"
    #   })

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
        "candidates_applied" : get_candidates_count(job)
      })
    return Response({
      "status" : HTTP_200_OK,
      "data" : job_list
    })