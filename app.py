from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/family_inventory'
app.config['SECRET_KEY'] = '220523'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        unit = request.form['unit']  
        description = request.form.get('description')
        try:
            quantity = int(quantity)
            if quantity < 1:
                flash('数量必须大于等于1 Quantity must be greater than or equal to 1', 'error')
                return redirect(url_for('add_item'))
        except ValueError:
            flash('Quantity must be a number', 'error')
            return redirect(url_for('add_item'))

        new_item = Item(name=name, quantity=quantity, unit=unit, description=description) 
        db.session.add(new_item)
        db.session.commit()
        flash('Item Added Successfully')
        return redirect(url_for('index'))
    return render_template('add_item.html')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash('Item Deleted Successfully')
        return redirect(url_for('index'))
    return render_template('delete_item.html', item=item)

@app.route('/confirm_delete/<int:id>', methods=['POST'])
def confirm_delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item Deleted Successfully')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        quantity = request.form['quantity']
        description = request.form.get('description')

        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity < 1:
                flash('数量必须大于等于1 Quantity must be greater than or equal to 1', 'error')
                return redirect(url_for('edit_item', id=id))
        except ValueError:
            flash('Quantity must be a number', 'error')
            return redirect(url_for('edit_item', id=id))

        item.quantity = quantity
        item.description = description
        db.session.commit()
        flash('Item quantity updated successfully')
        return redirect(url_for('index'))
    return render_template('edit_item.html', item=item)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)