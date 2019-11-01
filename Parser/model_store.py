import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import os
from model_parser import *
from model_writer import *
from constants import *
from tarski.syntax import VariableBinding, Variable
# db = MySQLdb.connect('localhost','root','yochan','radar')
# cur = db.cursor()
# cur.execute("CREATE TABLE modelFile(model VARCHAR(1000))")
model1 = parse_model('domain.pddl','problem.pddl')
# print(model1)
# sql = "INSERT INTO modelFile(model) VALUES (%s)"
# cur.execute(sql, model1)
# cur.commit()
model11 = ModelWriter(model1)
model11.write_files('write_domain1.pddl','write_problem1.pddl')
#
# from json import dumps, loads, JSONEncoder, JSONDecoder
# import pickle
# #Got this from stack overflow https://stackoverflow.com/questions/8230315/how-to-json-serialize-sets
# class PythonObjectEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
#             print("OBJECT..............................................",obj)
#             return JSONEncoder.default(self, obj)
#         if isinstance(obj, Variable):
#             print("OBJECT..............................................",obj,dir(obj))
#             return JSONEncoder.default(self, obj.sort.name)
#         return {'_python_object': pickle.dumps(obj)}
#
# def as_python_object(dct):
#     if '_python_object' in dct:
#         return pickle.loads(str(dct['_python_object']))
#     return dct
# j = dumps(model1, cls=PythonObjectEncoder)
