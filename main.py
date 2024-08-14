from sqlite3 import *
import datetime



connection = connect('my_database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers ( customer_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE );
'''
)

cursor.execute('''CREATE TABLE IF NOT EXISTS orders ( order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, order_date DATE NOT NULL, FOREIGN KEY (customer_id) REFERENCES customers(customer_id), FOREIGN KEY (product_id) REFERENCES products(product_id) )''')


#cursor.execute('INSERT INTO products (name, category, price) VALUES (?, ?, ?)', ("Laptop", "Computers&other", 990.99))
#cursor.execute('INSERT INTO products (name, category, price) VALUES (?, ?, ?)', ("Iron", "Household appliances", 149.50))
#cursor.execute('INSERT INTO products (name, category, price) VALUES (?, ?, ?)', ("Computer mouse", "Computers&other", 350.49))
#cursor.execute('INSERT INTO products (name, category, price) VALUES (?, ?, ?)', ("Vacuum cleaner", "Household appliances", 400.10))
#cursor.execute('INSERT INTO products (name, category, price) VALUES (?, ?, ?)', ("Garden gnome Chompski", "Garden decorations", 2000.0))

#cursor.execute('INSERT INTO customers (first_name, last_name, email) VALUES(?, ?, ?)', ("Coach", "Coach", "Coachsurvivor@gmail.com"))
#cursor.execute('INSERT INTO customers (first_name, last_name, email) VALUES(?, ?, ?)', ("Elis", "Murkey", "ThatonegirlwhosnameisElis@gmail.com"))
#cursor.execute('INSERT INTO customers (first_name, last_name, email) VALUES(?, ?, ?)', ("Matthew", "Dabrowski", "Madguy@gmail.com"))



def create_order(product_id:int,customer_id:int,quantity:int):
    date = datetime.datetime.now()
    cursor.execute('INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (?,?,?,?)', (customer_id, product_id, quantity, date))


def get_cost():
    cursor.execute('''SELECT orders.quantity*products.price AS total_sum
                   FROM orders
                   INNER JOIN products ON orders.product_id = products.product_id''')

    a = cursor.fetchall()
    return a

def category_with_most():
    cursor.execute('''SELECT category, COUNT(*) AS category_count
    FROM products
    GROUP BY category
    ORDER BY category DESC
    LIMIT 1''')
    a = cursor.fetchall()
    print(a)
def category_list():
    cursor.execute('''SELECT category, COUNT(*) AS category_count
    FROM products
    GROUP BY category
    ORDER BY category DESC
    ''')
    a = cursor.fetchall()
    print(a)


#Функції для підрахунку
def summiraze(list):
    count = 0
    for i in list:
        count += i[0]

    return count

def get_average(list):
    count = summiraze(list)
    count = count / len(list)

    return count

def update(percent, input_category):
    cursor.execute('''UPDATE products
     SET price = price+?*(price/100)
    WHERE category = ?''', (percent, input_category)
)
    
while True:
    input_ = int(input("1-create order;\n2-summary cost of every order\n3-average cost of an order;\n4-category_with_most;\n5-category list\n6-update price of one category;\n7-end operation."))
    match input_:
        case 1:
            product_id = int(input("Insert product id"))
            customer_id = int(input("Insert customer id"))
            quantity = int(input("Insert quantity"))
            create_order(product_id,customer_id,quantity)
        case 2:
            print(summiraze(get_cost()))
        case 3:
            print(get_average(get_cost()))
        case 4:
            category_with_most()
        case 5:
            category_list()
        case 6:
            percent = int(input("Percent of increasment"))
            category = input("Category which price got increased")
            update(200, "Garden decorations")
        case 7:
            save = input("Do you want to save everything you commited? Y/N")
            if save.lower() == "Y":
                connection.commit()
                break
            elif save.lower() == "N":
                break