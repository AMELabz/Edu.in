# Experiment 6
**Title:** Create and manipulate Key-Value and Document-oriented data models using NoSQL databases.

## Aim
To create a Key-Value model and a Document-oriented model in Python, and perform Create, Read, Update and Delete (CRUD) operations on both.

## Algorithm
1. Create a Python dictionary with product IDs as keys and product names as values (Key-Value model).
2. Display all products and read one product using its key.
3. Update an existing value, add a new key-value pair, and delete a key.
4. Create a list of dictionaries, where each dictionary is one product document with many fields (Document model).
5. Display all documents and filter the products by category.
6. Update the price of one product in the documents.
7. Add a new document, and delete one document from the list.
8. Display the final collections to confirm the changes.

## Program (exp6_nosql.py)
```python
# ---------- Key-Value model: product ID -> product name ----------
products = {"P101": "Laptop", "P102": "Smartphone", "P103": "Headphones"}

def show_kv(title):
    print(f"\n{title}")
    for key, value in products.items():
        print(f"{key} : {value}")

show_kv("Available Products:")
print("\nRetrieve Product P102:\n" + products.get("P102", "Product not found"))

products["P102"] = "5G Smartphone"      # update
show_kv("After Updating P102:")
products["P104"] = "Tablet"             # add
show_kv("After Adding P104:")
del products["P103"]                    # delete
show_kv("After Deleting P103:")

# ---------- Document model: each product is a JSON-like document ----------
docs = [
    {"ProductID": "P101", "ProductName": "Laptop",       "Category": "Electronics", "Price": 65000, "Stock": 20},
    {"ProductID": "P102", "ProductName": "Smartphone",   "Category": "Electronics", "Price": 28000, "Stock": 35},
    {"ProductID": "P103", "ProductName": "Office Chair", "Category": "Furniture",   "Price": 7500,  "Stock": 15},
]

def show_docs(title, items):
    print(f"\n{title}")
    for d in items:
        print(d)

show_docs("All Products:", docs)
show_docs("Electronics Products:", [d for d in docs if d["Category"] == "Electronics"])

for d in docs:                          # update
    if d["ProductID"] == "P102":
        d["Price"] = 26000
show_docs("After Updating P102 Price:", docs)

docs.append({"ProductID": "P104", "ProductName": "Tablet", "Category": "Electronics", "Price": 22000, "Stock": 18})  # add
show_docs("After Adding P104:", docs)

docs = [d for d in docs if d["ProductID"] != "P103"]   # delete
show_docs("After Deleting P103:", docs)
```

## Execution
```bash
python3 exp6_nosql.py
```

## Output
```
Available Products:
P101 : Laptop
P102 : Smartphone
P103 : Headphones

Retrieve Product P102:
Smartphone

After Updating P102:
P101 : Laptop
P102 : 5G Smartphone
P103 : Headphones

After Adding P104:
P101 : Laptop
P102 : 5G Smartphone
P103 : Headphones
P104 : Tablet

After Deleting P103:
P101 : Laptop
P102 : 5G Smartphone
P104 : Tablet

All Products:
{'ProductID': 'P101', 'ProductName': 'Laptop', 'Category': 'Electronics', 'Price': 65000, 'Stock': 20}
{'ProductID': 'P102', 'ProductName': 'Smartphone', 'Category': 'Electronics', 'Price': 28000, 'Stock': 35}
{'ProductID': 'P103', 'ProductName': 'Office Chair', 'Category': 'Furniture', 'Price': 7500, 'Stock': 15}

Electronics Products:
{'ProductID': 'P101', 'ProductName': 'Laptop', 'Category': 'Electronics', 'Price': 65000, 'Stock': 20}
{'ProductID': 'P102', 'ProductName': 'Smartphone', 'Category': 'Electronics', 'Price': 28000, 'Stock': 35}

After Updating P102 Price:
{'ProductID': 'P101', 'ProductName': 'Laptop', 'Category': 'Electronics', 'Price': 65000, 'Stock': 20}
{'ProductID': 'P102', 'ProductName': 'Smartphone', 'Category': 'Electronics', 'Price': 26000, 'Stock': 35}
{'ProductID': 'P103', 'ProductName': 'Office Chair', 'Category': 'Furniture', 'Price': 7500, 'Stock': 15}

After Adding P104:
{'ProductID': 'P101', 'ProductName': 'Laptop', 'Category': 'Electronics', 'Price': 65000, 'Stock': 20}
{'ProductID': 'P102', 'ProductName': 'Smartphone', 'Category': 'Electronics', 'Price': 26000, 'Stock': 35}
{'ProductID': 'P103', 'ProductName': 'Office Chair', 'Category': 'Furniture', 'Price': 7500, 'Stock': 15}
{'ProductID': 'P104', 'ProductName': 'Tablet', 'Category': 'Electronics', 'Price': 22000, 'Stock': 18}

After Deleting P103:
{'ProductID': 'P101', 'ProductName': 'Laptop', 'Category': 'Electronics', 'Price': 65000, 'Stock': 20}
{'ProductID': 'P102', 'ProductName': 'Smartphone', 'Category': 'Electronics', 'Price': 26000, 'Stock': 35}
{'ProductID': 'P104', 'ProductName': 'Tablet', 'Category': 'Electronics', 'Price': 22000, 'Stock': 18}
```

## Result
CRUD operations were performed successfully on both models. In the Key-Value model, P102 was updated to "5G Smartphone", P104 was added and P103 was deleted, leaving P101, P102 and P104. In the Document model, the P102 price changed to 26000, P104 (Tablet) was added and P103 was deleted, leaving P101, P102 and P104.
