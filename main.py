from datetime import datetime


class Emma:
    def __init__(self):
        self.name = "Emma"
        self.version = "0.1"
        self.creator = "Parzival"

    def boot(self):
        print("=" * 45)
        print(f"{self.name} AI")
        print(f"Version: {self.version}")
        print("=" * 45)
        print("STATUS : ONLINE")
        print(f"TIME   : {datetime.now().strftime('%H:%M:%S')}")
        print()
        print(f"Hello, {self.creator}.")
        print("I'm ready to assist you.")
        print("=" * 45)


if __name__ == "__main__":
    emma = Emma()
    emma.boot()