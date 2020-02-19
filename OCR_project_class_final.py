"""
This program will convert PDFs into images and read text from those images
and print the text over the screen.
This can also extract text directly from images and print it out.
"""


import os

# try is used to keep a check over the import. If there is an error, it will not close
# the program, but instead execute the except statement, similar to if & else.
from PIL import Image

# extracts text from images
import pytesseract

# convert pdf into images
from pdf2image import convert_from_path

# image processing library
import cv2 as cv
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class OCR:

    """
    OCR class to process PDFs and images to extract text from them.
    """

    def __init__(self, filename):

        """
        Initializes the memory of the object as the object is created using the parent class.

        :param filename: string parameter to save the path and name of the file.
        """

        self.filename = filename
        # self.key_word = key_word

    def split_pdf_and_convert_to_images(self):

        """
        A method of OCR class that takes pdf file and path as the input parameter
        and split the pdf into multiple images. After splitting the pdf,
        it takes every image, convert into binary color format, i.e., black and white,
        and extracts text from the images using the read_text function.

        :param: filename as string containing path of a PDF file.
        :return: text extracted from the PDF file.
        """

        # saving filename as dirName to create a directory of the same name as of the file
        dir_name = self.filename.split("\\")[1].split(".")[0]

        # create a directory with name similar to filename and do nothing if an error is raised.
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            pass
        dir_path = "{}\\".format(dir_name)

        # create images by random names of every page of the PDF within the created directory.
        convert_from_path(self.filename, output_folder=dir_path, fmt="png")

        # next method is used to iterate files within the directory, os.walk is used to scan
        # for files within a directory as we are only storing the file names as imageNames,
        # the earlier underscores stores the root directory name and child directory names.
        # This will give us imageNames as a list of files inside the directory.

        (_, _, imageNames) = next(os.walk(dir_path))
        for i in imageNames:
            i = dir_path + i

            # creating an openCV object of the image to perform image processing operations
            a = cv.imread(i)

            # changing image from coloured to gray
            gray_image = cv.cvtColor(a, cv.COLOR_BGR2GRAY)

            # changing images threshold to convert the image to black and white only.
            (thresh, blackAndWhiteImage) = cv.threshold(gray_image, 127, 255, cv.THRESH_BINARY)
            name_2 = dir_path + "a.png"

            # creating black and white image on path
            cv.imwrite(name_2, blackAndWhiteImage)

            # fetching the text from the image using read_text function
            self.filename = name_2
            text = self.read_text()

            # printing text of single image
            print(text)

            # Deleting b&w image from the directory
            os.unlink(name_2)

            # deleting gray image from the directory
            os.unlink(i)

        # removing the directory
        os.rmdir(dir_name)

    def read_text(self):
        """
        This function will handle the core OCR processing of images.
        :param: filename as string containing path of an image.
        :return: text extracted from the image.
        """

        text = pytesseract.image_to_string(Image.open(self.filename))
        string_text = text.split()
        return string_text

    @staticmethod
    def text_frequency(text_data, key_word):
        """

        :param text_data:
        :param key_word:
        :return:
        """

        return text_data.count(key_word)

    @staticmethod
    def neighbour_check(text_data, key_word):
        """

        :param text_data:
        :param key_word:
        :return:
        """
        neighbour_elements = []
        for i in range(len(text_data)):
            if text_data[i] == key_word:
                neighbour_back, neighbour_next = text_data[i-1], text_data[i+1]
                neighbour_elements.append([neighbour_back, neighbour_next])
        return neighbour_elements


# processing an individual image
full_path = filedialog.askopenfilename()

# enter the key word
print('Enter the keyword: ')
input_key = input()

# create an object of the OCR class
ocr_info = OCR(full_path)
file_text = ocr_info.read_text()

# check the frequency of input key
occurrence = ocr_info.text_frequency(file_text, input_key)

if occurrence == 0:
    print("Either entered keyword is wrong or input image quality is too bad")
elif occurrence == 1:
    print("Entered keyword is matched, input document is verified")
else:
    print("Multiple occurrence of the keyword, please check the following outcome tobe sure: ")
    print(ocr_info.neighbour_check(file_text, input_key))

