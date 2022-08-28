msg_0 = "Enter an equation"
msg_1 = "Do you even know what numbers are? Stay focused!"
msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
msg_3 = "Yeah... division by zero. Smart move..."
msg_4 = "Do you want to store the result? (y / n):" 
msg_5 = "Do you want to continue calculations? (y / n):"
msg_6 = " ... lazy"
msg_7 = " ... very lazy"
msg_8 = " ... very, very lazy"
msg_9 = "You are"
msg_ =  {
        10: "Are you sure? It is only one digit! (y / n)",
        11: "Don't be silly! It's just one number! Add to the memory? (y / n)",
        12: "Last chance! Do you really want to embarrass yourself? (y / n)"
}
memo = 0

def if_num(num: str):
    if "." in num:
        num = float(num)
    elif num.isnumeric():
        num = int(num)
    return num

def is_one_digit(num):
    try:
        output = num.is_integer()
    except AttributeError:
        if num > -10 and num < 10:
            return True
        else: 
            return False
    else:
        if output:
            if num > -10 and num < 10:
                return True
            else: 
                return False
        else:
            return False

def stage_2(num_1, num_2, sign):
    
    msg = ""
    if is_one_digit(num_1) and is_one_digit(num_2):
        msg = msg + msg_6
    if (num_1 == 1 or num_2 == 2) and sign == "*":
        msg = msg + msg_7
    if (num_1 == 0 or num_2 == 0) and (sign == "*" or sign == "+" or sign == "-"):
        msg = msg + msg_8
    if msg != "":
        msg = msg_9 + msg
    print(msg)

def stage_1():
    while True:
        print(msg_0)
        calc = input()

        global x ,oper, y
        try:
            x, oper, y = calc.split()
        except ValueError:
            print("Two nums and between them an operator buddy, c'mon!")

        x = if_num(x)
        y = if_num(y)

        if x == "M":
            x = float(memo)
        if y == "M":
            y = float(memo)    
    
        if type(x) is str or type(y) is str:
            print(msg_1) 
        if oper not in "+-/*":
            print(msg_2)
        else:
            stage_2(x, y, oper)
        if oper == "/" and y == 0:
            print(msg_3)
        else:
            break

    global result

    if oper == "+":
        result = float(x + y)
    if oper == "-":
        result = float(x - y)
    if oper == "*":
        result = float(x * y)
    if oper == "/":
        result = float(x / y)
    
    print(result)

stage_1()

while True:
    
    while True:
        print(msg_4)
        answer = input()

        if answer == "y":
            if is_one_digit(result):
                msg_index = 10
                
                while True:
                    print(msg_[msg_index])
                    ans = input()
                    if ans == "y":
                        if msg_index < 12:
                            msg_index = msg_index + 1
                        else:
                            memo = result
                            break
                    if ans == "n":
                        break
                    else:
                        continue
            else:
                memo = result

        elif answer == "n":
            pass
        else:
            continue

        print(msg_5)
        answer = input()
    
        if answer == "y":
            stage_1()
        elif answer == "n":
            break
        else:
            continue
    break
