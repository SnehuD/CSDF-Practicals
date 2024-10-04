from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string

def generate_captcha(text, width=200, height=70, font_size=36):
    # Create an image with white background
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.truetype('arial.ttf', font_size)
    
    # Calculate text width and height to center the text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    # Draw the text on the image
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    # Add noise
    for _ in range(1000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Add background patterns
    for _ in range(10):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=2)

    # Apply a blur filter to make it harder to read
    image = image.filter(ImageFilter.GaussianBlur(1))

    return image

def verify_captcha(input_text, captcha_text):
    return input_text == captcha_text

if __name__ == "__main__":
    # Generate a random CAPTCHA text
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    # Generate CAPTCHA image
    captcha_image = generate_captcha(captcha_text)
    captcha_image.show()

    # Simulate user input
    user_input = input("Enter the CAPTCHA text: ")

    # Verify CAPTCHA
    if verify_captcha(user_input, captcha_text):
        print("CAPTCHA verification passed.")
    else:
        print("CAPTCHA verification failed.")
