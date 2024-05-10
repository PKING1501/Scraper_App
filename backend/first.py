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
import random

# user_agent_list = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0"
# ]


# def generate_headers(user_agent_list):
#     user_agent = random.choice(user_agent_list)

#     headers = {
#         "User-Agent": user_agent,
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Accept-Encoding": "gzip, deflate",
#         "Connection": "keep-alive",
#         "Upgrade-Insecure-Requests": "1",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "none",
#         "Sec-Fetch-User": "?1",
#         "Cache-Control": "max-age=0",
#         "Referer": "http://www.google.com/"
#     }

#     return headers

# HEADERS=generate_headers(user_agent_list)

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

def scrape_attraction_names(soup):

    attraction_names = []
    div_tags = soup.findAll('div', class_='XfVdV o AIbhI')

    return div_tags

def scrape_attraction_links(soup):

    attraction_links = []
    div_tags = soup.findAll('div', class_='alPVI eNNhq PgLKC tnGGX')

    return div_tags

def scrape_attraction_no_reviews(soup):

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
  
  headers = convert_headers(headers)
  HEADERS.update(headers)
  print("")
  print(HEADERS)
  print("")
  attractionCount = int(attractionCount)
  base_url = fetched_link
  base_url = convert_link_to_pagination_format(base_url)

  url = base_url.format(0)
  bread_head= scrape_breadcrumb(url)
  print("Bread success!")
  r1 = requests.get(url, headers=HEADERS)
  soup1 = BeautifulSoup(r1.text, 'html.parser')

  number = 0
  div_ci = soup1.find('div', class_='Ci')
  if div_ci:
      content = div_ci.text.strip()
      last_part = content.split('of')[-1].strip()
      last_part = re.sub(r'<!--(.*?)-->', '', last_part)
      number = int(last_part.replace(',', ''))

  print(number)
  # print(number, type(number), attractionCount, type(attractionCount))
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
  section_texts = []
  ratings = []
  image_links = []
  timeStamp = []
  all_attraction_no_reviews = []
  all_attraction_links = []


  for page_number in range(total_pages):
    # HEADERS=generate_headers(user_agent_list)
    url = base_url.format(page_number * 30)
    soup = None
    while not soup:
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
        else:
            print("Failed to retrieve page. Status code:", r.status_code)
            continue

    attraction_names = scrape_attraction_names(soup)
    all_attraction_names.extend(attraction_names)
    attraction_no_reviews = scrape_attraction_no_reviews(soup)
    all_attraction_no_reviews.extend(attraction_no_reviews)
    attraction_links = scrape_attraction_links(soup)
    all_attraction_links.extend(attraction_links)
    print(page_number)
    # sleep_interval = random.uniform(1, 2)
    time.sleep(1)

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

  links = ["https://www.tripadvisor.com" + attraction.find('a')['href'] for attraction in all_attraction_links]

  emails = ['']*len(ratings)
  bread = [bread_head]*len(ratings)
  data = {'name': names_cleaned, 'emails':emails,'image': image_links, 'label': emails, 'phone': emails, 'rating':ratings, 'review_Count':section_texts, 'website': emails, 'breadcrumb':bread,'url':links, 'TimeStamp':timeStamp}
  df = pd.DataFrame(data)

#   final_content = []
#   for link in links:
#     r = requests.get(link, headers=HEADERS)
#     soup = BeautifulSoup(r.text, 'html.parser')

#     parent_div_tag = soup.find('div', class_='wgNTK')

#     if parent_div_tag:
#         div_tag = parent_div_tag.find('div', class_='MJ')
#         if div_tag:
#             final_content.append(div_tag.get_text(separator=' ', strip=True))
#         else:
#             final_content.append("")
#     else:
#         final_content.append("")
#     time.sleep(1)

#   output_list = []

#   for link in links:
#       try:
#           r = requests.get(link, headers=HEADERS)
#           soup = BeautifulSoup(r.text, 'html.parser')

#           button_tag = soup.find('button', class_='UikNM _G B- _S _W _T c G_ wSSLS wnNQG raEkE')

#           if button_tag:
#               span_tag = button_tag.find('span')
#               if span_tag:
#                   output_list.append(span_tag.text.strip())
#               else:
#                   output_list.append("")
#           else:
#               output_list.append("")

#       except Exception as e:
#           print(f"Error processing {link}: {e}")
#           output_list.append("")
      
#       time.sleep(1)

#   for i in range(len(final_content)):
#       if final_content[i] == '':
#           final_content[i] = output_list[i]
#   for i in range(len(final_content)):
#       if final_content[i].startswith('Address '):
#           final_content[i] = final_content[i][len('Address '):]
#   for i in range(len(final_content)):
#       if final_content[i].startswith('Call'):
#           final_content[i] = final_content[i][len('Call'):]
#   for i in range(len(final_content)):
#       if final_content[i].startswith('Email'):
#           final_content[i] = final_content[i][len('Email'):]
#   for i in range(len(final_content)):
#       if final_content[i].startswith('Visit website'):
#           final_content[i] = final_content[i][len('Visit website'):]

#   df.insert(1,'address',final_content)
#   print(df.to_json(orient='records'))
  print(df.tail())
  print(all_attraction_names)
  print(df.shape)
  return df

def name_of_city(headers, fetched_link):
    temp_link = convert_link_to_pagination_format(fetched_link)
    parts = temp_link.split('/')
    city_part = parts[-1]
    city_parts = city_part.split('-')
    city_name = city_parts[4]
    city_name = city_name.split('_')[0]
    print(city_name)
    return {"city_name": city_name}