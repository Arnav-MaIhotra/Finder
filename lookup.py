import requests
from bs4 import BeautifulSoup

def radaris(fname, lname):

  rad_info = {}
  
  url = 'https://radaris.com/p/{}/{}'.format(fname, lname)

  response = requests.get(url)

  soup = BeautifulSoup(response.content, 'html.parser')

  profiles = soup.find_all('a', class_='btn rounded-btn btn-primary')
  people = []
  for i in profiles:
    people.append('https://radaris.com' + i['href'])

  for i in people:
    iresponse = requests.get(i)

    isoup = BeautifulSoup(iresponse.content, 'html.parser')
    try:
      info = isoup.find_all('table', class_='profile-teaser-table')
      for j in info:
        rad_info[i + ' quick'] = j.text.replace('\n\n', '\n')
    except:
      None
    media_links = []
    try:
      media_cont = isoup.find('div', class_='mentions-container js-mentions-pos')
  
      socials = media_cont.find_all('div', class_='social')
  
      for j in socials:
        links = j.find_all('a')
        for k in links:
          if k['href'].startswith('http://'):
            media_links.append(k['href'])
    except:
      None
    rad_info[i] = media_links

  return rad_info

def realtyHop(fname, lname):

  real_info = []

  url = 'https://www.realtyhop.com/property-records/search/{}-{}'.format(fname, lname)

  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  try:
    results = soup.find('table', id='property-record-results')
    cont = results.find('td', class_='py-4 td-party-a')
    parties = cont.find('div', class_='font-size-9')
  
    spliced_ind = parties.text.index('Other Parties:')
    return parties.text[0:spliced_ind-1]
  except:
    None


def get_info(fname, lname, lage, hage, state):
  
  real = realtyHop(fname, lname)
  rad = radaris(fname, lname)
  print(real)
  for i in rad:
    for j in range(lage, hage):
      if 'Age:\n{}'.format(j) in rad[i] and state in rad[i]:
        if real:
          return rad[i].replace('[]', '') + real
        else:
          return rad[i].replace("[]", "")
        break


def phone(phone):
  url = 'https://radaris.com/phone/view?phone={}#findPhoneH'.format(phone)
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  try:
    city = soup.find('p', class_="dd-item")
    return city.text
  except Exception as e:
    return e
