from flask import  Flask,render_template,url_for,request
from Parser.parser_new import parse_model
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      domain = request.files['Domain_file']
      problem = request.files['Problem_file']
      domain.save('PDDLFiles/domain.pddl')
      problem.save('PDDLFiles/problem.pddl')
      model1 = parse_model('PDDLFiles/domain.pddl','PDDLFiles/problem.pddl')
      print(model1)
      return model1
if __name__ == "__main__":
    app.run(debug=True)