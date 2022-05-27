import sys

if len(sys.argv) == 2:
    lastChapter =int(sys.argv[1])
    n = 10
    print("\nDownload stating from chapter: ", lastChapter+1)
    print("\n3rd parameter not given - 10 Chapters to donwload\n")
elif len(sys.argv) == 3:
    lastChapter = int(sys.argv[1])
    n = sys.argv[2]
    print("\nDownload stating from chapter: ", lastChapter+1)
    print("\nChapters to download:", n, "\n")
else:
    lastChapter = 0
    n = 10
    print("\nParameters not given \n\nDownloading the first \nten chapters (1-10) of")
    print("\n"," "*3, "-"*15,"\n   Hunter x Hunter\n"," "*3,"-"*15, sep="")