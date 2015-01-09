import os, time, urllib.request, pickle, contextlib, img2pdf, re
from os import listdir
from os.path import isfile, isdir, join

#ititialList = [title, item1, item2, xxxxx]
initialList = ["Initial", "1: Load/reload manga list", "2: Select a manga", "3: Make PDF from local files (made using this tool)", "4: Quit"]
menu1 = ["Load/reload manga list", "1: Load from file", "2: Load from internet", "3: Back to main"]
menu2 = ["Select a manga", "1: Select by first letter/number", "2: Search by word"]

#mangaList
#[int, name, link]

#Good method ('_')b
def loadMenu(list):
    os.system("cls")
    print("###Luke's manga converter#############################")
    for item in list:
        print (item)
    selection = input("Option: ")
    if(selection.isdigit()):
        selection = int(selection)
        if ((selection > 0) and (selection < len(list))):
            return selection
        else:
            print ("Please choose a selection between 1-" + str(len(list)-1))
            time.sleep(2)
            return loadMenu(list)
    else:
        print("Please enter a numerical value")
        time.sleep(2)
        return loadMenu(list)

#Good method ('_')b
def getLetter():
    searchchar = input("Enter first letter/number: ")
    if (len(searchchar) < 1):
        print("Enter at least one character")
        time.sleep(2)
        getLetter()
    else:
        return searchchar[0:1]

#Good method ('_')b
def getLetters():
    searchstring = input("Enter search string: ")
    if (len(searchstring) < 1):
        print("Enter at least one character")
        time.sleep(2)
        getLetters()
    else:
        return searchstring

#Good method ('_')b
def getManga(sortedList):
    selection = input("Select number, or enter \"b\" to go back: ")
    if(selection.lower() == "b"):
        return -1
    elif selection.isdigit():
        selection = int(selection)
        for item in sortedList:
            if item[0] == selection:
                return item
        print("Couldn't find number. Try again or enter \"b\" to go back")
        getManga(sortedList)
    else:
        "Please enter \"b\" or a number"
        getManga(sortedList)

        
def getChapters(manga):
    #Manga in the format [number (ignored), Title, Link]
    #both methods should end here
    print("Chapter code")
    print(manga)
    
    #mainhtmlList = []
    chapterList = []
    url = ""
    url = manga[2]
    
    print (url)
    #url = url.replace(":","%3a")
    
    #url = url.replace("/","%2F")
    #url = url.strip()
    print ("URL: " + url )
    string = "Next</a>&nbsp;</td>"
    #url = "http://www.mangachapter.me/1527/liar-game.html"
    
    hasNext = True
    while (hasNext):
        #print(url)
        #input("Is this okay?URL")
        htmlList = getHTML(url)
        #mainhtmlList.append(htmlList) Not doing this anymore because I can't work out how lists work
        foundThisRun = False
        count = 0
        for line in htmlList:
            #print(line)
            #input("Is this okay?" + str(count))
            if line.strip() == '<div class="l1">':
                #print(line)
                #input("Is this okay?" + str(count))
                line = htmlList[count + 1]
                chapterLink = line[line.index("http"):line.index('" title=')]
                chapterTitle = line[line.index('title="')+7:line.index('">')]
                chapterList.append([chapterTitle, chapterLink])
            elif string in line:
                #get this url, and use it for the next search
                #print (line)
                #input("Is this okay?LINE")
                url = line[line.index("http"):line.index('">Next</a>')]
                foundThisRun = True
            count += 1
        if(foundThisRun == False):
            hasNext = False
    """
    chapterList = []
    #Now all the html has been put together (in an ugly way), lets get all the chapters
    count = 0
    for line in mainhtmlList:
        if line.strip() == '<div class="l1">':
            #<a href="http://www.mangachapter.me/746/naruto/700.html" title="Naruto ch700">
            line = mainhtmlList[count +1]
            link = line[line.index("http"):line.index('" title=')]
            title = line[line.index('title="')+7:line.index('">')]
            chapterList.append([title,link])
            count += 11
        count += 1
    """
    
    #print(chapterList)
    chapterList.reverse()
    start = chapterList[0][0]
    #print(start)
    
    startNum = start[start.index("ch")+2:]
    if " " in startNum:
        startNum = startNum[:startNum.index(" ")]
    #print(startNum)
    
    end = chapterList[len(chapterList) -1][0]
    #print(end)
    endNum = end[end.index("ch")+2:]
    if " " in endNum:
        endNum = endNum[:endNum.index(" ")]
    #print(endNum)
    
    #print (chapterList)
    
    print ("Chapters run from: " + start + " to " + end + " (or to " + str(len(chapterList)) + ")")
    print ("..or from: " + startNum + " to " + endNum)
    
    print("Sometimes there are more chapters than the numbers would suggest (e.g. Extras).")
    print("For ease of viewing, I'll ask you to confirm which chapters you want using")
    print("the number count, and not the chapter number, as well as 5 either side")
    
    while (True):
        startIndex = input("Please select where you'd like to start from (from 0 (inclusive) to " + str(len(chapterList)) + " exclusive)")
        if startIndex.isdigit():
            startIndex = int(startIndex)
        elif startIndex == "":
            startIndex = 0
        if (startIndex >= 0) and (startIndex < len(chapterList)):
            print("Did you mean this one?")
            for x in range(startIndex - 5, startIndex + 6):
                if(x >= 0) and (x < len(chapterList)):
                    if (x == startIndex):
                        print("---->" + chapterList[x][0])
                    else:
                        print(chapterList[x][0])
            inputSelection = input("Did you mean this one? (Y/n)")
            if (inputSelection.lower() == "y") or (inputSelection == ""):
                break
            else:
                print("Lets try again")
        else:
            print("Invalid input, please try again.")
    
    print("")
    print("Thanks")
    print("")
    
    while (True):
        endIndex = input("Please select where you'd like to end(from 0 (inclusive) to " + str(len(chapterList)) + " exclusive)")
        if endIndex.isdigit():
            if int(endIndex ) >= startIndex:
                endIndex = int(endIndex)
            else:
                print("The end index must be greater than or equal to the start index")
        elif endIndex == "":
            'CHANGE THIS BACK'
            #Default is to get everything.
            endIndex = len(chapterList) -1
            #endIndex = startIndex + 1
        if (endIndex >= 0) and (endIndex < len(chapterList)):
            print("Did you mean this one?")
            for x in range(endIndex - 5, endIndex + 6):
                if(x >= 0) and (x < len(chapterList)):
                    if (x == endIndex):
                        print("---->" + chapterList[x][0])
                    else:
                        print(chapterList[x][0])
            inputSelection = input("Did you mean this one? (Y/n)")
            if (inputSelection.lower() == "y") or (inputSelection == ""):
                break
            else:
                print("Lets try again")
        else:
            print("Invalid input, please try again.")
    
    print("Thanks. Getting chapters " + str(startIndex) + " to " + str(endIndex))
    time.sleep(5)
    #return chapterList[startIndex:endIndex]
    print(manga)
    saveChapter(manga[1],chapterList[startIndex:endIndex+1]) #Change this!
    
    #valid == False
    #while (valid == False):
        #this number may differ. not sure how to fix that, so going to use 
        #print ("Chapters run from: " + start + " to " + end + " (or " + len(chapterList)
        #print ("..or from: " + startNum + " to " + endNum)
    
    
        #chapterStart = input("Which chapters would you like to get? (START/end). Default (blank) is from the beginning: ")
        #chapterEnd = input("Which chapters would you like to get? (start/END). Default (blank) is to the end: ")    
    
        #if(chapterStart == ""):
        #    chapterStart = startNum
    
    #time.sleep(15)
    #Observations - chapters can be double.
    #Chapters can come in volumes (Vol __
    #Best to list chapters
    #http://www.mangachapter.me/mangalist.html
    #may be a better source
    #TODO:
    #1: Get a FULL list of chapters (getting from Next page until no more next
    #2: Present option of which chapters to get (sadly no volumes this time)
    # possibly rotate pages that are wider than longer?
    
#Good method ('_')b    (for old website)
"""
def loadFromInternet():
    #proceed as below
    htmlstring = ""
    dict = {}
    print("Loading...")
    with contextlib.closing(urllib.request.urlopen('http://www.mangahere.co/mangalist/')) as response:
        #response = urllib.request.urlopen('http://www.mangahere.co/mangalist/')
        html = response.read()
        htmlstring = str(html)
    #Trim html to get lists
    start = '<div class="list_manga">'
    end = '       </div>'
    startindex = htmlstring.index(start)
    endindex = htmlstring.index(end)
    htmlstring = htmlstring[startindex:endindex]
    #Iterate over html to get Name:Link from:
    #<li><a class="manga_info" rel="Liar Game" href="http://www.mangahere.co/manga/liar_game/"><span></span>Liar Game</a></li>
    tempstart = '<li><a class="manga_info" rel="'
    tempend = '"><span></span>'
    
    length = len(htmlstring)
    i = 0
    while i < length:
        currenttext = htmlstring[i:length]
        if(currenttext.find(tempstart) == 0):
            temptext = currenttext[0:currenttext.index(tempend)]
            tempname = temptext[temptext.index('rel="')+5:temptext.index('" href')].replace('&quot;','"')
            templink = temptext[temptext.index("http"):len(temptext)]
            dict.update({tempname:templink})
            i = i + len(temptext)
            currenttext = htmlstring[i:length]
            i = i + currenttext.find(tempstart)
        else:
            i = i + 1
    saveManga(dict)
    return dict
"""

def saveChapter(animeName, chapterList):

    for chapter in chapterList:
        print (chapter)
        print()
    for chapter in chapterList:
        
        
        directory = animeName + "/" + chapter[0] + "/"
        if ('//' in directory):
            directory = directory.replace("//","/")
        if not os.path.exists(directory):
            os.makedirs(directory)
        

        #input("Is this okay?")
        #Need to get pageList, then imageList(perhaps)(YES, can do when saving)
        pageList = []
        imageList = []
        
        #get all pages
        html = getHTML(chapter[1])
        startKey = '<div class="page-select">'
        count = 0
        for line in html:
            if startKey in line:
                line = html[count+1]
                '<option value="/746/naruto/0-1.html" selected>1/46</option>'
                lineArray = line.split("</option>")
                for item in lineArray:
                    if '"/' in item:
                        pageURL = item[item.index('"/')+1:]
                        #print("PageURL 1:" + pageURL)
                        pageURL = pageURL[:pageURL.index('" ')]
                        #print("PageURL 2:" + pageURL)
                        pageURL = "http://www.mangachapter.me" + pageURL
                        pageList.append(pageURL)
                break
            count +=1
                
        
        #parse images in those pages.
        for pageURL in pageList:
            #print (pageURL)
            html = getHTML(pageURL)#This may need to change if we get more than one.
            startKey = 'id="mangaImg" src="'
            for line in html:
                if startKey in line:
                    imageURL = line[line.index(startKey)+len(startKey):]
                    imageURL = imageURL[:imageURL.index('"')]
                    imageName = imageURL[imageURL.rindex("/") +1:]
        
        
                    #SAVING CODE< USE LATER!
                    if os.path.exists(directory + imageName):
                        print(imageName + " in " + directory + " exists. Skipping.")
                    else:
                        print("Saving " + imageName + " in " + directory)        
                        image=urllib.request.URLopener()
                        image.addheaders.append(('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'))
                        image.retrieve(imageURL,directory + imageName)
                    imageList.append(directory + imageName)
    ##Get the URL
    ##Get the page and download the picture
    #put it in a pdf
    print("Done!")
    
    while(True):
        selection = input("Would you like to convert these files to PDF? (N/y): ")
        if (selection.lower() == "y"):
            saveAsPDF(imageList)
            break
        elif (selection.lower() == "n" or selection.lower() == ""):
            break
        else:
            print("Please make a proper selection")
    
    time.sleep(5)


def saveAsPDF(imageList):
    
    """
    for image in imageList:
        print (image)
    
    time.sleep(15)
    """
    
    filename = "output"
    dpi = 167
    x = 600
    y = 800
    while(True):
        selection = input("Would you like the filename to be? ____.pdf (default: output): ")
        if (len(selection) > 0) :
            filename = selection
            if not ".pdf" in filename:
                filename = filename + ".pdf"
            break
        elif(selection == ""):
            filename = "output.pdf"
            break
        else:
            print("Please make a proper selection")
    
    while(True):
        selection = input("Would you like the dpi to be? (default: 167 (for kindle)): ")
        if (selection.isdigit()):
            dpi = int(selection)
            break
        elif(selection == ""):
            dpi = 167
            break
        else:
            print("Please make a proper selection")
            
    while(True):
        selection = input("Would you like the width (x) to be? (default: 0 (unchanged)): ")
        if (selection.isdigit()):
            x = int(selection)
            break
        elif(selection == ""):
            x = 0
            break
        else:
            print("Please make a proper selection")
            
    while(True):
        selection = input("Would you like the height (y) to be? (default: 0 (unchanged)): ")
        if (selection.isdigit()):
            y = int(selection)
            break
        elif(selection == ""):
            y = 0
            break
        else:
            print("Please make a proper selection")
                     
    print("Thanks. Making PDF")
    print(filename)
    print(dpi)
    print(x)
    print(y)
    #path = "C:/Users/Luke/Documents/pyspace/Menu/Liar Game/Liar Game ch1/cropped"
    #onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ]
    #onlyfiles2 = []
    #for files in onlyfiles:
    #    files = path + "/" + files
    #    onlyfiles2.append(files)
    pdf_bytes = img2pdf.convert(imageList, dpi,x,y)
    
    file = open(filename,"wb")
    file.write(pdf_bytes)
    file.close()
    print("Done.")

def findManga():
    onlyDirs = [ f for f in listdir(".") if isdir(join(".",f)) ]
    onlyDirs = natural_sort(onlyDirs)
    count = 0
    for dir in onlyDirs:
        print(str(count) + ": " + dir)
        count +=1
    
    
    mangaDir = ""
    startIndex = 0
    endIndex = 0
    imageList = []
    
    while(True):
        selection = input("Please select a manga directory number from the list:")
        if (selection.isdigit()):
            selection = int(selection)
            if (selection >=0 and selection < len(onlyDirs)-1):
                mangaDir = onlyDirs[selection] + "/"
                break
            else:
                print("Selection must be between 0 (inclusive) and " + len(onlyDirs) + " (exclusive)")
        else:
            print("Selection must be a digit")
    
    print (mangaDir)
    chapterDirs = [ f for f in listdir(mangaDir) if isdir(join(mangaDir,f)) ]
    chapterDirs = natural_sort(chapterDirs)
    count = 0
    for dir in chapterDirs:
        print(str(count) + ": " + dir)
        count +=1
    
    while(True):
        selection = input("Please select the start chapter directory number from the list:")
        if (selection.isdigit()):
            selection = int(selection)
            if (selection >=0 and selection < len(chapterDirs)-1):
                startIndex = selection
                break
            else:
                print("Selection must be between 0 (inclusive) and " + len(chapterDirs) + " (exclusive)")
        else:
            print("Selection must be a digit")
    
    count = 0
    for dir in chapterDirs:
        print(str(count) + ": " + dir)
        count +=1
    
    while(True):
        selection = input("Please select the end chapter directory number from the list:")
        if (selection.isdigit()):
            selection = int(selection)
            if (selection >=0 and selection < len(chapterDirs)):
                endIndex = selection
                break
            else:
                print("Selection must be between 0 (inclusive) and " + str(len(chapterDirs)) + " (exclusive)")
        else:
            print("Selection must be a digit")
            
    print("Thanks. Generating comic list")
    
    chapterDirs = chapterDirs[startIndex:endIndex+1]
    
    for chapter in chapterDirs:
        chapter = chapter + "/"
        chapterFiles = [ f for f in listdir(mangaDir + chapter) if isfile(join(mangaDir + chapter,f)) ]
        chapterFiles = natural_sort(chapterFiles)
        for file in chapterFiles:
            imageList.append(mangaDir + chapter + file)
    
    return imageList

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

#Good method ('_')b
def getHTML(url):
    htmlstring = ""
    #Needs user agents, otherwise gets a 403 forbidden page.
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 

    request=urllib.request.Request(url,None,hdr)
    response = urllib.request.urlopen(request)
    html = response.read()
    
    htmlstring = str(html)
    """
    #request=urllib.request.Request(url,None,headers) #The assembled request
    request=urllib.request.Request(url,None,hdr) #The assembled request
    with contextlib.closing(urllib.request.urlopen(request)) as response:
        #response = urllib.request.urlopen('http://www.mangahere.co/mangalist/')
        html = response.read()
        htmlstring = str(html)
    """
    #htmlList = htmlstring.split("\\r\\n\\r\\n\\r\\n")
    htmlstring = htmlstring.replace("\\r","")
    #print (htmlstring)
    #input("Is this okay?HTMLSTRING")
    htmlList = htmlstring.split("\\n")
    #print (htmlList)
    #input("Is this okay?HTMLSTRING")
    return htmlList

#Good method ('_')b
def saveList(list):
    f = open('dump.txt', 'w')
    for item in list:
        f.write(item + "\r\n")
    
#Good method ('_')b    (for new website)
def loadFromInternet():
    #proceed as below
    htmlstring = ""
    dict = {}
    print("Loading...")
    #Trim html to get lists
    start = '<td width="250"><a href="'
    end = '</a></td>'
    url = "http://www.mangachapter.me/mangalist.html"
    htmlList = getHTML(url)
    for line in htmlList:
        if (start in line) and (len(start) < 100):
            link = line[line.index(start) + len(start) : line.index("html") + 4]
            title = line[line.index(link) + len(link) + 2 : line.index("</a></td>")]
            dict.update({title:link})
    saveManga(dict)
    return dict

#Good method ('_')b
def replace(dict):
    #tri format (mebbe)
    newDict = {}
    for item in dict:
        newItem = item
        newItem = newItem.replace("&#33;","!")
        newItem = newItem.replace("&amp;","&")
        newItem = newItem.replace("&#39;","'")
        newItem = newItem.replace("&#039;","'")
        newItem = newItem.replace("&gt;",">")
        newItem = newItem.replace("&lt;","<")
        newItem = newItem.replace('&quot;','"')
        newItem = newItem.replace("&#036;","$")
        newItem = newDict.update({newItem:dict.get(item)})
    
    return newDict

#Good method ('_')b
def getSortedList(dict):
    tempList = []
    for item in dict:
        tempList.append(item)
    tempList.sort()
    bigList = []
    count = 0
    for item in tempList:
        bigList.append([count, item, dict.get(item)])
        count = count + 1
    bigList.sort()
    return bigList
    
#Good method ('_')b
def saveManga(mangalist):
    with open('mangalist.pickle', 'wb') as handle:
        pickle.dump(replace(mangalist), handle)
        
        saveList(replace(mangalist))
    loadManga()

#Good method ('_')b
def loadManga():
    filename = 'mangalist.pickle'
    if(os.path.isfile(filename)):
        with open(filename, 'rb') as handle:
            return pickle.load(handle)

#Good method ('_')b
def getMangaByChar(mangaList, singlechar):
    dict = {}
    for item in mangaList:
        #print(item)
        #print (item[0:1])
        #print (mangaList.get(item))
        #time.sleep(5)
        if (item[0:1].lower() == singlechar.lower()):
            dict.update({item:mangaList.get(item)})
    return dict

#Good method ('_')b
def getMangaByString(mangaList, searchstring):
    dict = {}
    for item in mangaList:
        #print(item)
        #print (item[0:1])
        #print (mangaList.get(item))
        #time.sleep(5)
        if (searchstring.lower() in item.lower()):
            dict.update({item:mangaList.get(item)})
    return dict

end = False
mangaList = loadManga()
backpoint = -1
while (end == False):
    selection = loadMenu(initialList)
    if (selection == 1):
        #Code to handle "Load/reload manga list" option
        print ("You have selected 1")
        selection = loadMenu(menu1)
        if (selection == 1):
            #Code to handle "1: Load from file" option
            mangaList = loadManga()
            print("Loaded")
            time.sleep(2)
        elif (selection == 2):
            #Code to handle "2: Load from internet" option
            mangalist = loadFromInternet()
            print("Loaded mangalist")
            time.sleep(5)
        elif (selection == 3):
            #Code to handle "3: Back to main" option
            time.sleep(5)
        #end = True #remove eventually
        
    elif (selection == 2):
        #Code to handle "2: Select a manga" option
        selection = loadMenu(menu2)
        if (selection == 1):
            #Code to handle "1: Select by first letter/number" option
            searchchar = getLetter()
            submanga = getMangaByChar(mangaList, searchchar)
            sortedList = getSortedList(submanga)
            for item in sortedList:
                print (str(item[0]) + ": " + str(item[1]))
            print()
            manga = getManga(sortedList)
            if (manga != -1):
                getChapters(manga)
            time.sleep(5)
            
        elif (selection == 2):
            #Code to handle "2: Search by word" option
            searchstring = getLetters()
            submanga = getMangaByString(mangaList, searchstring)
            sortedList = getSortedList(submanga)
            for item in sortedList:
                print (str(item[0]) + ": " + str(item[1]))
            print()
            manga = getManga(sortedList)
            if (manga != -1):
                getChapters(manga)
            time.sleep(5)
            
            #end = True #remove eventually
    elif (selection ==3):
        saveAsPDF(findManga())
    elif (selection == 4):
        end = True
    else:
        print("You have not selected 1, 2 or 3? How!")
        print("Please select 1")
        
print("Finished cleanly")