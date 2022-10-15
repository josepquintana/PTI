import pymongo
import hashlib

# Welcome
print('\nWelcome!\n')

# Confirmation
ask = input("Drop all DB documents? [y/n]:\n > ") 
if ask != "y":
    print("\nQuitting...\n")
    quit()
    
# Connect to MongoDB
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")

# Create a Database
pti_Database = mongoClient["DB_PTI"]

# Create a Collection (Table) for the USERS and assign it to usersCollection variable
usersCollection = pti_Database["users"]
usersCollection.drop()

# Create a Unique Compound Index for all the field to avoid having duplicate users
usersCollection.create_index([("email", 1)], unique=True)

new_password = "qwertyuiop"; # dummy password
hashed_new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
users = [
    { "email": "itoken@josepquintana.me", "password": hashed_new_password, "account": "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1", "api_key": "00000000" }
]

x = usersCollection.insert_many(users)
print(f"Inserted ids:  {x.inserted_ids}")

# Output messages
print("USERS:")
for x in usersCollection.find({}, { "something": 0 }):
    print(x)

databaseList = mongoClient.list_database_names()
if "DB_PTI" in databaseList:
    print("The database has been created.")

collectionList = pti_Database.list_collection_names()
if "users" in collectionList:
    print("The collection exists.")

