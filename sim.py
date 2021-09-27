import numpy as np
import os
import datetime
import pytz 
from flask import Flask,render_template,request,redirect
from conn import mongoConnect
from flask_mail import Mail,Message
from random import randint

app = Flask(__name__) 
app.secret_key = "ayush" 

app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465     
app.config["MAIL_USERNAME"] = 'Your mail here'  
app.config['MAIL_PASSWORD'] = 'password here'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
mail = Mail(app) 

mydb =mongoConnect()
pat=os.getcwd()

code=[]
restaurant_details=[]
user_details=[]
item_details=[]
restorLoginfo=[]
userloginfo=[]

def clear():
    code.clear()
    restaurant_details.clear()
    user_details.clear()
    item_details.clear()
    restorLoginfo.clear()
    userloginfo.clear()

@app.route("/")
def home():
    clear()
    mycol=mydb["Restaurants"]
    res=[]
    for x in mycol.find():
        res.append(x) 
    chunk_result=[]

    two_split = np.array_split(res, 3)
    for array in two_split:
        chunk_result.append(list(array))
    print(chunk_result)
    
    return render_template("home.html",columns=chunk_result,method="close()")

@app.route('/signup/<op>',methods=['post'])
def signup(op):
    code.clear()
    if op == 'Restaurant':
        email=request.form['email']
        code .append(randint(000000, 999999)) 
        print(code)
        msg = Message('Authentication Code', sender='foodyLover083@gmail.com',recipients=[email])
        msg.body = "Your Authentication code for now is : "+str(code[0])
        mail.send(msg)
        mycol = mydb["Restaurants"]

        query={"email":email}
        res=[]
        for x in mycol.find(query):
            res.append(x["Restaurant"])
        print(res)

        if len(res)==0:
            return render_template("Restaurantsignup.html",email=email)
        else:
            message="User already exist! login to continue ."
            return render_template('home.html',method="RestoLog()",email=email,message=message)
    elif op == "User":
        email=request.form['email']
        code .append(randint(000000, 999999)) 
        print(code)
        msg = Message('Authentication Code', sender='foodyLover083@gmail.com',recipients=[email])
        msg.body = "Your Authentication code for now is : "+str(code[0])
        mail.send(msg)

        mycol = mydb["Users"]

        query={"email":email}
        res=[]
        for x in mycol.find(query):
            res.append(x["Name"])
        print(res)

        if len(res)==0:
            return render_template("UserSign.html",email=email)
        else:
            message="User already exist! login to continue ."
            return render_template('home.html',email=email,message=message,method="UserLog()")

@app.route('/<op>/complete/SignUp',methods=['post'])
def CompleteSignUp(op):
    if op=='Restorant':
        otp=int(request.form['otp'])

        os.chdir(pat+"\static")

        restName=request.form['restName']
        email=request.form['email']
        contact=request.form['contact']

        f = request.files['pic']  
        f.save(f.filename)
        print("File : ",f.filename)
        extension="."+f.filename.split(".")[1]
        restimg=restName+str(randint(00, 99))+extension

        os.rename(f.filename,restimg)

        os.chdir(pat)
        
        state=request.form['state']
        dist=request.form['dist']
        tal=request.form['loc']
        area=request.form['area']
        pin=request.form['pin']

        data={
            "Restaurant":restName,
            "email":email,
            "contact":contact,
            "ImageFile":restimg,
            "area":area,
            "Talluk":tal,
            "dist":dist,
            "state":state,
            "pin":pin}

        restorLoginfo.append(data)
        print(code[0])
        if otp==code[0]:  
            code.clear()
            mycol=mydb['Restaurants']
            mycol.insert_one(data)
            return render_template("Restomain.html",disp="block")
        else:
            message="Invalid Authentication Code"
            return render_template("RestaurantSignup.html",message=message,email=email)
    elif op=='User':
        otp=int(request.form['otp'])

        name=request.form['username']
        email=request.form['email']
        contact=request.form['contact']

        state=request.form['state']
        dist=request.form['dist']
        tal=request.form['loc']
        area=request.form['area']
        pin=request.form['pin']

        data={
            "Name":name,
            "email":email,
            "contact":contact,
            "area":area,
            "Talluk":tal,
            "dist":dist,
            "state":state,
            "pin":pin
            }
            
        print(data)
        print(code[0])
        if otp==code[0]:  
            code.clear()
            mycol = mydb["Users"]
            mycol.insert_one(data)
            userloginfo.append(data)
            return redirect("/User/main")
        else:
            message="Invalid Authentication Code"
            return render_template("UserSign.html",message=message,email=email)


@app.route('/login/<op>' , methods=["POST"])
def login(op):
    code.clear()
    if op=="Restaurant":
        email=request.form["email"]
        code .append(randint(000000, 999999)) 
        print(code)
        msg = Message('Authentication Code', sender='foodyLover083@gmail.com',recipients=[email])
        msg.body = "Your Authentication code for now is : "+str(code[0])
        mail.send(msg)

        mycol = mydb["Restaurants"]

        query={"email":email}
        for x in mycol.find(query):
            restorLoginfo.append(x)
        print(restorLoginfo)
        if len(restorLoginfo)>=1:
            return render_template("RestoLog.html",email=email)
        else:
            message="User doesn't exist !! Continue with SignUp"
            return render_template("RestaurantSignup.html",email=email,message2=message)
    elif op=="User":
        email=request.form["email"]
        code.append(randint(000000, 999999)) 
        print(code)
        msg = Message('Authentication Code', sender='foodyLover083@gmail.com',recipients=[email])
        msg.body = "Your Authentication code for now is : "+str(code[0])
        mail.send(msg)

        mycol = mydb["Users"]

        query={"email":email}
        for x in mycol.find(query):
            userloginfo.append(x)
        print(userloginfo)
        if len(userloginfo)>=1:
            return render_template("UserLog.html",email=email)
        else:
            message="User doesn't exist !! Continue with SignUp"
            return render_template("UserSign.html",email=email,message2=message)

@app.route("/login/complete/<op>", methods=["POST"])
def Restomain(op):
    if op=="Restaurant":
        email=request.form["email"]
        restaurant_details.append(email)
        otp=int(request.form["otp"])
        print(email,otp,code)
        if otp==code[0]:
            print(restorLoginfo)
            return redirect("/Restaurant/main")
        else:
            return render_template("RestoLog.html",email=email,msg2="Invalid authentication code")
    elif op=="User":
        email=request.form["email"]
        userloginfo.append(email)
        otp=int(request.form["otp"])
        print(email,otp,code)
        if otp==code[0]:
            return redirect("/User/main")
        else:
            return render_template("RestoLog.html",email=email,msg2="Invalid authentication code")


@app.route('/<op>/main')
def showMain(op):
    if op=="Restaurant":
        mycol=mydb["Menu"]
        print(restorLoginfo[0]["email"])
        query={'email': restorLoginfo[0]["email"]}
        
        res2=[]
        for x in mycol.find(query):
            res2.append(x)
        if(len(res2)==0):
            return render_template("Restomain.html",disp="block",email=restorLoginfo[0]["email"])
        else:
            chunk_result=[]

            two_split = np.array_split(res2, 3)
            for array in two_split:
                chunk_result.append(list(array))
                
            for i in chunk_result:
                print(i)
            return render_template("Restomain.html",columns=chunk_result,disp="none",email=restorLoginfo[0]["email"])
    elif op=="User":
        mycol=mydb["Menu"]
        print(userloginfo[0]["email"])
        query={

            'Restorant talluk': userloginfo[0]["Talluk"],
            "Food Status":"Available"
            }
        res2=[]
        for x in mycol.find(query):
            res2.append(x)

        chunk_result=[]

        two_split = np.array_split(res2, 3)
        for array in two_split:
            chunk_result.append(list(array))
        print(chunk_result)
        return render_template("Usermain.html",chunks=chunk_result,email=userloginfo[0]["email"],top="Menus")

@app.route("/FOODS/<email>")
def restoFoods(email):
    mycol=mydb["Menu"]
    query={
        "email":email,
        "Food Status":"Available"
    }
    res=[]

    for x in mycol.find(query):
        res.append(x)
    chunk_result=[]

    two_split = np.array_split(res, 3)
    for array in two_split:
        chunk_result.append(list(array))
    top=res[0]["Restaurant"]
    return render_template("Usermain.html",chunks=chunk_result,email=userloginfo[0]["email"],top=top)

@app.route('/Restaurant/<email>/<status>')
def showfood(email,status):
    mycol=mydb["Menu"]
    query={
        "email":email,
        "Food Status":status
    }
    res=[]
    for x in mycol.find(query):
        res.append(x)
    chunk_result=[]

    two_split = np.array_split(res, 3)
    for array in two_split:
        chunk_result.append(list(array))
                
    for i in chunk_result:
        print(i)
    return render_template("Restomain.html",columns=chunk_result,disp="none",email=restorLoginfo[0]["email"])

@app.route("/add/<op>",methods=["POST"])
def add(op):
    mycol=mydb["Menu"]
    os.chdir(pat+"\static")
    print("#################################################",restaurant_details)
    if op=="single":
        fname=request.form["foodName"]
        fprice=request.form["foodPrice"]+"/-Rs"

        f = request.files["foodFile"]  
        f.save(f.filename)
        print("File : ",f.filename)
        extension="."+f.filename.split(".")[1]

        restimg=restorLoginfo[0]["Restaurant"]+str(randint(00, 99))+fname+extension

        os.rename(f.filename,restimg)
        status=request.form["status"]

        data={
            "Food Name":fname,
            "Food Price" :fprice,
            "File":restimg,
            "Food Status": status,
            "Restaurant":restorLoginfo[0]["Restaurant"],
            "email":restorLoginfo[0]["email"],
                "Restorant talluk":restorLoginfo[0]["Talluk"]
        }
        print(data)
    
        mycol.insert_one(data)
        os.chdir(pat)
        return redirect("/Restaurant/main")
    elif op=="many":
        ##########################################################
        food1Name=request.form["food1Name"]
        food1Price=request.form["food1Price"]+"/-Rs"

        f1 = request.files["food1File"]  
        f1.save(f1.filename)
        print("File : ",f1.filename)
        extension="."+f1.filename.split(".")[1]

        restimg1=restorLoginfo[0]["Restaurant"]+str(randint(00, 99))+food1Name+extension

        os.rename(f1.filename,restimg1)
        food1Status=request.form["food1Status"]

        ##################################################################
        food2Name=request.form["food2Name"]
        food2Price=request.form["food2Price"]+"/-Rs"

        f2 = request.files["food2File"]  
        f2.save(f2.filename)
        print("File : ",f2.filename)
        extension="."+f2.filename.split(".")[1]

        restimg2=restorLoginfo[0]["Restaurant"]+str(randint(00, 99))+food2Name+extension

        os.rename(f2.filename,restimg2)
        food2Status=request.form["food2Status"]
        ####################################################################
        food3Name=request.form["food3Name"]
        food3Price=request.form["food3Price"]+"/-Rs"

        f3 = request.files["food3File"]  
        f3.save(f3.filename)
        print("File : ",f3.filename)
        extension="."+f3.filename.split(".")[1]

        restimg3=restorLoginfo[0]["Restaurant"]+str(randint(00, 99))+food3Name+extension

        os.rename(f3.filename,restimg3)
        food3Status=request.form["food3Status"]

        ############################################################################
        food4Name=request.form["food4Name"]
        food4Price=request.form["food4Price"]+"/-Rs"

        f4 = request.files["food4File"]  
        f4.save(f4.filename)
        print("File : ",f4.filename)
        extension="."+f4.filename.split(".")[1]

        restimg4=restorLoginfo[0]["Restaurant"]+str(randint(00, 99))+food4Name+extension

        os.rename(f4.filename,restimg4)
        food4Status=request.form["food4Status"]
        #############################################################################
        food5Name=request.form["food5Name"]
        food5Price=request.form["food5Price"]+"/-Rs"

        f5 = request.files["food5File"]  
        f5.save(f5.filename)
        print("File : ",f5.filename)
        extension="."+f5.filename.split(".")[1]

        restimg5=restorLoginfo[0]["Restaurant"]+str(randint(00, 99))+food5Name+extension

        os.rename(f5.filename,restimg5)
        food5Status=request.form["food5Status"]
        ############################################################################

        data=[
            {
                "Food Name":food1Name,
                "Food Price" :food1Price,
                "File":restimg1,
                "Food Status": food1Status,
                "Restaurant":restorLoginfo[0]["Restaurant"],
                "email":restorLoginfo[0]["email"],
                "Restorant talluk":restorLoginfo[0]["Talluk"]
            },

            {
                "Food Name":food2Name,
                "Food Price" :food2Price,
                "File":restimg2,
                "Food Status": food2Status,
                "Restaurant":restorLoginfo[0]["Restaurant"],
                "email":restorLoginfo[0]["email"],
                "Restorant talluk":restorLoginfo[0]["Talluk"]
            },

            {
                "Food Name":food3Name,
                "Food Price" :food3Price,
                "File":restimg3,
                "Food Status": food3Status,
                "Restaurant":restorLoginfo[0]["Restaurant"],
                "email":restorLoginfo[0]["email"],
                "Restorant talluk":restorLoginfo[0]["Talluk"]
            },

            {
                "Food Name":food4Name,
                "Food Price" :food4Price,
                "File":restimg4,
                "Food Status": food4Status,
                "Restaurant":restorLoginfo[0]["Restaurant"],
                "email":restorLoginfo[0]["email"],
                "Restorant talluk":restorLoginfo[0]["Talluk"]
            },

            {
                "Food Name":food5Name,
                "Food Price" :food5Price,
                "File":restimg5,
                "Food Status": food5Status,
                "Restaurant":restorLoginfo[0]["Restaurant"],
                "email":restorLoginfo[0]["email"],
                "Restorant talluk":restorLoginfo[0]["Talluk"]
            },
        ]
        print(data)
        x=mycol.insert_many(data)
        print(x.inserted_ids)
        os.chdir(pat)
        return redirect("/Restaurant/main")

fname=[]
@app.route("/edit/<email>/<foodname>" , methods=["GET"])
def editFood(email,foodname):
    fname.append(foodname)
    if request.method=='GET':
        mycol=mydb["Menu"]
        query={
            "Food Name":foodname,
            "email":email
        }
        res=[]
        for x in mycol.find(query):
            res.append(x)
        fname.append(res[0]["File"])
        return render_template("editFood.html",vals=res[0])

@app.route("/remove/<email>/<filename>" )
def deleteFood(email,filename):
    os.chdir(pat+"\static")
    os.remove(filename)
    mycol=mydb["Menu"]
    query={
        "File":filename,
        "email":email
    }
    mycol.delete_one(query)
    os.chdir(pat)
    return redirect("/Restaurant/main")

@app.route("/update/food",methods=["POST"])
def updateFood():
    os.chdir(pat+"\static")
    mycol=mydb["Menu"]
    query={
        "Food Name":fname[0],
        "email":restorLoginfo[0]["email"]
       }
    food=request.form["foodName"]
    prc=request.form["foodPrice"]

    f4 = request.files["File"]  
    f4.save(f4.filename)
    print("File : ",f4.filename)
    extension="."+f4.filename.split(".")[1]
    restimg4=restorLoginfo[0]["Restaurant"]+str(randint(0,99))+food+extension
    os.rename(f4.filename,restimg4)

    status=request.form["status"]

    newVals={"$set":{"Food Name":food,
        "Food Price":prc,
        "File":restimg4,
        "Food Status":status
        }}
    
    mycol=mydb["Menu"]
    mycol.update_one(query, newVals)
    os.remove(fname[1])
    os.chdir(pat)
    return redirect("/Restaurant/main")

@app.route("/update/<op>", methods=["GET","POST"])
def upRestorant(op):
    if op=="Restaurant":
        if request.method=="GET":
            return render_template("restoUpdate.html",restovals=restorLoginfo[0],email=restorLoginfo[0]["email"])
        else:
            os.chdir(pat+"\static")
            os.remove(restorLoginfo[0]["ImageFile"])
            restName=request.form['restName']
            email=request.form['email']
            contact=request.form['contact']

            f = request.files['pic']  
            f.save(f.filename)
            print("File : ",f.filename)
            extension="."+f.filename.split(".")[1]
            restimg=restName+str(randint(00, 99))+extension
            
            os.rename(f.filename,restimg)

            os.chdir(pat)

            state=request.form['state']
            dist=request.form['dist']
            tal=request.form['loc']
            area=request.form['area']
            pin=request.form['pin']

            data={
                "Restaurant":restName,
                "email":email,
                "contact":contact,
                "ImageFile":restimg,
                "area":area,
                "Talluk":tal,
                "dist":dist,
                "state":state,
                "pin":pin}

            
            query={
                "email":restorLoginfo[0]["email"]
            }
            q2={"Restaurant mail":restorLoginfo[0]["email"]}
            newq={"$set":data}
            newq2={"$set":{
                    "Restaurant":restName,
                    "email":email,
                    "Restorant talluk":tal
                }
            }
            n3={
                "$set":{  
                "Restaurant":restName,
                "Restaurant mail":email,
                }
            }
            mycol=mydb["Menu"]
            mycol.update_many(query,newq2)

            mycol2=mydb["Restaurants"]
            mycol2.update_one(query,newq)

            mycol3=mydb["Orders"]
            mycol3.update_many(q2,n3)

            restorLoginfo.clear()
            restorLoginfo.append(data)
            return redirect("/Restaurant/main")
    else:
        if request.method=="GET":
            return render_template("userUpdate.html",res=userloginfo[0])
        else:
            name=request.form['username']
            email=request.form['email']
            contact=request.form['contact']

            state=request.form['state']
            dist=request.form['dist']
            tal=request.form['loc']
            area=request.form['area']
            pin=request.form['pin']

            data={"$set":
            {
                "Name":name,
                "email":email,
                "contact":contact,
                "area":area,
                "Talluk":tal,
                "dist":dist,
                "state":state,
                "pin":pin
                }
                }
            q={
                "email":userloginfo[0]["email"]
            }
            
            q2={
                "Customer mail":userloginfo[0]["email"]
            }
            data2={"$set":{
                "Customer mail":email
            }}

            mycol=mydb["Users"]
            mycol.update_one(q,data)

            mycol2=mydb["Orders"]
            mycol.update_one(q2,data2)

            userloginfo.append()
            userloginfo.append(data["$set"])
            return redirect("/User/main")


N = 15
@app.route("/order/<email>/<food>")
def insertOrders(email,food):
    restaurant_details.clear()
    mycol=mydb["Menu"]
    query={
        "Food Name":food,
        "email":email
    }
    for i in mycol.find(query):
        restaurant_details.append(i)
    
    
    mycol=mydb["Restaurants"]
    query={"email":email}
    for i in mycol.find(query):
        restaurant_details.append(i)
    
    restaurant_details.append(str(randint(00000000 , 99999999)))
    print(restaurant_details)
    print()
    print(userloginfo)

    x = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    d=x.strftime("%I")+":"+x.strftime("%M")+":"+x.strftime("%S")+" "+x.strftime("%p")
    return render_template("Order.html",usr=userloginfo[0],rest=restaurant_details,d=d)

@app.route("/confirm/order",methods=["POST"])
def insertORD():
    x = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

    d=str(x.strftime("%c"))[0:10]+", "+x.strftime("%I")+":"+x.strftime("%M")+":"+x.strftime("%S")+" "+x.strftime("%p")
    q=int(request.form["quantity"])
    delevery_address=request.form["DelAdd"]
    p=str(int(restaurant_details[0]['Food Price'].split("/")[0])*q)+"/-Rs"

    data={
        "Order id":restaurant_details[2],
        "File":restaurant_details[0]['File'],
        "Food name":restaurant_details[0]['Food Name'],
        "Quantity":q,
        "Total Price":p,
        "Order date-Time":d,
        "Customer mail":userloginfo[0]["email"],
        "Restaurant":restaurant_details[1]['Restaurant'],
        "Restaurant mail":restaurant_details[1]['email'],
        "Delevery Address":delevery_address,
        "Order status":"Ordered"
    }
    msg = Message('New Order', sender='foodyLover083@gmail.com',recipients=[userloginfo[0]["email"]])
    MsgString="Your order with id "+ str(data["Order id"])+" for "+data["Food name"]+" quantity of "+str(q) + " at "+data["Restaurant"]+" has been placed, And will be delivered with in 30 mins.\nThank you for ordering."
    msg.body =MsgString
    mail.send(msg)

    message2="New order arrived \n Order id : "+str(data["Order id"])+" for " + data["Food name"]+"  quantity of "+str(q)
    msg = Message('New Order', sender='foodyLover083@gmail.com',recipients=[data["Restaurant mail"]])
    msg.body =message2
    mail.send(msg)

    mycol=mydb["Orders"]
    mycol.insert_one(data)
    return redirect("/user/all/orders")

@app.route("/restaurant/<status>")
def showRestoOrders(status):
    q={
        "Order status":status
    }
    mycol=mydb["Orders"]
    res=[]
    for i in mycol.find(q):
        res.append(i)
    if status=="Ordered":
        return render_template("restOrders.html",res=res,email=restorLoginfo[0]["email"],todo1="disabled")
    elif status=="Recieved" :
        return render_template("restOrders.html",res=res,email=restorLoginfo[0]["email"],todo="disabled")
    else :
        
        return render_template("restOrders.html",res=res,email=restorLoginfo[0]["email"],todo="disabled",todo1="disabled")


@app.route("/user/all/orders")
def showOrders():
    mycol=mydb["Orders"]
    query={
        "Customer mail":userloginfo[0]["email"],
    }
    res=[]
    for x in mycol.find(query):
        res.append(x)
    return render_template("custOrders.html",res=res)

@app.route("/<op>/deregister/<email>")
def deregister(op,email):
    query={ "email":email }
    if op=="Restaurant":
        mycol=mydb["Restaurants"]
        mycol.delete_one(query)

        mycol=mydb["Menu"]
        mycol.delete_many(query)
        return render_template("home.html",method="close()")
    else :
        mycol=mydb["Users"]
        mycol.delete_one(query)

        mycol=mydb["Orders"]
        mycol.delete_many(query)
        return render_template("home.html",method="close()")

@app.route("/update/order/<oid>/<sts>")
def UpdateOrder(oid,sts):
    mycol=mydb["Orders"]
    q={
       "Order id":oid
    }
    n={"$set":{
        "Order status":sts
    }}
    mycol.update_one(q,n)
    return redirect("/restaurant/"+sts)

if __name__ == "__main__":
    app.run(debug=True)
