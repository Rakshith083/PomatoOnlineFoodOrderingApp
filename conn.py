import pymongo

def mongoConnect():
    conString="mongodb://localhost:27017/"
    myclient = pymongo.MongoClient(conString,tlsAllowInvalidCertificates=True)
    if myclient.server_info():
        print("Connected")
    else:
        print("Unable to connect")

    mydb = myclient["food"]
    return mydb
