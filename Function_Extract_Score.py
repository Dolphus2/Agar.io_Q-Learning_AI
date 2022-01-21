import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Teseract_path'
import cv2
import numpy as np
import tesserocr
from PIL import Image
from os import path
import pandas as pd
import openpyxl

def ExtractScore(board, ScreenDimensions, dataPath):
    # Get dimensions of board
    boardDim = np.shape(board)

    # Paths for files 
    excelPath = dataPath+'/gameData.xlsx'
    iterationPath = dataPath + '/gameIteration.txt'
    dataImagePath = dataPath + '/data' # This is only used to make it easier to view the failed identification images

    # make a copy 
    imgData = np.copy(board)
    
    # How much we up-scale the picture for recognition
    mult = 20
    board = cv2.resize(board, None, fx= mult, fy= mult, interpolation=cv2.INTER_LANCZOS4)

    # Threshold the picture
    board = cv2.threshold(board, 150, maxval=255, type=cv2.THRESH_BINARY)[1]

    # Threshold again, where colored pixels are changed to white
    Background = np.argwhere(np.max(board, axis = 2) != np.min(board, axis = 2)).T
    board[Background[0],Background[1]] = np.array([255,255,255])
    
    # Erode and dilate the picture
    kernel = np.ones((3,3),np.uint8)

    # Match result board variant #1 --------------------
    board = cv2.erode(board,kernel, iterations = 7)

    # Coordinates for the numbers we want to read
    heightRow1 = mult * np.array([75,90])
    heightRow2 = mult * np.array([110,125])
    heightRow3 = mult * np.array([145,160])
    widthCol1 = mult * np.array([55,100])
    widthCol2 = mult * np.array([195,245])

    # Match result board variant #2 -----------------
    # board = cv2.erode(board,kernel, iterations = 1)
    # board = cv2.dilate(board,kernel, iterations = 1)

    # heightRow1 = mult * np.array([int(0.481*boardDim[0]),int(0.557*boardDim[0])])
    # heightRow2 = mult * np.array([int(0.63*boardDim[0]),int(0.706*boardDim[0])])
    # heightRow3 = mult * np.array([int(0.783*boardDim[0]),int(0.86*boardDim[0])])
    # widthCol1 = mult * np.array([int(0.231*boardDim[1]),int(0.428*boardDim[1])])
    # widthCol2 = mult * np.array([int(0.612*boardDim[1]),int(0.835*boardDim[1])])

    # Pixels of the regions of scores
    foodeatenPic = board[heightRow1[0]:heightRow1[1],widthCol1[0]:widthCol1[1]]
    highestmassPic = board[heightRow1[0]:heightRow1[1],widthCol2[0]:widthCol2[1]]
    timealivePic = board[heightRow2[0]:heightRow2[1],widthCol1[0]:widthCol1[1]]
    cellseatenPic = board[heightRow3[0]:heightRow3[1],widthCol1[0]:widthCol1[1]]
    leaderboardtimePic = board[heightRow2[0]:heightRow2[1],widthCol2[0]:widthCol2[1]]
    toppositionPic = board[heightRow3[0]:heightRow3[1],widthCol2[0]:widthCol2[1]]
    

    #Convert to PIL image
    foodeatenPic = Image.fromarray(foodeatenPic.astype('uint8'), 'RGB')
    highestmassPic = Image.fromarray(highestmassPic.astype('uint8'), 'RGB')
    timealivePic = Image.fromarray(timealivePic.astype('uint8'), 'RGB')
    cellseatenPic = Image.fromarray(cellseatenPic.astype('uint8'), 'RGB')
    leaderboardtimePic = Image.fromarray(leaderboardtimePic.astype('uint8'), 'RGB')
    toppositionPic = Image.fromarray(toppositionPic.astype('uint8'), 'RGB')

    # Run ocr
    foodEaten = tesserocr.image_to_text(foodeatenPic, lang ='digits_comma') # Language can be found at: https://github.com/Shreeshrii/tessdata_shreetest/blob/master/digits_comma.traineddata
    highestMass = tesserocr.image_to_text(highestmassPic, lang ='digits_comma')
    timeAlive = tesserocr.image_to_text(timealivePic, lang ='digits_comma')
    cellsEaten = tesserocr.image_to_text(cellseatenPic, lang ='digits_comma')
    leaderboardTime = tesserocr.image_to_text(leaderboardtimePic, lang ='digits_comma')
    topPosition = tesserocr.image_to_text(toppositionPic, lang ='digits_comma')

    #______________
    # If wanted to use pytesseract instead.

    # foodEaten = pytesseract.image_to_string(foodeatenPic)
    # highestMass = pytesseract.image_to_string(highestmassPic)
    # timeAlive = pytesseract.image_to_string(timealivePic)
    # cellsEaten = pytesseract.image_to_string(cellseatenPic)
    # leaderboardTime = pytesseract.image_to_string(leaderboardtimePic)
    # topPosition = pytesseract.image_to_string(toppositionPic)
    #__________________

    numeric_filter = filter(str.isdigit, foodEaten)
    foodEaten = "".join(numeric_filter)

    numeric_filter = filter(str.isdigit, highestMass)
    highestMass = "".join(numeric_filter)

    numeric_filter = filter(str.isdigit, timeAlive)
    timeAlive = "".join(numeric_filter)

    numeric_filter = filter(str.isdigit, cellsEaten)
    cellsEaten = "".join(numeric_filter)

    numeric_filter = filter(str.isdigit, leaderboardTime)
    leaderboardTime = "".join(numeric_filter)

    numeric_filter = filter(str.isdigit, topPosition)
    topPosition = "".join(numeric_filter)


    try:
        with open(iterationPath,'r') as f:
            gameIteration = int(f.read())+1
        with open(iterationPath, "w") as f:
            f.write(str(gameIteration))
    except FileNotFoundError:
        with open(iterationPath, "w") as f:
            f.write(str(1))
        gameIteration = 1


    appendRow = np.array([[foodEaten,highestMass,timeAlive,cellsEaten,leaderboardTime,topPosition]], dtype=object)


    alreadySaved = False
    count = 0
    for i, e in enumerate(np.squeeze(appendRow)):
        if len(e) == 0:
            if i != 1:
                appendRow[0][i] = 'N/A'
                count += 1
                                    
            else:
                appendRow[0][i] = 'See picture: ' + str(gameIteration)
                cv2.imwrite(dataImagePath+f"/game_{gameIteration}.jpeg", imgData)
                alreadySaved = True
                
        else:
            appendRow[0][i] = int(e)
            if i in [2,4] and len(e) >= 3:
                    if len(e) == 3:
                        appendRow[0][i] = int(appendRow[0][i]) - int(e[0])*100 + int(e[0])*60
                        print(appendRow[0][i])
                    elif len(e) == 4:
                        appendRow[0][i] = int(appendRow[0][i]) - int(e[0])*1000 - int(e[1])*100 + int(e[0:2])*60

    if count > 2 and not alreadySaved: #Save a picture if there are 3 or more values that were missed and if picture isn't already saved
        cv2.imwrite(dataImagePath+f"/game_{gameIteration}.jpeg", imgData)

    if path.exists(excelPath): #If the excel has arleady been created, append row to the excel
        df = pd.DataFrame(np.array(appendRow), index=[gameIteration])
        book = openpyxl.load_workbook(excelPath)

        writer = pd.ExcelWriter(excelPath, engine='openpyxl')
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        df.to_excel(writer, startrow=gameIteration, header=False)
        writer.save()
        
    else: # Make a new excel with the appropiate col names and index name
        df = pd.DataFrame(appendRow,index = [gameIteration],columns=['Food Eaten','Highest Mass','Time Alive','Cells Eaten','Leaderboard Time','topPosition'])
        df.to_excel(excelPath)


dataPath = "Insert_path"
for i in range(1,391):
    impath = f"Your_folder_with_images/run_{i}.png"
    img = cv2.imread(impath)

    ExtractScore(img,0,dataPath)

