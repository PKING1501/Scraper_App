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
from flask_socketio import SocketIO, emit
from flask import Flask, Response, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# result = None

@app.route('/firstScraper', methods=['POST'])
def scraper1():
    emit_progress(0)
    data = request.json
    headers = data.get('headers')
    attractionCount = data.get('attractionCount')
    fetched_link = data.get('urls')
    result = first_scraper(headers, fetched_link, attractionCount)
    # return result
    csv_data = result.to_csv(index=False)
    
    # Set response headers to indicate CSV content
    headers = {
        "Content-Disposition": "attachment; filename=data.csv",
        "Content-Type": "text/csv",
    }
    
    # Return CSV data as a response
    return Response(csv_data, headers=headers)

@app.route('/scraper1name', methods=['POST'])
def nameOfScraper():
    emit_progress(100)
    data = request.json
    headers = data.get('headers')
    fetched_link = data.get('urls')
    result = name_of_city(headers, fetched_link)
    return result

@app.route('/secondScraper', methods=['POST'])
def scraper2():
    emit_progress(0)
    data = request.json
    headers = data.get('headers')
    attractionCount = data.get('attractionCount')
    base_url = data.get('urls')
    result = second_scraper(headers, base_url, attractionCount)
    # return result
    csv_data1 = result.to_csv(index=False)
    
    # Set response headers to indicate CSV content
    headers = {
        "Content-Disposition": "attachment; filename=data1.csv",
        "Content-Type": "text/csv",
    }
    
    # Return CSV data as a response
    return Response(csv_data1, headers=headers)
    
@app.route('/scraper2name', methods=['POST'])
def nameForScraper2():
    emit_progress(100)
    data = request.json
    headers = data.get('headers')
    base_url = data.get('urls')
    result1 = second_scraper_name(headers, base_url)
    return result1

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

def emit_progress(progress_percentage):
    socketio.emit('progress', {'percentage': progress_percentage})

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
        time.sleep(2)

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
  time.sleep(2)
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
            time.sleep(2)
        else:
            print("Failed to retrieve page. Status code:", r.status_code)
            time.sleep(2)
            continue

    attraction_names = scrape_attraction_names(soup)
    all_attraction_names.extend(attraction_names)
    attraction_no_reviews = scrape_attraction_no_reviews(soup)
    all_attraction_no_reviews.extend(attraction_no_reviews)
    attraction_links = scrape_attraction_links(soup)
    all_attraction_links.extend(attraction_links)
    print(page_number)
    # sleep_interval = random.uniform(1, 2)
    progress_percentage = (page_number + 1) / total_pages * 100
    emit_progress(progress_percentage)
    time.sleep(2)

  emit_progress(0)
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










def add_or_param(input_link):
    index = input_link.find('Reviews')
    if index != -1:
        return input_link[:index + len('Reviews')] + '-or{}' + input_link[index + len('Reviews'):]
    else:
        return input_link

def second_scraper(headers, base_url, attractionCount):

    attractionCount = int(attractionCount)
    base_url = add_or_param(base_url)
    headers = convert_headers(headers)
    HEADERS.update(headers)
    timeStamp = []

    def scrape_attraction_name(soup):
        h1_element = soup.find('h1', class_='biGQs _P fiohW eIegw')

        # Extract the text
        if h1_element:
            name = h1_element.text
            return name
        else:
            return "Attraction"
    def extract_rating_from_div_elements(soup):
    # Find all div elements with the specified classes
      div_elements = soup.find_all('div', class_=['wSSLS', 'jVDab o W f u w GOdjs'])

      # Initialize rating to None
      rating = None

      # Iterate through div elements
      for div_element in div_elements:
          # Check if aria-label attribute is present
          if 'aria-label' in div_element.attrs:
              aria_label = div_element['aria-label']
              # Extract the rating from the aria-label attribute
              rating_str = aria_label.split(" ")[0]
              rating = float(rating_str)
              break  # Break out of the loop after finding the first rating

      if rating is None:
          print("Rating not found.")

      return rating

    soup = None
    while not soup:
        r = requests.get(base_url, headers=HEADERS)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            time.sleep(2)
        else:
            print("Failed to retrieve page. Status code:", r.status_code)
            time.sleep(2)
            continue
    name_attraction = scrape_attraction_name(soup)
    print(name_attraction)
    rating = extract_rating_from_div_elements(soup)
    print(rating)



    def scrape_reviews(soup):
        reviews = []
        review_cards = soup.find_all('div', {'data-automation': 'reviewCard'})

        for card in review_cards:
            review_body = card.find('span', class_='JguWG')
            if review_body:
                review_text = review_body.text.strip()
                current_utc_time = datetime.now(timezone.utc)
                formatted_time = current_utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                timeStamp.append(formatted_time)
                reviews.append(review_text)

        return reviews

    def scrape_review_urls(soup):
        reviews = []

        review_cards = soup.find_all('div', {'data-automation': 'reviewCard'})

        for card in review_cards:
            div_tag = card.find('div', class_='biGQs _P fiohW qWPrE ncFvv fOtGX')
            if div_tag:
                a_tag = div_tag.find('a', class_='BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS')
                if a_tag:
                    href = a_tag.get('href')
                    reviews.append(href)
                else:
                    reviews.append('')
            else:
                reviews.append('')

        return reviews

    def scrape_profile_img(soup):
        links = []
        review_cards = soup.find_all('div', {'data-automation': 'reviewCard'})
        for card in review_cards:
            img_tag = card.find('img')
            try:
                src = img_tag.get('src')
            except AttributeError:
                src = ""  # If no img tag found, set src to empty string
            links.append(src)
        return links

    def scrape_review_heading(soup):
        reviews = []

        review_cards = soup.find_all('div', {'data-automation': 'reviewCard'})

        for card in review_cards:
            div_tag = card.find('div', class_='biGQs _P fiohW qWPrE ncFvv fOtGX')
            if div_tag:
                a_tag = div_tag.find('a', class_='BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS')
                if a_tag:
                    span_tag = a_tag.find('span')
                    if span_tag:
                        content = span_tag.text
                        reviews.append(content)
                    else:
                        reviews.append('')
                else:
                    reviews.append('')
            else:
                reviews.append('')
        return reviews

    def scrape_review_contributions(soup):
        reviews = []

        review_cards = soup.find_all('div', {'data-automation': 'reviewCard'})
        for card in review_cards:
            div_tag = card.find('div', class_='biGQs _P pZUbB osNWb')
            if div_tag:
                span_tag = div_tag.find('span', class_='IugUm')
                if span_tag:
                    text_content = span_tag.text
                    match = re.search(r'\d+\s*contributions', text_content)
                    if match:
                        number_of_contributions = int(re.search(r'\d+', match.group()).group())
                        reviews.append(number_of_contributions)
                    else:
                        reviews.append(0)
                else:
                    span_tag = div_tag.find('span')
                    if span_tag:
                        text_content = span_tag.text.strip()
                        match = re.search(r'\d+\s*contributions', text_content)
                        if match:
                            number_of_contributions = int(re.search(r'\d+', match.group()).group())
                            reviews.append(number_of_contributions)
                        else:
                            reviews.append(0)
                    else:
                        reviews.append(0)
            else:
                reviews.append(0)
        return reviews

    def scrape_ratings(soup):
        ratings = []

        # Find the div with class 'LbPSX'
        div_tag = soup.find('div', class_='LbPSX')

        if div_tag:
            # Find all svg tags with the specified class within the div
            rating_tags = div_tag.find_all('svg', class_='UctUV d H0')

            for tag in rating_tags:
                title_tag = tag.find('title')
                if title_tag:
                    rating = title_tag.text.strip()
                    ratings.append(rating)

        return ratings

    def scrape_date_of_stay(soup):
        date_of_stay_list = []

        unique_div = soup.find('div', class_='LbPSX')

        if unique_div:
            tab_divs = unique_div.find_all('div', {'data-automation': 'tab'})
            if(len(tab_divs)>10):
                for div in tab_divs[:10]:
                    rpe_cd_div = div.find('div', class_='RpeCd')
                    if rpe_cd_div:
                        date_of_stay_list.append(rpe_cd_div.text.strip())
                    else:
                        date_of_stay_list.append('')
            else:
                for div in tab_divs[:len(tab_divs)-1]:
                    rpe_cd_div = div.find('div', class_='RpeCd')
                    if rpe_cd_div:
                        date_of_stay_list.append(rpe_cd_div.text.strip())
                    else:
                        date_of_stay_list.append('')
        else:
            return date_of_stay_list

        return date_of_stay_list

    def remove_or_param(url):
        # Find the index of "-or{}" in the URL
        index = url.find("-or{}")
        # If "-or{}" exists, remove it from the URL
        if index != -1:
            url = url[:index] + url[index + len("-or{}"):]
        return url

    all_reviews = []
    review_headings = []
    date_of_stay = []
    review_urls = []
    review_contributions = []
    review_scores = []
    profile_img = []
    name_list = []
    overall_rating = []

    r = requests.get(base_url.format(0), headers=HEADERS)
    time.sleep(2)
    soup = BeautifulSoup(r.text, 'html.parser')
    time.sleep(2)
    number = 0

    lbpsx_div = soup.find('div', class_='LbPSX')
    if lbpsx_div:
        tab_divs = lbpsx_div.find_all('div', {'data-automation': 'tab'})
        if tab_divs:
            last_tab_div = tab_divs[-1]
            ci_div = last_tab_div.find('div', class_='Ci')
            if ci_div:
                text_content = ci_div.get_text()
                last_number = text_content.split()[-1].replace(',', '')
                number = int(last_number)
    
    if(attractionCount<=0):
        total_pages = math.ceil(number / 10)
    else:
        if number <= attractionCount:
            total_pages = math.ceil(number/10)
        else:
            total_pages = math.ceil(attractionCount/10)
    
    if not total_pages:
        total_pages=1
    print("Number: ",number," ",total_pages)

    for page_number in range(total_pages):
        url = base_url.format(page_number * 10)
        soup = None
        while not soup:
            r = requests.get(url, headers=HEADERS)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                time.sleep(2)
            else:
                print("Failed to retrieve page. Status code:", r.status_code)
                time.sleep(2)
                continue

        reviews = scrape_reviews(soup)
        all_reviews.extend(reviews)
        reviews = scrape_review_heading(soup)
        review_headings.extend(reviews)
        reviews = scrape_date_of_stay(soup)
        date_of_stay.extend(reviews)
        reviews = scrape_review_urls(soup)
        review_urls.extend(reviews)
        reviews = scrape_review_contributions(soup)
        review_contributions.extend(reviews)
        review_score = scrape_ratings(soup)
        review_scores.extend(review_score)
        img = scrape_profile_img(soup)
        profile_img.extend(img)
        print(page_number)
        progress_percentage = (page_number + 1) / total_pages * 100
        emit_progress(progress_percentage)
        time.sleep(2)
    
    emit_progress(0)
    review_urls_final = ["https://www.tripadvisor.com"+ link for link in review_urls]

    new_url = remove_or_param(base_url)

    r = requests.get(new_url, headers=HEADERS)
    time.sleep(2)
    soup = BeautifulSoup(r.text, 'html.parser')
    time.sleep(2)
    parts = base_url.split('-')

    g_part = parts[1]
    d_part = parts[2]

    geo_id = [g_part]*len(review_scores)
    hotel_id = [d_part]*len(review_scores)

    div_tag = soup.find('div', {'data-automation': 'poi-jsonld'})
    address = [''] * len(review_scores)
    name_list = [name_attraction] * len(review_scores)
    overall_rating = [rating] * len(review_scores)
    if div_tag:
        script_tag = div_tag.find('script')

        if script_tag:
            script_text = script_tag.text.strip()

            data = json.loads(script_text)

            addressLocality = data['address'].get('addressLocality', '')  # Use get() method with a default value
            addressRegion = data['address'].get('addressRegion', '')  # Use get() method with a default value

            final_output = f"{addressLocality} {addressRegion}"
            address = [final_output] * len(review_scores)
    else:
        print("Alt")

    company_response_date = ['']*len(review_scores)
    company_response = ['']*len(review_scores)
    company_responder = ['']*len(review_scores)

    max_length = max(len(name_list), len(address), len(geo_id), len(hotel_id), len(overall_rating), len(review_urls_final), len(profile_img), len(review_scores), len(review_headings), len(review_contributions), len(all_reviews), len(date_of_stay))

    # Pad arrays with empty values if their lengths are less than the maximum length
    name_list += [''] * (max_length - len(name_list))
    address += [''] * (max_length - len(address))
    geo_id += [''] * (max_length - len(geo_id))
    hotel_id += [''] * (max_length - len(hotel_id))
    overall_rating += [''] * (max_length - len(overall_rating))
    review_urls_final += [''] * (max_length - len(review_urls_final))
    profile_img += [''] * (max_length - len(profile_img))
    review_scores += [''] * (max_length - len(review_scores))
    review_headings += [''] * (max_length - len(review_headings))
    review_contributions += [''] * (max_length - len(review_contributions))
    all_reviews += [''] * (max_length - len(all_reviews))
    date_of_stay += [''] * (max_length - len(date_of_stay))

    data = {
        'names': name_list,
        'address': address,
        'geo_id': geo_id,
        'hotel_id': hotel_id,
        'rating': overall_rating,
        'url': review_urls_final,
        'profile_image': profile_img,
        'review_score': review_scores,
        'review_heading': review_headings,
        'profile_contr': review_contributions,
        'review_body': all_reviews,
        'date_of_stay': date_of_stay,
        'company_responder': company_responder,
        'company_response': company_response,
        'company_response_date': company_response_date,
        'timestamp': timeStamp
    }

    for key, value in data.items():
      print(f"Length of '{key}': {len(value)}")

    df = pd.DataFrame(data)
    return df

def second_scraper_name(headers, base_url):
    headers = convert_headers(headers)
    HEADERS.update(headers)
    r = requests.get(base_url, headers=HEADERS)
    time.sleep(2)
    soup = BeautifulSoup(r.text, 'html.parser')
    time.sleep(2)
    h1_element = soup.find('h1', class_='biGQs _P fiohW eIegw')

    Attname = "Attraction"
    # Extract the text
    if h1_element:
        name = h1_element.text
        Attname = name
    else:
        Attname = "Attraction"
    print(Attname)
    return {"city_name": Attname}

if __name__ == '__main__':
    socketio.run(app, debug=True)