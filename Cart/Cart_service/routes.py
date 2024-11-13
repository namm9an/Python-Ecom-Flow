from Cart_service import app,ma,db
from Cart_service.models import Cart
from flask import request,jsonify
class CartSchema(ma.Schema):
    class Meta:
        fields = ("id","user_id","p_id","qty","price")
cart_schema = CartSchema()
carts_schema = CartSchema(many=True)

@app.route('/',methods=['GET','POST','PUT','DELETE'])
def ref():
    if request.method == "GET":
        _id = request.args.get('user_id')
        cart_items = Cart.query.filter_by(user_id=_id).all()
        _ = carts_schema.dump(cart_items)
        total = sum(item.price * item.qty for item in cart_items)
        return jsonify({"cart_data":_,"total": total})
    if request.method == "POST":
        user_id = request.json['user_id']
        p_id = request.json['p_id']
        qty = request.json['qty']
        price = request.json['price']
        new_Cart = Cart(user_id,p_id,qty,price)
        db.session.add(new_Cart)
        db.session.commit()

        cart = cart_schema.dump(new_Cart)
        return jsonify({"success":True,"cart":cart})
    
    
@app.route('/cart',methods=['GET','PUT','DELETE'])
def cart_ref():
    if request.method=='GET':
        _id = request.args.get('id')
        cart_data = cart_schema.dump(Cart.query.get(_id).first())
        return jsonify({"success":True,"cart_data":cart_data})

    if request.method == "PUT":
        _id = request.args.get('id')
        _cart = Cart.query.get(_id)
        _cart.user_id = request.json['user_id']
        _cart.p_id = request.json['p_id']
        _cart.qty = request.json['qty']
        _cart.price = request.json['price']
        db.session.commit()
        return jsonify({"success":True})
    if request.method == "DELETE":
        _id = request.args.get('id')
        _temp = Cart.query.get(_id)
        db.session.delete(_temp)
        db.session.commit()
        return jsonify({"success":True})
    