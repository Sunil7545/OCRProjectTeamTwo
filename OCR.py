'''
This program will convert PDFs into images and read text from those images
and print the text over the screen.
This can also extract text directly from images and print it out.
'''
import os

# try is used to keep a check over the import. If there is an error, it will not close
# the program, but instead execute the except statement, similar to if & else.
try:
    from PIL import Image, ImageChops, ImageDraw
except ImportError:
    import Image, ImageChops, ImageDraw

# extracts text from images
import pytesseract

# convert pdf into images
from pdf2image import convert_from_path

# image processing library
import cv2 as cv

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class OCR:

    '''
    OCR class to process PDFs and images to extract text from them.
    '''
    def __init__(self, filename):
        '''
        Initializes the memory of the object as the object is created using the parent class.
        :param filename: string parameter to save the path and name of the file.
        '''
        self.filename = filename

    def split_pdf_and_convert_to_images(self):
        '''
        A method of OCR class that takes pdf file and path as the input parameter
        and split the pdf into multiple images. After splitting the pdf,
        it takes every image, convert into binary color format, i.e., black and white,
        and extracts text from the images using the read_text function.
        :param: filename as string containing path of a PDF file.
        :return: text extracted from the PDF file.
        '''

        # saving filename as dirName to create a directory of the same name as of the file
        dirName = self.filename.split("\\")[1].split(".")[0]

        # create a directory with name similar to filename and do nothing if an error is raised.
        try:
            os.mkdir(dirName)
        except:
            pass
        dirPath = "{}\\".format(dirName)

        # create images by random names of every page of the PDF within the created directory.
        convert_from_path(self.filename, output_folder=dirPath, fmt="png")

        # next method is used to iterate files within the directory, os.walk is used to scan
        # for files within a directory as we are only storing the filenames as imageNames,
        # the earlier underscores stores the root directory name and child directory names.
        # This will give us imageNames as a list of files inside the directory.
        (_, _, imageNames) = next(os.walk(dirPath))
        for i in imageNames:
            i = dirPath + i

            # creating an openCV object of the image to perform image processing operations
            a = cv.imread(i)

            # changing image from coloured to gray
            grayImage = cv.cvtColor(a, cv.COLOR_BGR2GRAY)

            # changing images threshold to convert the image to black and white only.
            (thresh, blackAndWhiteImage) = cv.threshold(grayImage, 127, 255, cv.THRESH_BINARY)
            name_2 = dirPath + "a.png"

            # creating black and white image on path
            cv.imwrite(name_2, blackAndWhiteImage)

            # fetching the text from the image using read_text function
            text = self.read_text(filename=name_2)

            # printing text of single image
            print(text)

            # Deleting b&w image from the directory
            os.unlink(name_2)

            # deleting gray image from the directory
            os.unlink(i)

        # removing the directory
        os.rmdir(dirName)

    def read_text(self, filename=None):
        """
        This function will handle the core OCR processing of images.
        :param: filename as string containing path of an image.
        :return: text extracted from the image.
        """
        if filename == None:
            filename = self.filename
        text = pytesseract.image_to_string(Image.open(filename))
        # We'll use Pillow's Image class to open the image and
        # pytesseract to detect the string in the image
        return text

# processing an individual image
filename = 'Images\\wordsworthwordle1.jpg'
file_text = OCR(filename)
print(file_text.read_text())
# or
# processing a PDF file
filename = 'Files\\cert.pdf'
file_text = OCR(filename)
print(file_text.split_pdf_and_convert_to_images())
