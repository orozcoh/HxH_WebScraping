from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import requests
import sys
import os
import io

#------------------------------- External Variables -----------------------------------

if len(sys.argv) == 2:
    startChapter =int(sys.argv[1])
    n = 10
    print("\nDownload stating from chapter: ", startChapter)
    print("3rd parameter not given - 10 Chapters to donwload\n")
elif len(sys.argv) == 3:
    startChapter = int(sys.argv[1])
    n = int(sys.argv[2])
    print("\nDownload stating from chapter: ", startChapter)
    print("Chapters to download:", n, "\n")
else:
    print("\n"," "*20, "-"*15,"\n   Hunter x Hunter\n"," "*20,"-"*15, sep="")
    startChapter = int(input("Which chapter do you want to start downloading from:  "))
    n = int(input("How many chapters do you want to donwload:  "))

#----------------------------------------------------------------------------------------

#----------------------------------- Directory creation ---------------------------------
folder_name = "Hunter_X"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)
#----------------------------------------------------------------------------------------

#------------------------------- Download function definition ---------------------------
def download_chapter(chapter):
  chapter_str = "0"* (2 if len(str(chapter)) == 1 else 1) + str(chapter)
  chapter_pdf_name = "./Hunter_X/HxH_" + chapter_str + ".pdf"

  font = ImageFont.truetype("./fonts/Road_Rage.otf", 300)

  url ="https://hunterxhuntermanga.online/manga/hunter-x-hunter-chapter-" + str(chapter)
  #print("URL:", url)

  resp = requests.get(url)

  soup = BeautifulSoup(resp.content, 'html.parser')

  temp_links = soup.find_all("meta", property="og:image")

  for i in range(len(temp_links)):
      temp_links[i] = temp_links[i].get('content')

  img_links = []

  for link in temp_links:
      if not link in img_links:
          img_links.append(link)

  print("Downloading",len(img_links), "pages from Chapter:", chapter)

  cover = Image.open("./cover/HxH_cover.jpeg")
  draw = ImageDraw.Draw(cover) # Call the ImageDraw functions to make the image editable 
  draw.text((280, 1000), chapter_str, font=font, fill=(0,0,0)) 

  chapter_img = []

  for page, link in enumerate(img_links):
    r = requests.get(link)
    try:
      im = Image.open(io.BytesIO(r.content))
    except:
      print("\nmissing page")
      im = cover

    chapter_img.append(im)

  cover.save(chapter_pdf_name, save_all=True, append_images=chapter_img)
#----------------------------------------------------------------------------------------

#------------------------------------- MAIN ---------------------------------------------
if __name__ == "__main__":
  for i in range(startChapter, startChapter+n):
    download_chapter(i)
