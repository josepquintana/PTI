import pymongo

# Welcome
print('\nWelcome!\n')

# Connect to MongoDB
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")

# Create a Database
pti_Database = mongoClient["DB_PTI"]

# Create a Collection (Table) for the open BIDS and assign it to bidsCollection variable
bidsCollection = pti_Database["bids"]
bidsCollection.drop()

# Create a Unique Compound Index for all the field to avoid having duplicate bids
bidsCollection.create_index([("owner", 1), ("buy_amount", 1), ("buy_currency", 1), ("sell_amount", 1), ("sell_currency", 1)], unique=True)

newBids = [
    { "owner": "jquintana", "buy_amount": 200, "buy_currency": "FBC", "sell_amount": 100, "sell_currency": "BNC"},
    { "owner": "trader1",   "buy_amount": 100, "buy_currency": "BNC", "sell_amount": 200, "sell_currency": "FBC"},
    { "owner": "jquintana", "buy_amount": 750, "buy_currency": "BNC", "sell_amount": 250, "sell_currency": "FBC"},
    { "owner": "trader2",   "buy_amount": 250, "buy_currency": "FBC", "sell_amount": 750, "sell_currency": "BNC"},
    { "owner": "jquintana", "buy_amount": 25,  "buy_currency": "BNC", "sell_amount": 250, "sell_currency": "FBC"},
    { "owner": "trader3",   "buy_amount": 750, "buy_currency": "FBC", "sell_amount": 25,  "sell_currency": "BNC"}
]

x = bidsCollection.insert_many(newBids)
print(f"Inserted ids:  {x.inserted_ids}")

# Output messages
print("BIDS:")
for x in bidsCollection.find({}, { "something": 0 }):
    print(x)

databaseList = mongoClient.list_database_names()
if "DB_PTI" in databaseList:
    print("The database has been created.")

collectionList = pti_Database.list_collection_names()
if "bids" in collectionList:
    print("The collection exists.")

