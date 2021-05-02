import requests

def get_parsed_data():
  API = "https://resumee-parser.herokuapp.com/api/v1/aiRec/getData"

  payload = {}
  headers = {}

  response = requests.request(
    'GET',
    API,
    headers=headers,
    data=payload
  )

  if response.status_code == 200:
    response = response.json()
    return {
      "data": response["data"],
      "count": len(response["data"])
    }
  else:
    return {
      "data": [],
      "count": 0
    }

get_parsed_data()