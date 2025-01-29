# AI Meme Generator

An AI-powered meme generator that creates images based on trending Reddit meme text. The generator uses Stable Diffusion to interpret the meme text and generate a relevant, custom image that captures the essence of the meme. Optimized for multiple compute platforms including NVIDIA GPUs (CUDA), Apple Silicon (MPS), and CPU.

## Features

- Fetches trending meme text from Reddit
- Generates contextually relevant images using Stable Diffusion
- Automatic device selection (CUDA > MPS > CPU)
- Efficient image generation with 30 inference steps
- Text overlay with system font detection
- White text with black outline for readability
- Memory-efficient operations on all platforms

## How it Works

1. Fetches trending meme text from Reddit
2. Uses the meme text to generate a relevant image using Stable Diffusion
3. Overlays the original meme text on the generated image
4. Creates a unique, AI-generated interpretation of trending memes


## Installation and Requirements

1. Clone the repository:
```bash
git clone https://github.com/yourusername/meme-generator.git
cd meme-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Automated Reddit Meme Generation

The main script automatically fetches trending meme topics from Reddit and generates corresponding images:

```bash
python main.py
```

This will:
1. Initialize the MemeComposer with your configuration
2. Fetch trending topics from Reddit using the trend analyzer
3. Generate an AI image interpretation for each trending topic
4. Add the original text as overlay
5. Save the generated memes in your configured output directory

The process is handled by the MemeComposer class, which orchestrates:
- Trend analysis from Reddit
- Image generation with Stable Diffusion
- Text overlay and final composition

### Custom Meme Generation

You can also generate memes from your own prompts:

```python
from src.image_generator import ImageGenerator
from src.text_overlay import TextOverlay

# Initialize generators
image_gen = ImageGenerator("runwayml/stable-diffusion-v1-5")
text_overlay = TextOverlay()

# Generate a custom meme
prompt = "A cat in a business suit making a presentation"
text = "When the intern gives better suggestions than the CEO"

# Generate and save
image = image_gen.generate_image(prompt)
meme = text_overlay.add_text(image, text)
meme.save("custom_meme.png")
```

### Environment Setup

For Reddit functionality, you'll need to set up your Reddit API credentials in a `.env` file:

```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

You can obtain these credentials by creating an application at [Reddit's App Preferences](https://www.reddit.com/prefs/apps).

## Device Support

The generator automatically selects the best available compute device:
- NVIDIA GPUs (CUDA)
- Apple Silicon (MPS)
- CPU (fallback)

## Contributing

Feel free to open issues or submit pull requests with improvements.
