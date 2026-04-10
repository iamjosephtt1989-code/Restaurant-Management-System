

#...............................RESTAURANT MANAGEMENT SYSTEM..............................

import sqlite3
from datetime import datetime



def create_all_tables():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

#table 1
    cursor.execute('''CREATE TABLE IF NOT EXISTS Staff(
        staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        salary REAL,
        password TEXT NOT NULL)''')
    
#table 2
    cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance(
        attend_id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id INTEGER,
        date TEXT,
        time_in TEXT,
        time_out TEXT,
        FOREIGN KEY(staff_id) REFERENCES Staff(staff_id))''')
#table 3
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sales(
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        waiter_id INTEGER,
        billing_staff_id INTEGER,
        customer_phone TEXT,
        items TEXT,
        amount REAL,
        payment_method TEXT,
        date TEXT,
        status TEXT DEFAULT 'pending',
        order_status TEXT DEFAULT 'Received',
        FOREIGN KEY (waiter_id) REFERENCES Staff(staff_id),
        FOREIGN KEY (billing_staff_id) REFERENCES Staff(staff_id))''')
#table 4
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks(
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        assigned_to INTEGER,
        description TEXT,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY (assigned_to) REFERENCES Staff(staff_id))''')
    
#tble 5
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customers(
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT DEFAULT 'Guest',
        phone TEXT UNIQUE,
        visit_counter INTEGER DEFAULT 0,
        loyalty_requests TEXT DEFAULT 'No',
        loyalty_card_no TEXT,
        loyalty_points INTEGER DEFAULT 0)''')
    
#table 6
    cursor.execute('''CREATE TABLE IF NOT EXISTS Feedback(
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_phone TEXT,
    rating INTEGER,
    comments TEXT,
    date TEXT,
    waiter_id INTEGER,
    FOREIGN KEY (waiter_id) REFERENCES Staff(staff_id))''')

#table 7
    cursor.execute('''CREATE TABLE IF NOT EXISTS Menu(
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dish_name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT)''')
    

    
    conn.commit()
    conn.close()
    

def initial_admin_setup():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Staff")
    if cursor.fetchone()[0] == 0:
        print("\n--- FIRST TIME SYSTEM SETUP: REGISTER ADMIN ---")
        name = input("Enter Admin Name: ")
        salary = float(input("Enter Monthly Salary (INR): "))
        password = input("Set Admin Password: ")

        cursor.execute('''INSERT INTO Staff (name, role, salary, password)
                       VALUES (?, ?, ?, ?)''',
                        (name, 'Admin Manager',salary, password))
        conn.commit()
        print(f"\n[SUCCESS] Admin created! Your Login ID is:{cursor.lastrowid}")
        print("Please remember this ID to log in.")
    conn.close()

def add_new_sale(staff_id):
    try:
        amount = float(input("Enter Bill Amount (INR): "))
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = sqlite3.connect('restaurant_management.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Sales(waiter_id, amount, date)VALUES (?, ?, ?)",(staff_id, amount, date_str))
        conn.commit()
        conn.close()
        print("[SUCCESS] Sale recorded!")
    except ValueError:
        print("[ERROR] Please enter a valid number for amount.")

def view_total_sales():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM Sales")
    total = cursor.fetchone()[0]
    conn.close()
    print(f"\n---TOTAL REVENU: {total if total else 0} INR---")

def view_my_salary(staff_id):
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Salary FROM Staff WHERE staff_id = ?", (staff_id,))
    row = cursor.fetchone()
    if row:
        salary = row[0]
        print(f"\n--- YOUR MONTHLY SALARY: {salary} INR ---")
    else:
        print("[ERROR] salary record not fount.")



def check_attendance_log():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    query = '''
        SELECT Staff.name, Attendance.date, Attendance.time_in
        FROM Attendance
        JOIN Staff ON Staff.staff_id = Attendance.staff_id
        ORDER BY Attendance.date DESC
        '''
    cursor.execute(query)
    logs = cursor.fetchall()
    conn.close()
    print("\n--- ATTENDANCE RECORDS ---")
    for name, date, time in logs:
        print(f"Date: {date} | Time: {time} | Name: {name}")
        
def mark_attendance(staff_id):
    """Duty In: Triggered automatically at login."""
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    now = datetime.now()

    cursor.execute("INSERT INTO Attendance (staff_id, date, time_in) VALUES (?, ?, ?)",
                    (staff_id, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")))
    conn.commit()
    conn.close()
    print(f"[SYSTEM] Attendance Marked.")

def mark_clock_out(staff_id):
    """Duty Out: Triggered by user from dashboard."""
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute('''UPDATE Attendance SET time_out = ?
                      WHERE staff_id = ? AND date = ? AND time_out IS NULL''',
                      (now.strftime("%H:%M:%S"), staff_id, now.strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()
    print(f"[SYSTEM] Duty out marked successfully.")

def waiter_create_bill(staff_id):
    try:
        amount = float(input("Enter Order Amount (INR): "))
        conn = sqlite3.connect('restaurant_management.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sales (waiter_id, amount, date, status) VALUES (?, ?, ?, ?)",
                       (staff_id, amount, datetime.now().strftime("%Y-%m-%d %H:%M"), 'pending'))
        conn.commit()
        conn.close()
        print(f"[SUCESS] Bill Created! Please request the guest to pay at the counter.")
    except ValueError:
        print("[ERROR] Invalid amount.")

def register_new_staff():
    print("\n--- ADMIN: REGISTER NEW STAFF ---")
    roles = ["Admin Manager", "Chef", "Waiter", "Billing staff"]
    name = input("Enter Name: ")
    for i, r in enumerate(roles, 1): 
        print(f"{i}.{r}")
    
    try:
        choice = int(input("Select Role Number: "))
        role = roles[choice-1]
        sal = float(input("Monthly Salary (INR): "))
        pwd = input("Set Password: ")


        conn = sqlite3.connect('restaurant_management.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Staff (name, role, salary, password) VALUES (?, ?, ?, ?)",
                        (name, role, sal, pwd))
        conn.commit()
        print(f"[SUCCESS] Registered! ID is: {cursor.lastrowid}")
        conn.close()
    except:
        print("[ERROR] something went wrong.")

def assign_staff_task():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT staff_id, name, role FROM Staff")
    staff_members = cursor.fetchall()

    print("\n--- SELECT STAFF TO ASSIGN TASK ---")
    for s_id, name, role in staff_members:
        print(f"ID: {s_id} | Name {name} ({role})")

    try:
        target_id = int(input("\nEnter Staff ID to assign task: "))
        task_desc = input("Enter Task Descreption:")

        cursor.execute('''INSERT INTO Tasks (Assigned_to, description, status)
                          VALUES (?, ?, ?)''', (target_id, task_desc, 'pending'))
        conn.commit()
        print(f"[SUCCESS] Task assigned to Staff ID {target_id}")
    except ValueError:
        print("[ERROR] Invalid input. Task not assigned.")
    finally:
        conn.close()

def view_orders_for_waiter():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sale_id, items, customer_phone, date 
        FROM Sales 
        WHERE order_status = 'Received'
    """)
    orders = cursor.fetchall()
    
    print("\n--- NEW CUSTOMER ORDERS ---")
    if not orders:
       print("No new orders to process.")
    else:
        for oid, items, phone, dt in orders:
            # Added a better format for the display
            print(f"Order ID: {oid} | Phone: {phone} | Time: {dt}")
            print(f"Items: {items}")
            print("-" * 30)
    
    conn.close()
    return orders

def waiter_view_orders():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT sale_id, customer_phone, items, amount FROM Sales WHERE order_status = 'Received'")
    orders = cursor.fetchall()
    
    print("\n--- NEW CUSTOMER ORDERS ---")
    if not orders:
        print("No new orders found.")
    else:
        for oid, phone, items, amt in orders:
            print(f"ID: {oid} | Phone: {phone} | Total: {amt}")
            print(f"Items: {items}")
            print("-" * 20)
    conn.close()

def send_to_kitchen(staff_id):
    orders = view_orders_for_waiter()
    if not orders:
        return

    try:
        order_id = int(input("\nEnter Order ID to send to Kitchen: "))
        
        conn = sqlite3.connect('restaurant_management.db')
        cursor = conn.cursor()

        
        cursor.execute('''UPDATE Sales 
                          SET order_status = 'In Progress', waiter_id = ? 
                          WHERE sale_id = ? AND order_status = 'Received' ''', 
                       (staff_id, order_id))

        if cursor.rowcount > 0:
            conn.commit()
            print(f"[SUCCESS] Order #{order_id} sent to kitchen. Chef will see it now!")
        else:
            print(f"[ERROR] Order #{order_id} not found or already processed.")
            
        conn.close()
    except ValueError:
        print("[ERROR] Please enter a valid numeric ID.")


def generate_bill(order_id, phone, items, total):
    print("\n" + "═"*35)
    print(f"║ {'RECEIPT':^31} ║") # ^ centers the text
    print("╠" + "═"*33 + "╣")
    print(f"║ Order ID: {order_id:<21} ║")
    print(f"║ Phone:    {phone:<21} ║")
    print(f"╟" + "─"*33 + "╢")
    
    # Split items if they are in a string like "Tea, biriyani"
    item_list = items.split(", ")
    for item in item_list:
        print(f"║ • {item:30} ║")
        
    print("╟" + "─"*33 + "╢")
    print(f"║ {'TOTAL AMOUNT:':<18} {total:>7.2f} INR ║")
    print("╚" + "═"*33 + "╝")
    print(f"{'Thank you for visiting!':^35}\n")

def view_and_complete_tasks(staff_id):
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, description, status FROM Tasks WHERE assigned_to = ?", (staff_id,))
    tasks = cursor.fetchall()

    print("\n--- MY TASKS ---")
    for tid, desc, stat in tasks:
        print(f"[{tid}] [{desc}] - {stat}")
    action = input("\nEnter Task ID to complete (or press enter to skip): ")
    if action :
        cursor.execute("UPDATE Tasks SET status = 'complete' WHERE task_id = ?", (action,))
        conn.commit()
        print("[SUCCESS] Task updated.")
    conn.close()

def process_pending_payments(billing_staff_id):
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sale_id, amount, date FROM Sales WHERE status = 'Pending'")
    pending_bills = cursor.fetchall()

    if not pending_bills:
        print("\n[INFO] No Pending bills to collect.")
        conn.close()
        return
    print("\n--- PENDING BILLS ---")
    for s_id, amt, dt in pending_bills:
        print(f"ID:{s_id} | Amount: {amt} | Date: {dt}")

    try:
        bill_to_pay = int(input("\nEnter Bill ID to process payment: "))
        print("Select Payment Method:  1. Cash | 2. Card | 3. UPI")
        
        method_choice = input("Select (1-3): ")
        
        selected_method_dict = {"1": "Cash", "2": "Card", "3": "UPI"}
        payment_final = selected_method_dict.get(method_choice, "cash")

       
        cursor.execute('''UPDATE Sales 
                          SET status = 'paid', 
                              payment_method = ?, 
                              billing_staff_id = ? 
                          WHERE sale_id = ?''', (payment_final, billing_staff_id, bill_to_pay))
        
        conn.commit()
        print(f"[SUCCESS] payment of {payment_final} recived for bill #{bill_to_pay}!")

    except ValueError:
        print("[ERROR] Invalid input. Transaction cancelled.")
    finally:
        conn.close()

def generate_daily_report():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute('''SELECT payment_method, SUM(amount), COUNT(sale_id)
                    FROM Sales
                    WHERE status = 'paid' AND date LIKE ?
                    GROUP BY payment_method''', (f"{today}%",))
    rows = cursor.fetchall()

    print(f"\n--- DAILY SALES REPORT({today}) ---")
    grand_total = 0
    if not rows:
        print("No transactions completed today.")
    else:
        for method, total, count in rows:
            print(f"{method:10}: {total:>8} INR ({count}) bills")
            grand_total += total
        print("-" * 30)
        print(f"GRAND TOTAL: {grand_total} INR")
    conn.close()

def view_loyalty_requests():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT name, phone FROM Customers WHERE loyalty_requests = 'Yes' AND loyalty_card_no IS NULL")
    requests = cursor.fetchall()
    
    if not requests:
        print("\n[INFO] No pending loyalty card requests.")
    else:
        print("\n--- PENDING LOYALTY REQUESTS ---")
        for name, phone in requests:
            print(f"Customer: {name} | Phone: {phone}")
            
    conn.close()

def manage_loyalty_cards():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()

    
    cursor.execute("SELECT name, phone FROM Customers WHERE loyalty_requests = 'Yes' AND loyalty_card_no IS NULL")
    requests = cursor.fetchall()

    if not requests:
        print("\n[INFO] No pending loyalty card requests.")
        conn.close()
        return
    
    print("\n--- PENDING LOYALTY REQUESTS ---")
    for name, phone in requests:
        print(f"Customer: {name} | Phone: {phone}")

    target_phone = input("\nEnter phone to issue card (or 'back' to cancel): ")
    if target_phone.lower() == 'back':
        conn.close()
        return

    card_no = "LOY" + target_phone[-4:]
    
    cursor.execute("UPDATE Customers SET loyalty_card_no = ?, loyalty_points = 0 WHERE phone = ?",
                   (card_no, target_phone))
    
    conn.commit()
    conn.close()
    print(f"[SUCCESS] Loyalty Card {card_no} issued to {target_phone}.")



def show_loyalty_card(phone, card_id, visits):
    print("\n" + "╔" + "═"*38 + "╗")
    print(f"║ {'LOYALTY MEMBER':^36} ║")
    print("╠" + "═"*38 + "╣")
    print(f"║  CARD ID: {card_id:26} ║")
    print(f"║  PHONE:   {phone:26} ║")
    print(f"║  STATUS:  {'★ PREMIUM MEMBER ★':26} ║")
    print("╟" + "─"*38 + "╢")
    print(f"║  Visits: {visits:27} ║")
    print("╚" + "═"*38 + "╝")



def add_menu_items():
    print("\n---- ADD NWE MENU ITEM ----")
    dish_name = input("Enter Dish Name: ")
    try:
        price = float(input("Enter Price (INR): "))
        category = input("Enter Category (e.g:  Starters, Main Course, Drinks): ")

        conn = sqlite3.connect('restaurant_management.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Menu (dish_name, price, category)
                          VALUES (?, ?, ?)''', (dish_name, price, category))
        conn.commit()
        print(f"[SUCCESS] {dish_name} added to the {category} category!")
    except ValueError:
        print("[ERROR] Invalid price. Please enter a numeric value.")
    except Exception as e:
        print(f"[ERROR] Could not add item: {e}")
    finally:
        conn.close()

def delete_menu_item():
    print("\n--- DELETE MENU ITEM ---")
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT item_id, dish_name, category FROM Menu")
    items = cursor.fetchall()

    if not items:
        print("[INFO] The menu is already empty.")
        conn.close()
        return
    
    for i_id, name, cat in items:
        print(f"ID: {i_id} | {name} ({cat})")

    try:
        target_id = int(input("\nEnter Item ID to Delete: "))
        confirm = input(f"Are you sure you want to Delete ID {target_id}? (yes/no): ").lower()
        if confirm == 'yes':
            cursor.execute("DELETE FROM Menu WHERE item_id = ?", (target_id,))
            conn.commit()
            print(f"[SUCCESS] Item Id {target_id} has been removed.")
        else:
            print("[CANCELLED] Delete operation aborted.")
    
    except ValueError:
        print("[ERROR] Please enter a valid numeric ID.")
    finally:
        conn.close()

def view_pending_orders(staff_id):
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()

    cursor.execute("SELECT sale_id, items, amount, date FROM Sales WHERE order_status = 'In Progress'")
    orders = cursor.fetchall()

    print("\n--- PENDING KITCHEN ORDERS ---")
    if not orders:
        print("No active orders in the kitchen.")
    for oid, items, amt, dt  in orders:
        print(f"Order ID: {oid} | Items: {items} | Amount:{amt} | Time: {dt}")
    conn.close()

def chef_view_orders():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT sale_id, items, date 
        FROM Sales 
        WHERE order_status = 'In Progress'
    """)
    orders = cursor.fetchall()
    
    print("\n--- KITCHEN ORDERS (TO COOK) ---")
    if not orders:
        print("No pending orders in the kitchen.")
    else:
        for oid, items, dt in orders:
            print(f"ORDER ID: {oid} | TIME: {dt}")
            print(f"DISHES: {items}")
            print("-" * 30)
            
    conn.close()
    return orders

def mark_orders_ready(staff_id):
    view_pending_orders(staff_id)
    try:
        order_id = int(input("\nEnter Order ID to mark as READY: "))

        conn = sqlite3.connect('restaurant_management.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE Sales SET order_status = 'Ready' WHERE sale_id = ?", (order_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print(f"[SUCCESS] Order #{order_id} is now ready!")
        else:
            print(f"[ERROR] Order #{order_id} not found.")
            conn.close()
    except ValueError:
        print("[ERROR] Please enter a valid numeric Order ID.")


def view_digital_menu():
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT dish_name, price, category FROM Menu")
    items = cursor.fetchall()


    print("╔" + "═" * 46 + "╗")
    print("║" + "      ✨ WELCOME TO OUR DIGITAL MENU ✨       " + "║")
    print("╠" + "═" * 20 + "╦" + "═" * 10 + "╦" + "═" * 14 + "╣")
    
    
    print(f"║ {'ITEM NAME':18} ║ {'PRICE':8} ║ {'CATEGORY':12} ║")
    print("╠" + "═" * 20 + "╬" + "═" * 10 + "╬" + "═" * 14 + "╣")

    
    for name, price, cat in items:
        
        print(f"║ {name:18} ║ {price:8.2f} ║ {cat:12} ║")

    
    print("╚" + "═" * 20 + "╩" + "═" * 10 + "╩" + "═" * 14 + "╝")
    
    conn.close()



def place_ordder(customer_phone):
    view_digital_menu()
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO Customers (phone) VALUES (?)", (customer_phone,))
    cursor.execute("UPDATE Customers SET visit_counter = visit_counter + 1 WHERE phone = ?", (customer_phone,))
    conn.commit()

    items_ordered = []
    total_amount = 0

    while True:
        dish = input("\nEnter Dish Name to order (or 'done' to finish): ")
        if dish.lower() == 'done': break

        cursor.execute("SELECT price FROM Menu WHERE dish_name = ?", (dish,))
        result = cursor.fetchone()

        if result:
            price = result [0]
            items_ordered.append(dish)
            total_amount += price
            print(f"[ADDED] {dish} - {price} INR")
        else:
            print("[ERROR] Dish not found. please check the spelling.")
    
    if items_ordered:
        dishes_string = ", ".join(items_ordered)
        
        cursor.execute('''INSERT INTO Sales (customer_phone, amount, date, status, order_status, items)
                          VALUES (?, ?, datetime('now'), 'Pending', 'Received', ?)''',
                       (customer_phone, total_amount, dishes_string))
        
        
        conn.commit()
        print(f"\n[SUCCESS] Order placed! Total: {total_amount} INR.")
    else: 
        print("\n[INFO] No items selected. Order cancelled.")
    conn.close()

def request_loyalty_card(customer_phone):
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO Customers (phone, name) VALUES (?, 'Guest')", (customer_phone,))
    cursor.execute("UPDATE Customers SET loyalty_requests = 'Yes' WHERE phone = ?", (customer_phone,))
    conn.commit()
    conn.close()
    print("[SUCCESS] Your request for a Loyalty Card has been sent to the Billing Staff.")

def view_customer_loyalty(phone):
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, visit_counter FROM Customers WHERE phone =?", (phone,))
    result = cursor.fetchone()
    conn.close()

    if result:
        name, visits = result
        print(f"\nHello{name}! You have visited us {visits} times.")
        if visits >= 10:
            print("* VIP STATUS: Show this screen for a 10% discount!")
    else:
        print("\n[INFO] Phone number not found. Register at the counter to start earning points!")

def show_loyalty_card_portal(phone):
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT loyalty_card_no, visit_counter FROM Customers WHERE phone = ?", (phone,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0]:  
        card_id, visits = result
        
        
        print("\n" + "╔" + "═"*38 + "╗")
        print(f"║ {'✨ DIGITAL LOYALTY CARD ✨':^36} ║")
        print("╠" + "═"*38 + "╣")
        print(f"║  CARD ID: {card_id:26} ║")
        print(f"║  PHONE:   {phone:26} ║")
        print(f"║  STATUS:  {'★ PREMIUM MEMBER ★':26} ║")
        print("╟" + "─"*38 + "╢")
        print(f"║  Visits: {visits:27} ║")
        print("╚" + "═"*38 + "╝")
    else:
        print("\n[INFO] No loyalty card found. Please request one first!")

def give_feedback(phone, waiter_id=None):
    print("\n--- RATE YOUR EXPERIENCE ---")
    try:
        rating = int(input("Rate us (1-5 Stars): "))
        if rating < 1 or rating > 5:
            print("Please enter a rating between 1 and 5.")
            return
        
        comments = input("Enter your comments: ")
        date_str =datetime.now().strftime("%Y-%m-%d %H:%M")

        conn = sqlite3.connect('restaurant_management.db')
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO Feedback (customer_phone, rating, comments, date, waiter_id)
                          VALUES (?, ?, ?, ?, ?)''',  (phone, rating, comments, date_str, waiter_id))
        conn.commit()
        conn.close()
        print("\n[THANK YOU] your feedback helps us serve you better!")
    except ValueError:
        print("[ERROR] Please enter a valid number for rating.")

def main_entry():
    while True:
        print("\n--- WELCOME TO THE RESTAURANT ---")
        print("1. Staff Login")
        print("2. Customer Portal")
        print("3. Exit")

        choice = input("Select an option: ")
        
        if choice == '1':
            login()
        elif choice == '2':
            customer_access()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please try again.")

def view_my_bill(phone):
    conn = sqlite3.connect('restaurant_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sale_id, amount, date FROM Sales WHERE customer_phone = ? AND status = 'Pending'", (phone,))
    bill = cursor.fetchone()
    conn.close()

    if bill:
        print("\n--- YOUR CURRENT BILL ---")
        print(f"Bill ID: {bill[0]}")
        print(f"Total Amount: {bill[1]} INR")
        print(f"Date: {bill[2]}")
    else:
        print("\n[INFO] No active pending bills found for this number.")

def admin_dashboard(staff_id):
    while True:
        print("\n" + "=" * 30)
        print("     ADMIN PANEL")
        print("=" * 30)
        print("1. Register Staff")
        print("2. View Total Sales Report")
        print("3. Check Attendance Logs")
        print("4. Assign Task to Staff")
        print("5. Logout")
        choice = input("Select: ")
        if choice == '1': 
            register_new_staff()
        elif choice == '2':
            view_total_sales()
        elif choice == '3':
            check_attendance_log()
        elif choice == '4':
            assign_staff_task()
        elif choice == '5':
            break

def chef_dashboard(staff_id):
    while True:
        print("\n" + "=" * 30)
        print("     KITCHEN & MENU MANAGEMENT")
        print("=" * 30)
        print("1. View Menu Items")
        print("2. Add Menu Items")
        print("3. Delete Menu Items")
        print("4. view Orders to Cook")
        print("5. View Pending Items")
        print("6. Mark Order as Ready")
        print("7. Duty Out")
        print("8. Logout")

        choice = input("Select")
        if choice == '1':
            view_digital_menu()
        elif choice == '2':
            add_menu_items()
        elif choice == '3':
            delete_menu_item()
        elif choice == '4':
            chef_view_orders()
        elif choice == '5':
            view_pending_orders(staff_id)
        elif choice == '6':
            mark_orders_ready(staff_id)
        elif choice == '7':
            mark_clock_out(staff_id)
        elif choice == '8':
            break


def billing_staff_dashboard(staff_id):
    while True:
        print("\n" + "=" * 30)
        print("     BILLING STAFF DASHBOARD")
        print("=" * 30)
        print("1. Process Pending Bills (Cash/Cadr/UPI)")
        print("2. Daily Sales Report")
        print("3. View/Complete My Tasks")
        print("4. Manage Loyalty Card Requests")
        print("5. Duty Out")
        print("6. Logout")

        choice = input("Select: ")

        if choice == '1':
            process_pending_payments(staff_id)
        elif choice == '2':
            generate_daily_report()
        elif choice == '3':
            view_and_complete_tasks(staff_id)
        elif choice == '4':
            manage_loyalty_cards()
        elif choice == '5':
            mark_clock_out(staff_id)
        elif choice == '6':
            break

def waiter_dashboard(staff_id):
    while True:
        print("\n" + "=" * 30)
        print("     WAITER DASHBOARD")
        print("=" * 30)
        print("1. View Customer Orders")
        print("2. Send Order to Kitchen (Mark In Progress)")
        print("3. Create Bill (In-Person Order)")
        print("4. Viwe My Tasks")
        print("5. View My Salary")
        print("6. Logout")

        choice = input("Select an option : ")

        if choice == '1':
            view_orders_for_waiter()
        elif choice == '2':
            send_to_kitchen(staff_id)
        elif choice == '3':
            waiter_create_bill(staff_id)
        elif choice == '4':
            view_and_complete_tasks(staff_id)
        elif choice == '5':
            view_my_salary(staff_id)
        elif choice == '6':
            break

def customer_access():
    
    
    phone = input("Enter your phone number: ")
    
    while True:

        print("\n" + "=" * 30)
        print("   CUSTOMER DASHBOARD")
        print("=" * 30)
        print("1. View Digital Menu")
        print("2. Place Order")
        print("3. My Loyalty Points/Visits")
        print("4. View My Bill")
        print("5. Give Feedback")
        print("6. Request Loyalty Card")
        print("7. Exit") 

        choice = input("\nEnter your choice (1-7): ")

        if choice == '1':
            view_digital_menu()
        elif choice == '2':
            place_ordder(phone) 
        elif choice == '3':
            show_loyalty_card_portal(phone)
        elif choice == '4':
            view_my_bill(phone)  
        elif choice == '5':
            give_feedback(phone) 
        elif choice == '6':
            request_loyalty_card(phone)
        elif choice == '7':
            print("Returning to Main Menu.....")
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")
   

def login():
    print("\n---- RESTAURANT ERP LOGIN ----")
    try:
        user_id = int(input("Enter Staff ID: "))
        user_pwd = input("Password: ") # Added missing colon for clarity

        conn = sqlite3.connect('restaurant_management.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, role FROM staff WHERE staff_id=? AND password=?", (user_id, user_pwd))
        user = cursor.fetchone()
        conn.close()

        if user:
            name, role = user
            print(f"\nWELCOME, {name}!")
            staff_id = user_id 
            mark_attendance(staff_id)

            if role == "Admin Manager":
                admin_dashboard(staff_id)
            elif role == "Waiter":
                waiter_dashboard(staff_id)
            elif role == "Billing staff": 
                billing_staff_dashboard(staff_id)
            elif role == "Chef":
                chef_dashboard(staff_id)
        else:
            print("[ERROR] Login Failed. Incorrect ID or Password.")

    except ValueError: 
        print("[ERROR] Invalid input. Please enter a numeric Staff ID.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")


if __name__ == "__main__":
    create_all_tables()
    initial_admin_setup()
    main_entry()
    
