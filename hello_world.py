from datetime import datetime


def hello():
    print("initialization")
    print("Hello world!")
    print(datetime.now())
    # print day of week
    print(datetime.now().strftime("%A"))
    print("Goodbye")


if __name__ == "__main__":
    hello()
