from PIL import Image

# Open the base image
img = Image.open("C:\\Users\\jhari\\Desktop\\data\\dedu\\test_image.jpeg")
# Save as different formats
img.save("test_image.jpg")
img.save("test_image.webp")

# Save a resized version
img.resize((img.width // 2, img.height // 2)).save("test_image_resized.png")