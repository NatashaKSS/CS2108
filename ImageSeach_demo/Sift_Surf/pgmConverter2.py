from PIL import Image
import numpy


#from jpg to pgm
#Image.open("sample.jpg").save("sample.pgm")

#from pgm to jpg
Image.open("basmati.pgm").save("basmati.jpg")
Image.open("book.pgm").save("book.jpg")
Image.open("box.pgm").save("box.jpg")
Image.open("result.pgm").save("result.jpg")
Image.open("scene.pgm").save("scene.jpg")