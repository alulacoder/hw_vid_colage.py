import os
import cv2
import random
import shutil
from PIL import Image, ImageOps

# Set the directory where your images are located
original_path = "/Users/Alula/Desktop/py game folder/open_cv/image/imgvid"
temp_path = os.path.join(original_path, "temp_effects")

# Create a temporary folder for edited images
if os.path.exists(temp_path):
    shutil.rmtree(temp_path)
os.makedirs(temp_path)

# Get all image files
images = [file for file in os.listdir(original_path) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Calculate average width and height
mean_width = 0
mean_height = 0
num_of_images = len(images)

for file in images:
    img = Image.open(os.path.join(original_path, file))
    width, height = img.size
    mean_width += width
    mean_height += height

mean_width //= num_of_images
mean_height //= num_of_images

# Resize and apply effects to each image
for file in images:
    img = Image.open(os.path.join(original_path, file)).resize((mean_width, mean_height), Image.LANCZOS)

    effect = random.choice(['none', 'grayscale', 'invert', 'rotate'])

    if effect == 'grayscale':
        img = ImageOps.grayscale(img).convert('RGB')
    elif effect == 'invert':
        img = ImageOps.invert(img.convert('RGB'))
    elif effect == 'rotate':
        angle = random.choice([15, -15, 30, -30])
        img = img.rotate(angle, expand=True, fillcolor='white')
        img = img.resize((mean_width, mean_height), Image.LANCZOS)

    # Save processed image to temp folder
    img.save(os.path.join(temp_path, file), 'JPEG', quality=95)
    print(f"{file} saved with effect: {effect}")

# Generate .mp4 video from processed images
def videoGenerator():
    video_name = "MyFirstVideo.mp4"
    os.chdir(temp_path)

    images = [img for img in os.listdir('.') if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
    images.sort()  # Sort alphabetically

    frame = cv2.imread(images[0])
    height, width, layers = frame.shape

    # Use mp4 codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # H.264 codec
    video = cv2.VideoWriter(os.path.join(original_path, video_name), fourcc, 1, (width, height))

    for image in images:
        video.write(cv2.imread(image))

    cv2.destroyAllWindows()
    video.release()
    print(f"✅ MP4 Video saved at: {os.path.join(original_path, video_name)}")

videoGenerator()
