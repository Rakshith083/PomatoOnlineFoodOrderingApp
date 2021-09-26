import pymongo

def mongoConnect():
    # conString="mongodb://localhost:27017/"
    conString="mongodb+srv://rakshith:rakshi12@cluster0.grxrq.mongodb.net/food"
    myclient = pymongo.MongoClient(conString,tlsAllowInvalidCertificates=True)
    if myclient.server_info():
        print("Connected")
    else:
        print("Unable to connect")

    mydb = myclient["food"]
    return mydb