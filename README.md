Inventory Reorder Planner

A terminal-based Inventory Reorder Planner written in Python. The project simulates fundamental inventory planning and procurement processes used in logistics and supply chain management.

Features

Inventory Management

* Add new SKU
* Prevent duplicate SKUs
* View all inventory items
* Search inventory by SKU
* Update stock levels
* Remove SKUs

Inventory Planning

* Reorder Point calculation
* Safety Stock support
* Recommended Order Quantity calculation
* Automatic reorder detection

Supplier Management

* Assign supplier to each SKU
* Supplier inventory summary
* Reorders grouped by supplier

Reporting

* Inventory Summary
* Reorder Report
* Supplier Summary
* Total inventory units
* Average stock level
* Highest stock item
* Lowest stock item
* Number of SKUs requiring reorder

Input Validation

* Prevent negative numbers
* Prevent empty text fields
* Prevent duplicate SKUs
* Handle invalid numeric input

⸻

Project Structure

main.py

Current version is intentionally implemented as a single Python file for learning purposes before being refactored into a multi-file application.

⸻

Example Menu

======================================
      INVENTORY REORDER PLANNER
======================================
1. Add SKU
2. View Inventory
3. Search SKU
4. Update Stock
5. Remove SKU
6. Inventory Summary
7. Reorder Report
8. Supplier Summary
9. Exit

⸻

Example Inventory Item

SKU: A100
Supplier: Bosch
Current Stock: 85
Daily Demand: 12
Lead Time: 7
Safety Stock: 20
Reorder Point: 104
Recommended Order: 295
Status:
REORDER REQUIRED

⸻

Concepts Demonstrated

* Object-Oriented Programming (OOP)
* Classes and Objects
* Methods
* Lists
* Dictionaries
* Loops
* Conditional Logic
* Input Validation
* Inventory Planning
* Procurement Fundamentals
* Supply Chain Logic

⸻

Future Improvements

* JSON data persistence
* CSV import/export
* Purchase Order generation
* Warehouse location management
* ABC Analysis
* EOQ (Economic Order Quantity)
* Demand Forecasting
* Inventory valuation
* Supplier performance scoring
* Multi-warehouse support
* Command history
* Logging system

⸻

Technologies

* Python 3
* Terminal / CLI

⸻

Purpose

This project is part of a logistics and supply chain learning portfolio. The objective is to model practical inventory planning workflows while continuously improving software design and Python programming skills.
