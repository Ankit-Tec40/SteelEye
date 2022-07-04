from functools import cache
from flask import Flask,jsonify, request;
from flask_mysqldb import MySQL
app=Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='pass'
app.config['MYSQL_DB']='steeleye'
mysql=MySQL(app)

@app.route("/")
def index():
        return ("Endpoints:-  /ListTrades, /SearchID, /SearchTrade")

@app.route("/ListTrades")
def ListTrades():
        query=f'''SELECT trade.trade_id,trade.asset_class,trade.counterparty,trade.instrument_id,trade.instrument_name,
        trade.trade_date_time,trade.trader,tradedetails.buySellIndicator,tradedetails.price,tradedetails.quantity FROM trade,tradedetails 
        WHERE trade.trade_id=tradedetails.trade_id'''
        try:
                cur=mysql.connection.cursor()
                cur.execute(query)
        except:
                return "Something Went Wrong"

        columns = cur.description
        result = []
        for value in cur.fetchall():
                tmp = {}
                for (index,column) in enumerate(value):
                        tmp[columns[index][0]] = column
                result.append(tmp)
        print(result)
        data=jsonify(result)
        return(data)

@app.route("/SearchID")
def SearchID():
        id=request.form.get("id")
        query=f'''SELECT * FROM 
        (SELECT trade.trade_id,trade.asset_class,trade.counterparty,trade.instrument_id,trade.instrument_name,trade.trade_date_time,trade.trader,tradedetails.buySellIndicator,tradedetails.price,tradedetails.quantity FROM trade,tradedetails WHERE trade.trade_id=tradedetails.trade_id) 
        AS alias WHERE trade_id={id}'''
        try:
                cur=mysql.connection.cursor()
                cur.execute(query)
        except:
                return "Something Went Wrong"

        columns = cur.description
        result = []
        for value in cur.fetchall():
                tmp = {}
                for (index,column) in enumerate(value):
                        tmp[columns[index][0]] = column
                result.append(tmp)
        print(result)
        data=jsonify(result)
        return(data)

@app.route("/SearchTrade")
def SearchTrade():
        searchField=request.form.get("searchField")
        print(searchField)

        query=f'''SELECT * FROM (
        SELECT trade.trade_id,trade.asset_class,trade.counterparty,trade.instrument_id,trade.instrument_name,trade.trade_date_time,trade.trader,tradedetails.buySellIndicator,tradedetails.price,tradedetails.quantity FROM trade,tradedetails WHERE trade.trade_id=tradedetails.trade_id
        ) AS alias WHERE (counterparty='{searchField}' OR instrument_id = '{searchField}' OR instrument_name='{searchField}' OR trader='{searchField}')'''
        try:
                cur=mysql.connection.cursor()
                cur.execute(query)
        except:
                return "Something Went Wrong"

        columns = cur.description
        result = []
        for value in cur.fetchall():
                tmp = {}
                for (index,column) in enumerate(value):
                        tmp[columns[index][0]] = column
                result.append(tmp)
        print(result)
        data=jsonify(result)
        return(data)



if __name__=="__main__":
        app.run(debug=True)
