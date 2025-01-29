# AI Meme Generator

An AI-powered meme generator that creates images based on trending Reddit meme text. The generator uses Stable Diffusion to interpret the meme text and generate a relevant, custom image that captures the essence of the meme. Optimized for multiple compute platforms including NVIDIA GPUs (CUDA), Apple Silicon (MPS), and CPU.

## Features

- Fetches trending meme text from Reddit
- Generates contextually relevant images using Stable Diffusion
- Automatic device selection (CUDA > MPS > CPU)
- Efficient image generation with customizable number of inference steps
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
git clone https://github.com/adithyab100/meme-generator.git
cd meme-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Model Setup

This project uses the Stable Diffusion v1.4 model from CompVis, hosted on Hugging Face. To use the model:

1. Create a Hugging Face account at [huggingface.co](https://huggingface.co)
2. Accept the model license at [CompVis/stable-diffusion-v1-4](https://huggingface.co/CompVis/stable-diffusion-v1-4)
3. Create a Hugging Face token:
   - Go to Settings → Access Tokens
   - Create a new token with read access
   - Set the token as an environment variable:
     ```bash
     export HUGGING_FACE_HUB_TOKEN=your_token_here
     ```
   - Or add it to your .env file:
     ```env
     HUGGING_FACE_HUB_TOKEN=your_token_here
     ```

The model will be automatically downloaded on first use. The default configuration uses:
- Model: CompVis Stable Diffusion v1.4
- Resolution: 512x512
- Inference Steps: 40 (customizable)
- Guidance Scale: 7.5

You can modify these parameters in `config.py` or pass them directly when calling `generate_image()`.

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
image_gen = ImageGenerator("CompVis/stable-diffusion-v1-4")
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
