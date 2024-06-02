from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file (optional)
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("CONNECTION_STRING")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Define a database model
# Base = declarative_base()

db = SQLAlchemy(app)

class Product(db.Model):
  __tablename__ = 'products'
  productid = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  description = Column(String, nullable=False)
  purchased_from = Column(String, nullable=False)
  cost = Column(String, nullable=False)
  imageurl = Column(String, nullable=True)

  def __repr__(self):
    return f'<Product {self.name}>'

# Create the database engine and sessionmaker
engine = create_engine(os.getenv("CONNECTION_STRING"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
  db = SessionLocal()
  yield db
  db.close()

# Log all requests
# @app.before_request
# def log_request_info():
#     app.logger.debug('Headers: %s', request.headers)
#     app.logger.debug('Body: %s', request.get_data())

# Health Check endpoint
@app.route("/health")
def health_check():
  """
  Performs a basic health check on the service.
  """
  return jsonify({"status": "healthy"}), 200

# GET endpoint
@app.route("/data", methods=["GET"])
def get_data():
  """
  Returns some sample data.
  """
  # You can access environment variables using os.getenv('VARIABLE_NAME')
  sample_message = os.getenv('APP_NAME', "Unknown App")
  data = {"message": sample_message}
  return jsonify(data), 200

# GET endpoint
@app.route("/products", methods=["GET"])
def get_products():
  """
  Fetches data from a PostgreSQL table using SQLAlchemy.
  """
  try:    
    dbsession = get_db()
    data = dbsession.query(Product).all()
    # data = Product.query.all()
    # Process and return data
    return jsonify({"data": [d.name for d in data]}), 200

  except Exception as e:
    return jsonify({"error": str(e)}), 500
  
# POST endpoint (similar changes)
# ...  
@app.route("/products", methods=["POST"])
def add_products():
  content = request.json
  print(content)
  new_product = Product(productid=content["productid"], name=content["name"], description=content["description"], cost=content["cost"], purchased_from=content["purchased_from"], imageurl=content["imageurl"])
  db = get_db()
  db.add(new_product)
  db.commit()

  message = "Successfully added " + content["name"]
  return jsonify({"message":message, "error":"nil"})



if __name__ == "__main__":
  app.run(debug=True)