from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
    
    # Model configurations
    IMAGE_MODEL = "CompVis/stable-diffusion-v1-4"
    CAPTION_MODEL = "microsoft/git-base"
    
    # Output configurations
    OUTPUT_DIR = "generated_memes"
    IMAGE_SIZE = (512, 512)
