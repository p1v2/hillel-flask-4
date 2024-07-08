from datetime import datetime
import platform


def hello():
    print("initialization")
    print("Hello world!")
    print(datetime.now())
    # Print operation system version
    print(platform.platform())
    # print day of week
    print(datetime.now().strftime("%A"))
    print("Goodbye")


if __name__ == "__main__":
    hello()
