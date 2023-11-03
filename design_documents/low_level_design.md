# Low level design

## Entity Relationship Diagram (ERD)

```
@startuml
!define RECTANGLE class

RECTANGLE User {
   :ID:
   :Username:
   :Password:
}

RECTANGLE Account {
   :ID:
   :Type:
   :Balance:
}

RECTANGLE Credit_Cards {
   :CardNumber:
   :ExpirationDate:
   :CardHolderName:
}

RECTANGLE Debit_Cards {
   :CardNumber:
   :ExpirationDate:
   :CardHolderName:
}

RECTANGLE Transaction {
   :ID:
   :Date:
   :Amount:
}

RECTANGLE Transaction_Details {
   :ProductID:
   :Quantity:
   :Price:
}

RECTANGLE Product {
   :ID:
   :Name:
   :Price:
}

RECTANGLE Validation {
   :ValidationType:
}

RECTANGLE Accounts_Receivable {
   :ID:
   :Amount:
   :DueDate:
}

User "1" -- "0..*" Account : Owns
User "1" -- "0..*" Credit_Cards : Owns
User "1" -- "0..*" Debit_Cards : Owns
Account "1" -- "0..*" Transaction : Initiates
Transaction "1" -- "0..*" Transaction_Details : Includes
Transaction_Details "0..*" -- "1" Product : Relates_to
Transaction "1" -- "0..1" Validation : Requires
Transaction "1" -- "0..*" Accounts_Receivable : Generates

@enduml
```

![ERD](img/ERD.png)

## Sequence Diagram of each ReST API

```angular2html
@startuml
actor User as user
participant "Load Balancer" as lb
participant "Web app servers" as fe
participant "Services(REST)" as be
participant "Database" as db

user -> fe: POST/ users
activate user
activate fe
fe -> be: postData(query)
activate be
be -> db: storeData(query)
activate db
fe --> user: User Creation Response
user -> fe: POST/ auth
fe --> user: User Authentication Response
user -> fe: POST/ accounts
fe --> user: Account Creation Response
user -> fe: POST/ transactions
fe --> user: Transaction Initiation response
user -> fe: POST/ creditcards
fe --> user: Credit Card Validation Response
user -> fe: POST/ debitcards
fe --> user: Debit Card Validation Response
user -> fe: POST /products
db --> be: data
be --> fe: data
fe --> user: Product Creation Response
user -> fe: GET /validation/creditcards/{card_number}
fe -> be: getData(query)
be -> db: getData(query)
fe --> user: Credit Card Status Response
user -> fe: GET /validation/debitcards/{card_number}
fe --> user: Debit Card Status Response
user -> fe: GET /transactions
fe --> user: Transaction List Response
user -> fe: GET /accounts/receivable
db --> be: data
be --> fe: data
fe --> user: Accounts Receivable List Response
user -> fe: PUT /products/{product_id}
fe -> be: putData(query)
be -> db: storeData(query)
db --> be: data
deactivate db
be --> fe: data
deactivate be
fe --> user: Product Update Response
deactivate fe

loop [Every 30 seconds]
fe -> be: getData(query)
activate fe
activate be
be -> db: getData(data)
activate db
db --> be: data
deactivate db
be --> fe: data
deactivate be
fe --> user: updateView
deactivate fe
deactivate user
end

@enduml
```

![sequence_diagram](<img/sequence_diagram.png>)

## ReST API design
```angular2html
1. Create User:
Endpoint: POST /users
Description: Registers a new user in the system.

Input:
Request Field	Field Type	Field Description
username        String      User's username
password        String      User's password

Output:
Response Field	    Field Type	Field Description
user_id	            String      ID of the newly created user
content-type	    MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/users -i -H 'Accept: application/json' -d '{"username": "example_user", "password": "secure_password"}' -X POST

Successful response:
HTTP/1.1 201 Created
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "user_id": "1234",
  "content-type": "application/json"
}

Other than successful:
HTTP/1.1 400 Bad Request
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "message": "Invalid username or password format"
}

2. Authenticate User:
Endpoint: POST /auth
Description: Verifies user credentials for login.
    
Input:
Request Field	Field Type	Field Description
username        String      User's username
password        String      User's password

Output:
Response Field	    Field Type	Field Description
access_token	    String      Token for authentication
content-type	    MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/auth -i -H 'Accept: application/json' -d '{"username": "example_user", "password": "secure_password"}' -X POST

Successful response:
HTTP/1.1 200 OK
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Other than successful:
HTTP/1.1 401 Unauthorized
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "message": "Invalid username or password"
}

3. Create Account:
Endpoint: POST /accounts
Description: Creates a new account for a user.
    
Input:
Request Field	Field Type	Field Description
user_id          String      User's ID
account_type     String      Type of account to be created
initial_balance  Float       Initial balance for the account

Output:
Response Field	    Field Type	Field Description
account_id	        String      ID of the newly created account
content-type	    MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/accounts -i -H 'Accept: application/json' -d '{"user_id": "1234", "account_type": "savings", "initial_balance": 1000}' -X POST

Successful response:
HTTP/1.1 201 Created
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "account_id": "5678",
  "content-type": "application/json"
}

Other than successful:
HTTP/1.1 400 Bad Request
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "message": "Invalid user ID or account type"
}

4. Initiate Transaction:
Endpoint: POST /transactions
Description: Initiates a financial transaction between accounts.
    
Input:
Request Field	Field Type	Field Description
from_account_id     String     Account ID for sender
to_account_id       String     Account ID for receiver
amount              Float      Amount to be transacted

Output:
Response Field	    Field Type	Field Description
transaction_id	    String      ID of the initiated transaction
content-type	    MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/transactions -i -H 'Accept: application/json' -d '{"from_account_id": "5678", "to_account_id": "9101", "amount": 500}' -X POST

Successful response:
HTTP/1.1 201 Created
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "transaction_id": "123456",
  "content-type": "application/json"
}

Other than successful:
HTTP/1.1 400 Bad Request
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "message": "Invalid account IDs or amount"
}

5. Validate Credit Card:
Endpoint: POST /creditcards/validate
Description: Validates a credit card.
    
Input:
Request Field	Field Type	Field Description
card_number       String     Credit card number
expiration_date   Date       Expiration date of the card

Output:
Response Field	   Field Type	Field Description
valid	           Boolean     Indicates card validity
content-type	   MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/creditcards/validate -i -H 'Accept: application/json' -d '{"card_number": "1234567890123456", "expiration_date": "12/25"}' -X POST

Successful response:
HTTP/1.1 200 OK
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "valid": true,
  "content-type": "application/json"
}

Other than successful:
HTTP/1.1 404 Not Found
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "valid": false,
  "content-type": "application/json"
}

6. Validate Debit Card:
Endpoint: POST /debitcards/validate
Description: Validates a debit card.
    
Input:
Request Field	Field Type	Field Description
card_number       String     Debit card number
balance           Float      Balance in the card

Output:
Response Field	   Field Type	Field Description
valid	           Boolean     Indicates card validity
content-type	   MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/debitcards/validate -i -H 'Accept: application/json' -d '{"card_number": "9876543210987654", "balance": 250}' -X POST

Successful response:
HTTP/1.1 200 OK
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "valid": true,
  "content-type": "application/json"
}

Other than successful:
HTTP/1.1 404 Not Found
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "valid": false,
  "content-type": "application/json"
}

7. Check Credit Card Validation Status:
Endpoint: GET /validation/creditcards/{card_number}
Description: Retrieves the validation status of a credit card.

Input:
Request Field	Field Type	Field Description
card_number       String     Credit card number

Output:
Response Field	    Field Type	Field Description
validation_status  String      Status of card validation
content-type	    MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/validation/creditcards/1234567890123456 -i -H 'Accept: application/json' -X GET

Successful response:
HTTP/1.1 200 OK
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "validation_status": "Valid",
  "content-type": "application/json"
}

Other than successful:
HTTP/1.1 404 Not Found
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "validation_status": "Invalid",
  "content-type": "application/json"
}

8. Check Debit Card Validation Status:
Endpoint: GET /validation/debitcards/{card_number}
Description: Retrieves the validation status of a debit card.
    
Input:
Request Field	Field Type	Field Description
card_number       String     Debit card number

Output:
Response Field	    Field Type	Field Description
validation_status  String      Status of card validation
content-type	    MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/validation/debitcards/9876543210987654 -i -H 'Accept: application/json' -X GET

Successful response:
HTTP/1.1 200 OK
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "validation_status": "Valid",
  "content-type": "application/json"
}

Other than successful:
HTTP/1.1 404 Not Found
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "validation_status": "Invalid",
  "content-type": "application/json"
}

9. Get Transaction List:
Endpoint: GET /transactions
Description: Retrieves a list of transactions.

Input:
Request Field	Field Type	Field Description
None

Output:
Response Field	    Field Type	Field Description
transactions	    List        List of transaction objects
content-type	    MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/transactions -i -H 'Accept: application/json' -X GET

Successful response:
HTTP/1.1 200 OK
date: <Date>
server: uvicorn
content-type: application/json
Response Body
[
  {
    "transaction_id": "123456",
    "amount": 500.00,
    "date": "2023-11-10",
    "content-type": "application/json"
  },
  {
    "transaction_id": "789012",
    "amount": 1000.00,
    "date": "2023-11-09",
    "content-type": "application/json"
  },
  ...
]

Other than successful:
HTTP/1.1 404 Not Found
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "message": "No transactions found"
}

10. Get Accounts Receivable List:
Endpoint: GET /accounts/receivable
Description: Retrieves a list of accounts receivable.

Input:
Request Field	Field Type	Field Description
None

Output:
Response Field	    Field Type	Field Description
receivables	        List        List of accounts receivable
content-type	    MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/accounts/receivable -i -H 'Accept: application/json' -X GET

Successful response:
HTTP/1.1 200 OK
date: <Date>
server: uvicorn
content-type: application/json
Response Body
[
  {
    "account_id": "5678",
    "amount": 1000.00,
    "due_date": "2023-12-01",
    "content-type": "application/json"
  },
  {
    "account_id": "9101",
    "amount": 750.00,
    "due_date": "2023-11-25",
    "content-type": "application/json"
  },
  ...
]

Other than successful:
HTTP/1.1 404 Not Found
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "message": "No accounts receivable found"
}

11. Create Product:
Endpoint: POST /products
Description: Adds a new product to the system.
    
Input:
Request Field	Field Type	Field Description
product_name      String     Name of the product
price             Float      Price of the product

Output:
Response Field	    Field Type	Field Description
product_id	        String      ID of the newly created product
content-type	    MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/products -i -H 'Accept: application/json' -d '{"product_name": "New Product", "price": 49.99}' -X POST

Successful response:
HTTP/1.1 201 Created
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "product_id": "1234",
  "content-type": "application/json"
}

Other than successful:
HTTP/1.1 400 Bad Request
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "message": "Invalid product name or price"
}

12. Update Product:
Endpoint: PUT /products/{product_id}
Description: Updates an existing product.

Input:
Request Field	Field Type	Field Description
product_name      String     New name of the product (optional)
price             Float      New price of the product (optional)

Output:
Response Field	    Field Type	Field Description
content-type	    MIME        MIME type of the response content

Example request/response:
$ curl 'http://localhost:8000/products/1234 -i -H 'Accept: application/json' -d '{"product_name": "Updated Product Name", "price": 59.99}' -X PUT

Successful response:
HTTP/1.1 200 OK
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "content-type": "application/json"
}

Other than successful:
HTTP/1.1 400 Bad Request
date: <Date>
server: uvicorn
content-type: application/json
Response Body
{
  "message": "Invalid product update data"
}
```

## how each backend module performs its job

```
@startuml
class UserModule {
   - userId: Integer
   - username: String
   - password: String

   + createUser(): Boolean
   + authenticateUser(): Boolean
}

class AccountModule {
   - accountId: Integer
   - balance: Float

   + createAccount(): Boolean
   + updateBalance(): Boolean
   + getBalance(): Float
}

class TransactionModule {
   - transactionId: Integer
   - amount: Float

   + initiateTransaction(): Boolean
   + processTransaction(): Boolean
   + validateTransaction(): Boolean
}

class CreditCardModule {
   - cardNumber: String
   - expirationDate: Date

   + validateCard(): Boolean
}

class DebitCardModule {
   - cardNumber: String
   - balance: Float

   + validateCard(): Boolean
}

class ValidationModule {
   + checkCreditCard(): Boolean
   + checkDebitCard(): Boolean
}

class BalanceModule {
   + calculateTotalBalance(): Float
   + calculatePeriodBalance(): Float
}

class TransactionManagementModule {
   + getTransactionList(): List
   + getAccountsReceivableList(): List
}

class ProductModule {
   - productId: Integer
   - price: Float

   + createProduct(): Boolean
   + updateProduct(): Boolean
}

UserModule "1" -- "0..*" AccountModule : Manages
AccountModule "1" -- "0..*" TransactionModule : Initiates
TransactionModule "0..*" -- "1" ValidationModule : Validates
TransactionModule "0..*" -- "0..1" ProductModule : Involves
CreditCardModule "0..*" -- "1" ValidationModule : Validated by
DebitCardModule "0..*" -- "1" ValidationModule : Validated by
TransactionModule "1" -- "0..1" BalanceModule : Calculates
TransactionManagementModule "1" -- "0..1" TransactionModule : Manages
@enduml
```

![module diagram](<img/module diagram .png>)
