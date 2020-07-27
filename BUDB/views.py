from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from bs4 import BeautifulSoup,NavigableString


semester_symbols = {'Summer': 'SUMM', 'Fall':'FALL', 'Spring':'SPRING'}
credits_symbols = {'any':'*','0':'0_1','1':'0_1','2':'2','3':'3','4':'4','5+':'5plus'}


# Create your views here.
def index(request):
  return HttpResponse('Hallo')

def api(request, sem, year, **kwargs):

  base = 'https://www.bu.edu/phpbin/course-search/search.php?adv=1&nolog=&search_adv_all='
  keyword = kwargs.get('keyword','').replace('_',' ')
  if keyword == '____':
    keyword = ''


  sem_symbol = semester_symbols[sem]
  credits_symbol = credits_symbols[kwargs.get('credit','any')]



  base = base + keyword + '&yearsem_adv=' + year + '-' + sem_symbol

  if not kwargs.get('school','') == '___':
    base = base + '&college%5B%5D=' + kwargs.get('school','')
  
  url = base + '&credits=' + credits_symbol + '&hub_match=all&pagesize=-1'
  
  major = None
  if not kwargs.get('major','') == '__':
    major = kwargs.get('major','')

  time = set()
  if not kwargs.get('time','') == '_':
    for letter in kwargs.get('time',''):
      time.add(letter)

  optional = None
  if not kwargs.get('condition','') == '':
    optional = kwargs.get('condition','').replace('_',' ')


  return getJson(url, year, sem, major, time, optional)



"""
get the Json result from url as a Dictionary
"""
def getJson(url,  year, sem,  req_major, req_time, optional):
  
  response = requests.get(url)
  data = response.text
  soup = BeautifulSoup(data, 'lxml')

  tags = soup.find_all("li", {"class": "coursearch-result"})
  no = 1
  Dict = dict()
  for tag in tags:
    heading = tag.find("div", {"class": "coursearch-result-heading"})
    
    course_id = heading.find("h6").contents[0]
    school, major, number = course_id.split(' ')
    if (req_major == None) or req_major == major:
      
      course = heading.find("h2")
      text = remove_span(course)
      

      p_s = tag.find('div', {'class':"coursearch-result-content-description" })
      p = remove_span(p_s.find_all('p')[4])

      credit = p_s.find_all('p')[5].contents[0][3]

      href = tag.find('a', {"class": "coursearch-result-sections-link"})
      classes = get_classes('https://www.bu.edu'+href['href'], year, sem, req_time, optional)

      if not classes == {}:
        Dict[no] = {'school':school, 'major':major, 'number':number, 'title':text, 'description':p, 'credit':credit,'classes':classes}
        no += 1
  return JsonResponse(Dict)


## remove span and a
def remove_span(tag):
  for match in tag.findAll('span'):
    match.unwrap()

  for match in tag.findAll('a'):
    match.unwrap()

  text = ""
  for child in tag.children:
    text = text + str(child)
  return text

## get Classes information
def get_classes(url, year, sem, req_time, optional):
  response = requests.get(url)
  data = response.text
  soup = BeautifulSoup(data, 'lxml')
  table_div = soup.find_all('div', {'class':'coursearch-course-section'})

  for div in table_div:
    text = div.find('h4').contents[0].split(' ')
    if text[0] == sem and text[-1] == year:
      table_div_result = div

  table = table_div_result.find('table')

  result = {}
  no = 1
  rows = table.find_all('tr')
  for row in rows[1:]:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    
    if len(cols) < 8:
      no -= 1
      space_index = cols[3].find(' ')
      Time = cols[3][space_index+1:]

      for index in range(space_index):
        result[no]['Schedule'][cols[5][index]] = Time

    else:
      space_index = cols[5].find(' ')
      Time = cols[5][space_index+1:]
      Schedule = dict()
      for index in range(space_index):
        Schedule[cols[5][index]] = Time

      result[no] = {'Instructor': cols[2], 'Type':cols[3], 'Localtion': cols[4],'Schedule':Schedule, 'Dates': cols[6], 'Notes': cols[7]} # Notes: 'Class Closed'/'Class Full'
    no += 1

  """
  Filter the result
  """
  if not optional == None:
    keys = list(result.keys())
    for key in keys:
      if not result[key]['Notes'] == optional:
        result.pop(key)

    
  if not req_time == set():
    keys = list(result.keys())
    for key in keys:
      if not set(result[key]['Schedule'].keys()).issubset(req_time):
        result.pop(key)
  
  """
  reorder result
  """
  Dict = dict()
  no = 1
  for key in result.keys():
    Dict[no] = result[key]
    no += 1


  return Dict

