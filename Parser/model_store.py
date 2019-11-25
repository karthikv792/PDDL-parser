import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
# import os
from parser_new import *
from writer_new import *
from constants import *
from json import dumps,loads

def add_model(cur,model):
    j = dumps(model)
    cur.execute("DROP TABLE modelFile")
    cur.execute("CREATE TABLE modelFile(model TEXT)")
    sql = "INSERT INTO modelFile(model) VALUES (%s)"
    cur.execute(sql, j)
    db.commit()

def retrieve_model(cur):
    cur.execute("SELECT * from modelFile")
    model = cur.fetchall()
    j = loads(model[0][0])
    return j

def parse_model1(domain,problem):
    model1 = parse_model(domain,problem)
    return model1

# db = MySQLdb.connect('localhost','root','yochan','radar')
# cur = db.cursor()
# model1 = retrieve_model(cur)
# print(model1)
# add_model(cur,j)
model1 = parse_model1('pr-domain.pddl','pr-problem.pddl')
model11 = ModelWriter(model1)
model11.write_files('write_domain1.pddl','write_problem1.pddl')






