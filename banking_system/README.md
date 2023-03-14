## Banking system
A simple banking system program with a database (sqlite3) with various operations:
* Create an account
    * Automatically creates a card number (with a valid Account Identifier using Luhn algorithm)
    * Generates a pin
    * Keeps the information in a database
    
* Log into account
    * Balance - returns the balance on said card
    * Add income - updated the database balance
    * Do transfer - allows tranfering money from one account to another
    * Close account - deletes the account from the database
    * Log out 

## Example
> python .\Small_projects\banking_system\banking_sys.py