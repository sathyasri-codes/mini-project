from flask import Flask, render_template, request

app = Flask(__name__)
test_users = {
    "student@gmail.com": {
        "password": "Test12345",
        "role": "student"
    },
    "owner@gmail.com": {
        "password": "Owner12345",
        "role": "owner"
    }
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")

        if password != confirm_password:
            return "Passwords do not match!"

        if role not in ["student", "owner"]:
            return "Invalid role!"

        if not all([name, email, password]):
            return "Please fill all fields!"

        return "Registration details received! Database integration is pending."

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Please fill all fields!"

        if email not in test_users:
            return "User not found!"

        if test_users[email]["password"] != password:
            return "Incorrect password!"

        role = test_users[email]["role"]

        if role == "student":
           return "Login successful! Welcome Student."

        elif role == "owner":
            return "Login successful! Welcome Owner."

        else:
           return "Invalid role!"
    return render_template("login.html")
resources = []
print("Resource list:",resources)
@app.route("/resources")
def show_resources():
    return render_template("resources.html")


@app.route("/add_resource", methods=["POST"])
def add_resource():
    resource_name = request.form.get("resource_name")
    resource_type = request.form.get("resource_type")
    description = request.form.get("description")

    if not all([resource_name, resource_type, description]):
        return "Please fill all fields!"

    resource = {
        "name": resource_name,
        "type": resource_type,
        "description": description
    }

    resources.append(resource)

    return "Resource added successfully!"


@app.route("/explore")
def explore():
    return render_template(
        "explore.html",
        resources=resources
    )
@app.route("/resource_details/<int:index>")
def resource_details(index):

    if 0 <= index < len(resources):
        return render_template(
            "resource_details.html",
            resource=resources[index]
        )

    return "Resource not found!"
@app.route("/delete_resource/<int:index>", methods=["POST"])
def delete_resource(index):

    if 0 <= index < len(resources):
        resources.pop(index)
        return "Resource deleted successfully!"

    return "Resource not found!"
@app.route("/update_resource/<int:index>", methods=["GET", "POST"])
def update_resource(index):

    if index < 0 or index >= len(resources):
        return "Resource not found!"

    if request.method == "POST":

        resources[index]["name"] = request.form.get("resource_name")
        resources[index]["type"] = request.form.get("resource_type")
        resources[index]["description"] = request.form.get("description")

        return "Resource updated successfully!"

    return render_template(
        "update_resource.html",
        resource=resources[index],
        index=index
    )
bookings = []

@app.route("/booking")
def booking():
    resource = request.args.get("resource", "")
    return render_template("booking.html", resource=resource)

@app.route("/book_resource", methods=["POST"])
def book_resource():

    student_name = request.form.get("student_name")
    resource_name = request.form.get("resource_name")
    booking_date = request.form.get("booking_date")
    purpose = request.form.get("purpose")

    if not all([student_name, resource_name, booking_date, purpose]):
        return "Please fill all fields!"

    booking_details = {
        "student_name": student_name,
        "resource_name": resource_name,
        "booking_date": booking_date,
        "purpose": purpose,
        "status": "Pending"
    }

    bookings.append(booking_details)

    return render_template(
    "booking_success.html",
    name=student_name,
    resource=resource_name
)
@app.route("/booking_requests")
def booking_requests():
    return render_template(
        "booking_requests.html",
        bookings=bookings
    )
@app.route("/owner_dashboard")
def owner_dashboard():
    return render_template("owner_dashboard.html")
@app.route("/update_booking_status/<int:index>/<status>", methods=["POST"])
def update_booking_status(index, status):

    if 0 <= index < len(bookings):

        if status not in ["Approved", "Rejected"]:
            return "Invalid status!"

        bookings[index]["status"] = status

        return "Booking " + status + " successfully!"

    return "Booking not found!"
@app.route("/booking_status")
def booking_status():
    return render_template(
        "booking_status.html",
        bookings=bookings
    )
if __name__ == "__main__":
    app.run(debug=True)