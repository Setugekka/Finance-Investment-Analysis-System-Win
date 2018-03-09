# coding: UTF-8
from flask import Blueprint,jsonify
from Library.wind_mysql.get_company_list import *
database_update = Blueprint(
    'database_update',
    __name__,
    url_prefix="/database_update"
)

# 数据库整体更新
@database_update.route('/update_cns_stock', methods=['GET', 'POST'])
def api_updata_cns_stock():
    data={}
    # first_updata()
    first_upData_cns_stock_basics()
    # end_time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
    # upData_company_list(end_time)
    #
    # results = table_update_time.query.filter_by(table_name='cns_stock_basics').first()
    # start_time = result.last_update_time
    # end_time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
    # upData_cns_stock_basics(start_time,end_time)
    #
    # results = table_update_time.query.filter_by(table_name='cns_balance_sheet').first()
    # start_time = result.last_update_time
    # end_time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
    # upData_cns_balance_sheet(start_time,end_time)
    #
    #
    # results = table_update_time.query.filter_by(table_name='cns_income_statement').first()
    # start_time = result.last_update_time
    # end_time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
    # upData_cns_income_statement(start_time,end_time)
    #
    #

    return jsonify(data)

# 表格单独更新
@database_update.route('/update_company_list', methods=['GET', 'POST'])
def api_updata_company_list():
    # end_time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
    # upData_company_list(end_time)
    data = {
        'message':'yes'
    }
    return jsonify(data)

@database_update.route('/upDate_cns_stock_basics', methods=['GET', 'POST'])
def api_upData_cns_stock_basics():
    result = table_update_time.query.filter_by(table_name='cns_stock_basics').first()
    start_time = result.last_update_time
    end_time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
    upData_cns_stock_basics(start_time,end_time)
    data = {

    }
    return jsonify(data)

@database_update.route('/upDate_cns_balance_sheet', methods=['GET', 'POST'])
def api_upData_cns_balance_sheet():
    result = table_update_time.query.filter_by(table_name='cns_balance_sheet').first()
    start_time = result.last_update_time
    end_time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
    upData_cns_balance_sheet(start_time,end_time)
    data = {
    }
    return jsonify(data)

@database_update.route('/upDate_cns_income_statement', methods=['GET', 'POST'])
def api_upData_cns_income_statement():
    result = table_update_time.query.filter_by(table_name='cns_income_statement').first()
    start_time = result.last_update_time
    end_time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
    upData_cns_income_statement(start_time,end_time)
    data = {}
    return jsonify(data)

@database_update.route('/upDate_cns_statement_of_cash_flows', methods=['GET', 'POST'])
def api_upData_cns_statement_of_cash_flows():
    data = {}
    result = table_update_time.query.filter_by(table_name='cns_statement_of_cash_flows').first()
    start_time = result.last_update_time
    end_time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
    upData_cns_statement_of_cash_flows(start_time,end_time)
    return jsonify(data)

# 生成管理员界面中表格更新时间表格
@database_update.route('/creat_update_time_table', methods=['GET', 'POST'])
def creat_update_time_table():
    table_name_list = []
    time_list = []
    results = table_update_time.query.all()
    for result in results:
        table_name_list.append(result.table_name)
        time_list.append(result.last_update_time)
    data = {
        'table_name_list':table_name_list,
        'time_list':time_list
    }
    return jsonify(data)