from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *

def get_hashed_id(id):
  return "HR_{id}".format(id=hex(id))

def get_unhashed_id(hashed_id):
  return int(hashed_id.split("_")[1], 16)

class Index(APIView):
  def post(self, request):
    params = request.data
    c_id = get_unhashed_id(params["id"])
    try:
      company = Company.objects.get(id=c_id)
      hr = HR(
        name=params.get("name"),
        email=params.get("email"),
        company=company,
      )
      hr.save()
      return Response({
        "status" : HTTP_201_CREATED,
        "message" : "HR added",
        "data" : {
          "id" : get_hashed_id(hr.id),
        }
      })
    except:
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "Some error occured"
      })

  def get(self, request, **kwargs):
    params=kwargs
    hr_id = get_unhashed_id(params["id"])
    try:
      hr = HR.objects.get(id=hr_id)
      return Response({
        "status" : HTTP_200_OK,
        "data" : {
          "name" : hr.name,
          "email" : hr.email,
          "company" : hr.company.name
        }
      })
    except:
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "HR not found"
      })

  def delete(self, request):
    params=request.data
    hr_id = get_unhashed_id(params["id"])
    try:
      hr = HR.objects.get(id=hr_id)
      hr.delete()
      return Response({
        "status" : HTTP_200_OK,
        "message" : "HR deleted",
      })
    except:
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "HR not found"
      })

  def put(self, request):
    # can be implemented if needed
    pass