import bcrypt
import string

class Passwordstrength:
    common_passwords = [  "123456","123456789","12345","12345678","qwerty","abc123","password","111111","123123","admin","letmein","welcome","monkey","login","starwars","dragon","sunshine","football","princess","master"]
    def __init__(self, password):
        self.password = password
   
    def count_upper(self):
        return sum(1 for char in self.password if char.isupper())
    def count_lower(self):
        return sum(1 for char in self.password if char.islower())
    def count_digits(self):
        return sum(1 for char in self.password if char.isdigit())
    def count_special(self):
        return sum(1 for char in self.password if char in string.punctuation)
    def check_strength(self):
        if len(self.password) == 6:
            return "Weak"
        elif len(self.password) in range(7, 11):
            return "Moderate"
        elif len(self.password) > 11:
            return "Strong"
        elif self.count_upper() or self.count_lower() or self.count_digits() or self.count_special() == 1:
            return "Weak"
        elif self.count_upper() or self.count_lower() or self.count_digits() or self.count_special() in range(1,3):
            return "Moderate"
        elif self.count_upper() or self.count_lower() or self.count_digits() or self.count_special() > 3:
            return "Strong"
        elif self.password in self.common_passwords:
            return "Weak"
        
USER_DATA_FILE = "users.txt"
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Decode the hash back to a string to store in a text file
    return hashed_password.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    # Encode both the plaintext password and stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # bcrypt.checkpw handles extracting the salt and comparing
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def register_user(username, password, role="user"): 
    try:
        with open("users.txt", "r") as f:
            existing_users = [line.split(",")[0] for line in f.read().splitlines()]
    except FileNotFoundError:
        open("users.txt", "w").close()
        existing_users = []        
    if username in existing_users:
        print(f"Error: Username {username} already exists.")
        return False
    
    """Register a new user.""" 
    hashed_password = hash_password(password) 
    with open("users.txt", "a") as f: 
        f.write(f"{username},{hashed_password},{role}\n") 
    print(f"Success: User '{username}' registered successfully!.")
    return True

def user_exists(username):
    try:
        with open("users.txt", "r") as f:
            for line in f:
                stored_username = line.strip().split(",")[0]
                if stored_username == username:
                 return True
    except FileNotFoundError:
        return False

    return False
def login_user(username, password): 
    try:
        with open("users.txt" , "r") as f:
            for line in f.readlines():
                user, hashed_password, role = line.strip().split(',', 1) 
                if user == username:
                    if verify_password(password, hashed_password):
                        print(f"Success: Welcome, {username}!")
                        return role
                    else:
                        print("Invalid password or username, Please try again")
                        return False 
    except FileNotFoundError:
        print("No users are registered yet")
        return False

    print("Error: Username not found.")
    return False

def validate_username(username):
    if username == "":
        return(False, "Username should not be empty")
    elif len(username) < 3:
        return(False, "Username should be atleast 3 characters long") 
    elif " " in username:
        return (False, "Username cannot contain spaces")
    return(True,"Username validation successful")

def validate_password(password):
    if password == "":
        return(False, "Password should not be empty")
    elif len(password) < 6:
        return(False, "Password should not be less than 6 characters")
    elif not any(char.isupper() for char in password):
        return(False, "Password should contain atleast one uppercase letter")
    elif not any(char.islower() for char in password):
        return(False, "Password should contain atleast one lowercase letter")
    elif not any(char.isdigit() for char in password):
        return(False, "Password should contain atleast one number")
    elif not any(char in string.punctuation for char in password):
        return(False, "Password should contain atleast one special character")
    elif " " in password:
        return(False, "Error! Password cannot contain any spaces")
    return(True, "Password validation successful")


def display_menu():
 """Displays the main menu options."""
 print("\n" + "="*50)
 print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
 print(" Secure Authentication System")
 print("="*50)
 print("\n[1] Register a new user")
 print("[2] Login")
 print("[3] Exit")
 print("-"*50)
       
def main():
 """Main program loop."""
 print("\nWelcome to the Week 7 Authentication System!")

 while True:
    display_menu()
    choice = input("\nPlease select an option (1-3): ").strip()

    if choice == '1':
        # Registration flow
        print("\n--- USER REGISTRATION ---")
        username = input("Enter a username: ").strip()

        # Validate username
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            print(f"Error: {error_msg}")
            continue

        password = input("Enter a password: ").strip()
        
        strength_checker = Passwordstrength(password)
        strength = strength_checker.check_strength()
        if "Weak" in strength:
            print("Password is too weak")
            continue
        
        # Validate password
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            print(f"Error: {error_msg}")
            continue

        # Confirm password
        password_confirm = input("Confirm password: ").strip()
        if password != password_confirm:
            print("Error: Passwords do not match.")
            continue
        role = input("Please enter your role (user/admin/analyst)[default = user]: ").strip().lower()
        if role == "":
            role = "user"

        # Register the user
        register_user(username, password, role)

    elif choice == '2':
        # Login flow
        print("\n--- USER LOGIN ---")
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        # Attempt login
        role = login_user(username, password)
        if role:
            print(f"\nYou are now logged in as {role}.")

            # Optional: Ask if they want to logout or exit
            input("\nPress Enter to return to main menu.")

    elif choice == '3':
        # Exit
        print("\nThank you for using the authentication system.")
        print("Exiting...")
        break

    else:
        print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
  main()