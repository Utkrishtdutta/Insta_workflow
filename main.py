import os
import requests
import torch
import random
import time
import schedule
import hashlib
import uuid
import hmac
from datetime import datetime
from dotenv import load_dotenv
from instagrapi import Client

# Load environment variables
load_dotenv()

# Instagram credentials
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

# Initialize Instagram client
cl = Client()


# Free AI text generation API (example using a hypothetical free API)
# You'd need to replace this with whatever free service you're using
def generate_ai_text(prompt="Create an inspirational quote"):
    """Generate text content using a free AI API"""
    url = "http://localhost:11434/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3.2",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["message"]["content"].split('"')[1]


# Function to create a simple image with text
# def create_image_with_text(text, filename="content.jpg"):
#     """
#     Create a simple image with text using Pillow
#     """
#     try:
#         from PIL import Image, ImageDraw, ImageFont
#         import textwrap
#         import random
#         import os
        
#         # Create directory for images if it doesn't exist
#         os.makedirs("images", exist_ok=True)
        
#         # Set full path for the image
#         filepath = os.path.join("images", filename)
        
#         # Define some background colors for variety
#         bg_colors = [
#             (73, 109, 137),   # Blue
#             (106, 153, 78),   # Green
#             (165, 105, 189),  # Purple
#             (214, 137, 16),   # Orange
#             (41, 128, 185),   # Bright Blue
#             (192, 57, 43),    # Red
#             (46, 64, 83)      # Dark Blue
#         ]
        
        # # Randomly choose a background color
        # bg_color = random.choice(bg_colors)
        
        # # Create a blank square image (1080x1080 is good for Instagram)
        # img = Image.new('RGB', (1080, 1080), color=bg_color)
        # draw = ImageDraw.Draw(img)
        
        # # Try to use a font, or default if not available
        # try:
        #     # Try some common system fonts that might be available
        #     common_fonts = ['Arial.ttf', 'Verdana.ttf', 'Tahoma.ttf', 'Georgia.ttf', 
        #                   'Times New Roman.ttf', 'Courier New.ttf', 'Helvetica.ttf']
            
        #     font = None
        #     for font_name in common_fonts:
        #         try:
        #             font = ImageFont.truetype(font_name, 65)
        #             break
        #         except IOError:
        #             continue
                    
        #     # If none of the fonts worked, use default
        #     if font is None:
        #         font = ImageFont.load_default()
        # except Exception:
        #     font = ImageFont.load_default()
        
        # # Word wrap the text to fit in the image
        # margin = 100
        # offset = 40
        # wrapped_text = textwrap.fill(text, width=30)  # Adjust width as needed
        
        # Calculate text position (centered)
        # Using the updated method for Pillow 10+
    #     left, top, right, bottom = draw.textbbox((0, 0), wrapped_text, font=font)
    #     text_width = right - left
    #     text_height = bottom - top
    #     position = ((1080 - text_width) / 2, (1080 - text_height) / 2)
        
    #     # Add a subtle shadow for readability
    #     shadow_color = tuple(max(0, c - 50) for c in bg_color)
    #     draw.text((position[0] + 3, position[1] + 3), wrapped_text, font=font, fill=shadow_color)
        
    #     # Draw the main text
    #     draw.text(position, wrapped_text, font=font, fill=(255, 255, 255))
        
    #     # Add a small attribution at the bottom
    #     attribution = "Daily AI • @" + INSTAGRAM_USERNAME
    #     attr_font = ImageFont.load_default()
    #     attr_left, attr_top, attr_right, attr_bottom = draw.textbbox((0, 0), attribution, font=attr_font)
    #     draw.text((20, 1080 - attr_bottom - 20), attribution, font=attr_font, fill=(255, 255, 255, 128))
        
    #     # Save the image
    #     img.save(filepath)
    #     print(f"Created image with text at {filepath}")
        
    #     return filepath
    # except Exception as e:
        # print(f"Error creating image: {e}")
        # # Try to create a very basic fallback image if PIL fails
        # try:
        #     from PIL import Image
        #     img = Image.new('RGB', (1080, 1080), color=(0, 0, 0))
        #     filepath = os.path.join("images", "fallback_" + filename)
        #     img.save(filepath)
        #     return filepath
        # except:
        #     print("Failed to create even a fallback image")
        #     return None

def create_image_with_text(text, filename="content.jpg"):
    """
    Create a simple image with very large, prominent text using Pillow
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        import textwrap
        import random
        import os
        
        # Create directory for images if it doesn't exist
        os.makedirs("images", exist_ok=True)
        
        # Set full path for the image
        filepath = os.path.join("images", filename)
        
        # Define some background colors for variety
        bg_colors = [
            (73, 109, 137),   # Blue
            (106, 153, 78),   # Green
            (165, 105, 189),  # Purple
            (214, 137, 16),   # Orange
            (41, 128, 185),   # Bright Blue
            (192, 57, 43),    # Red
            (46, 64, 83)      # Dark Blue
        ]
        
        # Randomly choose a background color
        bg_color = random.choice(bg_colors)
        
        # Create a blank square image (1080x1080 is good for Instagram)
        img = Image.new('RGB', (1080, 1080), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Calculate optimal font size based on text length
        text_length = len(text)
        
        # For very short texts, use extremely large font
        if text_length < 20:
            base_font_size = 200
            wrap_width = 15
        # For short texts, use very large font    
        elif text_length < 50:
            base_font_size = 180
            wrap_width = 18
        # For medium texts, use large font
        elif text_length < 100:
            base_font_size = 160
            wrap_width = 20
        # For longer texts, adjust font size accordingly
        elif text_length < 200:
            base_font_size = 140
            wrap_width = 22
        else:
            base_font_size = 120
            wrap_width = 25
        
        # Try to use a font, or default if not available
        try:
            # Try some common system fonts that might be available
            common_fonts = ['Arial.ttf', 'Verdana.ttf', 'Tahoma.ttf', 'Georgia.ttf', 
                          'Times New Roman.ttf', 'Courier New.ttf', 'Helvetica.ttf']
            
            main_font = None
            for font_name in common_fonts:
                try:
                    main_font = ImageFont.truetype(font_name, base_font_size)
                    break
                except IOError:
                    continue
                    
            # If none of the fonts worked, use default
            if main_font is None:
                main_font = ImageFont.load_default()
        except Exception:
            main_font = ImageFont.load_default()
        
        # Word wrap the text to fit in the image
        wrapped_text = textwrap.fill(text, width=wrap_width)
        
        # Calculate text position (centered)
        left, top, right, bottom = draw.textbbox((0, 0), wrapped_text, font=main_font)
        text_width = right - left
        text_height = bottom - top
        
        # Center text
        text_x = (1080 - text_width) / 2
        text_y = (1080 - text_height) / 2
        
        # Add a semi-transparent background rectangle behind text for better readability
        padding = 50  # Padding around text
        rectangle_coords = [
            text_x - padding,
            text_y - padding,
            text_x + text_width + padding,
            text_y + text_height + padding
        ]
        
        # Create semi-transparent background for text
        overlay_color = tuple(max(0, c - 40) for c in bg_color)
        draw.rectangle(rectangle_coords, fill=(*overlay_color, 180))
        
        # Add a visible shadow for better readability
        shadow_offset = 10
        shadow_color = (30, 30, 30)  # Darker shadow
        draw.text((text_x + shadow_offset, text_y + shadow_offset), 
                 wrapped_text, font=main_font, fill=shadow_color)
        
        # Draw the main text with bright white for maximum contrast
        draw.text((text_x, text_y), wrapped_text, font=main_font, fill=(255, 255, 255))
        
        # Add a small attribution at the bottom
        attribution = "Daily AI • @" + INSTAGRAM_USERNAME
        # Try to get a smaller font for attribution but still visible
        try:
            attr_font = None
            for font_name in common_fonts:
                try:
                    attr_font = ImageFont.truetype(font_name, 36)
                    break
                except IOError:
                    continue
            if attr_font is None:
                attr_font = ImageFont.load_default()
        except Exception:
            attr_font = ImageFont.load_default()
            
        attr_left, attr_top, attr_right, attr_bottom = draw.textbbox((0, 0), attribution, font=attr_font)
        
        # Make attribution more visible with a small dark rectangle
        attr_width = attr_right - attr_left
        attr_height = attr_bottom - attr_top
        attr_x = 20
        attr_y = 1080 - attr_height - 20
        
        # Draw attribution background
        draw.rectangle([attr_x - 5, attr_y - 5, attr_x + attr_width + 5, attr_y + attr_height + 5], 
                      fill=(0, 0, 0, 128))
        
        # Draw attribution text
        draw.text((attr_x, attr_y), attribution, font=attr_font, fill=(255, 255, 255))
        
        # Save the image
        img.save(filepath)
        print(f"Created image with text at {filepath}")
        
        return filepath
    except Exception as e:
        print(f"Error creating image: {e}")
        # Try to create a very basic fallback image if PIL fails
        try:
            from PIL import Image
            img = Image.new('RGB', (1080, 1080), color=(0, 0, 0))
            filepath = os.path.join("images", "fallback_" + filename)
            img.save(filepath)
            return filepath
        except:
            print("Failed to create even a fallback image")
            return None

def login_to_instagram():
    """Login to Instagram using the instagrapi client"""
    try:
        # Login to Instagram
        print(f"Logging in to Instagram as {INSTAGRAM_USERNAME}...")
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        print("Successfully logged in to Instagram")
        return True
    except Exception as e:
        print(f"Error logging in to Instagram: {e}")
        return False

def post_to_instagram(image_path, caption):
    """Post content to Instagram using instagrapi"""
    try:
        # Ensure we're logged in
        if not cl.user_id:
            logged_in = login_to_instagram()
            if not logged_in:
                return False
        
        # Upload the photo
        print(f"Uploading {image_path} to Instagram...")
        media = cl.photo_upload(
            path=image_path,
            caption=caption
        )
        
        print(f"Successfully posted to Instagram with caption: {caption}")
        print(f"Media ID: {media.id}")
        return True
            
    except Exception as e:
        print(f"Error posting to Instagram: {e}")
        
        # If posting failed due to login issues, try to login again
        if "login" in str(e).lower():
            print("Attempting to re-login...")
            login_success = login_to_instagram()
            if login_success:
                # Try posting again
                try:
                    media = cl.photo_upload(
                        path=image_path,
                        caption=caption
                    )
                    print(f"Successfully posted to Instagram after re-login")
                    return True
                except Exception as e2:
                    print(f"Error posting even after re-login: {e2}")
        
        return False

def generate_unique_filename():
    """Generate a unique filename for images"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    return f"content_{timestamp}_{random_str}.jpg"

def daily_post_job():
    """Daily job to generate and post content"""
    print(f"Running daily post job at {datetime.now()}")
    
    # First, try to login to Instagram
    if not login_to_instagram():
        print("Failed to login to Instagram. Skipping today's post.")
        return
    
    try:
        # 1. Generate AI content
        prompt_types = [
            "Create an inspirational quote about success",
            "Generate a motivational quote about perseverance",
            "Write a short philosophical thought about life",
            "Create a positive affirmation for today",
            "Write a mindful thought about being present"
        ]
        
        # Select a random prompt type
        selected_prompt = random.choice(prompt_types)
        ai_text = generate_ai_text(selected_prompt)
        
        # 2. Create an image with the text
        filename = generate_unique_filename()
        image_path = create_image_with_text(ai_text, filename)
        if not image_path:
            print("Failed to create image. Skipping post.")
            return
        
        # 3. Create a caption with hashtags
        hashtags = [
            "#motivation", "#inspiration", "#daily", "#quotes",
            "#thoughts", "#positivity", "#mindset", "#success",
            "#growth", "#wisdom", "#life", "#journey",
            "#goals", "#dream", "#believe", "#achieve"
        ]
        
        # Categories of hashtags for better engagement
        category_hashtags = {
            "success": ["#success", "#achieve", "#goals", "#winning", "#entrepreneur"],
            "motivation": ["#motivation", "#nevergiveup", "#hustle", "#grind", "#focus"],
            "mindfulness": ["#mindfulness", "#present", "#awareness", "#calm", "#peace"],
            "inspiration": ["#inspiration", "#inspire", "#creative", "#passion", "#purpose"]
        }
        
        # Add some category hashtags based on the content
        extra_hashtags = []
        for category, tags in category_hashtags.items():
            if category.lower() in ai_text.lower() or category.lower() in selected_prompt.lower():
                extra_hashtags.extend(random.sample(tags, min(2, len(tags))))
        
        # Combine general and category hashtags, taking 8-10 random ones
        all_hashtags = list(set(hashtags + extra_hashtags))  # Remove duplicates
        selected_hashtags = " ".join(random.sample(all_hashtags, min(random.randint(8, 10), len(all_hashtags))))
        
        caption = f"{ai_text}\n.\n.\n.\n{selected_hashtags}"
        
        # 4. Post to Instagram
        success = post_to_instagram(image_path, caption)
        
        if success:
            print(f"Successfully posted to Instagram at {datetime.now()}")
        else:
            print(f"Failed to post to Instagram at {datetime.now()}")
    
    except Exception as e:
        print(f"Error in daily post job: {e}")

def setup_scheduled_posting(times=None):
    """Set up scheduled posting at specific times daily"""
    if times is None:
        # Default posting times (best engagement times)
        times = ["08:00", "12:30", "17:45"]
    
    for time_to_post in times:
        schedule.every().day.at(time_to_post).do(daily_post_job)
        print(f"Scheduled daily posting at {time_to_post}")
    
    print(f"Instagram automation set up with {len(times)} daily posts")
    
    # Run continuously
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            print(f"Error in scheduler: {e}")
            time.sleep(300)  # Wait 5 minutes if there's an error

if __name__ == "__main__":
    print("Starting Instagram AI Content Automation")
    
    # Create required directories
    os.makedirs("images", exist_ok=True)
    
    # Option 1: For testing - Run a post immediately
    daily_post_job()
    
    # Option 2: Custom schedule with specific times
    # setup_scheduled_posting(["09:00", "18:00"])
    
    # Option 3: Default schedule (runs at optimized engagement times)
    # setup_scheduled_posting()