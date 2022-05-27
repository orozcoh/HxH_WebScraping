from bs4 import BeautifulSoup
import requests
import os
from PIL import Image, ImageDraw, ImageFont
import io

if not os.path.exists('Hunter_X'):
    os.makedirs('Hunter_X')

def download_chapter(chapter):
  chapter_str = "0"* (2 if len(str(chapter)) == 1 else 1) + str(chapter)
  chapter_pdf_name = "./Hunter_X/HxH_" + chapter_str + ".pdf"

  font = ImageFont.truetype("./fonts/Road_Rage.otf", 300)

  url ="https://hunterxhuntermanga.online/manga/hunter-x-hunter-chapter-" + str(chapter)
  print("URL:", url)

  resp = requests.get(url)
  #print("\nStatus code:", resp.status_code)

  soup = BeautifulSoup(resp.content, 'html.parser')

  #print(soup.prettify())
  #print("\nManga title:",soup.title.string)

  temp_links = soup.find_all("meta", property="og:image")

  for i in range(len(temp_links)):
      temp_links[i] = temp_links[i].get('content')

  img_links = []

  for link in temp_links:
      if not link in img_links:
          img_links.append(link)

  print("\nChapter", chapter, "has", len(img_links), "pages.\n")

  cover = Image.open("./cover/HxH_cover.jpeg")
  draw = ImageDraw.Draw(cover) # Call the ImageDraw functions to make the image editable 
  draw.text((280, 1000), chapter_str, font=font, fill=(0,0,0)) 

  #cover # image with chapter number added


  chapter_img = []

  for page, link in enumerate(img_links):
    r = requests.get(link)
    try:
      im = Image.open(io.BytesIO(r.content))
    except:
      print("\nmissing page")
      im = cover

    chapter_img.append(im)

  #print("Saving to PDF")

  cover.save(chapter_pdf_name, save_all=True, append_images=chapter_img)

lastChapter = 55
n = 1

for i in range(lastChapter+1, lastChapter+1+n):
  download_chapter(i)