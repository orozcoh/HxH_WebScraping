from base64 import urlsafe_b64decode
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
    print("\n"," "*20, "-"*15,"\n"," "*20,"Hunter x Hunter\n"," "*20,"-"*15, sep="")
    print("\nDownload stating from chapter: ", startChapter)
    print("3rd parameter not given - 10 Chapters to donwload\n")
elif len(sys.argv) == 3:
    startChapter = int(sys.argv[1])
    n = int(sys.argv[2])
    print("\n"," "*16, "-"*20,"\n"," "*20,"Hunter x Hunter\n"," "*20,"-"*20, sep="")
    print("\nDownload stating from chapter: ", startChapter)
    print("Chapters to download:", n, "\n")
else:
    print("\n","-"*53,"\n"," "*17,"Manga Downloader\n","-"*53, sep="")
    print("\nAvailable Mangas:")
    print("\n1: One Piece\n2: Hunter X\n\n" + "-"*53)
    option = int (input("\nSelect manga (1 or 2): "))
    startChapter = int(input("\nWhich chapter do you want to start downloading from:  "))
    n = int(input("\nHow many chapters do you want to download:  "))
    if option == 1:
      print("\n" + "-"*53 + "\n   Downloading chapters: " + str(startChapter) + " -> " + str(startChapter + n) + " of ONE PIECE\n" + "-"*53 + "\n" )
    elif option == 2:
      print("\n" + "-"*53 + "\n   Downloading chapters: " + str(startChapter) + " -> " + str(startChapter + n) + " of HUNTER X\n" + "-"*53 + "\n" )

#----------------------------------------------------------------------------------------
url = 'https://hunterxhuntermanga.online/manga/hunter-x-hunter-chapter-' 
url_HxH_2 = 'https://ww3.hunterxhunter.xyz/manga/hunter-x-hunter-chapter-'
url_OP_1 = 'https://read1.manga1piece.com/manga/one-piece-chapter-'

urls = { 'One Piece': url_OP_1, 'Hunter X': url, 'Hunter x 2': url_HxH_2}

if option == 1:
  url = urls['One Piece']
  folder_name = "One_Piece"
  chapter_name = "One_Piece_"
  cover = Image.open("./cover/OP_cover.jpeg")
elif option == 2:
  url = urls['Hunter X']
  folder_name = "Hunter_X"
  chapter_name = "HxH_"
  cover = Image.open("./cover/HxH_cover.jpeg")
else:
  print("\n\nOption selected no valid, try again.\n\n")

#----------------------------------- Directory creation ---------------------------------

if not os.path.exists(folder_name):
    os.makedirs(folder_name)
#----------------------------------------------------------------------------------------

#------------------------------- Download function definition ---------------------------
def download_chapter(chapter):
  chapter_str = ""
  
  if len(str(chapter)) <= 2:
    chapter_str = "0"* (2 if len(str(chapter)) == 1 else 1)

  chapter_str = chapter_str + str(chapter)

  chapter_pdf_name = "./" + folder_name + "/" + chapter_name + chapter_str + ".pdf"

  font = ImageFont.truetype("./fonts/Road_Rage.otf", 300)

  resp = requests.get((url + "1-2") if option == 1 and chapter == 1 else (url + str(chapter)))    # how to avoid if

  soup = BeautifulSoup(resp.content, 'html.parser')

  temp_links = soup.find_all("meta", property="og:image")

  for i in range(len(temp_links)):
      temp_links[i] = temp_links[i].get('content')

  img_links = []

  for link in temp_links:
      if not link in img_links:
          img_links.append(link)

  print("Downloading",len(img_links), "pages from Chapter:", chapter)

  if option == 1:
    cover = Image.open("./cover/OP_cover.jpeg")
  elif option == 2:
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
