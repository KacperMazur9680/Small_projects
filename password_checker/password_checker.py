# Prompt user to enter a password
password = input("Podaj hasło: ")

lower_case = False
upper_case = False
space = False
special_char = False

# Checking each character of the password
for char in password:
    if char.islower():
        lower_case = True
    elif char.isupper():
        upper_case = True
    elif char.isspace():
        space = True
    else:
        special_char = True

length = len(password) >= 8

correct = lower_case and upper_case and not space and special_char and length

raport = ""

# Informing the user if the password is correct, if not, listing what's wrong
if correct:
    raport += "Hasło poprawne"
else:
    raport += "Uwagi: \n"
    if not lower_case:
        raport += "- hasło nie posiada małej litery\n"
    if not upper_case:
        raport += "- hasło nie posiada dużej litery\n"
    if space:
        raport += "- hasło nie może zawierać spacji\n"
    if not special_char:
        raport += "- hasło nie posiada znaku specjalnego\n"
    if not length:
        raport += "- hasło za krótkie\n"

print(raport)