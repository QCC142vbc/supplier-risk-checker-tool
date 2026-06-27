import json


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

        self.demand_history = []

    def forecast_demand(self, window=7):
        if not self.demand_history:
            return self.daily_demand

        data = self.demand_history[-window:]
        return sum(data) / len(data)

    def record_demand(self, value):
        self.demand_history.append(value)

        if len(self.demand_history) > 30:
            self.demand_history.pop(0)

    def reorder_point(self):
        return (self.forecast_demand() * self.lead_time) + self.safety_stock

    def recommended_order_quantity(self):
        target_stock = (self.daily_demand * 30) + self.safety_stock
        quantity = target_stock - self.stock

        return max(0, quantity)

    def needs_reorder(self):
        return self.stock <= self.reorder_point()

    def status(self):
        return "REORDER REQUIRED" if self.needs_reorder() else "STOCK LEVEL OK"

    def display(self):
        print("\n------------------------------")
        print(f"SKU: {self.sku}")
        print(f"Supplier: {self.supplier}")
        print(f"Current Stock: {self.stock}")
        print(f"Daily Demand: {self.daily_demand}")
        print(f"Forecast Demand: {self.forecast_demand():.2f}")
        print(f"Lead Time: {self.lead_time} days")
        print(f"Safety Stock: {self.safety_stock}")
        print(f"Reorder Point: {self.reorder_point()}")
        print(f"Recommended Order: {self.recommended_order_quantity()}")
        print(f"Status: {self.status()}")
        print("------------------------------")

    def to_dict(self):
        return {
            "sku": self.sku,
            "supplier": self.supplier,
            "stock": self.stock,
            "daily_demand": self.daily_demand,
            "lead_time": self.lead_time,
            "safety_stock": self.safety_stock
        }

    @staticmethod
    def from_dict(data):
        return InventoryItem(
            data["sku"],
            data["supplier"],
            data["stock"],
            data["daily_demand"],
            data["lead_time"],
            data["safety_stock"]
        )


def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid number.")


def get_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Cannot be empty.")
            continue
        return value


FILE_NAME = "inventory.json"


class InventoryManager:
    def __init__(self):
        self.items = []
        self.load_inventory()

    def add_item(self):
        print("\nADD NEW SKU")

        sku = get_non_empty("SKU: ")

        for item in self.items:
            if item.sku.lower() == sku.lower():
                print("SKU already exists.")
                return

        supplier = get_non_empty("Supplier: ")
        stock = get_positive_int("Current Stock: ")
        demand = get_positive_int("Daily Demand: ")
        lead = get_positive_int("Lead Time (days): ")
        safety = get_positive_int("Safety Stock: ")

        item = InventoryItem(sku, supplier, stock, demand, lead, safety)
        self.items.append(item)

        self.save_inventory()
        print("SKU added successfully.")

    def show_inventory(self):
        if not self.items:
            print("Inventory is empty.")
            return

        for item in self.items:
            item.display()

    def search_sku(self):
        sku = get_non_empty("Enter SKU: ")

        for item in self.items:
            if item.sku.lower() == sku.lower():
                item.display()
                return

        print("SKU not found.")

    def update_stock(self):
        sku = get_non_empty("Enter SKU: ")

        for item in self.items:
            if item.sku.lower() == sku.lower():
                item.stock = get_positive_int("New Stock: ")
                self.save_inventory()
                print("Stock updated.")
                return

        print("SKU not found.")

    def remove_sku(self):
        sku = get_non_empty("Enter SKU: ")

        for item in self.items:
            if item.sku.lower() == sku.lower():
                self.items.remove(item)
                self.save_inventory()
                print("SKU removed.")
                return

        print("SKU not found.")

    def inventory_summary(self):
        print("\nSUMMARY")
        print(f"Total SKUs: {len(self.items)}")

        if not self.items:
            return

        total_stock = sum(i.stock for i in self.items)
        reorder_count = sum(1 for i in self.items if i.needs_reorder())

        print(f"Total Stock: {total_stock}")
        print(f"Reorders Needed: {reorder_count}")

    def reorder_report(self):
        print("\nREORDER REPORT")

        found = False

        for item in self.items:
            if item.needs_reorder():
                found = True
                print(f"{item.sku} | {item.recommended_order_quantity()} pcs")

        if not found:
            print("No products require reorder.")

    def abc_analysis(self):
        if not self.items:
            print("Inventory is empty.")
            return

        scored = []

        for item in self.items:
            value = item.daily_demand * 365 * item.stock
            scored.append((item, value))

        scored.sort(key=lambda x: x[1], reverse=True)

        total = sum(v for _, v in scored)

        if total == 0:
            print("No meaningful demand data.")
            return

        print("\nABC ANALYSIS")

        cumulative = 0

        for item, value in scored:
            cumulative += value
            ratio = cumulative / total

            if ratio <= 0.7:
                cat = "A"
            elif ratio <= 0.9:
                cat = "B"
            else:
                cat = "C"

            print(f"{item.sku} | {cat}")

    def supplier_summary(self):
        suppliers = {}

        for item in self.items:
            if item.supplier not in suppliers:
                suppliers[item.supplier] = {"sku": 0, "stock": 0, "reorders": 0}

            suppliers[item.supplier]["sku"] += 1
            suppliers[item.supplier]["stock"] += item.stock
            suppliers[item.supplier]["reorders"] += int(item.needs_reorder())

        for s, d in suppliers.items():
            print(f"\n{s}")
            print(d)

    def save_inventory(self):
        data = [i.to_dict() for i in self.items]

        with open(FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)

        print("Inventory saved.")

    def load_inventory(self):
        try:
            with open(FILE_NAME, "r") as f:
                data = json.load(f)

            self.items = [InventoryItem.from_dict(x) for x in data]

        except FileNotFoundError:
            self.items = []

    def generate_purchase_orders(self):
        print("\nPURCHASE ORDERS")

        supplier_map = {}

        for item in self.items:
            if item.needs_reorder():
                supplier_map.setdefault(item.supplier, []).append(item)

        if not supplier_map:
            print("No purchase orders needed.")
            return

        po_id = 1

        for supplier, items in supplier_map.items():
            print(f"\nPO-2026-{po_id:03d} | {supplier}")

            for item in items:
                print(f"- {item.sku} | {item.recommended_order_quantity()} pcs")

            po_id += 1

    def menu(self):
        while True:
            print("\n1 Add  2 View  3 Search  4 PO  5 Update  6 Remove")
            print("7 Summary 8 Reorder  9 Supplier  10 Save 11 Load 12 ABC 13 Exit")

            choice = input("> ")

            if choice == "1":
                self.add_item()
            elif choice == "2":
                self.show_inventory()
            elif choice == "3":
                self.search_sku()
            elif choice == "4":
                self.generate_purchase_orders()
            elif choice == "5":
                self.update_stock()
            elif choice == "6":
                self.remove_sku()
            elif choice == "7":
                self.inventory_summary()
            elif choice == "8":
                self.reorder_report()
            elif choice == "9":
                self.supplier_summary()
            elif choice == "10":
                self.save_inventory()
            elif choice == "11":
                self.load_inventory()
            elif choice == "12":
                self.abc_analysis()
            elif choice == "13":
                break


def main():
    InventoryManager().menu()


if __name__ == "__main__":
    main()