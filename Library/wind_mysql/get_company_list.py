# coding: UTF-8

# 初始化接口#
from WindPy import *
import pandas as pd
import json
from Api.models import *
import MySQLdb, time, re
import time as Time
from sqlalchemy import create_engine, or_, func, desc, distinct  # me func用于计数,desc用于逆序找max值
from sqlalchemy.orm import sessionmaker

# 测试期间所有函数只读取两条股票
# date:yyyy-mm-dd
def upData_company_list(date):
    db_engine = create_engine('mysql://root:0000@localhost/company_list?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
    w.start();
    # 获取所有A股代码#
    AllAStock = w.wset("sectorconstituent", "sectorid=a001010100000000;field=wind_code");
    if AllAStock.ErrorCode != 0:
        print("Get Data failed! exit!")
        exit()
    for stock in AllAStock.Data[0]:
    # for i in range(0,20):
    #     stock = AllAStock.Data[0][i]
        wdata = w.wsd(stock, "sec_name,ipo_date", "2018-01-04", date , "Period=Y;Days=Weekdays")
        # 存入数据库
        # 更新company_list
        result = company_list.query.filter_by(Code=stock[0:6]).first()
        if result is None:
            updata = company_list()
            updata.Code = stock[0:6]
            updata.Name = wdata.Data[0]
            updata.IPO_Date = wdata.Data[1]
            updata.Up_Date = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
            updata.Wind_Code = stock
            # '%Y-%m-%d'
            db.session.add(updata)
        else:
            result.Name = wdata.Data[0]
            result.Up_Date = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
            result.Wind_Code = stock

    table_update= table_update_time.query.filter_by(table_name='company_list').first_or_404()
    table_update.last_update_time = date
    db.session.commit()

# 以下四个函数股票列表不是实时获取而是从company_list中获取
def upData_cns_stock_basics(start_date,end_date):
    db_engine = create_engine('mysql://root:0000@localhost/cns_stock_basics?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
    w.start();
    # 从company_list中获取股票列表#
    AllAStock = []
    results = company_list.query.all()
    for result in results:
        AllAStock.append( result.Wind_Code)
    for stock in AllAStock:
    # for i in range(0, 2):
    #     stock = AllAStock[i]
        wdata = w.wsd(stock,
                      "sec_name,ipo_date,exch_city,industry_gics,concept,curr,fiscaldate,auditor,province,city,founddate,nature1,boardchairmen,holder_controller,website,phone,majorproducttype,majorproductname",
                      start_date, end_date, "unit=1;rptType=1;Period=Q;Days=Alldays")
        result = cns_stock_basics.query.filter_by(trade_code=stock[0:6]).first()
        # 更新cns_stock_basics
        if result is None:
            updata = cns_stock_basics()
            updata.trade_code = stock[0:6]
            updata.sec_name = wdata.Data[0]
            updata.ipo_date = wdata.Data[1]
            updata.exch_city = wdata.Data[2]
            updata.industry_gics = wdata.Data[3]
            updata.concept = wdata.Data[4]
            updata.curr = wdata.Data[5]
            updata.fiscaldate = wdata.Data[6]
            updata.auditor = wdata.Data[7]
            updata.province = wdata.Data[8]
            updata.city = wdata.Data[9]
            updata.founddate = wdata.Data[10]
            updata.nature1 = wdata.Data[11]
            updata.boardchairmen = wdata.Data[12]
            updata.holder_controller = wdata.Data[13]
            updata.website = wdata.Data[14]
            updata.phone = wdata.Data[15]
            updata.majorproducttype = wdata.Data[16]
            updata.majorproductname = wdata.Data[17]
            db.session.add(updata)
        else:
            result.trade_code = stock[0:6]
            result.sec_name = wdata.Data[0]
            result.ipo_date = wdata.Data[1]
            result.exch_city = wdata.Data[2]
            result.industry_gics = wdata.Data[3]
            result.concept = wdata.Data[4]
            result.curr = wdata.Data[5]
            result.fiscaldate = wdata.Data[6]
            result.auditor = wdata.Data[7]
            result.province = wdata.Data[8]
            result.city = wdata.Data[9]
            result.founddate = wdata.Data[10]
            result.nature1 = wdata.Data[11]
            result.boardchairmen = wdata.Data[12]
            result.holder_controller = wdata.Data[13]
            result.website = wdata.Data[14]
            result.phone = wdata.Data[15]
            result.majorproducttype = wdata.Data[16]
            result.majorproductname = wdata.Data[17]
    table_update= table_update_time.query.filter_by(table_name='cns_stock_basics').first_or_404()
    table_update.last_update_time = Time.strftime('%Y-%m-%d', Time.localtime(Time.time()))
    db.session.commit()
    return wdata.Data

def upData_cns_balance_sheet(start_date,end_date):
    db_engine = create_engine('mysql://root:0000@localhost/cns_balance_sheet?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
    w.start();
    # 从company_list中获取股票列表#
    AllAStock = []
    results = company_list.query.all()
    for result in results:
        AllAStock.append( result.Wind_Code)
    for stock in AllAStock:
    # for i in range(0, 2):
    #     stock = AllAStock[i]
        wdata = w.wsd(stock,
                      "sec_name,monetary_cap,tradable_fin_assets,notes_rcv,acct_rcv,prepay,int_rcv,dvd_rcv,inventories,non_cur_assets_due_within_1y,oth_cur_assets,fin_assets_avail_for_sale,held_to_mty_invest,long_term_rec,long_term_eqy_invest,invest_real_estate,fix_assets,const_in_prog,proj_matl,fix_assets_disp,productive_bio_assets,oil_and_natural_gas_assets,intang_assets,r_and_d_costs,goodwill,long_term_deferred_exp,deferred_tax_assets,oth_non_cur_assets,st_borrow,tradable_fin_liab,notes_payable,acct_payable,adv_from_cust,empl_ben_payable,taxes_surcharges_payable,int_payable,dvd_payable,oth_payable,non_cur_liab_due_within_1y,oth_cur_liab,lt_borrow,bonds_payable,lt_payable,specific_item_payable,provisions,deferred_tax_liab,oth_non_cur_liab,cap_stk,cap_rsrv,tsy_stk,surplus_rsrv,undistributed_profit,tot_cur_assets,tot_non_cur_assets,tot_cur_liab,tot_non_cur_liab,tot_liab,tot_equity",
                      start_date, end_date, "unit=1;rptType=1;Period=Q;Days=Alldays")

        # 更新cns_stock_basics
        for i in range(0, len(wdata.Times)):
            result = cns_balance_sheet.query.filter_by(trade_code=stock[0:6],the_date=wdata.Times[i]).first()
            if result is None:
                updata = cns_balance_sheet()
                updata.stock_code = stock[0:6]
                updata.the_date = wdata.Times[i]
                updata.sec_name = wdata.Data[0][i]
                updata.monetary_cap = wdata.Data[1][i]
                updata.tradable_fin_assets = wdata.Data[2][i]
                updata.notes_rcv = wdata.Data[3][i]
                updata.acct_rcv = wdata.Data[4][i]
                updata.prepay = wdata.Data[5][i]
                updata.int_rcv = wdata.Data[6][i]
                updata.dvd_rcv = wdata.Data[7][i]
                updata.inventories = wdata.Data[8][i]
                updata.non_cur_assets_due_within_1y=wdata.Data[9][i]
                updata.oth_cur_assets = wdata.Data[10][i]
                updata.fin_assets_avail_for_sale = wdata.Data[11][i]
                updata.held_to_mty_invest = wdata.Data[12][i]
                updata.long_term_rec = wdata.Data[13][i]
                updata.long_term_eqy_invest = wdata.Data[14][i]
                updata.invest_real_estate = wdata.Data[15][i]
                updata.fix_assets = wdata.Data[16][i]
                updata.const_in_prog = wdata.Data[17][i]
                updata.proj_matl = wdata.Data[18][i]
                updata.fix_assets_disp = wdata.Data[19][i]
                updata.productive_bio_assets = wdata.Data[20][i]
                updata.oil_and_natural_gas_assets = wdata.Data[21][i]
                updata.intang_assets = wdata.Data[22][i]
                updata.r_and_d_costs = wdata.Data[23][i]
                updata.goodwill = wdata.Data[24][i]
                updata.long_term_deferred_exp = wdata.Data[25][i]
                updata.deferred_tax_assets = wdata.Data[26][i]
                updata.oth_non_cur_assets = wdata.Data[27][i]
                updata.st_borrow = wdata.Data[28][i]
                updata.tradable_fin_liab = wdata.Data[29][i]
                updata.notes_payable = wdata.Data[30][i]
                updata.acct_payable = wdata.Data[31][i]
                updata.adv_from_cust = wdata.Data[32][i]
                updata.empl_ben_payable = wdata.Data[33][i]
                updata.taxes_surcharges_payable = wdata.Data[34][i]
                updata.int_payable = wdata.Data[35][i]
                updata.dvd_payable = wdata.Data[36][i]
                updata.oth_payable = wdata.Data[37][i]
                updata.non_cur_liab_due_within_1y = wdata.Data[38][i]
                updata.oth_cur_liab = wdata.Data[39][i]
                updata.lt_borrow = wdata.Data[40][i]
                updata.bonds_payable = wdata.Data[41][i]
                updata.lt_payable = wdata.Data[42][i]
                updata.specific_item_payable = wdata.Data[43][i]
                updata.provisions = wdata.Data[44][i]
                updata.deferred_tax_liab = wdata.Data[45][i]
                updata.oth_non_cur_liab = wdata.Data[46][i]
                updata.cap_stk = wdata.Data[47][i]
                updata.cap_rsrv = wdata.Data[48][i]
                updata.tsy_stk = wdata.Data[49][i]
                updata.surplus_rsrv = wdata.Data[50][i]
                updata.undistributed_profit = wdata.Data[51][i]
                updata.tot_cur_assets= wdata.Data[52][i]
                updata.tot_non_cur_assets= wdata.Data[53][i]
                updata.tot_cur_liab= wdata.Data[54][i]
                updata.tot_non_cur_liab= wdata.Data[55][i]
                updata.tot_liab= wdata.Data[56][i]
                updata.tot_equity= wdata.Data[57][i]
                db.session.add(updata)
            else:
                result.stock_code = stock[0:6]
                result.the_date = wdata.Times[i]
                result.sec_name = wdata.Data[0][i]
                result.monetary_cap = wdata.Data[1][i]
                result.tradable_fin_assets = wdata.Data[2][i]
                result.notes_rcv = wdata.Data[3][i]
                result.acct_rcv = wdata.Data[4][i]
                result.prepay = wdata.Data[5][i]
                result.int_rcv = wdata.Data[6][i]
                result.dvd_rcv = wdata.Data[7][i]
                result.inventories = wdata.Data[8][i]
                result.non_cur_assets_due_within_1y=wdata.Data[9][i]
                result.oth_cur_assets = wdata.Data[10][i]
                result.fin_assets_avail_for_sale = wdata.Data[11][i]
                result.held_to_mty_invest = wdata.Data[12][i]
                result.long_term_rec = wdata.Data[13][i]
                result.long_term_eqy_invest = wdata.Data[14][i]
                result.invest_real_estate = wdata.Data[15][i]
                result.fix_assets = wdata.Data[16][i]
                result.const_in_prog = wdata.Data[17][i]
                result.proj_matl = wdata.Data[18][i]
                result.fix_assets_disp = wdata.Data[19][i]
                result.productive_bio_assets = wdata.Data[20][i]
                result.oil_and_natural_gas_assets = wdata.Data[21][i]
                result.intang_assets = wdata.Data[22][i]
                result.r_and_d_costs = wdata.Data[23][i]
                result.goodwill = wdata.Data[24][i]
                result.long_term_deferred_exp = wdata.Data[25][i]
                result.deferred_tax_assets = wdata.Data[26][i]
                result.oth_non_cur_assets = wdata.Data[27][i]
                result.st_borrow = wdata.Data[28][i]
                result.tradable_fin_liab = wdata.Data[29][i]
                result.notes_payable = wdata.Data[30][i]
                result.acct_payable = wdata.Data[31][i]
                result.adv_from_cust = wdata.Data[32][i]
                result.empl_ben_payable = wdata.Data[33][i]
                result.taxes_surcharges_payable = wdata.Data[34][i]
                result.int_payable = wdata.Data[35][i]
                result.dvd_payable = wdata.Data[36][i]
                result.oth_payable = wdata.Data[37][i]
                result.non_cur_liab_due_within_1y = wdata.Data[38][i]
                result.oth_cur_liab = wdata.Data[39][i]
                result.lt_borrow = wdata.Data[40][i]
                result.bonds_payable = wdata.Data[41][i]
                result.lt_payable = wdata.Data[42][i]
                result.specific_item_payable = wdata.Data[43][i]
                result.provisions = wdata.Data[44][i]
                result.deferred_tax_liab = wdata.Data[45][i]
                result.oth_non_cur_liab = wdata.Data[46][i]
                result.cap_stk = wdata.Data[47][i]
                result.cap_rsrv = wdata.Data[48][i]
                result.tsy_stk = wdata.Data[49][i]
                result.surplus_rsrv = wdata.Data[50][i]
                result.undistributed_profit = wdata.Data[51][i]
                result.tot_cur_assets= wdata.Data[52][i]
                result.tot_non_cur_assets= wdata.Data[53][i]
                result.tot_cur_liab= wdata.Data[54][i]
                result.tot_non_cur_liab= wdata.Data[55][i]
                result.tot_liab= wdata.Data[56][i]
                result.tot_equity= wdata.Data[57][i]
    table_update= table_update_time.query.filter_by(table_name='cns_balance_sheet').first_or_404()
    table_update.last_update_time = Time.strftime('%Y-%m-%d', Time.localtime(Time.time()))
    db.session.commit()
    return wdata.Data

def upData_cns_income_statement(start_date,end_date):
    db_engine = create_engine('mysql://root:0000@localhost/cns_income_statement?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
    w.start();
     # 从company_list中获取股票列表#
    AllAStock = []
    results = company_list.query.all()
    for result in results:
        AllAStock.append( result.Wind_Code)
    for stock in AllAStock:
    # for i in range(0, 2):
    #     stock = AllAStock[i]
        wdata = w.wsd(stock, "sec_name,oper_rev,oper_cost,taxes_surcharges_ops,selling_dist_exp,gerl_admin_exp,fin_exp_is,impair_loss_assets,net_gain_chg_fv,net_invest_inc,opprofit,non_oper_rev,non_oper_exp,tot_profit,net_profit_is,eps_basic_is,eps_diluted_is,tax",
                       start_date,end_date, "unit=1;rptType=1;Period=Q;Days=Alldays")
        print(wdata.Data)
        # print(wdata.Data[1])
        # print(wdata.Data[2])
        # 更新cns_stock_basics
        for i in range(0, len(wdata.Times)):
            result = cns_income_statement.query.filter_by(trade_code=stock[0:6],the_date=wdata.Times[i]).first()
            if result is None:
                updata = cns_income_statement()
                updata.stock_code = stock[0:6]
                updata.the_date = wdata.Times[i]
                updata.sec_name = wdata.Data[0][i]
                updata.oper_rev = wdata.Data[1][i]
                updata.oper_cost = wdata.Data[2][i]
                updata.taxes_surcharges_ops = wdata.Data[3][i]
                updata.selling_dist_exp = wdata.Data[4][i]
                updata.gerl_admin_exp = wdata.Data[5][i]
                updata.fin_exp_is = wdata.Data[6][i]
                updata.impair_loss_assets = wdata.Data[7][i]
                updata.net_gain_chg_fv = wdata.Data[8][i]
                updata.net_invest_inc = wdata.Data[9][i]
                updata.opprofit = wdata.Data[10][i]
                updata.non_oper_rev = wdata.Data[11][i]
                updata.non_oper_exp = wdata.Data[12][i]
                updata.tax = wdata.Data[13][i]
                updata.tot_profit = wdata.Data[14][i]
                updata.net_profit_is = wdata.Data[15][i]
                updata.eps_basic_is = wdata.Data[16][i]
                updata.eps_diluted_is = wdata.Data[17][i]
                db.session.add(updata)
            else:
                result.stock_code = stock[0:6]
                result.the_date = wdata.Times[i]
                result.sec_name = wdata.Data[0][i]
                result.oper_rev = wdata.Data[1][i]
                result.oper_cost = wdata.Data[2][i]
                result.taxes_surcharges_ops = wdata.Data[3][i]
                result.selling_dist_exp = wdata.Data[4][i]
                result.gerl_admin_exp = wdata.Data[5][i]
                result.fin_exp_is = wdata.Data[6][i]
                result.impair_loss_assets = wdata.Data[7][i]
                result.net_gain_chg_fv = wdata.Data[8][i]
                result.net_invest_inc = wdata.Data[9][i]
                result.opprofit = wdata.Data[10][i]
                result.non_oper_rev = wdata.Data[11][i]
                result.non_oper_exp = wdata.Data[12][i]
                result.tax = wdata.Data[13][i]
                result.tot_profit = wdata.Data[14][i]
                result.net_profit_is = wdata.Data[15][i]
                result.eps_basic_is = wdata.Data[16][i]
                result.eps_diluted_is = wdata.Data[17][i]

    table_update= table_update_time.query.filter_by(table_name='cns_income_statement').first_or_404()
    table_update.last_update_time = Time.strftime('%Y-%m-%d', Time.localtime(Time.time()))
    db.session.commit()
    return wdata.Data

def upData_cns_statement_of_cash_flows(start_date,end_date):
    db_engine = create_engine('mysql://root:0000@localhost/cns_statement_of_cash_flows?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
    w.start();
     # 从company_list中获取股票列表#
    AllAStock = []
    results = company_list.query.all()
    for result in results:
        AllAStock.append( result.Wind_Code)
    for stock in AllAStock:
    # for i in range(0, 2):
    #     stock = AllAStock[i]
        wdata = w.wsd(stock,
                      "sec_name,cash_recp_sg_and_rs,recp_tax_rends,other_cash_recp_ral_oper_act,stot_cash_inflows_oper_act,cash_pay_goods_purch_serv_rec,cash_pay_beh_empl,pay_all_typ_tax,other_cash_pay_ral_oper_act,stot_cash_outflows_oper_act,net_cash_flows_oper_act,cash_recp_disp_withdrwl_invest,cash_recp_return_invest,net_cash_recp_disp_fiolta,other_cash_recp_ral_inv_act,stot_cash_inflows_inv_act,cash_pay_acq_const_fiolta,cash_paid_invest,other_cash_pay_ral_inv_act,stot_cash_outflows_inv_act,net_cash_flows_inv_act,cash_recp_cap_contrib,cash_recp_borrow,other_cash_recp_ral_fnc_act,stot_cash_inflows_fnc_act,cash_prepay_amt_borr,cash_pay_dist_dpcp_int_exp,other_cash_pay_ral_fnc_act,stot_cash_outflows_fnc_act,net_cash_flows_fnc_act,eff_fx_flu_cash,net_incr_cash_cash_equ_dm,cash_cash_equ_beg_period,cash_cash_equ_end_period,net_profit_cs,prov_depr_assets,depr_fa_coga_dpba,amort_intang_assets,amort_lt_deferred_exp,loss_disp_fiolta,loss_scr_fa,loss_fv_chg,fin_exp_cs,invest_loss,decr_deferred_inc_tax_assets,incr_deferred_inc_tax_liab,decr_inventories,decr_oper_payable,incr_oper_payable,others,im_net_cash_flows_oper_act,conv_debt_into_cap,conv_corp_bonds_due_within_1y,fa_fnc_leases,end_bal_cash,beg_bal_cash,end_bal_cash_equ,beg_bal_cash_equ,net_incr_cash_cash_equ_im",
                       start_date,end_date, "unit=1;rptType=1;Period=Q;Days=Alldays")
        print(wdata.Data)
        # print(wdata.Data[1])
        # print(wdata.Data[2])
        # 更新cns_stock_basics
        for i in range(0, len(wdata.Times)):
            result = cns_statement_of_cash_flows.query.filter_by(trade_code=stock[0:6],the_date=wdata.Times[i]).first()
            if result is None:
                updata = cns_statement_of_cash_flows()
                updata.stock_code = stock[0:6]
                updata.the_date = wdata.Times[i]
                updata.sec_name = wdata.Data[0][i]
                updata.cash_recp_sg_and_rs = wdata.Data[1][i]
                updata.recp_tax_rends = wdata.Data[2][i]
                updata.other_cash_recp_ral_oper_act= wdata.Data[3][i]
                updata.stot_cash_inflows_oper_act = wdata.Data[4][i]
                updata.cash_pay_goods_purch_serv_rec = wdata.Data[5][i]
                updata.cash_pay_beh_empl = wdata.Data[6][i]
                updata.pay_all_typ_tax = wdata.Data[7][i]
                updata.other_cash_pay_ral_oper_act = wdata.Data[8][i]
                updata.stot_cash_outflows_oper_act = wdata.Data[9][i]
                updata.net_cash_flows_oper_act = wdata.Data[10][i]
                updata.cash_recp_disp_withdrwl_invest = wdata.Data[11][i]
                updata.cash_recp_return_invest = wdata.Data[12][i]
                updata.net_cash_recp_disp_fiolta = wdata.Data[13][i]
                updata.other_cash_recp_ral_inv_act = wdata.Data[14][i]
                updata.stot_cash_inflows_inv_act = wdata.Data[15][i]
                updata.cash_pay_acq_const_fiolta = wdata.Data[16][i]
                updata.cash_paid_invest = wdata.Data[17][i]
                updata.other_cash_pay_ral_inv_act = wdata.Data[18][i]
                updata.stot_cash_outflows_inv_act = wdata.Data[19][i]
                updata.net_cash_flows_inv_act = wdata.Data[20][i]
                updata.cash_recp_cap_contrib = wdata.Data[21][i]
                updata.cash_recp_borrow = wdata.Data[22][i]
                updata.other_cash_recp_ral_fnc_act = wdata.Data[23][i]
                updata.stot_cash_inflows_fnc_act = wdata.Data[24][i]
                updata.cash_prepay_amt_borr = wdata.Data[25][i]
                updata.cash_pay_dist_dpcp_int_exp = wdata.Data[26][i]
                updata.other_cash_pay_ral_fnc_act = wdata.Data[27][i]
                updata.stot_cash_outflows_fnc_act = wdata.Data[28][i]
                updata.net_cash_flows_fnc_act = wdata.Data[29][i]
                updata.eff_fx_flu_cash = wdata.Data[30][i]
                updata.net_incr_cash_cash_equ_dm = wdata.Data[31][i]
                updata.cash_cash_equ_beg_period = wdata.Data[32][i]
                updata.cash_cash_equ_end_period = wdata.Data[33][i]
                updata.net_profit_cs = wdata.Data[34][i]
                updata.prov_depr_assets = wdata.Data[35][i]
                updata.depr_fa_coga_dpba = wdata.Data[36][i]
                updata.amort_intang_assets = wdata.Data[37][i]
                updata.amort_lt_deferred_exp = wdata.Data[38][i]
                updata.loss_disp_fiolta = wdata.Data[39][i]
                updata.loss_scr_fa	 = wdata.Data[40][i]
                updata.loss_fv_chg = wdata.Data[41][i]
                updata.fin_exp_cs = wdata.Data[42][i]
                updata.invest_loss = wdata.Data[43][i]
                updata.decr_deferred_inc_tax_assets = wdata.Data[44][i]
                updata.incr_deferred_inc_tax_liab = wdata.Data[45][i]
                updata.decr_inventories = wdata.Data[46][i]
                updata.decr_oper_payable = wdata.Data[47][i]
                updata.incr_oper_payable = wdata.Data[48][i]
                updata.others = wdata.Data[49][i]
                updata.im_net_cash_flows_oper_act = wdata.Data[50][i]
                updata.conv_debt_into_cap = wdata.Data[51][i]
                updata.conv_corp_bonds_due_within_1y= wdata.Data[52][i]
                updata.fa_fnc_leases = wdata.Data[53][i]
                updata.end_bal_cash = wdata.Data[54][i]
                updata.beg_bal_cash = wdata.Data[55][i]
                updata.end_bal_cash_equ = wdata.Data[56][i]
                updata.beg_bal_cash_equ = wdata.Data[57][i]
                updata.net_incr_cash_cash_equ_im = wdata.Data[58][i]
                db.session.add(updata)
            else:
                result.stock_code = stock[0:6]
                result.the_date = wdata.Times[i]
                result.sec_name = wdata.Data[0][i]
                result.cash_recp_sg_and_rs = wdata.Data[1][i]
                result.recp_tax_rends = wdata.Data[2][i]
                result.other_cash_recp_ral_oper_act= wdata.Data[3][i]
                result.stot_cash_inflows_oper_act = wdata.Data[4][i]
                result.cash_pay_goods_purch_serv_rec = wdata.Data[5][i]
                result.cash_pay_beh_empl = wdata.Data[6][i]
                result.pay_all_typ_tax = wdata.Data[7][i]
                result.other_cash_pay_ral_oper_act = wdata.Data[8][i]
                result.stot_cash_outflows_oper_act = wdata.Data[9][i]
                result.net_cash_flows_oper_act = wdata.Data[10][i]
                result.cash_recp_disp_withdrwl_invest = wdata.Data[11][i]
                result.cash_recp_return_invest = wdata.Data[12][i]
                result.net_cash_recp_disp_fiolta = wdata.Data[13][i]
                result.other_cash_recp_ral_inv_act = wdata.Data[14][i]
                result.stot_cash_inflows_inv_act = wdata.Data[15][i]
                result.cash_pay_acq_const_fiolta = wdata.Data[16][i]
                result.cash_paid_invest = wdata.Data[17][i]
                result.other_cash_pay_ral_inv_act = wdata.Data[18][i]
                result.stot_cash_outflows_inv_act = wdata.Data[19][i]
                result.net_cash_flows_inv_act = wdata.Data[20][i]
                result.cash_recp_cap_contrib = wdata.Data[21][i]
                result.cash_recp_borrow = wdata.Data[22][i]
                result.other_cash_recp_ral_fnc_act = wdata.Data[23][i]
                result.stot_cash_inflows_fnc_act = wdata.Data[24][i]
                result.cash_prepay_amt_borr = wdata.Data[25][i]
                result.cash_pay_dist_dpcp_int_exp = wdata.Data[26][i]
                result.other_cash_pay_ral_fnc_act = wdata.Data[27][i]
                result.stot_cash_outflows_fnc_act = wdata.Data[28][i]
                result.net_cash_flows_fnc_act = wdata.Data[29][i]
                result.eff_fx_flu_cash = wdata.Data[30][i]
                result.net_incr_cash_cash_equ_dm = wdata.Data[31][i]
                result.cash_cash_equ_beg_period = wdata.Data[32][i]
                result.cash_cash_equ_end_period = wdata.Data[33][i]
                result.net_profit_cs = wdata.Data[34][i]
                result.prov_depr_assets = wdata.Data[35][i]
                result.depr_fa_coga_dpba = wdata.Data[36][i]
                result.amort_intang_assets = wdata.Data[37][i]
                result.amort_lt_deferred_exp = wdata.Data[38][i]
                result.loss_disp_fiolta = wdata.Data[39][i]
                result.loss_scr_fa	 = wdata.Data[40][i]
                result.loss_fv_chg = wdata.Data[41][i]
                result.fin_exp_cs = wdata.Data[42][i]
                result.invest_loss = wdata.Data[43][i]
                result.decr_deferred_inc_tax_assets = wdata.Data[44][i]
                result.incr_deferred_inc_tax_liab = wdata.Data[45][i]
                result.decr_inventories = wdata.Data[46][i]
                result.decr_oper_payable = wdata.Data[47][i]
                result.incr_oper_payable = wdata.Data[48][i]
                result.others = wdata.Data[49][i]
                result.im_net_cash_flows_oper_act = wdata.Data[50][i]
                result.conv_debt_into_cap = wdata.Data[51][i]
                result.conv_corp_bonds_due_within_1y= wdata.Data[52][i]
                result.fa_fnc_leases = wdata.Data[53][i]
                result.end_bal_cash = wdata.Data[54][i]
                result.beg_bal_cash = wdata.Data[55][i]
                result.end_bal_cash_equ = wdata.Data[56][i]
                result.beg_bal_cash_equ = wdata.Data[57][i]
                result.net_incr_cash_cash_equ_im = wdata.Data[58][i]
    table_update= table_update_time.query.filter_by(table_name='cns_statement_of_cash_flows').first_or_404()
    table_update.last_update_time = Time.strftime('%Y-%m-%d', Time.localtime(Time.time()))
    db.session.commit()
    return wdata.Data

# 初始化数据表
def first_updata():
    db_engine = create_engine('mysql://root:0000@localhost/cns_stock_basics?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
    w.start();
    now_date = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
    upData_company_list(now_date)
    first_upData_cns_stock_basics()
    first_upData_cns_balance_sheet()
    first_upData_cns_income_statement()
    first_upData_cns_statement_of_cash_flows()

def first_upData_cns_stock_basics():
    db_engine = create_engine('mysql://root:0000@localhost/cns_stock_basics?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
    w.start();
    # 从company_list中获取股票列表#
    AllAStock = []
    results = company_list.query.all()
    for result in results:
        AllAStock.append( result.Wind_Code)
    # for stock in AllAStock:
    for i in range(0, 2):
        stock = AllAStock[i]
        # result = company_list.query.filter_by(Code=stock[0:6]).first_or_404()
        start_date =  result.IPO_Date
        end_date = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
        result = cns_stock_basics.query.filter_by(trade_code=stock[0:6]).first()
        wdata = w.wsd(stock,
                      "sec_name,ipo_date,exch_city,industry_gics,concept,curr,fiscaldate,auditor,province,city,founddate,nature1,boardchairmen,holder_controller,website,phone,majorproducttype,majorproductname",
                      start_date, end_date, "unit=1;rptType=1;Period=Q;Days=Alldays")
        result = cns_stock_basics.query.filter_by(trade_code=stock[0:6]).first()
        # 更新cns_stock_basics
        if result is None:
            updata = cns_stock_basics()
            updata.trade_code = stock[0:6]
            updata.sec_name = wdata.Data[0]
            updata.ipo_date = wdata.Data[1]
            updata.exch_city = wdata.Data[2]
            updata.industry_gics = wdata.Data[3]
            updata.concept = wdata.Data[4]
            updata.curr = wdata.Data[5]
            updata.fiscaldate = wdata.Data[6]
            updata.auditor = wdata.Data[7]
            updata.province = wdata.Data[8]
            updata.city = wdata.Data[9]
            updata.founddate = wdata.Data[10]
            updata.nature1 = wdata.Data[11]
            updata.boardchairmen = wdata.Data[12]
            updata.holder_controller = wdata.Data[13]
            updata.website = wdata.Data[14]
            updata.phone = wdata.Data[15]
            updata.majorproducttype = wdata.Data[16]
            updata.majorproductname = wdata.Data[17]
            db.session.add(updata)
        else:
            result.trade_code = stock[0:6]
            result.sec_name = wdata.Data[0]
            result.ipo_date = wdata.Data[1]
            result.exch_city = wdata.Data[2]
            result.industry_gics = wdata.Data[3]
            result.concept = wdata.Data[4]
            result.curr = wdata.Data[5]
            result.fiscaldate = wdata.Data[6]
            result.auditor = wdata.Data[7]
            result.province = wdata.Data[8]
            result.city = wdata.Data[9]
            result.founddate = wdata.Data[10]
            result.nature1 = wdata.Data[11]
            result.boardchairmen = wdata.Data[12]
            result.holder_controller = wdata.Data[13]
            result.website = wdata.Data[14]
            result.phone = wdata.Data[15]
            result.majorproducttype = wdata.Data[16]
            result.majorproductname = wdata.Data[17]
    table_update= table_update_time.query.filter_by(table_name='cns_stock_basics').first_or_404()
    table_update.last_update_time = Time.strftime('%Y-%m-%d', Time.localtime(Time.time()))
    db.session.commit()
    return wdata.Data

def first_upData_cns_balance_sheet():
    db_engine = create_engine('mysql://root:0000@localhost/cns_balance_sheet?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
    w.start();
    # 从company_list中获取股票列表#
    AllAStock = []
    results = company_list.query.all()
    for result in results:
        AllAStock.append( result.Wind_Code)
    # for stock in AllAStock:
    for i in range(0, 2):
        stock = AllAStock[i]
        result = company_list.query.filter_by(Code=stock[0:6]).first()
        start_date =  result.IPO_Date
        end_date = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
        wdata = w.wsd(stock,
                      "sec_name,monetary_cap,tradable_fin_assets,notes_rcv,acct_rcv,prepay,int_rcv,dvd_rcv,inventories,non_cur_assets_due_within_1y,oth_cur_assets,fin_assets_avail_for_sale,held_to_mty_invest,long_term_rec,long_term_eqy_invest,invest_real_estate,fix_assets,const_in_prog,proj_matl,fix_assets_disp,productive_bio_assets,oil_and_natural_gas_assets,intang_assets,r_and_d_costs,goodwill,long_term_deferred_exp,deferred_tax_assets,oth_non_cur_assets,st_borrow,tradable_fin_liab,notes_payable,acct_payable,adv_from_cust,empl_ben_payable,taxes_surcharges_payable,int_payable,dvd_payable,oth_payable,non_cur_liab_due_within_1y,oth_cur_liab,lt_borrow,bonds_payable,lt_payable,specific_item_payable,provisions,deferred_tax_liab,oth_non_cur_liab,cap_stk,cap_rsrv,tsy_stk,surplus_rsrv,undistributed_profit,tot_cur_assets,tot_non_cur_assets,tot_cur_liab,tot_non_cur_liab,tot_liab,tot_equity",
                      start_date, end_date, "unit=1;rptType=1;Period=Q;Days=Alldays")

        # 更新cns_stock_basics
        for i in range(0, len(wdata.Times)):
            result = cns_balance_sheet.query.filter_by(trade_code=stock[0:6],the_date=wdata.Times[i]).first()
            if result is None:
                updata = cns_balance_sheet()
                updata.stock_code = stock[0:6]
                updata.the_date = wdata.Times[i]
                updata.sec_name = wdata.Data[0][i]
                updata.monetary_cap = wdata.Data[1][i]
                updata.tradable_fin_assets = wdata.Data[2][i]
                updata.notes_rcv = wdata.Data[3][i]
                updata.acct_rcv = wdata.Data[4][i]
                updata.prepay = wdata.Data[5][i]
                updata.int_rcv = wdata.Data[6][i]
                updata.dvd_rcv = wdata.Data[7][i]
                updata.inventories = wdata.Data[8][i]
                updata.non_cur_assets_due_within_1y=wdata.Data[9][i]
                updata.oth_cur_assets = wdata.Data[10][i]
                updata.fin_assets_avail_for_sale = wdata.Data[11][i]
                updata.held_to_mty_invest = wdata.Data[12][i]
                updata.long_term_rec = wdata.Data[13][i]
                updata.long_term_eqy_invest = wdata.Data[14][i]
                updata.invest_real_estate = wdata.Data[15][i]
                updata.fix_assets = wdata.Data[16][i]
                updata.const_in_prog = wdata.Data[17][i]
                updata.proj_matl = wdata.Data[18][i]
                updata.fix_assets_disp = wdata.Data[19][i]
                updata.productive_bio_assets = wdata.Data[20][i]
                updata.oil_and_natural_gas_assets = wdata.Data[21][i]
                updata.intang_assets = wdata.Data[22][i]
                updata.r_and_d_costs = wdata.Data[23][i]
                updata.goodwill = wdata.Data[24][i]
                updata.long_term_deferred_exp = wdata.Data[25][i]
                updata.deferred_tax_assets = wdata.Data[26][i]
                updata.oth_non_cur_assets = wdata.Data[27][i]
                updata.st_borrow = wdata.Data[28][i]
                updata.tradable_fin_liab = wdata.Data[29][i]
                updata.notes_payable = wdata.Data[30][i]
                updata.acct_payable = wdata.Data[31][i]
                updata.adv_from_cust = wdata.Data[32][i]
                updata.empl_ben_payable = wdata.Data[33][i]
                updata.taxes_surcharges_payable = wdata.Data[34][i]
                updata.int_payable = wdata.Data[35][i]
                updata.dvd_payable = wdata.Data[36][i]
                updata.oth_payable = wdata.Data[37][i]
                updata.non_cur_liab_due_within_1y = wdata.Data[38][i]
                updata.oth_cur_liab = wdata.Data[39][i]
                updata.lt_borrow = wdata.Data[40][i]
                updata.bonds_payable = wdata.Data[41][i]
                updata.lt_payable = wdata.Data[42][i]
                updata.specific_item_payable = wdata.Data[43][i]
                updata.provisions = wdata.Data[44][i]
                updata.deferred_tax_liab = wdata.Data[45][i]
                updata.oth_non_cur_liab = wdata.Data[46][i]
                updata.cap_stk = wdata.Data[47][i]
                updata.cap_rsrv = wdata.Data[48][i]
                updata.tsy_stk = wdata.Data[49][i]
                updata.surplus_rsrv = wdata.Data[50][i]
                updata.undistributed_profit = wdata.Data[51][i]
                updata.tot_cur_assets= wdata.Data[52][i]
                updata.tot_non_cur_assets= wdata.Data[53][i]
                updata.tot_cur_liab= wdata.Data[54][i]
                updata.tot_non_cur_liab= wdata.Data[55][i]
                updata.tot_liab= wdata.Data[56][i]
                updata.tot_equity= wdata.Data[57][i]
                db.session.add(updata)
            else:
                result.stock_code = stock[0:6]
                result.the_date = wdata.Times[i]
                result.sec_name = wdata.Data[0][i]
                result.monetary_cap = wdata.Data[1][i]
                result.tradable_fin_assets = wdata.Data[2][i]
                result.notes_rcv = wdata.Data[3][i]
                result.acct_rcv = wdata.Data[4][i]
                result.prepay = wdata.Data[5][i]
                result.int_rcv = wdata.Data[6][i]
                result.dvd_rcv = wdata.Data[7][i]
                result.inventories = wdata.Data[8][i]
                result.non_cur_assets_due_within_1y=wdata.Data[9][i]
                result.oth_cur_assets = wdata.Data[10][i]
                result.fin_assets_avail_for_sale = wdata.Data[11][i]
                result.held_to_mty_invest = wdata.Data[12][i]
                result.long_term_rec = wdata.Data[13][i]
                result.long_term_eqy_invest = wdata.Data[14][i]
                result.invest_real_estate = wdata.Data[15][i]
                result.fix_assets = wdata.Data[16][i]
                result.const_in_prog = wdata.Data[17][i]
                result.proj_matl = wdata.Data[18][i]
                result.fix_assets_disp = wdata.Data[19][i]
                result.productive_bio_assets = wdata.Data[20][i]
                result.oil_and_natural_gas_assets = wdata.Data[21][i]
                result.intang_assets = wdata.Data[22][i]
                result.r_and_d_costs = wdata.Data[23][i]
                result.goodwill = wdata.Data[24][i]
                result.long_term_deferred_exp = wdata.Data[25][i]
                result.deferred_tax_assets = wdata.Data[26][i]
                result.oth_non_cur_assets = wdata.Data[27][i]
                result.st_borrow = wdata.Data[28][i]
                result.tradable_fin_liab = wdata.Data[29][i]
                result.notes_payable = wdata.Data[30][i]
                result.acct_payable = wdata.Data[31][i]
                result.adv_from_cust = wdata.Data[32][i]
                result.empl_ben_payable = wdata.Data[33][i]
                result.taxes_surcharges_payable = wdata.Data[34][i]
                result.int_payable = wdata.Data[35][i]
                result.dvd_payable = wdata.Data[36][i]
                result.oth_payable = wdata.Data[37][i]
                result.non_cur_liab_due_within_1y = wdata.Data[38][i]
                result.oth_cur_liab = wdata.Data[39][i]
                result.lt_borrow = wdata.Data[40][i]
                result.bonds_payable = wdata.Data[41][i]
                result.lt_payable = wdata.Data[42][i]
                result.specific_item_payable = wdata.Data[43][i]
                result.provisions = wdata.Data[44][i]
                result.deferred_tax_liab = wdata.Data[45][i]
                result.oth_non_cur_liab = wdata.Data[46][i]
                result.cap_stk = wdata.Data[47][i]
                result.cap_rsrv = wdata.Data[48][i]
                result.tsy_stk = wdata.Data[49][i]
                result.surplus_rsrv = wdata.Data[50][i]
                result.undistributed_profit = wdata.Data[51][i]
                result.tot_cur_assets= wdata.Data[52][i]
                result.tot_non_cur_assets= wdata.Data[53][i]
                result.tot_cur_liab= wdata.Data[54][i]
                result.tot_non_cur_liab= wdata.Data[55][i]
                result.tot_liab= wdata.Data[56][i]
                result.tot_equity= wdata.Data[57][i]
    table_update= table_update_time.query.filter_by(table_name='cns_balance_sheet').first_or_404()
    table_update.last_update_time = Time.strftime('%Y-%m-%d', Time.localtime(Time.time()))
    db.session.commit()
    return wdata.Data

def first_upData_cns_income_statement():
    db_engine = create_engine('mysql://root:0000@localhost/cns_income_statement?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
    w.start();
     # 从company_list中获取股票列表#
    AllAStock = []
    results = company_list.query.all()
    for result in results:
        AllAStock.append( result.Wind_Code)
    # for stock in AllAStock:
    for i in range(0, 2):
        stock = AllAStock[i]
        result = company_list.query.filter_by(Code=stock[0:6]).first()
        start_date =  result.IPO_Date
        end_date = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
        wdata = w.wsd(stock, "sec_name,oper_rev,oper_cost,taxes_surcharges_ops,selling_dist_exp,gerl_admin_exp,fin_exp_is,impair_loss_assets,net_gain_chg_fv,net_invest_inc,opprofit,non_oper_rev,non_oper_exp,tot_profit,net_profit_is,eps_basic_is,eps_diluted_is,tax",
                       start_date,end_date, "unit=1;rptType=1;Period=Q;Days=Alldays")
        print(wdata.Data)
        # print(wdata.Data[1])
        # print(wdata.Data[2])
        # 更新cns_stock_basics
        for i in range(0, len(wdata.Times)):
            result = cns_income_statement.query.filter_by(trade_code=stock[0:6],the_date=wdata.Times[i]).first()
            if result is None:
                updata = cns_income_statement()
                updata.stock_code = stock[0:6]
                updata.the_date = wdata.Times[i]
                updata.sec_name = wdata.Data[0][i]
                updata.oper_rev = wdata.Data[1][i]
                updata.oper_cost = wdata.Data[2][i]
                updata.taxes_surcharges_ops = wdata.Data[3][i]
                updata.selling_dist_exp = wdata.Data[4][i]
                updata.gerl_admin_exp = wdata.Data[5][i]
                updata.fin_exp_is = wdata.Data[6][i]
                updata.impair_loss_assets = wdata.Data[7][i]
                updata.net_gain_chg_fv = wdata.Data[8][i]
                updata.net_invest_inc = wdata.Data[9][i]
                updata.opprofit = wdata.Data[10][i]
                updata.non_oper_rev = wdata.Data[11][i]
                updata.non_oper_exp = wdata.Data[12][i]
                updata.tax = wdata.Data[13][i]
                updata.tot_profit = wdata.Data[14][i]
                updata.net_profit_is = wdata.Data[15][i]
                updata.eps_basic_is = wdata.Data[16][i]
                updata.eps_diluted_is = wdata.Data[17][i]
                db.session.add(updata)
            else:
                result.stock_code = stock[0:6]
                result.the_date = wdata.Times[i]
                result.sec_name = wdata.Data[0][i]
                result.oper_rev = wdata.Data[1][i]
                result.oper_cost = wdata.Data[2][i]
                result.taxes_surcharges_ops = wdata.Data[3][i]
                result.selling_dist_exp = wdata.Data[4][i]
                result.gerl_admin_exp = wdata.Data[5][i]
                result.fin_exp_is = wdata.Data[6][i]
                result.impair_loss_assets = wdata.Data[7][i]
                result.net_gain_chg_fv = wdata.Data[8][i]
                result.net_invest_inc = wdata.Data[9][i]
                result.opprofit = wdata.Data[10][i]
                result.non_oper_rev = wdata.Data[11][i]
                result.non_oper_exp = wdata.Data[12][i]
                result.tax = wdata.Data[13][i]
                result.tot_profit = wdata.Data[14][i]
                result.net_profit_is = wdata.Data[15][i]
                result.eps_basic_is = wdata.Data[16][i]
                result.eps_diluted_is = wdata.Data[17][i]

    table_update= table_update_time.query.filter_by(table_name='cns_income_statement').first_or_404()
    table_update.last_update_time = Time.strftime('%Y-%m-%d', Time.localtime(Time.time()))
    db.session.commit()
    return wdata.Data

def first_upData_cns_statement_of_cash_flows():
    db_engine = create_engine('mysql://root:0000@localhost/cns_statement_of_cash_flows?charset=utf8')
    Session = sessionmaker(bind=db_engine)
    session = Session()
    w.start();
     # 从company_list中获取股票列表#
    AllAStock = []
    results = company_list.query.all()
    for result in results:
        AllAStock.append( result.Wind_Code)
    # for stock in AllAStock:
    for i in range(0, 2):
        stock = AllAStock[i]
        result = company_list.query.filter_by(Code=stock[0:6]).first()
        start_date =  result.IPO_Date
        end_date = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(Time.time()))
        wdata = w.wsd(stock,
                      "sec_name,cash_recp_sg_and_rs,recp_tax_rends,other_cash_recp_ral_oper_act,stot_cash_inflows_oper_act,cash_pay_goods_purch_serv_rec,cash_pay_beh_empl,pay_all_typ_tax,other_cash_pay_ral_oper_act,stot_cash_outflows_oper_act,net_cash_flows_oper_act,cash_recp_disp_withdrwl_invest,cash_recp_return_invest,net_cash_recp_disp_fiolta,other_cash_recp_ral_inv_act,stot_cash_inflows_inv_act,cash_pay_acq_const_fiolta,cash_paid_invest,other_cash_pay_ral_inv_act,stot_cash_outflows_inv_act,net_cash_flows_inv_act,cash_recp_cap_contrib,cash_recp_borrow,other_cash_recp_ral_fnc_act,stot_cash_inflows_fnc_act,cash_prepay_amt_borr,cash_pay_dist_dpcp_int_exp,other_cash_pay_ral_fnc_act,stot_cash_outflows_fnc_act,net_cash_flows_fnc_act,eff_fx_flu_cash,net_incr_cash_cash_equ_dm,cash_cash_equ_beg_period,cash_cash_equ_end_period,net_profit_cs,prov_depr_assets,depr_fa_coga_dpba,amort_intang_assets,amort_lt_deferred_exp,loss_disp_fiolta,loss_scr_fa,loss_fv_chg,fin_exp_cs,invest_loss,decr_deferred_inc_tax_assets,incr_deferred_inc_tax_liab,decr_inventories,decr_oper_payable,incr_oper_payable,others,im_net_cash_flows_oper_act,conv_debt_into_cap,conv_corp_bonds_due_within_1y,fa_fnc_leases,end_bal_cash,beg_bal_cash,end_bal_cash_equ,beg_bal_cash_equ,net_incr_cash_cash_equ_im",
                       start_date,end_date, "unit=1;rptType=1;Period=Q;Days=Alldays")
        print(wdata.Data)
        # print(wdata.Data[1])
        # print(wdata.Data[2])
        # 更新cns_stock_basics
        for i in range(0, len(wdata.Times)):
            result = cns_statement_of_cash_flows.query.filter_by(trade_code=stock[0:6],the_date=wdata.Times[i]).first()
            if result is None:
                updata = cns_statement_of_cash_flows()
                updata.stock_code = stock[0:6]
                updata.the_date = wdata.Times[i]
                updata.sec_name = wdata.Data[0][i]
                updata.cash_recp_sg_and_rs = wdata.Data[1][i]
                updata.recp_tax_rends = wdata.Data[2][i]
                updata.other_cash_recp_ral_oper_act= wdata.Data[3][i]
                updata.stot_cash_inflows_oper_act = wdata.Data[4][i]
                updata.cash_pay_goods_purch_serv_rec = wdata.Data[5][i]
                updata.cash_pay_beh_empl = wdata.Data[6][i]
                updata.pay_all_typ_tax = wdata.Data[7][i]
                updata.other_cash_pay_ral_oper_act = wdata.Data[8][i]
                updata.stot_cash_outflows_oper_act = wdata.Data[9][i]
                updata.net_cash_flows_oper_act = wdata.Data[10][i]
                updata.cash_recp_disp_withdrwl_invest = wdata.Data[11][i]
                updata.cash_recp_return_invest = wdata.Data[12][i]
                updata.net_cash_recp_disp_fiolta = wdata.Data[13][i]
                updata.other_cash_recp_ral_inv_act = wdata.Data[14][i]
                updata.stot_cash_inflows_inv_act = wdata.Data[15][i]
                updata.cash_pay_acq_const_fiolta = wdata.Data[16][i]
                updata.cash_paid_invest = wdata.Data[17][i]
                updata.other_cash_pay_ral_inv_act = wdata.Data[18][i]
                updata.stot_cash_outflows_inv_act = wdata.Data[19][i]
                updata.net_cash_flows_inv_act = wdata.Data[20][i]
                updata.cash_recp_cap_contrib = wdata.Data[21][i]
                updata.cash_recp_borrow = wdata.Data[22][i]
                updata.other_cash_recp_ral_fnc_act = wdata.Data[23][i]
                updata.stot_cash_inflows_fnc_act = wdata.Data[24][i]
                updata.cash_prepay_amt_borr = wdata.Data[25][i]
                updata.cash_pay_dist_dpcp_int_exp = wdata.Data[26][i]
                updata.other_cash_pay_ral_fnc_act = wdata.Data[27][i]
                updata.stot_cash_outflows_fnc_act = wdata.Data[28][i]
                updata.net_cash_flows_fnc_act = wdata.Data[29][i]
                updata.eff_fx_flu_cash = wdata.Data[30][i]
                updata.net_incr_cash_cash_equ_dm = wdata.Data[31][i]
                updata.cash_cash_equ_beg_period = wdata.Data[32][i]
                updata.cash_cash_equ_end_period = wdata.Data[33][i]
                updata.net_profit_cs = wdata.Data[34][i]
                updata.prov_depr_assets = wdata.Data[35][i]
                updata.depr_fa_coga_dpba = wdata.Data[36][i]
                updata.amort_intang_assets = wdata.Data[37][i]
                updata.amort_lt_deferred_exp = wdata.Data[38][i]
                updata.loss_disp_fiolta = wdata.Data[39][i]
                updata.loss_scr_fa	 = wdata.Data[40][i]
                updata.loss_fv_chg = wdata.Data[41][i]
                updata.fin_exp_cs = wdata.Data[42][i]
                updata.invest_loss = wdata.Data[43][i]
                updata.decr_deferred_inc_tax_assets = wdata.Data[44][i]
                updata.incr_deferred_inc_tax_liab = wdata.Data[45][i]
                updata.decr_inventories = wdata.Data[46][i]
                updata.decr_oper_payable = wdata.Data[47][i]
                updata.incr_oper_payable = wdata.Data[48][i]
                updata.others = wdata.Data[49][i]
                updata.im_net_cash_flows_oper_act = wdata.Data[50][i]
                updata.conv_debt_into_cap = wdata.Data[51][i]
                updata.conv_corp_bonds_due_within_1y= wdata.Data[52][i]
                updata.fa_fnc_leases = wdata.Data[53][i]
                updata.end_bal_cash = wdata.Data[54][i]
                updata.beg_bal_cash = wdata.Data[55][i]
                updata.end_bal_cash_equ = wdata.Data[56][i]
                updata.beg_bal_cash_equ = wdata.Data[57][i]
                updata.net_incr_cash_cash_equ_im = wdata.Data[58][i]
                db.session.add(updata)
            else:
                result.stock_code = stock[0:6]
                result.the_date = wdata.Times[i]
                result.sec_name = wdata.Data[0][i]
                result.cash_recp_sg_and_rs = wdata.Data[1][i]
                result.recp_tax_rends = wdata.Data[2][i]
                result.other_cash_recp_ral_oper_act= wdata.Data[3][i]
                result.stot_cash_inflows_oper_act = wdata.Data[4][i]
                result.cash_pay_goods_purch_serv_rec = wdata.Data[5][i]
                result.cash_pay_beh_empl = wdata.Data[6][i]
                result.pay_all_typ_tax = wdata.Data[7][i]
                result.other_cash_pay_ral_oper_act = wdata.Data[8][i]
                result.stot_cash_outflows_oper_act = wdata.Data[9][i]
                result.net_cash_flows_oper_act = wdata.Data[10][i]
                result.cash_recp_disp_withdrwl_invest = wdata.Data[11][i]
                result.cash_recp_return_invest = wdata.Data[12][i]
                result.net_cash_recp_disp_fiolta = wdata.Data[13][i]
                result.other_cash_recp_ral_inv_act = wdata.Data[14][i]
                result.stot_cash_inflows_inv_act = wdata.Data[15][i]
                result.cash_pay_acq_const_fiolta = wdata.Data[16][i]
                result.cash_paid_invest = wdata.Data[17][i]
                result.other_cash_pay_ral_inv_act = wdata.Data[18][i]
                result.stot_cash_outflows_inv_act = wdata.Data[19][i]
                result.net_cash_flows_inv_act = wdata.Data[20][i]
                result.cash_recp_cap_contrib = wdata.Data[21][i]
                result.cash_recp_borrow = wdata.Data[22][i]
                result.other_cash_recp_ral_fnc_act = wdata.Data[23][i]
                result.stot_cash_inflows_fnc_act = wdata.Data[24][i]
                result.cash_prepay_amt_borr = wdata.Data[25][i]
                result.cash_pay_dist_dpcp_int_exp = wdata.Data[26][i]
                result.other_cash_pay_ral_fnc_act = wdata.Data[27][i]
                result.stot_cash_outflows_fnc_act = wdata.Data[28][i]
                result.net_cash_flows_fnc_act = wdata.Data[29][i]
                result.eff_fx_flu_cash = wdata.Data[30][i]
                result.net_incr_cash_cash_equ_dm = wdata.Data[31][i]
                result.cash_cash_equ_beg_period = wdata.Data[32][i]
                result.cash_cash_equ_end_period = wdata.Data[33][i]
                result.net_profit_cs = wdata.Data[34][i]
                result.prov_depr_assets = wdata.Data[35][i]
                result.depr_fa_coga_dpba = wdata.Data[36][i]
                result.amort_intang_assets = wdata.Data[37][i]
                result.amort_lt_deferred_exp = wdata.Data[38][i]
                result.loss_disp_fiolta = wdata.Data[39][i]
                result.loss_scr_fa	 = wdata.Data[40][i]
                result.loss_fv_chg = wdata.Data[41][i]
                result.fin_exp_cs = wdata.Data[42][i]
                result.invest_loss = wdata.Data[43][i]
                result.decr_deferred_inc_tax_assets = wdata.Data[44][i]
                result.incr_deferred_inc_tax_liab = wdata.Data[45][i]
                result.decr_inventories = wdata.Data[46][i]
                result.decr_oper_payable = wdata.Data[47][i]
                result.incr_oper_payable = wdata.Data[48][i]
                result.others = wdata.Data[49][i]
                result.im_net_cash_flows_oper_act = wdata.Data[50][i]
                result.conv_debt_into_cap = wdata.Data[51][i]
                result.conv_corp_bonds_due_within_1y= wdata.Data[52][i]
                result.fa_fnc_leases = wdata.Data[53][i]
                result.end_bal_cash = wdata.Data[54][i]
                result.beg_bal_cash = wdata.Data[55][i]
                result.end_bal_cash_equ = wdata.Data[56][i]
                result.beg_bal_cash_equ = wdata.Data[57][i]
                result.net_incr_cash_cash_equ_im = wdata.Data[58][i]
    table_update= table_update_time.query.filter_by(table_name='cns_statement_of_cash_flows').first_or_404()
    table_update.last_update_time = Time.strftime('%Y-%m-%d', Time.localtime(Time.time()))
    db.session.commit()
    return wdata.Data
