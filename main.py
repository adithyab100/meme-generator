from src.meme_composer import MemeComposer
from config import Config

def main():
    config = Config()
    composer = MemeComposer(config)
    
    # Get trending topics
    trends = composer.trend_analyzer.get_trending_topics()
    
    # Generate memes for each trending topic
    for trend in trends:
        try:
            output_path = composer.generate_meme(trend)
            print(f"Generated meme: {output_path}")
        except Exception as e:
            print(f"Error generating meme for {trend['title']}: {str(e)}")

if __name__ == "__main__":
    main()