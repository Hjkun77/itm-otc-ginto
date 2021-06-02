import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]
order_management_db = myclient["order_management"]

# products = {
#     100: {"name":"Tea House","price":320,"image": "../static/images/tea-house.png", "description": "barley tea and malayco cake ice cream inspired by dim sum houses of Hong Kong, best for the adventurous"},
#     200: {"name":"Vietnamese Coffee","price":320, "image": "../static/images/vietnamese-coffee.png", "description": "boldly flavored ice cream crafted from Robusta beans and mixed with milky fudge chunks, ideal for coffee lovers"},
#     300: {"name":"White Rabbit","price":320, "image": "../static/images/white-rabbit.png", "description": "super creamy ice cream made from white rabbit candy, perfect for the nostalgic sweet tooth"},
# }

# users = {
#     "harveyjaysison@example.com":{"password":"12345678",
#                          "first_name":"Harvey",
#                          "last_name":"Sison"}
# }

##  Products
# def get_product(code):
#     return products[code]

# def get_products():
#     product_list = []

#     for i,v in products.items():
#         product = v
#         product.setdefault("code",i)
#         product_list.append(product)

#     return product_list
    
# def get_products():
#     product_list = []

#     products_coll = products_db["products"]
    
#     for p in products_coll.find({}):
#         product_list.append(p)

#     print(product_list)
#     return product_list

# def get_product(code):
#     products_coll = products_db["products"]

#     product = products_coll.find_one({"code":code})

#     return product

## Production
def get_product(code):
    products_coll = products_db["products"]

    product = products_coll.find_one({"code":code},{"_id":0})

    return product

def get_products():
    product_list = []

    products_coll = products_db["products"]

    for p in products_coll.find({},{"_id":0}):
        product_list.append(p)

    return product_list

## Users
def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user

# def get_user(username):
#     try:
#        return users[username]
#     except KeyError:
#        return None


## Orders
def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)

## Additional
def change_pass(username, password):
    order_management_db['customers'].update({"username":username}, {"$set":{"password":password}})
    return True