from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from api.models import *

class Index(APIView):
  def post(self, request):
    params = request.data
    company = Company(
      name=params.get('name'),
      contact_email=params.get('email'),
      address=params.get('address'),
      website=params.get('website'),
    )
    try:
      company.save()
      return Response({
        "status" : HTTP_201_CREATED,
        "message" : "Company registered",
        "data" : {
          "id" : "COMP_{id}".format(id=hex(company.id))
        }
      })
    except:
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "Some error occured"
      })

  def get(self, request, **kwargs):
    params = kwargs
    c_id = int(params["id"].split("_")[1], 16)
    try:
      company = Company.objects.get(id=c_id)
      return Response({
        "status" : HTTP_200_OK,
        "data" : {
          "name" : company.name,
          "contact" : company.contact_email,
          "address" : company.address,
          "website" : company.website
        }
      })
    except:
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "Company not found"
      })

  def delete(self, request):
    params = request.data
    c_id = int(params.get("id").split("_")[1], 16)
    try:
      company = Company.objects.get(id=c_id)
      company.delete()
      return Response({
        "status" : HTTP_200_OK,
        "message" : "Company deleted"
      })
    except:
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "Company not found or cannot be deleted"
      })

  def put(self, request):
    params = request.data
    c_id = int(params.get("id").split("_")[1], 16)
    try:
      company = Company.objects.get(id=c_id)
      company.contact_email = params.get('email')
      company.website = params.get('website')
      company.address = params.get('address')
      company.save()
      return Response({
        "status" : HTTP_200_OK,
        "message" : "Company data updated"
      })
    except:
      return Response({
        "status" : HTTP_400_BAD_REQUEST,
        "message" : "Company not found or cannot be updated"
      })