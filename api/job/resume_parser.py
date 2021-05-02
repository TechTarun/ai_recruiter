from docx import Document

BASE_PATH = 'ai_recruiter/api/resumes/'

def read_docx_resume(resume):
  resume_path = BASE_PATH + resume
  content = ""
  document = Document(resume_path)
  for p in document.paragraphs:
    text = p.text.replace('\n', ' ')
    content += text
    content += " "
  return content

def read_txt_resume(resume):
  resume_path = BASE_PATH + resume
  fobj = open(resume_path)
  content = fobj.read().replace("\n", " ")
  return content