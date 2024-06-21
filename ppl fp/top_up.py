class Database: #singleton
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.data = []
        return cls._instance

    def add_transaction(self, transaction):
        self.data.append(transaction)

    def get_transactions(self):
        return self.data

class GameTopUpFacade: #facade
    def __init__(self):
        self.db = Database()

    def top_up(self, user, game, amount):
        transaction = {"user": user, "game": game, "amount": amount}
        self.db.add_transaction(transaction)
        print(f"Top up successful for {user} in game {game} with amount {amount}")

    def get_history(self):
        transactions = self.db.get_transactions()
        if transactions:
            for t in transactions:
                print(f"User: {t['user']}, Game: {t['game']}, Amount: {t['amount']}")
        else:
            print("No transaction history found.")

class State: #state
    def handle(self, context):
        pass

class NewState(State):
    def handle(self, context):
        context.state = ProcessingState()
        print("State changed from New to Processing")

class ProcessingState(State):
    def handle(self, context):
        context.state = CompletedState()
        print("State changed from Processing to Completed")

class CompletedState(State):
    def handle(self, context):
        print("Transaction is already completed")

class Context:
    def __init__(self, state):
        self.state = state

    def request(self):
        self.state.handle(self)

class TopUpModel:
    def __init__(self):
        self.facade = GameTopUpFacade()

    def add_top_up(self, user, game, amount):
        self.facade.top_up(user, game, amount)

    def get_history(self):
        self.facade.get_history()

class TopUpView:
    def display_message(self, message):
        print(message)

    def display_history(self, history):
        for record in history:
            print(f"User: {record['user']}, Game: {record['game']}, Amount: {record['amount']}")

class TopUpController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def top_up(self, user, game, amount):
        self.model.add_top_up(user, game, amount)
        self.view.display_message(f"Top up of {amount} for {user} in {game} is successful.")

    def show_history(self):
        history = self.model.get_history()
        if history:
            self.view.display_history(history)
        else:
            self.view.display_message("No transaction history found.")

def main():
    model = TopUpModel()
    view = TopUpView()
    controller = TopUpController(model, view)

    while True:
        print("\n1. Top Up")
        print("\n2. Show History")
        print("\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user = input("Enter user name: ")
            game = input("Enter game name: ")
            amount = input("Enter top-up amount: ")
            controller.top_up(user, game, amount)
        elif choice == '2':
            controller.show_history()
        elif choice == '3':
            print("Thank you")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
