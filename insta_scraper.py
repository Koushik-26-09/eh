import instaloader
from collections import Counter
import re
from datetime import datetime

class InstagramScraper:
    def __init__(self):
        # Initialize Instaloader with anonymous session
        self.L = instaloader.Instaloader()
        self.username = ""
        self.profile = None

    def get_profile(self, username):
        try:
            self.username = username
            self.profile = instaloader.Profile.from_username(self.L.context, username)
            print(f"Successfully loaded profile: {username}")
            return True
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"Profile {username} does not exist")
            return False
        except Exception as e:
            print(f"Error loading profile: {str(e)}")
            return False

    def get_location(self):
        # Instagram doesn't directly provide location unless in posts
        locations = []
        try:
            for post in self.profile.get_posts():
                if post.location:
                    locations.append(post.location.name)
                if len(locations) >= 3:  # Limit to first few posts
                    break
            return locations[0] if locations else "Not available"
        except Exception:
            return "Not available"

    def get_full_name(self):
        try:
            return self.profile.full_name if self.profile.full_name else "Not available"
        except Exception:
            return "Not available"

    def get_birth_date(self):
        # Instagram doesn't provide birth date directly
        # We'll look for patterns in bio or posts (very unreliable)
        bio = self.profile.biography.lower()
        
        # Common date patterns
        patterns = [
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',  # dd/mm/yyyy or dd-mm-yyyy
            r'born on (\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',
            r'(\d{1,2})(?:st|nd|rd|th)? (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* (\d{2,4})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, bio)
            if match:
                if len(match.groups()) == 3:
                    day, month, year = match.groups()
                    return day, month, year
        return "Not available", "Not available", "Not available"

    def get_interests(self):
        try:
            # Collect captions from posts
            captions = []
            for post in self.profile.get_posts():
                if post.caption:
                    captions.extend(post.caption.lower().split())
                if len(captions) > 1000:  # Limit word count
                    break
            
            # Remove common words and get most common keywords
            stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'you', 'your', 'yours', 
                         'he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its', 'they', 'them', 
                         'their', 'what', 'which', 'who', 'whom', 'this', 'that', 'a', 'an', 'the',
                         'and', 'but', 'if', 'or', 'because', 'as', 'at', 'by', 'for', 'with'}
            
            # Filter words
            words = [word.strip('#.,!?') for word in captions 
                    if word and word not in stop_words and len(word) > 3]
            
            # Get 3 most common words
            word_counts = Counter(words)
            top_interests = [word for word, count in word_counts.most_common(3)]
            return top_interests if top_interests else ["Not available"]
        except Exception:
            return ["Not available"]

    def scrape_profile(self):
        username = input("Enter Instagram username to scrape: ").strip()
        if not self.get_profile(username):
            return

        # Gather all details
        location = self.get_location()
        full_name = self.get_full_name()
        day, month, year = self.get_birth_date()
        interests = self.get_interests()

        # Display results
        print("\nScraped Information:")
        print(f"Full Name: {full_name}")
        print(f"Location: {location}")
        print(f"Date of Birth:")
        print(f"  Day: {day}")
        print(f"  Month: {month}")
        print(f"  Year: {year}")
        print("Top 3 Interests:")
        for i, interest in enumerate(interests, 1):
            print(f"  {i}. {interest}")

def main():
    scraper = InstagramScraper()
    scraper.scrape_profile()

if __name__ == "__main__":
    main()
