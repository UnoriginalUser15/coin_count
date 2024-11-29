import os
import time
import ast



"""reads the data from 'CoinCount.txt' and converts it into a list"""
def read():
    with open(f".\\Coin Count\\Data.txt", "r") as txt: # opens CoinCount.txt in read mode
        return ast.literal_eval(txt.read()) # reads the .txt and convert's it from a string to a list


"""writes the data from the 'data' variable into 'CoinCount.txt' and 'Data.txt"""
def write(data):
    with open(f".\\Coin Count\\Data.txt", "w") as txt: # writes the unformatted list into 'Data.txt'
        txt.write(str(data))

    with open(f".\\Coin Count\\CoinCount.txt", "w") as txt: # writes the formatted list into 'CoinCount.txt'
        # writes the 'overall' dict at the start of 'CoinCount.txt'
        txt.write(f"""Overall:
    Bags Checked - {data[0]["bags_checked"]}
    Valid Bags - {data[0]["valid_bags"]}
    Funds - {data[0]["total"]}
    Accuracy - {accuracy(data[0]["valid_bags"], data[0]["bags_checked"])} %
    """)
        
        for line in data: # iterates through the list
            if line["name"] != "overall": # prevents it from writing the 'overall' dict
                txt.write(f"""
{line["name"]}:
    Bags Checked - {line["bags_checked"]}
    Valid Bags - {line["valid_bags"]}
    Accuracy - {accuracy(line["valid_bags"], line["bags_checked"])} %""")


"""calculates the accuracy of a volunteer for the 'write()' function"""
def accuracy(valid, total):
    # if volunteer hasn't checked any bags yet, it will return N/A
    try:
        return round((valid / total) * 100, 2)
    except:
        return "N/A"


"""creates the menu that the user can use to choose what they want to do with the program"""
def menu(valid_menu):
    # loops until a valid option has been selected
    while True:
        print("""==| options |==

1 - Check Bag
2 - Volunteer Info
3 - Add New Volunteer
4 - Quit Session (YOU MUST CLOSE THE PROGRAM USING THIS TO SAVE DATA FROM THIS SESSION)

-------------------
""")
        selection = str(input("Type the number coresponding to the menu option you want: "))
        # checks if 'selection' is a valid menu option
        if selection in valid_menu:
            print("\n-------------------\n")
            return selection
        else:
            input("Please select a valid menu option.\nPress ENTER to return to option select ")
            os.system("cls")


"""checks the validity of the coin type and weight of a bag"""
def bag_check():
    pass


"""displays information about overall bags counted and individual volunteer performance"""
def volunteer_info():
    pass


"""adds a new volunteer to 'CoinCount.txt'"""
def add_new_volunteer(data):
    current_names = [] # creates a list of current names in the system
    for i in range(len(data)):
        current_names.append(data[i]["name"])
    
    name = input("Input the name of the volunteer being added (Leave blank and press enter to cancel): ")
    
    # if 'name' isn't blank and does not already exist in 'data', it will add a new dict to the list
    if name != "" and name not in current_names:
        # creates new dictionary for the inputed volunteer
        new_volunteer_dict = {'name': name, 'bags_checked': 0, 'valid_bags': 0, 'accuracy': 0}
        # appends a new dictionary to the 'data' list
        data.append(new_volunteer_dict)
        
        print(f"\n'{name}' is being added to the system...")
        time.sleep(3) # makes the program wait for 3 seconds to make the user think it's doing something (spoiler alert: it's not)
        input(f"'{name}' has been added to the system. Press ENTER to return to the options menu ")
    elif name in current_names:
        input(f"\n'{name}' is already in the system. Press ENTER to return to the options menu ")

    return data


"""quits the current session and saves all the data"""
def quit_session(data):
    # try except checks if the 'write()' function has completed without an error
    try:
        write(data) # writes the current value of the 'data' list into the .txt file
        print("Data has been saved.")
    except:
        print(f"""An error occured that resulted in data failing to save to 'CoinCount.txt'. 
Here is the data currently stored in temporary memory:
{data}""")
    return False # results in 'active_session' being set to False, ending the while loop


### MAIN PROGRAM ###

data = read() # assigns the list created in 'read()' to a variable
# dictionary of different possible coins, format = coin: [bag value, coin weight]
coin_dict = {
    "£2": [20, 12.00],
    "£1": [20, 8.75],
    "50p": [10, 8.00],
    "20p": [10, 5.00],
    "10p": [5, 6.50],
    "5p": [5, 2.35],
    "2p": [1, 7.12],
    "1p": [1, 3.56]
    }
valid_menu = ["1", "2", "3", "4"] # used in 'menu()' to verify if menu selection is valid
active_session = True # used to control if the while loop is active or not

while active_session == True:
    os.system("cls") # clears the display
    selection = menu(valid_menu)

    # runs the process the user requested in the menu
    match selection:
        case "1":
            bag_check()
        case "2":
            volunteer_info()
        case "3":
            data = add_new_volunteer(data)
        case "4":
            active_session = quit_session(data)