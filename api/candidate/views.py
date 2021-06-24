from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from datetime import datetime
from api.models import *
from api.milestones import milestones_hash

def get_hashed_id(id, model):
  if model == "job":
    return "JOB_{id}".format(id=hex(id))
  elif model == "application":
    return "APP_{id}".format(id=hex(id))
  elif model  == "candidate":
    return "CAND_{id}".format(id=hex(id))

def get_unhashed_id(hashed_id):
  return int(hashed_id.split("_")[1], 16)

def get_latest_event(application):
  all_events = list(ProgressEvent.objects.filter(belong_to=application))
  if len(all_events) > 0:
    print(all_events)
    all_keys = []
    for event in all_events:
      all_keys.append(event.key)
    print(all_keys)
    latest_key = max(all_keys)
    latest_event = milestones_hash[latest_key]
    return latest_event
  else:
    return ""

def get_all_status(application):
  all_events = list(ProgressEvent.objects.filter(belong_to=application))
  status_data = []
  for event in all_events:
    status_data.append({
      "key" : event.key,
      "event" : milestones_hash[event.key],
      "remarks" : event.remark
    })
  return status_data

class Signup(APIView):
  def post(self, request):
    params = request.data
    name = params["name"]
    email = params["email"]
    password = params["password"]
    candidate = Candidate.objects.filter(email=email).first()
    if candidate:
      raise ParseError(
        detail="Email ID already registered..."
      )
    else:
      new_candidate = Candidate(
        name=name,
        email=email,
        password=password
      )
      new_candidate.save()
      return Response({
        "status" : HTTP_200_OK,
        "message" : "Account registered...",
        "data" : {
          "id" : new_candidate.id
        }
      })

class Login(APIView):
  def post(self, request):
    params = request.data
    email = params["email"]
    password = params["password"]
    try:
      candidate = Candidate.objects.get(email=email)
      if candidate.password == password:
        return Response({
          "status" : HTTP_200_OK,
          "message" : "Login successfully...",
          "data" : {
            "id" : get_hashed_id(candidate.id, "candidate")
          }
        })
      else:
        raise
    except:
      raise ParseError(
        detail="Email ID or password is incorrect..."
      )

class AllApplied(APIView):
  def get(self, request, **kwargs):
    applications = []
    params = kwargs
    cand_id = get_unhashed_id(params["cand_id"])
    candidate = Candidate.objects.get(id=cand_id)
    all_applications = list(Job_Candidate_Map.objects.filter(candidate=candidate))
    for application in all_applications:
      applications.append({
        "app_id" : get_hashed_id(application.id, "application"),
        "job_id" : get_hashed_id(application.job.id, "job"),
        "profile" : application.job.profile,
        "applied_on" : application.applied_on,
        "company" : application.job.company.name,
        "latest_status" : get_latest_event(application)
      })
    return Response({
      "status" : HTTP_200_OK,
      "data" : applications
    })

class AppliedDetails(APIView):
  def get(self, request, **kwargs):
    params = kwargs
    app_id = get_unhashed_id(params["app_id"])
    application = Job_Candidate_Map.objects.get(id=app_id)
    events = get_all_status(application)
    slot = application.interview_slot
    return Response({
      "status" : HTTP_200_OK,
      "data" : {
        "id" : get_hashed_id(app_id, "application"),
        "events_data" : {
          "events" : events,
          "slot" : slot
        }
      }
    })

class BookSlot(APIView):
  def post(self, request):
    params = request.data
    app_id = get_unhashed_id(params["app_id"])
    slot_datetime = params["slot"] # string type date e.g. - Sat, May 15 2021
    application = Job_Candidate_Map.objects.get(id=app_id)
    application.interview_slot = slot_datetime
    application.save()
    event = ProgressEvent(belong_to=application, key=3)
    event.save()
    return Response({
      "status" : HTTP_200_OK,
      "message" : "Personality assessment scheduled..."
    })