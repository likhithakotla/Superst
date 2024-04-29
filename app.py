from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import json

app = Flask(__name__)
customer_query = "SELECT CustomerID, CustomerName FROM Customers WHERE CustomerID = %s;"
order_query = "select o.orderid, c.customername from customers c inner join orders o on c.customerid=o.customerid Where c.customerid= %s;"
details_query = "select p.productname, d.quantity, d.sales, d.discount, d.shippingcost, d.shipmode from orders o inner join orderdetails d on d.orderid=o.orderid inner join products p on p.productid=d.productid where o.orderid=%s;"


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5434",
        database="SuperStore",
        user="postgres",
        password="Mohan$2001",
    )
    return conn


def convert_to_json(orders, main, columns):
    result = {}
    result[main] = []
    for order in orders:
        details = {}
        for i in range(len(order)):
            details[columns[i]] = order[i]
        print(details)
        result[main].append(details)
    return json.dumps(result)


@app.route("/")
def index():
    # The root URL will render index.html.
    return render_template("./index.html")


@app.route("/fetch-orders", methods=["GET", "POST"])
def fetch_orders():
    customer_details = None
    if request.method == "POST":
        customer_id = request.form["customerID"]
        conn = get_db_connection()
        cur = conn.cursor()  # Change to regular cursor since you're printing as a list
        query = customer_query
        cur.execute(query, (customer_id,))
        customer_details = cur.fetchone()  # Assuming one row per customer_id
        cur.close()
        conn.close()
        print(customer_details)  # For debugging
        return render_template("query.html", customer_details=customer_details)
    elif request.method == "GET":
        cust_id = request.args.get("custid")
        conn = get_db_connection()
        cur = conn.cursor()  # Change to regular cursor since you're printing as a list
        query = order_query
        print("Fetching customer detials for customer ID: " + cust_id + " ...")
        cur.execute(query, (cust_id,))
        order_details = cur.fetchall()  # Assuming one row per customer_id
        cur.close()
        conn.close()
        print(order_details)
        return convert_to_json(order_details, "orders", ["orderid", "custname"])


@app.route("/fetch-details", methods=["GET"])
def fetch_details():
    orderid = request.args.get("orderid")
    conn = get_db_connection()
    cur = conn.cursor()  # Change to regular cursor since you're printing as a list
    query = details_query
    print("Fetching detials for order ID: " + orderid + " ...")
    cur.execute(query, (orderid,))
    order_details = cur.fetchall()  # Assuming one row per customer_id
    cur.close()
    conn.close()
    print(order_details)
    return convert_to_json(
        order_details,
        "details",
        ["prodname", "quantity", "sale", "discount", "shippingcost", "shipmode"],
    )


if __name__ == "__main__":
    app.run(debug=True)
