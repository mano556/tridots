from flask import Flask,render_template,url_for,request,redirect,flash
from flask_mysqldb import MySQL

#mysql connection
app=Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="Gyrados@123"
app.config["MYSQL_DB"]="Tridots"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM Product"
    con.execute(sql)
    res=con.fetchall()
    return render_template('product.html',datas=res)
@app.route("/addProducts",methods=['POST','GET'])
def addProducts():
    if request.method=='POST':
        products_name=request.form['products name']
        Description=request.form['Description']
        price=request.form['price']
        con=mysql.connection.cursor()
        sql="insert into Product(product_name,product_description,product_price) values(%s,%s,%s)"
        con.execute(sql,[products_name,Description,price])
        mysql.connection.commit()
        con.close()
        flash("Product added successfully!!!...")
        return redirect(url_for('home'))
    return render_template('Addproduct.html')

@app.route("/editproduct/<string:id>",methods=['POST','GET'])
def editproducts(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        products_name=request.form['products name']
        Description=request.form['Description']
        price=request.form['price']
        sql="update Product set product_name=%s,product_description=%s,product_price=%s where product_id=%s"
        con.execute(sql,[products_name,Description,price,id])
        mysql.connection.commit()
        con.close()
        flash("Product Updated successfully!!!...")
        return redirect(url_for('home'))

        
    sql= "select * from Product where product_id=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("EditProduct.html",datas=res)

@app.route("/deleteproduct/<string:id>",methods=['POST','GET'])
def deleteproduct(id):
     con=mysql.connection.cursor()
     sql="delete from Product where product_id=%s "
     con.execute(sql,[id])
     mysql.connection.commit()
     con.close()
     flash("Product Deleted successfully!!!...")
     return redirect(url_for('home'))

# Product Movement functions

@app.route("/MovementView")
def MovementView():
        con=mysql.connection.cursor()
        sql="SELECT * FROM ProductMovement"
        con.execute(sql)
        res=con.fetchall()
        return render_template('movement/MovementView.html',datas=res)
@app.route("/AddMovement",methods=['POST','GET'])
def AddMovement():
    if request.method=='POST':
        PRODUCT_ID=request.form['PRODUCT_ID']
        FROM_LOCATION=request.form['FROM_LOCATION']
        TO_LOCATION=request.form['TO_LOCATION']
        QUANTITY=request.form['QUANTITY']
        TIMESTAMP=request.form['TIMESTAMP']
        con=mysql.connection.cursor()
        sql="insert into ProductMovement(product_id,from_location,to_location,quantity,timestamp) values(%s,%s,%s,%s,%s)"
        con.execute(sql,[PRODUCT_ID,FROM_LOCATION,TO_LOCATION,QUANTITY,TIMESTAMP])
        mysql.connection.commit()
        con.close()
        flash("MOVEMENT added successfully!!!...")
        return redirect(url_for('MovementView'))
    return render_template("movement/AddMovement.html")
    

@app.route("/EditMovement/<string:id>",methods=['POST','GET'])
def EditMovement(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        PRODUCT_ID=request.form['PRODUCT_ID']
        FROM_LOCATION=request.form['FROM_LOCATION']
        TO_LOCATION=request.form['TO_LOCATION']
        QUANTITY=request.form['QUANTITY']
        TIMESTAMP=request.form['TIMESTAMP']
        sql="update  ProductMovement set product_id=%s,from_location=%s,to_location=%s,quantity=%s,timestamp=%s  where Movement_id=%s"
        con.execute(sql,[PRODUCT_ID,FROM_LOCATION,TO_LOCATION,QUANTITY,TIMESTAMP,id])   #add id to this list
        mysql.connection.commit()
        con.close()
        flash("MOVEMENT updated successfully!!!...")
        return redirect(url_for('MovementView'))
    sql= "select * from ProductMovement where Movement_id=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("movement/EditMovement.html",datas=res)


    
    
@app.route("/DeleteMovement/<string:id>",methods=['POST','GET'])
def DeleteMovement(id):
     con=mysql.connection.cursor()
     sql="delete from ProductMovement where Movement_id=%s "
     con.execute(sql,[id])
     mysql.connection.commit()
     con.close()
     flash("Product Deleted successfully!!!...")
     return redirect(url_for('MovementView'))





if __name__=="__main__":
    app.run(debug=True)