import requests

def get_all_parsed_resumes():
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

def parse_resume(filepath, job_id):
  API = "https://resumee-parser.herokuapp.com/api/v1/aiRec/postResume"

  payload={'jobId': job_id}
  files=[
    ('tmp',('resume',open(filepath,'rb'),'application/vnd.openxmlformats-officedocument.wordprocessingml.document'))
  ]
  print(files)
  headers = {}

  response = requests.request("POST", API, headers=headers, data=payload, files=files)

  return response.status_code