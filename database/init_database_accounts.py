import pymongo

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

# Create a Collection (Table) for the ACCOUNTS and assign it to accountsCollection variable
accountsCollection = pti_Database["accounts"]
accountsCollection.drop()

# Create a Unique Compound Index for all the field to avoid having duplicate accounts
accountsCollection.create_index([("account", 1), ("private_key", 1)], unique=True)

accounts = [
    { "account": "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1", "private_key": "4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d" },
    { "account": "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0", "private_key": "6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1" },
    { "account": "0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b", "private_key": "6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c" },
    { "account": "0xE11BA2b4D45Eaed5996Cd0823791E0C93114882d", "private_key": "646f1ce2fdad0e6deeeb5c7e8e5543bdde65e86029e2fd9fc169899c440a7913" },
    { "account": "0xd03ea8624C8C5987235048901fB614fDcA89b117", "private_key": "add53f9a7e588d003326d1cbf9e4a43c061aadd9bc938c843a79e7b4fd2ad743" },
    { "account": "0x95cED938F7991cd0dFcb48F0a06a40FA1aF46EBC", "private_key": "395df67f0c2d2d9fe1ad08d1bc8b6627011959b79c53d7dd6a3536a33ab8a4fd" },
    { "account": "0x3E5e9111Ae8eB78Fe1CC3bb8915d5D461F3Ef9A9", "private_key": "e485d098507f54e7733a205420dfddbe58db035fa577fc294ebd14db90767a52" },
    { "account": "0x28a8746e75304c0780E011BEd21C72cD78cd535E", "private_key": "a453611d9419d0e56f499079478fd72c37b251a94bfde4d19872c44cf65386e3" },
    { "account": "0xACa94ef8bD5ffEE41947b4585a84BdA5a3d3DA6E", "private_key": "829e924fdf021ba3dbbc4225edfece9aca04b929d6e75613329ca6f1d31c0bb4" },
    { "account": "0x1dF62f291b2E969fB0849d99D9Ce41e2F137006e", "private_key": "b0057716d5917badaf911b193b12b910811c1497b5bada8d7711f758981c3773" }
]

x = accountsCollection.insert_many(accounts)
print(f"Inserted ids:  {x.inserted_ids}")

# Output messages
print("ACCOUNTS:")
for x in accountsCollection.find({}, { "something": 0 }):
    print(x)

databaseList = mongoClient.list_database_names()
if "DB_PTI" in databaseList:
    print("The database has been created.")

collectionList = pti_Database.list_collection_names()
if "accounts" in collectionList:
    print("The collection exists.")

