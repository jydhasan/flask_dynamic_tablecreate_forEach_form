# app.py
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Replace with your database URI
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
db = SQLAlchemy(app)

class NewTableForm(FlaskForm):
    field1 = StringField('Field 1', validators=[DataRequired()])
    field2 = StringField('Field 2', validators=[DataRequired()])
    submit = SubmitField('Submit')

def create_dynamic_table(entry_id):
    class_name = f"NewTable_{entry_id}"
    table_name = f"new_table_{entry_id}"

    class DynamicTable(db.Model):
        __tablename__ = table_name
        id = db.Column(db.Integer, primary_key=True)
        field1 = db.Column(db.String(100), nullable=False)
        field2 = db.Column(db.String(100), nullable=False)
        # Add more fields as needed

    return class_name, DynamicTable

@app.route('/create_entry', methods=['GET', 'POST'])
def create_entry():
    form = NewTableForm()

    if form.validate_on_submit():
        field1_data = form.field1.data
        field2_data = form.field2.data

        entry_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        class_name, DynamicTable = create_dynamic_table(entry_id)

        # Create the table in the database
        DynamicTable.__table__.create(db.engine)

        # Insert the data into the dynamic table
        new_entry = DynamicTable(field1=field1_data, field2=field2_data)
        db.session.add(new_entry)
        db.session.commit()

        return "New entry added to the dynamic table."

    return render_template('create_entry.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
