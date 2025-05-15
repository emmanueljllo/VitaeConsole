import sys

#Creation function
def add_product(nam, pri, amo):
    for prod in inv:
        
        #Here we check if the product already exists
        if prod["name"].lower().strip() == nam.lower().strip():
            
            #If the product exists we just print the next line
            print(f"\nProduct {nam} already exists")
            return inv
    
    #if the product dont exist we add it
    inv.append({"name" : nam, "price" : pri, "amount" : amo})
    print(f"\nProduct {nam} was added succesfully")
    return inv

#Searching function
def search_product(nam):
    for prod in inv:
        
        #Here we check all the inventory to search for the product
        if prod["name"].lower().strip() == nam.lower().strip():
            
            #if the product was found we print the product
            print(f"""
Product found
Name: {prod["name"]}
Price: {prod["price"]}
Amount: {prod["amount"]}
""")
            return
   
    #if the product was not found it prints the next line
    print(f"\nProduct {nam} wasn't found")

#Price update function
def price_upd(nam, newpri):
    for prod in inv:
        
        #We check for the product in the inventory
        if prod["name"].lower().strip() == nam.lower().strip():
            
            #if we find the product we update the price
            prod["price"] = newpri
            print(f"\nThe price of the product {prod["name"]} has been updated to {prod["price"]: ,.2f} ")
            return
    
    #If we don't find the product we print the next line
    print(f"\nProduct {nam} wasn't found")


#Deleting function
def del_prod(nam):
    for i, prod in enumerate(inv):
        
        #We check in the inventory for the product, getting name and index
        if prod["name"].lower().strip() == nam.lower().strip():
            
            #if we find the product we delete it by its index
            del(inv[i])
            print(f"\nProduct {nam} was succesfully deleted")
            return
    
    #if we don't find the product we print the next line
    print(f"\nProduct {nam} wasn't found")

#Functions that may be neccesary (not asked by the client)

#updating Amount function
def amo_upd(nam, newamo):
    for prod in inv:
        
        #We check for the product in the inventory
        if prod["name"].lower().strip() == nam.lower().strip():
            
            #if we find the product we update the amount
            prod["amount"] = newamo
            print(f"\nThe amount of the product {prod["name"]} has been updated to {prod["amount"]} ")
            return
    
    #if we don't find the product we just print the next line
    print(f"\nProduct {nam} wasn't found")


#Listing function
def list_products():
    if not inv:
        print("Inventory is empty")
        return
    print("\nInventory")
    
    #We take all the products and we show them to the user
    for prod in inv:
        print(f"""Name: {prod["name"]}
Price: {prod["price"]: ,.2f}
Amount: {prod["amount"]}
""")

#Clearing inventory function
def clear_inventory():
    
    while True:
    #We make sure the user wants o do this
        agree = str(input("Are you sure you want to clear inventory? (Y/N):  "))
        if agree.lower().strip() == "y" or agree.lower().strip() == "yes":

            #If the user agrees we delete all the elements in the inventory
            inv.clear()
            print("\nInventory deleted succesfully")
            return
        elif agree.lower().strip() == "n" or agree.lower().strip() == "no":

            #If the user doesn't want to clear the inventory we just return it
            return
        else:

            #If the user makes an uknown answer we ask him to try again
            print("Please enter a valid option (N/Y or NO/YES)")

#Exit function
def exi():
    print("\nSee you later...\n")
    sys.exit()

#We create the menu with the options
def menu():
    print("""
--------------------------------
Select an option
1. Add product
2. Search product
3. List products
4. Update price
5. Update amount
6. Delete product
7. Clear inventory
8. Total value
9. Exit 
--------------------------------
        """)
    
    #We validate the option the user is selecting
    while True:
        try:
            opt = int(input("Select an option: "))
            if 1<=opt<=9:
                return opt 
            print("\nSelect a valid option (1-9)")
        except:
            print("\nSelect a valid option")

#We create the list neccesary for the exercise
inv = [
    {"name" : "fish", "price" : 12.99, "amount" : 20},
    {"name" : "Carrot", "price" : 5.99, "amount" : 30},
    {"name" : "Steak", "price" : 15.99, "amount" : 45},
    {"name" : "Cheese", "price" : 9.99, "amount" : 60},
    {"name" : "Rice", "price" : 7.99, "amount" : 57}
]

#We start the program
print("""
------------------------------------------
                Welcome
------------------------------------------
      """)
while True:
    opt = menu()

#We search for the option given
    match opt:
        
        #Adding case
        case 1:
           
           #ask for the name
            nam = str(input("Insert a name: "))
            
            #We ask for a price with a validation
            while True:
                try:
                    pri = float(input("Insert a price: "))
                    if 0<pri:
                        pri = round(pri, 2)
                        break
                    print("\nInsert a valid price\n")
                except:
                    print("\nInsert a valid price\n")
            
            #We ask for the amount with another validation
            while True:
                try:
                    amo = int(input("Insert an amount: "))
                    if 0<amo:
                        break
                    print("\nInsert a valid amount\n")
                except:
                    print("\nInsert a valid amount\n")
            
            #We call the function to add
            inv = add_product(nam, pri, amo)

        #Searching case
        case 2:
            
            #We ask for the name of the product we're looking for
            nam = str(input("Insert the name of the product you're looking for: "))
            
            #We call the search function
            search_product(nam)

        #Listing case
        case 3:
            
            #We just call for the listing function
            list_products()
        
        #Updating price case
        case 4:
            
            #We ask for the name of the product we're updating
            nam = str(input("Insert the name of the product you want to update: "))
            
            #We ask for the new value with a validation
            while True:
                try:
                    newpri = float(input("Insert the new price: "))
                    
                    #We check if the price is upper than 0
                    if 0 < newpri:
                        newpri = round(newpri, 2)
                        break
                    print("\nInsert a valid price\n")
                except:
                    print("\nInsert a valid price\n")
            
            #We call the updating price function
            price_upd(nam, newpri)
        
        #Updating amount case
        case 5:
            #We ask for the name of the product we're updating
            nam = str(input("Insert the name of the product you want to update: "))
            
            #We ask for the new amount with a validation
            while True:
                try:
                    newamo = int(input("Insert the new amount: "))
                    
                    #We check if the amount is upper than 0
                    if 0 < newamo:
                        break
                    print("\nInsert a valid amount\n")
                except:
                    print("\nInsert a valid amount\n")
            
            #We call the updating amount function
            amo_upd(nam, newamo)
        
        #Deleting case
        case 6:
            
            #We ask for the name of the product we want to delete
            nam = str(input("Insert the name of the product you want to delete: "))

            #We call the deleting function
            del_prod(nam)
        
        #Clearing case
        case 7:
            
            #We just need to call the clearing function
            clear_inventory()
        
        #Total value case
        case 8:
            
            #Here were gonna use a lambda function
            total = round(sum(map(lambda x: x["price"] * x["amount"], inv)), 2)
            
            #We print the total
            print(f"The total value of the inventory is '{total}'")

        #Exit case
        case 9:

            #We just call the exit function
            exi()

        #Empty case
        case _:

            #this case is if the option is empty, so we just gonna say there was a mistake and to try again
            print("emmanuelnf")
