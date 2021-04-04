from django.db import models

# Create your models here.
from django.db import models

class Entity(models.Model):
  name = models.CharField(max_length=100)
  email = models.CharField(max_length=100)

class Company(models.Model):
  name = models.CharField(max_length=100)
  contact_email = models.CharField(max_length=100)
  address = models.CharField(max_length=1000)
  website = models.CharField(max_length=100)
  def __str__(self):
    return self.name

class HR(Entity):
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  def __str__(self):
    return "{hr_name} ({company_name})".format(hr_name=self.name, company_name=self.company.name)

class Job(models.Model):
  profile = models.CharField(max_length=50)
  description = models.TextField()
  qualifications = models.TextField() # array converted to string
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  hr_posted = models.ForeignKey(HR, on_delete=models.CASCADE)
  posted_on = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return "{profile} ({company_name})".format(profile=self.profile, company_name=self.company.name)

class Candidate(Entity):
  resume = models.CharField(max_length=1000)
  def __str__(self):
    return self.name

class Skill(models.Model):
  skill = models.CharField(max_length=20)
  def __str__(self):
    return self.skill

class Job_Skill_Map(models.Model):
  job = models.ForeignKey(Job, on_delete=models.CASCADE)
  skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
  def __str__(self):
    return "{job} => {skill}".format(job=self.job.profile, skill=self.skill.skill)

class Candidate_Skill_Map(models.Model):
  candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
  skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
  def __str__(self):
    return "{candidate} => {skill}".format(candidate=self.candidate.name, skill=self.skill.skill)

class Job_Candidate_Map(models.Model):
  candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
  job = models.ForeignKey(Job, on_delete=models.CASCADE)
  def __str__(self):
    return "{name} => {job} ({company})".format(name=self.name, job=job.profile, company=job.company.name)

class Experience(models.Model):
  description = models.TextField()
  candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
  job = models.ForeignKey(Job, on_delete=models.CASCADE)
  def __str__(self):
    return "{candidate} => {job}".format(candidate=self.candidate.name, job=self.job.profile)