from selenium import webdriver

def get_job_desc(job_url):
  browser = webdriver.Chrome('/home/hardcoderr/Downloads/chromedriver/chromedriver')
  browser.get(job_url)
  job_desc = browser.find_element_by_xpath('//*[@id="job-detail-body"]/div/div[1]/div/div[2]/p').text
  return job_desc.replace("\n", " ")
