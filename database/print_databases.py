import pymongo

# Welcome
print('\nDATABASE CONTENT:\n')
print('====================================================================\n\n')

# Connect to MongoDB
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")

# Select Database
pti_Database = mongoClient["DB_PTI"]

# ACCOUNTS DB
print("ACCOUNTS: ")
for x in pti_Database["accounts"].find({}):
    print(x)

print('\n\n====================================================================\n\n')
    
# USERS DB
print("USERS: ")
for x in pti_Database["users"].find({}):
    print(x)
    
print('\n\n====================================================================\n\n')
    
# BIDS DB
print("BIDS: ")
for x in pti_Database["bids"].find({}):
    print(x)
    
print('\n\n====================================================================\n\n')    
    
print('BYE!\n')