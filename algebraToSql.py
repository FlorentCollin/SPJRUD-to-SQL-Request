import copy
from types import *

class DBSchema(object):
    """docstring for DBSchema."""
    def __init__(self, name, colsName, colsType):
        if not isinstance(name, str):
            raise ValueError(errorMessage(name, "name", "String"))
        if not isinstance(colsName, list) and not all(isinstance(item, str) for item in colsName):
            raise ValueError(errorMessage(colsName, "colsName", "list of String"))
        if not all(isinstance(item, str) for item in colsType):
            raise ValueError(errorMessage(colsType, "colsType", "list of String"))
        self.name = name
        self.colsName = colsName
        self.colsType = colsType

    def add(self, colName, colType):
        self.colsName.append(colName)
        self.colsType.append(colType)

    def copy(self):
        return DBSchema(self.name, self.colsName, self.colsType)
		
    def __str__(self):
        return str(self.name)+" "+str(self.colsName)+" "+str(self.colsType)
		
    def __repr__(self):
        return __str__

    def getColType(self, col):
        for i in range(len(self.colsName)):
            if self.colsName[i] == col:
                return self.colsType[i]

class Request:
    def __init__(self, table):
        if not isinstance(table, DBSchema) and not isinstance(table, Request):
            raise ValueError(errorMessage(table, "table", "DBSchema or Request"))
        self.table = table
		
    def getTable(self):
        if isinstance(self.table, Operation):
            return self.table.getTable()
        return self.table

class Select(Request):
    """docstring for Select."""
    def __init__(self, table, column, value):
        super().__init__(table)
        if not isinstance(column, str):
            raise ValueError(errorMessage(column, "column", "String"))
        if not colIsInTable(column, table):
            raise columnError(errorColumnMessage(column, table))
        if not checkType(value, column, table):
            raise columnError("The type of "+str(value)+" is not equal to the type of '"+str(col)+"' ("+table.getColType(col)+")")

class Proj(Request):
    def __init__(self, table, column):
        if not colIsInTable(col, table):
            raise columnError(errorColumnMessage(col, table))
        super().__init__(table)
        self.column = column

class Join(Request):
    def __init__(self, table1, table2):
        if not isinstance(table1, DBSchema):
            raise ValueError(errorMessage(table1, "table1", "DBSchema"))
        if not isinstance(table2, DBSchema):
            raise ValueError(errorMessage(table2, "table2", "DBSchema"))
        self.table1 = table1
        self.table2 = table2

class Rename(Request):
    def __init__(self, table, column, newName):
        super().__init__(table)
        if not isinstance(column, str):
            raise ValueError(errorMessage(column, "column", "String"))
        if not colIsInTable(column, table):
            raise columnError(errorColumnMessage(column, table))
        if not isinstance(newName, str):
            raise ValueError(errorMessage(newName, "newName", "String"))
        self.column = column
        self.newName = newName

class Union(Request):
    def __init__(self, table1, table2):
        if not isinstance(table1, DBSchema):
            raise ValueError(errorMessage(table1, "table1", "DBSchema"))
        if not isinstance(table2, DBSchema):
            raise ValueError(errorMessage(table2, "table2", "DBSchema"))
        if not checkSort(table1, table2):
            raise columnError(errorSort(table1, table2))
        self.table1 = table1
        self.table2 = table2

class Difference(Request):
    def __intit__(self, table1, table2):
        print()


class columnError(Exception):
    def __init__(self, message):
        self.message = message

class Operation:
    def __init__(self, symbol):
        self.symbol = symbol

class Eq:
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2



def checkSort(table1, table2):
    for i in range(len(table1.colsName)):
        if table1.colsName[i] != table2.colsName[i]:
            return False
    return True
    

def colIsInTable(col, table):
    for column in table.colsName:
        if col == column:
            return True
    return False

def checkType(value, column, table):
    for i in range(len(table.colsName)):
        if table.colsName[i] == column and table.colsType[i] == getType(value):
            return True
    return False

"""
Input : value, the value to test
Output : the type of the value for SPJRUD
Effect : NONE
Qu'en penses-tu si on fait ça ?
"""
def getType(value):
    if isinstance(value, int):
        return "int"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, float):
        return "float"
    else:
        return "boolean"

def errorSort(table1, table2):
    return "There any columns not compatible between "+str(table1)+" "+str(table2)

def errorColumnMessage(column, table):
    return "The column "+str(column)+" is not in the table "+str(table)

def errorMessage(arg, argName, correctType):
    return "Argument " + str(argName) + " must be a " + str(correctType) + ". But " + str(arg) + " is a " + str(type(arg)) + "."

db = DBSchema("test", ["a"], ["str"])
a = Request(Request(db))
b = Request(a)
d = b.getTable()
print(d)
a = 1
print(type(a))
db2 = db.copy()
db2.add("b", "int")
print(db)
print(db2)
Select(db, "a", "a")
Join(db, "a")
