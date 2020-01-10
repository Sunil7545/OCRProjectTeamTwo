import os

try:
    from PIL import Image, ImageChops, ImageDraw
except ImportError:
    import Image, ImageChops, ImageDraw
import pytesseract
from pdf2image import convert_from_path
import tempfile

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class OCR:

    def __init__(self, filename):
        self.filename = filename

    def split_pdf_and_convert_to_images(self):
        cwd = os.getcwd()
        dirName = self.filename.split("\\")[1].split(".")[0]
        try:
            os.mkdir(dirName)
        except:
            pass
        dirPath = "{}\\".format(dirName)
        # dirPath = "{0}\\{1}\\".format(cwd, dirName)
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(self.filename, output_folder=dirPath)

        (_, _, imageNames) = next(os.walk(dirPath))
        for i in imageNames:
            image_i = Image.open(dirPath + i)
            name = dirPath + i.split('.')[0] + '.png'
            image_i.save(name)
            # image_i.close()
            # os.remove(dirPath + i)
            text = self.read_text(filename=name)
            print(text)

    def read_text(self, filename=None):
        """
        This function will handle the core OCR processing of images.
        """

        if filename == None:
            filename = self.filename
        text = pytesseract.image_to_string(Image.open(filename))
        # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
        return text


filename = 'Images\\wordsworthwordle1.jpg'
file_text = OCR(filename)
print(file_text.read_text())
# or
filename = 'Files\\0a16ef09-1a7d-4d25-afd5-31ed8096409c-160313082428.pdf'
file_text = OCR(filename)
print(file_text.split_pdf_and_convert_to_images())
