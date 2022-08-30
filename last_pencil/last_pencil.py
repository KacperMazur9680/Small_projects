from random import randint

print("How many pencils would you like to use:")
while True:
    try:
        pencils = int(input())
    except ValueError:
        print("The number of pencils should be numeric")
    else:
        if pencils <= 0:
            print("The number of pencils should be positive")
        else: 
            break

print("Who will be the first (John, Jack):")
while True:
    name = input()
    if name != "John" and name != "Jack":
        print("Choose between 'John' and 'Jack'")
    else: 
        break

print("|" * pencils)


while pencils > 0:

    # The algorithm
    if name == "Jack":
        print("Jack's turn:")
        if pencils % 2 == 0:
            even_num = pencils
        else:
            even_num = pencils + 1
        for losing_num in range(1, even_num, 4):
            if losing_num == pencils and pencils > 2:
                rm = randint(1, 3)
            elif losing_num + 1 == pencils:
                rm = 1
            elif losing_num + 2 == pencils:
                rm = 2            
            elif losing_num + 3 == pencils:
                rm = 3
            else:
                rm = 1
        print(rm)

    # Player's move
    else:
        try:
            print("John's turn!")
            rm = int(input())
        except ValueError:
            print("Possible values: '1', '2', '3'")  

    if rm <= 0 or rm > 3:
        print("Possible values: '1', '2', '3'")
    elif (pencils - rm) < 0:
        print("Too many pencils were taken")
    else:
        if rm <= 3:
            print("|" * (pencils - rm))

            if name == "John":
                name = "Jack"
            elif name == "Jack":
                name = "John"
                
            pencils -= rm

if pencils == 0 and name == "John":
    print(f"John won!")

if pencils == 0 and name == "Jack":
    print("Jack won!")