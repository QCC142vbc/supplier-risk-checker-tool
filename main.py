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
    
    def forecast_demand(self, window=7):
    if not self.demand_history:
        return self.daily_demand

    data = self.demand_history[-window:]

    return sum(data) / len(data)
    
    def record_demand(self, value):
    self.demand_history.append(value)

    # limit memory (last 30 days)
    if len(self.demand_history) > 30:
        self.demand_history.pop(0)
    
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

FILE_NAME = "inventory.json"
self.demand_history = []
class InventoryManager:

    def __init__(self):
        self.items = []
        self.load_inventory()
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
        self.save_inventory()
    
    def show_inventory(self):

        if len(self.items) == 0:

            print(
                "\nInventory is empty."
            )
            return

        print("\n===== INVENTORY =====")

        for item in self.items:
            item.display()
    
    def search_sku(self):

        if len(self.items) == 0:
            print("\nInventory is empty.")
            return

        sku = get_non_empty(
            "Enter SKU to search: "
        )

        for item in self.items:

            if item.sku.lower() == sku.lower():

                print("\nSKU FOUND")
                item.display()
                return

        print("SKU not found.")

    def update_stock(self):

        if len(self.items) == 0:
            print("\nInventory is empty.")
            return

        sku = get_non_empty(
            "Enter SKU: "
        )

        for item in self.items:

            if item.sku.lower() == sku.lower():

                print(
                    f"\nCurrent Stock: "
                    f"{item.stock}"
                )

                new_stock = get_positive_int(
                    "New Stock: "
                )

                item.stock = new_stock

                print(
                    "Stock updated successfully."
                )

                return

        print("SKU not found.")
        self.save_inventory()
        
    def remove_sku(self):

        if len(self.items) == 0:
            print("\nInventory is empty.")
            return

        sku = get_non_empty(
            "Enter SKU to remove: "
        )

        for item in self.items:

            if item.sku.lower() == sku.lower():

                self.items.remove(item)

                print(
                    "SKU removed successfully."
                )

                return

        print("SKU not found.")
        self.save_inventory()
    def inventory_summary(self):

        print("\n========== SUMMARY ==========")

        print(
            f"Total SKUs: "
            f"{len(self.items)}"
        )

        if len(self.items) == 0:

            print("Inventory is empty.")
            print("============================")
            return

        total_stock = 0
        reorder_count = 0

        highest_stock = self.items[0]
        lowest_stock = self.items[0]

        for item in self.items:

            total_stock += item.stock

            if item.needs_reorder():
                reorder_count += 1

            if item.stock > highest_stock.stock:
                highest_stock = item

            if item.stock < lowest_stock.stock:
                lowest_stock = item

        average_stock = (
            total_stock / len(self.items)
        )

        print(
            f"Total Units: {total_stock}"
        )

        print(
            f"Average Stock: "
            f"{average_stock:.2f}"
        )

        print(
            f"Reorders Needed: "
            f"{reorder_count}"
        )

        print(
            f"Highest Stock: "
            f"{highest_stock.sku}"
            f" ({highest_stock.stock})"
        )

        print(
            f"Lowest Stock: "
            f"{lowest_stock.sku}"
            f" ({lowest_stock.stock})"
        )

        print("============================")

    def reorder_report(self):

        print("\n====== REORDER REPORT ======")

        found = False

        for item in self.items:

            if item.needs_reorder():

                found = True

                print(
                    f"{item.sku}"
                )

                print(
                    f"Supplier: "
                    f"{item.supplier}"
                )

                print(
                    f"Current Stock: "
                    f"{item.stock}"
                )

                print(
                    f"Reorder Point: "
                    f"{item.reorder_point()}"
                )

                print(
                    f"Recommended Order: "
                    f"{item.recommended_order_quantity()}"
                )

                print("----------------------")

        if not found:

            print(
                "No products require reorder."
            )

    def abc_analysis(self):
    if not self.items:
        print("Inventory is empty.")
        return

    # Annual consumption proxy (demand * stock importance)
    scored_items = []

    for item in self.items:
        annual_value = item.daily_demand * 365 * item.stock
        scored_items.append((item, annual_value))

    # sort descending
    scored_items.sort(key=lambda x: x[1], reverse=True)

    total = sum(score for _, score in scored_items)

    if total == 0:
        print("No meaningful demand data.")
        return

    print("\n==============================")
    print(" ABC ANALYSIS")
    print("==============================")

    cumulative = 0

    for item, score in scored_items:
        cumulative += score
        ratio = cumulative / total

        if ratio <= 0.7:
            category = "A"
        elif ratio <= 0.9:
            category = "B"
        else:
            category = "C"

        print(
            f"{item.sku} | "
            f"Supplier: {item.supplier} | "
            f"Category: {category}"
        )

    def supplier_summary(self):

        if len(self.items) == 0:

            print("\nInventory is empty.")
            return

        suppliers = {}

        for item in self.items:

            if item.supplier not in suppliers:

                suppliers[item.supplier] = {
                    "sku": 0,
                    "stock": 0,
                    "reorders": 0
                }

            suppliers[item.supplier]["sku"] += 1
            suppliers[item.supplier]["stock"] += item.stock

            if item.needs_reorder():
                suppliers[item.supplier]["reorders"] += 1

        print("\n===== SUPPLIER SUMMARY =====")

        for supplier, data in suppliers.items():

            print(
                f"\nSupplier: {supplier}"
            )

            print(
                f"SKUs: {data['sku']}"
            )

            print(
                f"Total Stock: "
                f"{data['stock']}"
            )

            print(
                f"Reorders: "
                f"{data['reorders']}"
            )
    def save_inventory(self):
    data = [item.to_dict() for item in self.items]

    with open(self.FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

    print("Inventory saved.")
            
    def load_inventory(self):
    try:
        with open(self.FILE_NAME, "r") as f:
            data = json.load(f)

        self.items = [
            InventoryItem.from_dict(item)
            for item in data
        ]

        print(f"Loaded {len(self.items)} items.")

    except FileNotFoundError:
        print("No save file found. Starting empty inventory.")
        self.items = []
                                                                        
def generate_purchase_orders(self):
    print("\n==============================")
    print(" PURCHASE ORDERS")
    print("==============================")

    supplier_map = {}

    for item in self.items:
        if item.needs_reorder():
            if item.supplier not in supplier_map:
                supplier_map[item.supplier] = []
            supplier_map[item.supplier].append(item)

    if not supplier_map:
        print("No purchase orders needed.")
        return

    po_id = 1

    for supplier, items in supplier_map.items():
        print("\n------------------------------")
        print(f"PO ID: PO-2026-{po_id:03d}")
        print(f"Supplier: {supplier}")
        print("Items:")

        total_items = 0

        for item in items:
            qty = item.recommended_order_quantity()
            total_items += 1

            print(f"- {item.sku} | {qty} pcs")

        print(f"Total SKUs: {total_items}")
        print("------------------------------")

        po_id += 1
            
    def menu(self):

        while True:

            print("\n======================================")
            print("      INVENTORY REORDER PLANNER")
            print("======================================")
            print("1. Add SKU")
            print("2. View Inventory")
            print("3. Search SKU")
            print("4. Generate Purchase Orders")
            print("5. Update Stock")
            print("6. Remove SKU")
            print("7. Inventory Summary")
            print("8. Reorder Report")
            print("9. Supplier Summary")
            print("10. Save Inventory")
            print("11. Load Inventory")
            print("12. ABC Analysis")
            print("13. Exit")

            choice = input("\nSelect option: ").strip()

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

                print("\nGoodbye.")
                break

            else:
                print("\nInvalid option.")


def main():

    manager = InventoryManager()

    manager.menu()


if __name__ == "__main__":
    main()