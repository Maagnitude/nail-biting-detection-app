import sys
from validate_email import validate_email
from tools.nail_biting_detection import NailBitingDetection

if __name__ == '__main__':
    if len(sys.argv) > 1:
        receiver_email = sys.argv[1]
        if not validate_email(receiver_email):
            print("Invalid email address!")
            sys.exit(1)
        else:
            username = input("Enter your email address: ")
            password = input("Enter your email password: ")
            email_dict = {
                "username": username,
                "password": password,
                "receiver_email": receiver_email
            }
    else:
        email_dict = None
        
    nbd = NailBitingDetection()
    nbd.detect(email_dict)