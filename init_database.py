import pymongo

# Welcome
print('\nWelcome!\n')

# Connect to MongoDB
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")

# Create a Database
pti_Database = mongoClient["DB_PTI"]

# Create a Collection (Table) for the open BIDS and assign it to bidsCollection variable
bidsCollection = pti_Database["bids"]
#bidsCollection.drop()

# Create a Unique Compound Index for all the field to avoid having duplicate bids
bidsCollection.create_index([("user", 1), ("buy_amount", 1), ("buy_currency", 1), ("sell_amount", 1), ("sell_currency", 1)], unique=True)

bid = { 
    "user": "trader3",
    "buy_amount": "750",
    "buy_currency": "LTC", 
    "sell_amount": "250",
    "sell_currency": "ETH"
}
#x = bidsCollection.insert_one(bid)
#print(f"Inserted id:  {x.inserted_id}")

print("BIDS:")
for x in bidsCollection.find({}, { "something": 0 }):
    print(x)

# Output messages (won't work, there's no content stored)
databaseList = mongoClient.list_database_names()
if "DB_PTI" in databaseList:
    print("The database has been created.")

collectionList = pti_Database.list_collection_names()
if "bids" in collectionList:
    print("The collection exists.")

