from flask import Flask, render_template, request, redirect, url_for,jsonify
import psycopg2
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URL']='postgresql://postgres:root@localhost:5432/Telecom_database'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/Telecom_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db=SQLAlchemy(app)

#Define model

class Customers(db.Model):
  __tablename__='customers'
  customer_id=db.Column(db.Integer,primary_key=True)
  is_new_customer=db.Column(db.Boolean,nullable=False)

class Technology(db.Model):
  __tablename__ = 'technology'
  technology_id = db.Column(db.Integer, primary_key=True)
  technology_type = db.Column(db.String(50), nullable=False)


class Service(db.Model):
  __tablename__ = 'services'
  service_id = db.Column(db.Integer, primary_key=True)
  service_type = db.Column(db.String(50), nullable=False)


class Order(db.Model):
  __tablename__ = 'orders'
  order_id = db.Column(db.Integer, primary_key=True)
  customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
  service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)
  technology_id = db.Column(db.Integer, db.ForeignKey('technology.technology_id'), nullable=False)
  order_date = db.Column(db.Date, nullable=False)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date)
  order_status = db.Column(db.String(50), nullable=False)
  contract_type = db.Column(db.String(50), nullable=False)
  price_per_month = db.Column(db.Numeric(10, 2), nullable=False)
  installation_fee = db.Column(db.Numeric(10, 2), nullable=False)

    # Relationships
  customer = db.relationship('Customers', backref='orders')
  service = db.relationship('Service', backref='orders')
  technology = db.relationship('Technology', backref='orders')


class Contract(db.Model):
  __tablename__ = 'contracts'
  contract_id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
  contract_type = db.Column(db.String(50), nullable=False)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date)

@app.route('/api/orders/details',methods=['GET'])
def get_orders_details():
  try:
    is_new_customer=request.args.get('is_new_customer')

    query=db.session.query(
            Customers.is_new_customer,
            Technology.technology_type,
            Service.service_type,
            Order.order_date,
            Order.start_date,
            Order.end_date,
            Order.order_status,
            Order.contract_type,
            Order.price_per_month,
            Order.installation_fee
        ).join(Customers, Order.customer_id == Customers.customer_id) \
         .join(Service, Order.service_id == Service.service_id) \
         .join(Technology, Order.technology_id == Technology.technology_id)

    if is_new_customer is not None:
      is_new_customer=is_new_customer.lower()=='true'
      query=query.filter(Customers.is_new_customer==is_new_customer)
      print(f"Query parameter 'is_new_customer': {is_new_customer}")


    result=query.all()

    response=[]
    for row in result:
      response.append({
                  "is_new_customer": row.is_new_customer,
                  "technology_type": row.technology_type,
                  "service_type": row.service_type,
                  "order_date": row.order_date.isoformat(),
                  "start_date": row.start_date.isoformat(),
                  "end_date": row.end_date.isoformat() if row.end_date else None,
                  "order_status": row.order_status,
                  "contract_type": row.contract_type,
                  "price_per_month": str(row.price_per_month),
                  "installation_fee": str(row.installation_fee),
              })


    return jsonify(response),200

  except Exception as e:
    return jsonify({'error':str(e)}),500


@app.route('/api/orders/simple-filters/', methods=['GET'])
def get_orders():
    try:
        is_new_customer = request.args.get('is_new_customer')  # Corrected typo
        order_status = request.args.get('order_status')
        contract_type = request.args.get('contract_type')

        # Start building the query
        query = db.session.query(Order)

        # Apply filters conditionally
        if is_new_customer:
            is_new_customer = is_new_customer.lower() == 'true'  # Convert string to boolean
            query = query.join(Customers).filter(Customers.is_new_customer == is_new_customer)

        if order_status:
            query = query.filter(Order.order_status == order_status)

        if contract_type:
            query = query.filter(Order.contract_type == contract_type)

        # Fetch and process results
        result = query.all()
        return jsonify([{
            'order_id': order.order_id,
            "order_status": order.order_status,
            "contract_type": order.contract_type
        } for order in result]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)