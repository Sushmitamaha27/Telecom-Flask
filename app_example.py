from flask import Flask, render_template, request, redirect, url_for,jsonify
import psycopg2

app=Flask(__name__)

conn=psycopg2.connect(database="Telecom_database",user="postgres",
                          password="root",
                          host="localhost", port="5432")

@app.route('/')
def index():

  cur = conn.cursor()

  # Fetch data from all tables
  cur.execute('SELECT * FROM Customers')
  customers_data = cur.fetchall()

  cur.execute('SELECT * FROM Technology')
  technology_data = cur.fetchall()

  cur.execute('SELECT * FROM Services')
  services_data = cur.fetchall()

  cur.execute('SELECT * FROM Orders')
  orders_data = cur.fetchall()

  cur.execute('SELECT * FROM Contracts')
  contracts_data = cur.fetchall()

  # Close cursor and connection
  cur.close()
  conn.close()

  # Pass the data to the template
  return render_template(
      'index.html',
      customers=customers_data,
      technology=technology_data,
      services=services_data,
      orders=orders_data,
      contracts=contracts_data
  )