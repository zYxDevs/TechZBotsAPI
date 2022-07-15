from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

MONGO_DB_URI = "mongodb+srv://techz:wall@techzwallbotdb.katsq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.api.req

data = {'thumb':0,'wall/logo':0,'other':0}
pos = 0

async def add_to_db(type):
    global pos, data

    try:
        if data['thumb'] == 0:
            x = await db.find_one({"id": 1})
            data = x['data']
    except:
        pass

    if type == 1:
        data['thumb'] += 1
    elif type == 2:
        data['wall/logo'] += 1
    elif type == 3:
        data['other'] += 1

    if pos > 20 :
        pos = 0
        data = await db.update_one({"id": 1},{"$set": {"data": data}},upsert=True)
    return