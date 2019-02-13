from flask import Flask, render_template, request
from mysqlconnection import connectToMySQL
import json

app = Flask('__name__')

@app.route("/")
def index():
    mysql = connectToMySQL('lead_gen_business')
    query = """SELECT a.client_id, CONCAT(a.first_name, ' ', a.last_name) full_name, count(c.leads_id) total_number
                FROM clients a join sites b ON a.client_id = b.client_id join leads c ON b.site_id = c.site_id
                group by client_id;"""
    customerList = mysql.query_db(query)

    # data prepared for the graph preparation
    data = []
    for customer in customerList:
        data.append({ customer['total_number'], str(customer['full_name'])})
    print(data)

    return render_template("index.html", customerList=customerList, data=data)

@app.route("/filter_result_by_date", methods=['POST'])
def filter_result_by_date():
    mysql = connectToMySQL('lead_gen_business')
    query = """SELECT a.client_id, CONCAT(a.first_name, ' ', a.last_name) full_name, count(c.leads_id) total_number 
    FROM clients a join sites b ON a.client_id = b.client_id join leads c ON b.site_id = c.site_id 
    WHERE c.registered_datetime between %(dateFrom)s and %(dateTo)s 
    GROUP BY client_id;"""
    data = {
        'dateFrom': request.form['date_from'],
        'dateTo': request.form['date_to']
    }
    customerList = mysql.query_db(query, data)
    
    return render_template("index.html", customerList=customerList)

if __name__ == '__main__':
    app.run(debug=True)
