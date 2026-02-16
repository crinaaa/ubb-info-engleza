def create_product(name: str, price: int, quantity: int):
    return {"name": name, "price": price, "quantity": quantity}

def get_name(product: dict):
    return product["name"]

def get_price(product:dict):
    return product["price"]

def get_quantity(product:dict):
    return product["quantity"]

def add_product(products: list, name: str, quantity: int, price: int):
    products.append(create_product(name, price, quantity))

def remove_product(products: list, name: str):
    pos = None
    for i in range(0, len(products)):
        if get_name(products[i]) == name:
            pos = i
            break
    for i in range(pos, len(products) - 1):
        products[i] = products[i+1]
    products.pop()

def list_all(products: list):
    pproducts = []
    pproducts.extend(products)
    for i in range(0, len(pproducts) - 1):
        for j in range(i+1, len(pproducts)):
            if get_name(pproducts[i]) < get_name(pproducts[j]):
                pproducts[i], pproducts[j] = pproducts[j], pproducts[i]
    return pproducts