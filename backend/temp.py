import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import math
from datetime import datetime, timezone
from random import randint
from IPython.display import clear_output
clear_output(wait=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
    "Referer" :"http://www.google.com/"
}

def scrape_attraction_names(url):

    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    attraction_names = []
    div_tags = soup.findAll('div', class_='XfVdV o AIbhI')

    return div_tags

def scrape_attraction_links(url):

    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    attraction_links = []
    div_tags = soup.findAll('div', class_='alPVI eNNhq PgLKC tnGGX')

    return div_tags

def scrape_attraction_no_reviews(url):

    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    div_tags = soup.find_all('section', {'data-automation': 'WebPresentation_SingleFlexCardSection'})

    return div_tags[:30]

def convert_link_to_pagination_format(link):
    pattern = r'(?<=-oa)\d+(?=-)'

    # Check if the pattern exists in the link
    match = re.search(pattern, link)

    if match:
        # If the pattern exists, replace it with {}
        new_link = re.sub(pattern, '{}', link)
    else:
        # If the pattern doesn't exist, insert -oa{}-
        new_link = re.sub(r'(?<=Activities-)', 'oa{}-', link)

    return new_link

def scrape_breadcrumb(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    div_tag = soup.find('div', {'data-automation': 'breadcrumbs'})

    while div_tag is None:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        div_tag = soup.find('div', {'data-automation': 'breadcrumbs'})

    attraction_names = [a_tag.text.strip() for a_tag in div_tag.find_all('a')]

    return '>'.join(attraction_names)

def convert_headers(headers):
    formatted_headers = {}
    for header in headers:
        key = header['key']
        value = header['value']
        formatted_headers[key] = value
    return formatted_headers

def first_scraper(headers, fetched_link, attractionCount):
#   print(HEADERS)
  headers = convert_headers(headers)
#   if(headers==HEADERS):
#     SCRAPEOPS_API_KEY = '71254d9c-929a-4eb4-ad75-a6968ca4ae20'

#     def get_headers_list():
#         response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + SCRAPEOPS_API_KEY)
#         json_response = response.json()
#         return json_response.get('result', [])
    
#     header_list = get_headers_list()

#     def get_random_header(header_list):
#         random_index = randint(0, len(header_list) - 1)
#         return header_list[random_index]
    
#     HEADERS.update(get_random_header(header_list))

#   else:
  print("")
  HEADERS.update(headers)

  print(HEADERS)
  # Base URL
  attractionCount = int(attractionCount)
  base_url = fetched_link
  base_url = convert_link_to_pagination_format(base_url)

  url = base_url.format(0)
  bread_head= scrape_breadcrumb(url)
  r1 = requests.get(url, headers=HEADERS)
  soup1 = BeautifulSoup(r1.text, 'html.parser')

  number = 0
  div_ci = soup1.find('div', class_='Ci')
  if div_ci:
    content = div_ci.text.strip()
    number = int(re.search(r'\d+$', content).group())
#   print(number, type(number), attractionCount, type(attractionCount))
  if(attractionCount<=0):
      total_pages = math.ceil(number / 30)
  else:
      if number <= attractionCount:
        total_pages = math.ceil(number/30)
      else:
        total_pages = math.ceil(attractionCount/30)

  if not total_pages:
      total_pages=1
  print(total_pages)

  all_attraction_names = []

  for page_number in range(total_pages):
      url = base_url.format(page_number * 30)
      attraction_names = scrape_attraction_names(url)
      while len(attraction_names) == 0:
          attraction_names = scrape_attraction_names(url)
      all_attraction_names.extend(attraction_names)
  print("-----------------")
  all_attraction_no_reviews = []

  for page_number in range(total_pages):
      url = base_url.format(page_number * 30)
      attraction_no_reviews = scrape_attraction_no_reviews(url)
      while len(attraction_no_reviews) == 0:
          attraction_no_reviews = scrape_attraction_no_reviews(url)
      all_attraction_no_reviews.extend(attraction_no_reviews)

#   print("Done2")
  section_texts = []
  ratings = []
  image_links = []
  timeStamp = []

  for section in all_attraction_no_reviews:
      img_tag = section.find('img')
      if img_tag:
          src_value = img_tag.get('src')
          image_links.append(src_value)
      else:
          image_links.append("")

      svg_tag = section.find('svg', class_='UctUV d H0 hzzSG')

      ########
      if svg_tag:
          title_tag = svg_tag.find('title')
          if title_tag:
              title_content = title_tag.get_text()[:3]
              ratings.append(title_content)
          else:
              ratings.append(0)
      else:
          ratings.append(0)

      ########
      span_tag = section.find('span', class_="biGQs _P pZUbB osNWb")
      if span_tag:
          section_texts.append(span_tag.get_text())
      else:
          section_texts.append('0')
      current_utc_time = datetime.now(timezone.utc)
      formatted_time = current_utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
      timeStamp.append(formatted_time)

  names = [attraction.get_text() for attraction in all_attraction_names]
  names_cleaned = [name.split('. ')[1] for name in names]

  all_attraction_links = []

  for page_number in range(total_pages):
      url = base_url.format(page_number * 30)
      attraction_links = scrape_attraction_links(url)
      while len(attraction_links) == 0:
          attraction_links = scrape_attraction_links(url)
      all_attraction_links.extend(attraction_links)

  links = ["https://www.tripadvisor.com" + attraction.find('a')['href'] for attraction in all_attraction_links]

  emails = ['']*len(ratings)
  bread = [bread_head]*len(ratings)
  data = {'name': names_cleaned, 'emails':emails,'image': image_links, 'label': emails, 'phone': emails, 'rating':ratings, 'review_Count':section_texts, 'website': emails, 'breadcrumb':bread,'url':links, 'TimeStamp':timeStamp}
  df = pd.DataFrame(data)

  final_content = []
  for link in links:
    r = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    parent_div_tag = soup.find('div', class_='wgNTK')

    if parent_div_tag:
        div_tag = parent_div_tag.find('div', class_='MJ')
        if div_tag:
            final_content.append(div_tag.get_text(separator=' ', strip=True))
        else:
            final_content.append("")
    else:
        final_content.append("")

  output_list = []

  for link in links:
      try:
          r = requests.get(link, headers=HEADERS)
          soup = BeautifulSoup(r.text, 'html.parser')

          button_tag = soup.find('button', class_='UikNM _G B- _S _W _T c G_ wSSLS wnNQG raEkE')

          if button_tag:
              span_tag = button_tag.find('span')
              if span_tag:
                  output_list.append(span_tag.text.strip())
              else:
                  output_list.append("")
          else:
              output_list.append("")

      except Exception as e:
          print(f"Error processing {link}: {e}")
          output_list.append("")

  for i in range(len(final_content)):
      if final_content[i] == '':
          final_content[i] = output_list[i]
  for i in range(len(final_content)):
      if final_content[i].startswith('Address '):
          final_content[i] = final_content[i][len('Address '):]
  for i in range(len(final_content)):
      if final_content[i].startswith('Call'):
          final_content[i] = final_content[i][len('Call'):]
  for i in range(len(final_content)):
      if final_content[i].startswith('Email'):
          final_content[i] = final_content[i][len('Email'):]
  for i in range(len(final_content)):
      if final_content[i].startswith('Visit website'):
          final_content[i] = final_content[i][len('Visit website'):]

  df.insert(1,'address',final_content)
  print(df.to_json(orient='records'))
  return df.to_json(orient='records')

def name_of_city(headers, fetched_link):
    temp_link = convert_link_to_pagination_format(fetched_link)
    parts = temp_link.split('/')
    city_part = parts[-1]
    city_parts = city_part.split('-')
    city_name = city_parts[4]
    city_name = city_name.split('_')[0]
    print(city_name)
    return {"city_name": city_name}
