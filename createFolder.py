from PIL import Image
import numpy as np
import re
import cv2
import os, shutil
import pytesseract


# Function to rename multiple files 
def main():
    i = 0
    # read images from this folder
    for filename in os.listdir('.'):
      src = filename
      # Seperate file extention
      filename_w_ext = os.path.basename(filename)
      filename, file_extension = os.path.splitext(filename_w_ext)

      try:# try for processing only image file
        img = Image.open(src)
        width, height = img.size
        crop_img = img.crop((width/15, height-(height/2.5), width-(width/15), height))

        cvImage = np.array(crop_img)
        frame_blur = cv2.GaussianBlur(cvImage.copy(), (5, 5), 0)# apply gausion blur to given frame
        # frame_blur = cv2.bilateralFilter(cvImage,9,75,75)
        frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)# convert color image into gray image
        frame_out = cvImage.copy()# output frame
        ret,thresh = cv2.threshold(frame_gray,180,255,0)
        
        # Find contours
        cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Find the biggest contour
        biggestContour = cnts[0]
        for c in cnts:
          if cv2.contourArea(biggestContour) < cv2.contourArea(c):
            biggestContour = c
        # Get point of the biggest contour
        (x, y, w, h) = cv2.boundingRect(biggestContour)
        # cv2.rectangle(frame_out, (x, y), (x + w, y + h), (255, 0, 0), 2)# display rectangle of moving object

        # Convert to Black and White
        (thresh2, im_bw) = cv2.threshold(frame_gray, 120, 255, 0)
        crop_contour = im_bw[y+int(h/10):y+h-int(h/10), x+int(w/25):x+w-int(w/25)]
        # crop_contour = cv2.resize(crop_contour, (int(w/2), int(h/2)))
        
        # Show image
        # cv2.imshow("cropped", crop_contour)
        # cv2.imshow('frame_out',frame_out)
        # cv2.imshow('thresh',thresh) 
        # cv2.waitKey(0) # Waits forever for user to press any key
        
        i+=1
        # OCR
        text = pytesseract.image_to_string(crop_contour, lang='eng', config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789');
        text = re.sub(r'[^0-9-]+', '', text, re.I)
        print(i,": Filename "+filename +" to "+text)
        dst = "./" + text

        try:
            os.mkdir(dst)
        except OSError:  
            print ("The directory already exists")
        # rename() function will 
        # rename all the files
        shutil.move(src, dst)
        # os.rename(src, dst+file_extension)


      except IOError:
        if file_extension != '.py' and file_extension != '.bat':
          print('Error on file = ' + src)

      cv2.destroyAllWindows()        # Closes displayed windows
  
# Driver Code 
if __name__ == '__main__': 
      
    # Calling main() function 
    main()