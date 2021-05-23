from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from datetime import datetime
from api.models import *
from api.milestones import milestones_hash

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
    try:
      candidate = Candidate.objects.get(email=email)
      raise ParseError(
        detail="Email ID already registered..."
      )
    except:
      pass
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
            "id" : candidate.id
          }
        })
      else:
        raise ParseError(
          detail="Password is incorrect..."
        )
    except:
      raise ParseError(
        detail="Email ID not registered..."
      )

class AllApplied(APIView):
  def get(self, request, **kwargs):
    applications = []
    params = kwargs
    cand_id = params["app_id"]
    candidate = Candidate.objects.get(id=cand_id)
    all_applications = list(Job_Candidate_Map.objects.filter(candidate=candidate))
    for application in all_applications:
      applications.append({
        "app_id" : application.id,
        "job_id" : application.job.id,
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
    app_id = params["app_id"]
    application = Job_Candidate_Map.objects.get(id=app_id)
    events = get_all_status(application)
    slot = application.interview_slot
    return Response({
      "status" : HTTP_200_OK,
      "data" : {
        "id" : app_id,
        "data" : {
          "events" : events,
          "slot" : slot
        }
      }
    })

class BookSlot(APIView):
  def post(self, request):
    params = request.data
    app_id = params["app_id"]
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