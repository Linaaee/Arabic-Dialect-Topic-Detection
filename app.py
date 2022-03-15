from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from module import reponse
app=Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'

class text_form(FlaskForm):
    text=TextAreaField("Enter your text",validators=[DataRequired()])
    submit=SubmitField("Detect")

@app.route('/') 
def home():
	return render_template("index.html")

@app.route('/Try_it',methods=['GET','POST'])
def try_it():
    l=""
    text=""
    form=text_form()
    if form.validate_on_submit():
        text = form.text.data
        form.text.data = ''
        l=reponse(text)
    return render_template('base.html', form=form, answer=l)   
 
if __name__=="__main__":
	app.run(debug=True)  
   