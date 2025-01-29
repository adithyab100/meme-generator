from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple

class TextOverlay:
    def __init__(self, font_path: str = None):
        # Try to find a suitable system font
        if font_path:
            self.font_path = font_path
        else:
            # Common font locations on different systems
            font_locations = [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",  # macOS
                "/System/Library/Fonts/Helvetica.ttc",  # macOS alternative
                "/Library/Fonts/Arial Bold.ttf",  # macOS user fonts
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
                "C:\\Windows\\Fonts\\arial.ttf"  # Windows
            ]
            
            for font in font_locations:
                if os.path.exists(font):
                    self.font_path = font
                    break
            else:
                # If no specific font is found, use default
                self.font_path = None

    def _get_font_size(self, text: str, image_width: int, draw: ImageDraw.ImageDraw) -> ImageFont.FreeTypeFont:
        """Calculate the optimal font size to fit text within image width."""
        target_width = image_width * 0.9  # Leave some margin
        size = 40  # Start with size 40
        
        try:
            if self.font_path:
                font = ImageFont.truetype(self.font_path, size=size)
            else:
                return ImageFont.load_default()
                
            # Binary search for the right font size
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= target_width:
                # Try larger sizes
                while text_width <= target_width and size <= 100:
                    size += 5
                    font = ImageFont.truetype(self.font_path, size=size)
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                size -= 5  # Go back one step
            else:
                # Try smaller sizes
                while text_width > target_width and size >= 20:
                    size -= 5
                    font = ImageFont.truetype(self.font_path, size=size)
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
            
            return ImageFont.truetype(self.font_path, size=size)
        except Exception as e:
            print(f"Error calculating font size: {str(e)}, using default")
            return ImageFont.load_default()

    def add_text(self, image: Image.Image, text: str, position: Tuple[int, int] = None):
        """Add text overlay to image with automatic font sizing."""
        draw = ImageDraw.Draw(image)
        
        # Get font with appropriate size
        font = self._get_font_size(text, image.width, draw)
        
        if position is None:
            # Calculate vertical position (20% from top)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_height = bbox[3] - bbox[1]
            x = (image.width - (bbox[2] - bbox[0])) // 2  # Center horizontally
            y = int(image.height * 0.2)  # 20% from top
            position = (x, y)
        
        # Add white text with black outline for readability
        x, y = position
        outline_width = max(1, font.size // 25)  # Scale outline with font size
        
        # Draw outline
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx*dx + dy*dy <= outline_width*outline_width:  # Circular outline
                    draw.text((x+dx, y+dy), text, font=font, fill='black')
        
        # Draw main text
        draw.text((x, y), text, font=font, fill='white')
        
        return image