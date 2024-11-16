from flask import Flask, render_template, request, redirect, url_for,session
from bson import ObjectId
from pymongo import MongoClient

cluster = MongoClient("mongodb://127.0.0.1:27017")
database = cluster['events']
uregister = database['uregister']
addevents = database['addevents']
bookings = database['bookings']

api = Flask(__name__)
api.secret_key='1234567890'

@api.route('/')
def home():
    return render_template("index.html")

@api.route("/adminpage")
def admin():
    return render_template("admin.html")

@api.route("/events")
def events():
    return render_template("events.html")

@api.route("/eventinfo")
def eventinfo():
    return render_template("events_info.html")

@api.route("/loginfail")
def loginf():
    return render_template("loginfail.html")

@api.route("/participants")
def participants():
    return render_template("participants.html")

@api.route("/userlogin")
def ulogin():
    return render_template("userlogin.html")

@api.route("/userregister")
def uregister1():
    return render_template("userregister.html")

@api.route("/eventsss")
def eve():
    return render_template("events1.html")

@api.route("/adevents")
def adeve():
    return render_template("adminevents.html")

@api.route("/hello")
def viewd():
    return render_template("viewdetails.html")

@api.route("/indx")
def indxx():
    return render_template("index1.html")

@api.route("/details")
def detail():
    return render_template("viewdetails.html")

@api.route("/conform")
def conformation():
    return render_template("booking_confirmation.html")

@api.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@api.route("/events11")
def events11():
    return render_template("addevents1.html")


@api.route("/userregistration", methods=['POST'])
def register():
    uname = request.form.get("username")
    uemail = request.form.get("email")
    uphone = request.form.get("phone")
    upassword = request.form.get("password")
    print(uname, uemail, uphone, upassword)
    user = uregister.find_one({"username": uname})
    if user:
        return render_template("userregister.html", status="Username already exists")
    uregister.insert_one({"username": uname, "email": uemail, "phone": uphone, "password": upassword})
    return render_template("userregister.html", status="Registration Successful")

@api.route("/login", methods=['POST'])
def userlog():
    uname = request.form.get("username")
    upass = request.form.get("password")
    print(uname, upass)
    user = uregister.find_one({"username": uname})
    if user:
        if user["password"] == upass:
            session['username']=uname
            events_d=addevents.find()
            return render_template("events1.html",events=list(events_d),username=session['username'])
    return render_template("userlogin.html", status="Invalid Credentials")

@api.route("/adminlogin", methods=['POST'])
def adminlog():
    admin_username = "admin"
    admin_password = "password1234"
    uname = request.form.get("username")
    upass = request.form.get("password")
    print(uname, upass)
    if uname == admin_username and upass == admin_password:
        return render_template("index1.html", status="Login Successfully")
    return render_template("admin.html", status="Invalid Credentials")

@api.route("/eventdetails", methods=['POST'])
def addevent():
    name = request.form.get("EventName")
    type = request.form.get("EventType")
    date = request.form.get("EventDate")
    stime = request.form.get("StartTime")
    etime = request.form.get("EndTime")
    duration = request.form.get("Duration")
    event_image = request.form.get("EventImage")
    print(name, type, date, stime, etime, duration)
    addevents.insert_one({"EventName": name, "EventType": type, "EventDate": date, "StartTime": stime, "EndTime": etime, "Duration": duration, "EventImage": event_image})
    return render_template("index1.html", status="Event Added Successfully")

@api.route("/hii", methods=['GET'])
def index():
    events_data = list(addevents.find())    
    return render_template("events1.html", events=events_data)

@api.route("/admin/events")
def admin_events():
    events = addevents.find()
    events_list = []
    for event in events:
        event_data = {
            "_id": str(event["_id"]),
            "EventName": event["EventName"],
            "EventType": event["EventType"],
            "EventDate": event["EventDate"],
            "StartTime": event["StartTime"],
            "EndTime": event["EndTime"],
            "Duration": event["Duration"],
            "EventImage": event["EventImage"]
        }
        events_list.append(event_data)
    return render_template("adminevents.html", events=events_list)

@api.route("/deleteevent/<event_id>", methods=["POST"])
def delete_event(event_id):
    addevents.delete_one({"_id": ObjectId(event_id)})
    return redirect(url_for("admin_events"))

@api.route("/updateevent/<event_id>", methods=["GET", "POST"])
def update_event(event_id):
    if request.method == "GET":

        event = addevents.find_one({"_id": ObjectId(event_id)})
        print(event)
        return render_template("addevents1.html", event=event)
    
    if request.method == "POST":
        # Logic for updating the event details
        name = request.form.get("EventName")
        type = request.form.get("EventType")
        date = request.form.get("EventDate")
        stime = request.form.get("StartTime")
        etime = request.form.get("EndTime")
        duration = request.form.get("Duration")

        addevents.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": {
                "EventName": name,
                "EventType": type,
                "EventDate": date,
                "StartTime": stime,
                "EndTime": etime,
                "Duration": duration
            }}
        )
        return redirect(url_for("admin_events"))  # Redirect to the admin page or another relevant page

@api.route("/eventdetails/<event_id>", methods=['GET'])
def event_details(event_id):
    # Fetch the event details from the database using the provided event ID
    event = addevents.find_one({"_id": ObjectId(event_id)})
    print(event)
    if not event:
        return "Event not found", 404
    return render_template("viewdetails.html", eventdetail=event)

@api.route("/eventdetailss/<event_id>", methods=['GET', 'POST'])
def event_details1(event_id):
    # Fetch the event details from the database using the provided event ID
    event = addevents.find_one({"_id": ObjectId(event_id)})
    user= uregister.find_one({'username':session['username']})
    eventname=event['EventName']
    if request.method == 'POST':
        # Extract the booking form data
        
        # Store booking in the database (you can adjust this as needed)
        booking = {
            'event_id': ObjectId(event_id),
            'eventname':eventname,
            'name': user['username'],
            'phone': user['phone'],
            'email': user['email']
        }
        bookings.insert_one(booking)
        return render_template('viewdetails.html',status="Event booking Successful",eventdetail=event)


@api.route("/booking_history",methods=['GET'])
def booking_history():
    # Fetch all bookings from the database
    all_bookings = bookings.find()

    # Render the booking history page with the fetched data
    return render_template("booking_history.html", bookings=all_bookings)










if __name__ == "__main__":
    api.run(port=5000, debug=True)
