from datetime import datetime


def hello():
    print("initialization")
    # Input username
    username = input("Enter your name: ")
    print(f"Hello {username}!")
    print(datetime.now())
    # Print current timezone
    print(datetime.now().astimezone().tzinfo)
    # print day of week
    print(datetime.now().strftime("%A"))
    print("Goodbye")


if __name__ == "__main__":
    hello()
