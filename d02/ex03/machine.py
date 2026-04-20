
import random
from beverages import HotBeverage, Coffee, Tea, Chocolate, Cappuccino


class CoffeeMachine:

    def __init__(self):
        self.drinks = 0

    class EmptyCup(HotBeverage):
        name = "empty cup"
        price = 0.90

        def description(self):
            return "An empty cup?! Gimme my money back!"  
        
    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def repair(self):
        self.drinks = 0
    
    def serve(self, beverage_class):
        if self.drinks >= 10:
            raise CoffeeMachine.BrokenMachineException()

        if not isinstance(beverage_class, type) or not issubclass(beverage_class, HotBeverage):
            raise TypeError("serve() expects a HotBeverage subclass.")

        self.drinks += 1
        if random.choice([True, False]):
            return CoffeeMachine.EmptyCup()
        return beverage_class()


if __name__ == "__main__":
    machine = CoffeeMachine()
    orders = [Coffee, Tea, Chocolate, Cappuccino]

    def run_until_break(title):
        print(f"\n--- {title} ---")
        i = 0
        try:
            while True:
                drink_class = orders[i % len(orders)]
                served = machine.serve(drink_class)
                print(served)
                print()
                i += 1
        except CoffeeMachine.BrokenMachineException as err:
            print(err)

    run_until_break("Cycle 1")
    machine.repair()
    run_until_break("Cycle 2")


