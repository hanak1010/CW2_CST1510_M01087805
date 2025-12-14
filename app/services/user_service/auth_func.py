# Hana Mundambra
# M01087805

import bcrypt
import string
from app.data.db import connect_database

# Strength check class
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

# Helper functions

# Hashing the plain-text password
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Decode the hash back to a string to store in a text file
    return hashed_password.decode('utf-8')      

# Verifying the password (if it matches or not)
def verify_password(plain_text_password, hashed_password):
    # Encode both the plaintext password and stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # bcrypt.checkpw handles extracting the salt and comparing
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

# Validate the username
def validate_username(username):
    if username == "":
        return(False, "Username should not be empty")
    elif len(username) < 3:
        return(False, "Username should be atleast 3 characters long") 
    elif " " in username:
        return (False, "Username cannot contain spaces")
    return(True,"Username validation successful")

# Validate the password
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


# REGISTER FUNCTION
def register_user(username, password, role="user"):
    """
    Register a new user in the database.
    """
    conn = connect_database()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."
    
    # Validating username and password using week 07 functions
    is_valid, msg = validate_username(username)
    if not is_valid:
        return False, msg
    
    is_valid, msg = validate_password(password)
    if not is_valid:
        return False, msg
    
    # Check password strength
    strength = Passwordstrength(password).check_strength()
    if strength == "Weak":
        return False, "Password is too weak!"
    
    # Hash the password
    password_hashed = hash_password(password)
    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hashed, role)
    )
    conn.commit()
    conn.close()

    return True, f"User '{username}' registered successfully!"

# LOGIN FUNCTION
def login_user(username, password):
    """
    Authenticate a user against the database.

    This is a COMPLETE IMPLEMENTATION as an example.

    Args:
        username: User's login name
        password: Plain text password to verify

    Returns:
        tuple: (success: bool, message: str)
    """
    conn = connect_database()
    cursor = conn.cursor()

    # Find user
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "Username not found."

    # Verify password (user[2] is password_hash column)
    stored_hash = user[2]
    if verify_password(password, stored_hash):
        return True, f"Welcome, {username}!"
    else:
        return False, "Invalid password."