class InventoryItem:
    def __init__(
        self,
        sku,
        supplier,
        stock,
        daily_demand,
        lead_time,
        safety_stock
    ):
        self.sku = sku
        self.supplier = supplier
        self.stock = stock
        self.daily_demand = daily_demand
        self.lead_time = lead_time
        self.safety_stock = safety_stock

    def reorder_point(self):
        return (
            self.daily_demand *
            self.lead_time
        ) + self.safety_stock

    def recommended_order_quantity(self):
        target_stock = (
            self.daily_demand * 30
        ) + self.safety_stock

        quantity = target_stock - self.stock

        if quantity < 0:
            return 0

        return quantity

    def needs_reorder(self):
        return self.stock <= self.reorder_point()

    def status(self):
        if self.needs_reorder():
            return "REORDER REQUIRED"

        return "STOCK LEVEL OK"

    def display(self):
        print("\n------------------------------")
        print(f"SKU: {self.sku}")
        print(f"Supplier: {self.supplier}")
        print(f"Current Stock: {self.stock}")
        print(f"Daily Demand: {self.daily_demand}")
        print(f"Lead Time: {self.lead_time} days")
        print(f"Safety Stock: {self.safety_stock}")
        print(f"Reorder Point: {self.reorder_point()}")
        print(
            f"Recommended Order: "
            f"{self.recommended_order_quantity()}"
        )
        print(f"Status: {self.status()}")
        print("------------------------------")


def get_positive_int(prompt):
    while True:

        try:
            value = int(input(prompt))

            if value < 0:
                print(
                    "Value cannot be negative."
                )
                continue

            return value

        except ValueError:
            print(
                "Please enter a valid number."
            )


def get_non_empty(prompt):

    while True:

        value = input(prompt).strip()

        if value == "":
            print(
                "Input cannot be empty."
            )
            continue

        return value


class InventoryManager:

    def __init__(self):
        self.items = []

    def add_item(self):

        print("\nADD NEW SKU")

        sku = get_non_empty("SKU: ")

        for item in self.items:

            if item.sku.lower() == sku.lower():

                print(
                    "SKU already exists."
                )
                return

        supplier = get_non_empty(
            "Supplier: "
        )

        stock = get_positive_int(
            "Current Stock: "
        )

        demand = get_positive_int(
            "Daily Demand: "
        )

        lead = get_positive_int(
            "Lead Time (days): "
        )

        safety = get_positive_int(
            "Safety Stock: "
        )

        item = InventoryItem(
            sku,
            supplier,
            stock,
            demand,
            lead,
            safety
        )

        self.items.append(item)

        print(
            "\nSKU added successfully."
        )

    def show_inventory(self):

        if len(self.items) == 0:

            print(
                "\nInventory is empty."
            )
            return

        print("\n===== INVENTORY =====")

        for item in self.items:
            item.display()