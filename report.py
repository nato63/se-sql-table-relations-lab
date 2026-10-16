import sqlite3
import pandas as pd

conn = sqlite3.connect("data.sqlite")

QUERIES = {
    "1": (
        "Top 10 selling products",
        """
        SELECT p.productName, SUM(od.quantityOrdered) AS totalunits
        FROM products p
        JOIN orderdetails od ON p.productCode = od.productCode
        GROUP BY p.productCode
        ORDER BY totalunits DESC
        LIMIT 10
    """,
    ),
    "2": (
        "Customers per office",
        """
        SELECT o.city, COUNT(c.customerNumber) AS n_customers
        FROM customers c
        JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber
        JOIN offices o ON e.officeCode = o.officeCode
        GROUP BY o.officeCode
        ORDER BY n_customers DESC
    """,
    ),
    "3": (
        "Customers who never ordered",
        """
        SELECT c.contactFirstName, c.contactLastName, c.phone,
               c.salesRepEmployeeNumber
        FROM customers c
        LEFT JOIN orders o ON c.customerNumber = o.customerNumber
        WHERE o.orderNumber IS NULL
        ORDER BY c.contactLastName
    """,
    ),
    "4": (
        "Sales reps with highest average credit limit",
        """
        SELECT e.firstName, e.lastName,
               COUNT(c.customerNumber) AS n_customers,
               ROUND(AVG(c.creditLimit), 2) AS avg_credit
        FROM employees e
        JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
        GROUP BY e.employeeNumber
        ORDER BY avg_credit DESC
        LIMIT 5
    """,
    ),
}


def main():
    while True:
        print("\n--- Northwind Reports ---")
        for key, (title, _) in QUERIES.items():
            print(f"{key}. {title}")
        print("q. Quit")
        choice = input("Choose: ").strip().lower()
        if choice == "q":
            break
        if choice in QUERIES:
            title, sql = QUERIES[choice]
            print(f"\n{title}\n")
            print(pd.read_sql(sql, conn).to_string(index=False))
        else:
            print("Invalid choice.")
    conn.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
