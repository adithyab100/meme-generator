from .image_generator import ImageGenerator
from .text_overlay import TextOverlay
from .trend_analyzer import TrendAnalyzer
import os

class MemeComposer:
    def __init__(self, config):
        self.config = config
        self.image_generator = ImageGenerator(config.IMAGE_MODEL)
        self.text_overlay = TextOverlay()
        self.trend_analyzer = TrendAnalyzer(config)
        
        if not os.path.exists(config.OUTPUT_DIR):
            os.makedirs(config.OUTPUT_DIR)
    
    def generate_meme(self, topic: dict):
        """Generate a meme based on a trending topic."""
        # Generate base image
        prompt = f"meme style image about {topic['title']}"
        image = self.image_generator.generate_image(prompt)
        
        # Add text overlay
        image_with_text = self.text_overlay.add_text(image, topic['title'])
        
        # Save meme
        output_path = os.path.join(
            self.config.OUTPUT_DIR,
            f"meme_{topic['title'][:30]}.png"
        )
        image_with_text.save(output_path)
        return output_path
