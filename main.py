import pdfPaths
import urllib
import re
import requests
import PyPDF2

pdfsFolder = "folder/to/your/pdfs"

def downloadFiles():
    for nm, i in zip(allFileUrlNames, allFileInfos): # download files, and make saveNames
        yr, nord = i
        sn = pdfsFolder + str(yr) + '_' + str(
            nord) + '.pdf'
        try:
            mf = requests.get(nm, allow_redirects=True)
            acf = open(sn, 'wb')
            acf.write(mf.content)
            acf.close()
        except:
            print('downloadFiles(): Error: ' + nm)

def getSaveNames():
    for file in pdfPaths.officialReportsTableData: # turn pdfPaths urls into actual usable urls
        url = fileUrlStart + file["OfficialReportPath"]
        allFileRawUrls.append(url)
        url = urllib.parse.quote(url, safe=':/')
        allFileUrlNames.append(url)

    for fun in allFileRawUrls: # get year and order from raw urls, and fill savenames
        yearOrder = re.findall("\d+", fun)

        if int(yearOrder[0]) <= int(yearOrder[1]):
            yearOrder[0], yearOrder[1] = yearOrder[1], yearOrder[0]

        allFileInfos.append((yearOrder[0], yearOrder[1]))
        fileSaveNames.append(pdfsFolder + str(yearOrder[0]) + '_' + str(
            yearOrder[1]) + '.pdf')

def fromPdfToTxt():
    for filename, info in zip(fileSaveNames, allFileInfos): # read pdf's
        try:
            pdfFileObj = open(filename, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pageObj = pdfReader.getPage(0)
            pdfTexts[info] = pageObj.extractText()
            pdfFileObj.close()
        except:
            pdfTexts[info] = ' fromPdfToTxt(): Couldnt Read'

    for key in pdfTexts: # put the text you read into txt's
        i1, i2 = key
        file = open('txts/' + i1 + '_' + i2 + '.txt', 'w', encoding='utf-8')
        file.write(pdfTexts[key])
        file.close()

def readFromTxt():
    for info in allFileInfos:
        i1, i2 = info
        file = open('txts/' + i1 + '_' + i2 + '.txt', 'r', encoding='utf-8')
        pdfTexts[info] = file.read()
        file.close()

def outNo12Results():
    file = open('results.txt', 'w')
    for key in pdfTexts:
        i1, i2 = key
        if int(i1) <= 2012:
            continue # break should also work, but this is more safe

        txt = pdfTexts[key]
        try:
            tmp1 = re.findall("\).*\(.*\)", txt)
            tmp2 = re.findall('\(.*\)', tmp1[0])
            file.write(i1 + ', ' + i2 + ': ' + tmp2[0])
            if str(i1 + ', ' + i2) != '2013, 1':
                file.write('\n')
        except:
            print('outNo12Results(): Error: ' + i1 + ' ' + i2)

    file.close()

def readFinal():
    file = open('results.txt', 'r')
    lines = file.read().split('\n')
    names = [x.split(': ')[0] for x in lines]
    numsText = [x.split('(')[1] for x in lines]
    nums = [x[:-1].split(', ') for x in numsText]
    for x, y in zip(names, nums):
        lotoNumbers[x] = y

def numPerYear():
    for year in range(2013, 2021):
        for num in range(1, 40):
            yearlyNumFrequency[(year, num)] = 0

    for key in lotoNumbers:
        info = key.split(', ')
        for x in lotoNumbers[key]:
            try:
                yearlyNumFrequency[(int(info[0]), int(x))] += 1
            except:
                print('numPerYear(): Probably no key: ' + info[0] + ', ' + x)

def printNumPerYear():
    for key in yearlyNumFrequency:
        x, y = key
        print(str(x) + ', ' + str(y) + ' -> ' + str(yearlyNumFrequency[key]))

    print('\n')

def numFreq():
    for x in range(0, 40):
        numFrequency.append(0)

    for key in yearlyNumFrequency:
        x, y = key
        numFrequency[y] += yearlyNumFrequency[key]

def printNumFrequency():
    for x in range(1, 40):
        print(str(x) + ' -> ' + str(numFrequency[x]))

    print('\n')

def printSortedNumFreq():
    temp = []
    for x in range(0, 40):
        temp.append((numFrequency[x], x))

    for x in sorted(temp):
        if x == (0, 0):
            continue
        i, j = x
        print(str(j) + ' -> ' + str(i))

    print('\n')

fileUrlStart = 'https://www.lutrija.rs'
allFileUrlNames = []
allFileRawUrls = []
allFileInfos = []
fileSaveNames = []
pdfTexts = {}
lotoNumbers = {}
yearlyNumFrequency = {}
numFrequency = []

# getSaveNames()
# downloadFiles() # relies on getsavenames(runtime)
# fromPdfToTxt() # relies on getsavenames(runtime) and downloadFiles
# readFromTxt() # relies on getsavenames(runtime) and fromPdfToTxt
# outNo12Results() # relies on readfromtxt(runtime)

readFinal() # relies on outNo12Results

numPerYear() # relies on readFinal(runtime)
printNumPerYear() # relies on numPerYear(runtime)
numFreq() # relies on numPerYear(runtime)
printNumFrequency() # relies on numFreq(runtime)
printSortedNumFreq() # relies on numFreq(runtime)

