suppliers = []

def add_supplier():
    print("Enter supplier details:")
    
    name = input("Supplier Name: ")
    contact = input("Contact Information: ")
    email = input("Email Address: ")
    on_time = float(input("On-time Delivery (%): "))
    

    delays = float(input("Number of Delays: "))

    quality_issues = int(input("Number of Quality Issues: "))
    price_change = float(input("Price Change (%): "))

    supplier = {
        "name": name,
        "contact": contact,
        "email": email,
        "on_time": on_time,
        "delays": delays,
        "quality_issues": quality_issues,
        "price_change": price_change
    }

    suppliers.append(supplier)

    print(f"Supplier '{name}' added successfully!")

def view_suuppliers():
    print("Supplier List:")
    for index, supplier in enumerate(suppliers):
        print(f"{index + 1}. {supplier['name']} - Contact: {supplier['contact']}, Email: {supplier['email']}, On-time Delivery: {supplier['on_time']}, Delays: {supplier['delays']}, Quality Issues: {supplier['quality_issues']}, Price Change: {supplier['price_change']}%")

    if len (suppliers) == 0:
        print("No suppliers available.")
        return
    
    for index, supplier in enumerate(suppliers):
        print(f"{index + 1}. {supplier['name']} - Contact: {supplier['contact']}, Email: {supplier['email']}, On-time Delivery: {supplier['on_time']}, Delays: {supplier['delays']}, Quality Issues: {supplier['quality_issues']}, Price Change: {supplier['price_change']}%")

    print()

def calculate_risk(supplier):  
    score = 0

    score += (100 - supplier["on_time"]) * 0.5
    score += supplier["delays"] * 5
    score += supplier["quality_issues"] * 10
    score += supplier["price_change"] * 2

    return round(score, 1)


def get_risk_level(score):
    if score < 30:
        return "Low"
    elif score < 60:
        return "Medium"
    else:
        return "High"

def generate_risk_report():
    print("Supplier Risk Report:")
    for supplier in suppliers:
        score = calculate_risk(supplier)
        risk_level = get_risk_level(score)

        print(f"Supplier: {supplier['name']}, Risk Score: {score}, Risk Level: {risk_level}")
        print(f"Contact: {supplier['contact']}, Email: {supplier['email']}, On-time Delivery: {supplier['on_time']}, Delays: {supplier['delays']}, Quality Issues: {supplier['quality_issues']}, Price Change: {supplier['price_change']}%")
        print(f"Risk Level: {risk_level}")
        print(f"Risk Score: {score}")
        print(f"on-time Delivery: {supplier['on_time']}, Delays: {supplier['delays']}, Quality Issues: {supplier['quality_issues']}, Price Change: {supplier['price_change']}%")
        print(f"delays: {supplier['delays']}, Quality Issues: {supplier['quality_issues']}, Price Change: {supplier['price_change']}%")
        print(f"Quality Issues: {supplier['quality_issues']}, Price Change: {supplier['price_change']}%")
        print(f"Price Change: {supplier['price_change']}%")
        print("-" * 35)

def main():
    while True:
        print("Supplier Management System")
        print("1. Add Supplier")
        print("2. View Suppliers")
        print("3. Generate Risk Report")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            add_supplier()
        elif choice == '2':
            view_suuppliers()
        elif choice == '3':
            generate_risk_report()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()