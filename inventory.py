
from tabulate import tabulate


#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
        
        
    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"



#==========Functions for error checking==============
#Function that takes an input message as an argument (possibly an error message aswell) and generalises the try-except block for catching value-errors.
def try_except_value_error_int(input_message, error_message = "You have not entered a number."):
    while True:
        user_input = input(f"{input_message}")
        try:
            if int(user_input)>=0:
                break
            else:
                print("You must enter an integer greater than or equal to zero. ")
        except ValueError:
            print(f"{error_message}")
    return user_input

def try_except_value_error_float(input_message, error_message = "You have not entered a number."):
    while True:
        user_input = input(f"{input_message}")
        try:
            if float(user_input)>=0:
                break
            else:
                print("You must enter an integer greater than or equal to zero. ")
        except ValueError:
            print(f"{error_message}")
    return user_input

def is_letter(input_message, error_message = "You have entered characters that are not a-z letters. "):
    while True:
        user_input = input(f"{input_message}").split(' ')
        user_input_split_list = [user_input[i].isalpha() for i in range(len(user_input))]
        if False in user_input_split_list:
            print(f"{error_message}")
        else:
            break
    return " ".join(user_input)

def choice_from_list(lst, input_message):
    while True:
        user_input = input(f"{input_message}")
        if user_input in lst:
            break
        else:
            print("The value you have entered is invalid. ")
    return user_input

#==============Main Functions================

#Opens the 'inventory.txt' file if it exists and initialises a new  Shoe object for each line of data and adds each object to a list. Returns said list.
def read_shoes_data():
    try:
        with open('inventory.txt', 'r') as file:
            file = file.readlines()
            for i in range(1, len(file)):
                file[i] = file[i].strip().split(',')
    
        errors=[]
        for j in range(1, len(file)):
            if len(file[j])!=5:
                errors.append(file[j])
        
        if errors!=[]:
            print("The following lines of data were removed as they were in the wrong format. Please re-enter this data correctly by selecting 'add data' from the menu below.")
            for error in errors:
                print(error)
                file.remove(error)
        shoe_list = [Shoe(file[i][0], file[i][1], file[i][2], float(file[i][3]), int(file[i][4])) for i in range(1, len(file))]
            
        
        return shoe_list
    
    #Creates file if it doesn't exist.
    except FileNotFoundError:
        print("The file 'inventory.txt' did not exist. It has now been created with the appropriate headings. Please select option 2 from the menu to add the requisute data.")
        with open('inventory.txt', 'w+') as file:
            file.write('Country,Code,Product,Cost,Quantity\n')
        return []
            
        
#Calls the read_shoes_data function to retrieve the shoe data.
shoe_list = read_shoes_data()

#Displays all the data in a table.
def view_all(): 

    nested_list = [shoe.__str__().split(',') for shoe in shoe_list]
    for i in range(len(nested_list)):
        nested_list[i].insert(0, i+1)
    print(tabulate(nested_list, headers = ['Index', 'Country', 'Code', 'Product', 'Cost', 'Quantity'], tablefmt = 'presto'))
    print()
    print(50*'-')

#Function that re-writes the 'inventory.txt' file with the data from the objects in shoe_list.
def update_inventory():
    with open('inventory.txt', 'w') as file:
            file.write('Country,Code,Product,Cost,Quantity\n')
            for shoe in shoe_list:
                file.write(shoe.__str__() + '\n')

#Function that gets the user to correct any data in incorrect formats when read from the .txt file.
def correct_shoes_data():
    view_all()
    
    wrong_list = []
    #Checks each shoe object's attributes, if one is in the incorrect format an index for that attribute is added to the wrong_list.
    for i in range(len(shoe_list)):
        
        #Test of country attribute.
        country = shoe_list[i].country.split(" ")
        country_letter = [word.isalpha() for word in country]
        if False in country_letter:
            wrong_list.append(0)
        
        #Tests the code attribute.
        code = shoe_list[i].code

        try:
            if (code[:3]=='SKU') and (len(code)==8) and (int(code[3:]) >= 0):
                pass
                
            else:
                wrong_list.append(1)
        except IndexError:
            wrong_list.append(1)
        
        
        
        #Tests the cost attribute.
        cost = shoe_list[i].cost
        try:
            if float(cost)>0:
                pass
            else:
                wrong_list.append((3))
        except ValueError:
            wrong_list.append((3))
            
        #Tests the quantity function.
        quantity = shoe_list[i].quantity
        try:
            if int(quantity)>=0:
                pass
            else:
                wrong_list.append((4))
        except ValueError:
            wrong_list.append((4))
        
        header = ['Country', 'Code', 'Product', 'Cost', 'Quantity']
        
        
        #If the wrong list is non-empty, the attributes that need to be changed are displayed to the user adn they are prompted to change them into a desired format.
        if wrong_list!=[]:
            print(f"The following attributes for row {i+1} need to be changed: ")
            print()
            for number in wrong_list:
                print(f"{header[number]}")
        
            print("Please enter the corrected version of this data in the following prompts. ")
            country1 = is_letter("Please enter the country your warehouse is based. ").lower()
            country1 = country1.split(" ")
            for j in range(len(country1)): 
        
                country1[j] = country1[j][0].upper() + country1[j][1:]
        
            country1 = " ".join(country1)
            
            while True:
                code1 = try_except_value_error_int("Please enter the 5-digit product code following the letters 'SKU'. ")
                if len(code1) == 5:
                    break
                else:
                    print("The code you have entered is not the correct length.")
            code1 = 'SKU' + code1
            product_name1 = input("Please enter the product name. ").lower()
            #Ensures that each word is capitalised.
            product_name1 = product_name1.split(" ")
            for j in range(len(product_name1)): 
        
                product_name1[j] = product_name1[j][0].upper() + product_name1[j][1:]
        
            product_name1 = " ".join(product_name1)
            
            product_cost1 = float(try_except_value_error_float("Please enter the cost of the product. "))
            product_quantity1 = int(try_except_value_error_int("Please enter the number of units of this product in the warehouse."))
            
            shoe_list[i] = Shoe(country1, code1, product_name1, product_cost1, product_quantity1)
            
            update_inventory()
            
            print("The data has been updated with your entry.")
            
            wrong_list=[]
            print()
            print(50*'-')

#Function is called here before any other functions can be manually called by the user so that there are no data inconsistencies.
correct_shoes_data()

                
#Function that allows the user to enter new data about shoes in their warehouse in a desired format.
def capture_shoes():
    
    country1 = is_letter("Please enter the country your warehouse is based. ").lower()
    country1 = country1.split(" ")
    for i in range(len(country1)): 

        country1[i] = country1[i][0].upper() + country1[i][1:]

    country1 = " ".join(country1)
    
    while True:
        code1 = try_except_value_error_int("Please enter the 5-digit product code following the letters 'SKU'. ")
        if len(code1) == 5:
            break
        else:
            print("The code you have entered is not the correct length.")
    code1 = 'SKU' + code1
    product_name1 = input("Please enter the product name. ").lower()
    #Ensures that each word is capitalised.
    product_name1 = product_name1.split(" ")
    for i in range(len(product_name1)): 

        product_name1[i] = product_name1[i][0].upper() + product_name1[i][1:]

    product_name1 = " ".join(product_name1)
    
    product_cost1 = float(try_except_value_error_float("Please enter the cost of the product. "))
    product_quantity1 = int(try_except_value_error_int("Please enter the number of units of this product in the warehouse."))
    
    for i in range(len(shoe_list)):
        if (shoe_list[i].country == country1) and (shoe_list[i].code == code1):
            print("This product is already listed in this database. Use the edit function to update the data as required.")
            return
    shoe_list.append(Shoe(country1, code1, product_name1, product_cost1, product_quantity1))
    
    #The new data is then written to the .txt file.
    update_inventory()
    print("This data has been recorded.")
    print()
    print(50*'-')
            

#Function that displays to the user the shoe with the least stock remaining and asks them if they want to re-stock the item.
#If re-stocked the new quantity is written to the .txt file.
def re_stock():
    if shoe_list == []:
        print("Please add some data using option 2 from the menu to use the re-stock function.")
        return
    
    shoe_qty_list = [int(shoe.quantity) for shoe in shoe_list]
    index = shoe_qty_list.index(min(shoe_qty_list))
    
    print(f"The shoe with the fewest pairs in stock is the {shoe_list[index].product} with {shoe_list[index].quantity} remaining.")
    add_stock_question = input("Would you like to re-stock this product? If so, please enter 'Yes'. Otherwise, press any character to continue. ").lower()
    if add_stock_question == 'yes':
        add_stock_quantity = 0
        while add_stock_quantity <= 0:
            try:
                add_stock_quantity = int(input("Please enter the number of shoes you'd like to add to the stock list. "))
                break
            except ValueError:
                print("Please enter a number only.")
        
        shoe_list[index].quantity += add_stock_quantity
        
        update_inventory()
        print("The quantity of this shoe recorded has been updated.")
        print()
        print(50*'-')

#Asks the user to enter an identifying code to search 'shoe_list' for shoes with that matching code and returns a list of said objects.
def search_shoe():
    if shoe_list == []:
        print("Please add some data using option 2 from the menu to use the search function.")
        return []
    
    shoe_code_list = [shoe.code for shoe in shoe_list]
    target_shoe = 0
    
    while target_shoe not in shoe_code_list:
        target_shoe = input("Please enter the 'SKU' code for the shoe you would like to search for or enter 'exit' to quit the search function. ").upper()
        if target_shoe == "EXIT":
            break
        
        elif target_shoe not in shoe_code_list:
            print("Sorry, the code you have entered does not exist.")
    
    #Creates a list to store the index of all shoes with the target code (allows the system to have data about the same shoe across warehouses in different countries).
    objects_index = []
    
    #Adds the index of all shoes across warehouses matching the target code to the above list.
    for i in range(len(shoe_code_list)):
        if shoe_code_list[i] == target_shoe:
            objects_index.append(i)
    
    #Adds the shoe objects with the target code to a list and returns as the output of the function.
    objects = [shoe_list[index] for index in objects_index]
    return objects

#Displays a table with the total value of each shoe object in stock in a table.
def value_per_item():
    if shoe_list == []:
        print("Please add some data using option 2 from the menu to use this function.")
        return []
    
    nested_list = [shoe.__str__().split(',')[:3] for shoe in shoe_list]
    for i in range(len(shoe_list)):
        value = int(shoe_list[i].cost) * int(shoe_list[i].quantity)
        nested_list[i].append(value)
    print(tabulate(nested_list, headers = ['Country', 'Code', 'Product', 'Stock Value'], tablefmt = 'presto'))
    print()
    print(50*'-')


#Searches for the shoe with the greatest level of stock and displays it as being for sale.
def highest_qty():
    if shoe_list == []:
        print("Please add some data using option 2 from the menu to use this function.")
        return []
    shoe_qty_list = [int(shoe.quantity) for shoe in shoe_list]
    index = shoe_qty_list.index(max(shoe_qty_list))
    print()
    print(f"The {shoe_list[index].product} is for sale.")
    print()
    print(50*'-')
    return shoe_list[index]

#Function that allows the user to edit existing data.
def edit_data():
    if shoe_list == []:
        print("Please add some data using option 2 from the menu to use this function.")
        return []
    view_all()
    
    #Asks user to pick which entry to edit.
    choice1 = choice_from_list([str(i+1) for i in range(len(shoe_list))], "Please enter the index of the line of data you wish to edit.")
    
    #Asks the user if they want to edit quantity, cost or delete an entry.
    choice2 = choice_from_list(['1', '2', '3', '4'], """Please make a choice from the list below:
                    
Edit quantity - 1
Edit cost - 2
Delete an entry - 3
Exit - 4
""")
    
    if choice2 == '1':
        print("The line in the file 'inventory.txt' is currently the following")
        with open('inventory.txt', 'r') as file:
            file = file.readlines()
            print(file[int(choice1)])
        
        quantity1 = try_except_value_error_int('Please enter the updated quantity for this product. ')

        shoe_list[int(choice1)-1] = Shoe(shoe_list[int(choice1)-1].country, shoe_list[int(choice1)-1].code, shoe_list[int(choice1)-1].product, shoe_list[int(choice1)-1].cost, quantity1)
        print(shoe_list[0].__str__())
        print(shoe_list[1].__str__())
        update_inventory()
        
        
    if choice2 == '2':
        print("The line in the file 'inventory.txt' is currently the following")
        with open('inventory.txt', 'r') as file:
            file = file.readlines()
            print(file[int(choice1)])
        
        cost1 = float(try_except_value_error_float('Please enter the updated cost for this product. '))
        shoe_list[int(choice1)-1] = Shoe(shoe_list[int(choice1)-1].country, shoe_list[int(choice1)-1].code, shoe_list[int(choice1)-1].product, cost1, shoe_list[int(choice1)-1].quantity)
        update_inventory()
        
        print("The data has been updated with your entry.")
        
        
    if choice2 == '3':
        print("The line in the file 'inventory.txt' is currently the following")
        with open('inventory.txt', 'r') as file:
            file = file.readlines()
            print(file[int(choice1)])
        
        confirm = input("Are you sure you want to delete this instance. Yes/No?").lower()
        if confirm == 'yes':
            
            shoe_list.pop(int(choice1)-1)
            update_inventory()
        
            print("The data you chose has been deleted.")
    if choice2 == '4':
        pass
    print()
    print(50*'-')




#==========Main Menu=============

#Menu for users to choose which function to use.

while True:
    choice_menu = choice_from_list([str(num) for num in range(1,9)], '''Please select an option from the menu below:
1 - View all data
2 - Add data
3 - Edit data
4 - Search for a shoe
5 - Display the value per shoe
6 - Display shoe with greatest quantity
7 - Re-stock a shoe
8 - Exit
''')
    
#Displays all data in a table.
    if choice_menu == '1':
        view_all()

#Allows user to enter new data.
    if choice_menu == '2':
        capture_shoes()

#Allows user to edit existing data.
    if choice_menu == '3':
        edit_data()

#Allows user to search for shoe by code.
#Prints each shoe returned from the search_shoe function.
    if choice_menu == '4':
        searched_shoes = search_shoe()
        print()
        
        for shoe in searched_shoes:
            print(shoe.__str__())
        print()
        print(50*'-')

#Displays table of the total value of all shoe objects.
    if choice_menu == '5':
        value_per_item()

#Displays that the shoe with the highest quantity is for sale.
    if choice_menu == '6':
        highest_qty()

#Asks the user if they want to re-stock the shoe with the lowest level of stock.
    if choice_menu == '7':
        re_stock()

#Allows the user tp exit the programme.
    if choice_menu == '8':
        break
    





    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
