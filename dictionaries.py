import random
from datetime import datetime

class ProfileGenerator:
    def __init__(self):
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.dob_day = ""
        self.dob_month = ""
        self.dob_year = ""
        self.location = ""
        self.interest = ""
        self.person_of_interest = ""
        
        # Sample dictionaries for simulation
        self.common_passwords = ["password", "123456", "qwerty", "letmein"]
        self.common_locations = ["NYC", "LA", "London", "Chennai"]
        self.categories = {
            "Music": ["rock", "pop", "jazz"],
            "Art": ["painting", "sketch"],
            "AutoMobile": ["car", "bike", "ferrari"],
            "Cosmetics": ["lakme", "maybelline"]
        }

    def get_basic_info(self):
        self.first_name = input("Enter First Name (press Enter to skip): ").strip()
        self.middle_name = input("Enter Middle Name (press Enter to skip): ").strip()
        self.last_name = input("Enter Last Name (press Enter to skip): ").strip()
        self.dob_day = input("Enter Day of Birth (press Enter to skip): ").strip()
        self.dob_month = input("Enter Month of Birth (press Enter to skip): ").strip()
        self.dob_year = input("Enter Year of Birth (press Enter to skip): ").strip()
        self.location = input("Enter Location (press Enter to skip): ").strip()
        self.interest = input("Enter Interest Category (press Enter to skip): ").strip()
        self.person_of_interest = input("Enter Person of Interest (press Enter to skip): ").strip()

    def simulate_api_call(self, query_type):
        # Simulated API response - in real implementation, this would call actual APIs
        if query_type == "location":
            return random.choice(self.common_locations) if not self.location else self.location
        elif query_type == "interest":
            return random.choice(list(self.categories.keys())) if not self.interest else self.interest
        elif query_type == "person":
            names = ["Rose", "John", "Emma", "Mike"]
            return random.choice(names)
        return ""

    def generate_usernames(self):
        usernames = []
        base_name = self.first_name.lower()
        if self.middle_name:
            base_name += self.middle_name.lower()
        if self.last_name:
            base_name += self.last_name.lower()
            
        # Basic variations
        if base_name:
            usernames.append(base_name)
            if self.dob_year:
                usernames.append(base_name + self.dob_year)
            if self.location:
                usernames.append(base_name + self.location.lower())
            if self.person_of_interest:
                usernames.append(base_name + self.person_of_interest.lower())
                
        return usernames

    def generate_passwords(self):
        passwords = []
        base_name = self.first_name.lower()
        
        # Basic combinations
        if base_name:
            passwords.append(base_name)
            if self.dob_year:
                passwords.append(base_name + self.dob_year)
                passwords.append(self.dob_year + base_name)
            
            # Location-based
            location = self.simulate_api_call("location")
            passwords.append(base_name + location.lower())
            passwords.append(location.lower() + base_name)
            
            # Interest-based
            interest = self.simulate_api_call("interest")
            if interest in self.categories:
                specific = random.choice(self.categories[interest])
                passwords.append(base_name + specific)
                passwords.append(specific + base_name)
                
            # Person of interest
            person = self.simulate_api_call("person")
            passwords.append(base_name + "loves" + person.lower())
            passwords.append(person.lower() + "loves" + base_name)
            
            # Common passwords with name
            for common in self.common_passwords:
                passwords.append(base_name + common)
                passwords.append(common + base_name)

        return passwords

    def save_to_files(self, usernames, passwords):
        with open("usernames.txt", "a") as u_file:
            for username in usernames:
                u_file.write(username + "\n")
                
        with open("passwords.txt", "a") as p_file:
            for password in passwords:
                p_file.write(password + "\n")

def main():
    generator = ProfileGenerator()
    print("Enter target information (press Enter to skip any field):")
    generator.get_basic_info()
    
    usernames = generator.generate_usernames()
    passwords = generator.generate_passwords()
    
    generator.save_to_files(usernames, passwords)
    print(f"\nGenerated {len(usernames)} usernames and {len(passwords)} passwords")
    print("Data appended to usernames.txt and passwords.txt")

if __name__ == "__main__":
    main()
