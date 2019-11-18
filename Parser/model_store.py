import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import os
from parser_new import *
from writer_new import *
from constants import *
from tarski.syntax import VariableBinding, Variable
# db = MySQLdb.connect('localhost','root','yochan','radar')
# cur = db.cursor()
# cur.execute("CREATE TABLE modelFile(model VARCHAR(1000))")
model1 = parse_model('domain.pddl','problem.pddl')
from json import dumps,loads
j = dumps(model1)
model1=loads(j)
# print(model1.keys())
# sql = "INSERT INTO modelFile(model) VALUES (%s)"
# cur.execute(sql, model1)
# cur.commit()
model11 = ModelWriter(model1)
model11.write_files('write_domain1.pddl','write_problem1.pddl')
#

