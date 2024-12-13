import os
import time
import ast


"""reads the data from 'CoinCount.txt' and converts it into a list"""
def read():
    with open("Data.txt", "r") as txt: # opens CoinCount.txt in read mode
        return ast.literal_eval(txt.read()) # reads the .txt and convert's it from a string to a list


"""writes the data from the 'data' variable into 'CoinCount.txt' and 'Data.txt"""
def write(data):
    # writes the unformatted list into 'Data.txt'
    with open("Data.txt", "w") as txt:
        txt.write(str(data))
    # writes the formatted list into 'CoinCount.txt'
    with open("CoinCount.txt", "w") as txt:
        # writes the 'overall' dict at the start of 'CoinCount.txt'
        txt.write(f"""Overall:
| Bags Checked - {data[0]["bags_checked"]}
| Valid Bags - {data[0]["valid_bags"]}
| Funds - {data[0]["funds"]}
| Accuracy - {accuracy(data[0]["valid_bags"], data[0]["bags_checked"])} %
===================""")
        for line in data: # iterates through the list
            if line["name"] != "overall": # prevents it from writing the 'overall' dict
                txt.write(f"""
{line["name"]}:
| Bags Checked - {line["bags_checked"]}
| Valid Bags - {line["valid_bags"]}
| Accuracy - {accuracy(line["valid_bags"], line["bags_checked"])} %
-------------------""")


"""calculates the accuracy of a volunteer for the 'write()' function"""
def accuracy(valid, total):
    try:
        return round((valid / total) * 100, 2)
    except: # if volunteer hasn't checked any bags yet, it will return N/A
        return "N/A"


"""creates the menu that the user can use to choose what they want to do with the program"""
def menu(valid_menu):
    # loops until a valid option has been selected
    while True: 
        print("""==| The Coincount-inator |==

By Doofenshmirtz Evil Inc. - Trying to take over the tri-state area est. 1977

1 - Check Bag-inator
2 - Volunteer Info-inator
3 - Add New Volunteer-inator
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
            os.system("cls") # clears the terminal, specifically on windows


"""checks the validity of the coin type and weight of a bag"""
def bag_check(data, coin_dict):
    # creates a list of current names in the system
    current_names = []
    for i in range(len(data)):
        if data[i]["name"] != "overall":
            current_names.append(data[i]["name"])
    
    os.system("cls") # clears the terminal, specifically on windows
    print("""==| Bag Check-inator |==
If you ever want to cancel, just leave an input blank and press ENTER""")

    # makes sure a valid name is input before continuing
    while True:
        volunteer_name = input("\nInput volunteer name: ")
        # checks if user wants to cancel
        if volunteer_name == "":
            print("\nCancelling bag check...")
            time.sleep(2) # the fake-loading-time-inator makes the program wait before continuing
            return data, False
        # notifys user that 'volunteer_name' is not in the system
        elif volunteer_name not in current_names:
            print("""\nThat name does not currently exist in the system.
Make sure the capitalisation of the name is correct.""")
        # breaks while loop if 'volunteer_name' is in the system
        else:
            print("-------------------")
            break
    
    # makes sure a valid coin is input before continuing
    while True:
        coin = input("Input coin type: ").strip()
        # checks if user wants to cancel
        if coin == "":
            print("\nCancelling bag check...")
            time.sleep(2) # the fake-loading-time-inator makes the program wait before continuing
            return data, False
        # notifys user that 'coin' is not a valid coin
        elif coin not in coin_dict.keys():
            print("""That is not a valid coin. The valid coins are as follows:
£2, £1, 50p, 20p, 10p, 5p, 2p, 1p""")
        # breaks while loop if 'coin' is valid
        else:
            print("-------------------")
            break
    
    # checks if bag weight is valid or not (the actual purpose of the bag check-inator)
    while True:
        bag_weight = input("Input bag weight (g): ").strip()
        # checks if user wants to cancel
        if bag_weight == "":
            print("\nCancelling bag check...")
            time.sleep(2) # the fake-loading-time-inator makes the program wait before continuing
            return data, False
        # the try except checks if the user has input a numerical value or not and converts 'bag_weight' to a float
        try:
            bag_weight = round(float(bag_weight), 2)
        except:
            print("You have to input a numerical value for the weight")
            continue
        # breaks while loop if bag weight is correct for chosen coin
        if bag_weight == coin_dict[coin][1]:
            print("\nBag weight is valid ^-^\n-------------------")
            # adds 1 to "bags_checked" and "valid_bags" in the 'overall' dictionary along with the value of the bag
            data[0]["bags_checked"] += 1
            data[0]["valid_bags"] += 1
            data[0]["funds"] += coin_dict[coin][0]
            # adds 1 to "bags_checked" and "valid_bags" in the volunteers assigned dictionary in 'data'
            for i in range(len(data)):
                    if data[i]["name"] == volunteer_name:
                        data[i]["bags_checked"] += 1
                        data[i]["valid_bags"] += 1
            break
        # notifies the user that their bag has negative mass and thus breaks the laws of physics
        elif bag_weight <= 0:
            print("You need to input a value greater than 0 for the weight.")
        # checks if an invalid weight is a number of coins off or outright not possible given coin type
        else:
            # invalid weight is divisible fully by coin type
            if bag_weight % coin_dict[coin][2] == 0:
                weight_difference = coin_dict[coin][1] - bag_weight # calculates difference in weight between invalid and valid
                coin_difference = weight_difference / coin_dict[coin][2] # calculates difference in coins
                # provides relevant message depending on if there are more or less coins than required
                if coin_difference > 0:
                    print(f"""\nYou need to add {int(coin_difference)} coin(s) to the bag.
-------------------""")
                else:
                    print(f"""\nYou need to remove {int(coin_difference)*-1} coin(s) from the bag.
-------------------""")
                # adds 1 to the "bags_checked" key in the 'overall' dictionary in 'data'
                data[0]["bags_checked"] += 1
                # adds 1 to the "bags_checked" key in the volunteers assigned dictionary in 'data'
                for i in range(len(data)):
                    if data[i]["name"] == volunteer_name:
                        data[i]["bags_checked"] += 1
                        break
                break
            # message for if invalid weight isn't divisible fully by coin type
            else:
                print("""\nBag's weight is not divisible by the selected coin's weight. The bag
was possibly weighed incorrectly or the wrong coin type was selected.

No data has been recorded in relation to this bag because of this.
(Will not effect number of bags checked, total raised or accuracy)
-------------------""")
                break

    # lets the user choose if they want to return to the menu or check another bag
    check_another_bag = input("Do you want to check another bag? (Y/N): ").lower()
    # returns the value of 'data' and the relevant boolian which controls the while loop
    if check_another_bag == "y":
        return data, True
    else:
        return data, False


"""displays information about overall bags counted and individual volunteer performance"""
def volunteer_info(data):
    accuracy_dict = {} # creates a dictionary that records volunteer accuracy
    sorted_accuracy = {} # creates a dictionary to store volunteer accuracy in decending order
    
    for line in data: # iterates throught 'data' to fill 'accuracy_dict'
        if line["name"] != "overall": # excludes the 'overall' dict
            accuracy_dict.update({line["name"]: accuracy(line["valid_bags"], line["bags_checked"])})
    
    # sorts the items from 'accuracy_dict' by value in decending order
    # yes i know it's some lines of code only a mother could love, but i am the mother
    sorted_accuracy = dict(sorted(accuracy_dict.items(), key=lambda item: item[1]
    if item[1] != "N/A" else float("-inf"), reverse=True))
    # the line above checks if the value is not "N/A" and if it is make the 'sorted()' function compare it as -inf
    
    os.system("cls") # clears the terminal, specifically on windows
    print("""==| Volunteer Info-inator |==

Volunteers listed in decending order of accuracy
-------------------""")
# iterates through 'data' and searches for the values of the key "name" in order of 'sorted_accuracy' then prints them
    for name in sorted_accuracy:
        for i in range(len(data)):
            if name == data[i]["name"]:
                print(f"""{data[i]["name"]}:
| Bags Checked - {data[i]["bags_checked"]}
| Valid Bags - {data[i]["valid_bags"]}
| Accuracy - {accuracy(data[i]["valid_bags"], data[i]["bags_checked"])} %
""")
    input("""-------------------
Press ENTER to return to the main menu """)


"""adds a new volunteer to 'CoinCount.txt'"""
def add_new_volunteer(data):
    # creates a list of current names in the system
    current_names = []
    for i in range(len(data)):
        current_names.append(data[i]["name"])
    
    os.system("cls") # clears the terminal, specifically on windows
    print("""==| Add New Volunteer-inator |==
If you ever want to cancel, just leave the input blank and press ENTER""")

    name = input("\nInput the name of the volunteer being added: ")
    
    # if 'name' isn't blank and does not already exist in 'data', it will add a new dict to the list
    if name != "" and name not in current_names:
        # creates new dictionary for the inputed volunteer
        new_volunteer_dict = {'name': name, 'bags_checked': 0, 'valid_bags': 0, 'accuracy': 0}
        # appends a new dictionary to the 'data' list
        data.append(new_volunteer_dict)
        
        print(f"\n'{name}' is being added to the system...")
        time.sleep(3) # makes the program wait for 3 seconds to make the user think it's doing something (spoiler alert: it's not)
        input(f"'{name}' has been added to the system.\nPress ENTER to return to the main menu ")
    elif name in current_names:
        input(f"\n'{name}' is already in the system.\nPress ENTER to return to the main menu ")
    else:
        input("\nCancelling adding a new volunteer.\nPress ENTER to return to the main menu ")

    return data


"""quits the current session and saves all the data"""
def quit_session(data):
    print("Saving Data...\n")
    time.sleep(2) # the fake-loading-time-inator strikes again

    try: # try except checks if the 'write()' function has completed without an error
        write(data) # writes the current value of the 'data' list into the .txt file
        print("Data has been saved.")
    except:
        print(f"""An error occured that resulted in data failing to save to 'CoinCount.txt' or 'Data.txt'.
Here is the data currently stored in temporary memory:
{data}""")
    """this hopefully prevents complete data
    |    | | 
    |    | | |
    -----+-----
    | |  | |
    | |  | | __"""
    return False # results in 'active_session' being set to False, ending the while loop


### MAIN PROGRAM ###


data = read() # assigns the list created in 'read()' to a variable
# dictionary of different possible coins, format = coin: [bag value, bag weight, coin weight]
coin_dict = {
    "£2": [20, 120.00 , 12.00],
    "£1": [20, 175, 8.75],
    "50p": [10, 160, 8.00],
    "20p": [10, 250, 5.00],
    "10p": [5, 325, 6.50],
    "5p": [5, 235, 2.35],
    "2p": [1, 356, 7.12],
    "1p": [1, 356, 3.56]
    }
valid_menu = ["1", "2", "3", "4"] # used in 'menu()' to verify if menu selection is valid
active_session = True # used to control if the while loop is active or not

while active_session == True:
    try: # try except catches any errors that may occur from things like keyboard interupts (e.g ctrl + c)
        os.system("cls") # clears the terminal, specifically on windows
        selection = menu(valid_menu)
        # runs the process the user requested in the menu
        match selection:
            case "1":
                active_loop = True # this variable is used to control the loop of 'bag_check()'
                
                while active_loop:
                    bag_check_output = bag_check(data, coin_dict) # variable that stores the values returned by 'bag_check()'
                    data = bag_check_output[0] # index [0] is for the data that returned
                    active_loop = bag_check_output[1] # index [1] is for the boolian value that's returned
            case "2":
                volunteer_info(data)
            case "3":
                data = add_new_volunteer(data)
            case "4":
                active_session = quit_session(data)
    except:
        print("\nError has occured with you input, returning to menu.")
        time.sleep(3) # it's everyone's favourite! the fake-loading-time-inator is back!

# hi joel, the song which i am listening to, which is one of my favourite songs might i add, just said skibidi
# i never took note of that until you mentioned skibidi toilet ruining jazz
# i just want you to know the consequences of your actions