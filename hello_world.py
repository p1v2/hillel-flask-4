from datetime import datetime


def hello():
    print("=" * 10)
    print("initialization")
    # Input username
    username = input("Enter your name: ")
    print(f"Hello {username}!")
    print("=" * 10)
    print(datetime.now())
    # Print current timezone
    print(datetime.now().astimezone().tzinfo)
    # print day of week
    print(datetime.now().strftime("%A"))
    # print day of month
    print(datetime.now().strftime("%d"))
    print("Goodbye")
    print("end")
    print("=" * 10)


if __name__ == "__main__":
    hello()
