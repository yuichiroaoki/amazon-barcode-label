#!/usr/bin/env python3
from PIL import Image
from pdf2image import convert_from_path
import sys


pdf_filename = sys.argv[1]
print_start_index = int(sys.argv[2])
product_count = int(sys.argv[3])

# convert amazonsell2.pdf to images
def convert_pdf_to_images(pdf_path):
	images = convert_from_path(pdf_path)
	for i, image in enumerate(images):
		image.save(f"output_{i}.png", "PNG")


# divide the iamge into 40 parts(4 columns and 10 rows)
def divide_image(image_path):
	image = Image.open(image_path)
	width, height = image.size
	label_width = width // 4
	label_height = height // 10
	labels = []
	for j in range(4):
		for i in range(10):
			x = j * label_width
			y = i * label_height
			labels.append(image.crop((x, y, x + label_width, y + label_height)))
	return labels

# create a new image from the labels
def create_new_image(labels):
	width, height = labels[0].size
	new_image = Image.new("RGB", (width * 4, height * 10))
	# paste white background
	new_image.paste((255, 255, 255), (0, 0, width * 4, height * 10))

	for i, label in enumerate(labels):
		new_idx = i + print_start_index
		x = (new_idx // 10) * width
		y = (new_idx % 10) * height
		new_image.paste(label, (x, y))
	new_image.save("new_image.png", "PNG")

convert_pdf_to_images(pdf_filename)

# divide the image into 40 parts
labels = divide_image("output_0.png")
assert len(labels) == 40
labels = labels[:product_count]
create_new_image(labels)