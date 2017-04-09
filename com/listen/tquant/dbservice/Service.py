# -*- coding: utf-8 -*-

import pymysql
import configparser
import os
import traceback
import sys

from com.listen.tquant.utils.Utils import Utils

class DbService(object):
    def __init__(self):
        # charset必须设置为utf8，而不能为utf-8
        config = configparser.ConfigParser()
        os.chdir('../config')
        config.read('database.cfg')
        mysql_section = config['mysql']
        if mysql_section:
            host = mysql_section['db.host']
            port = int(mysql_section['db.port'])
            username = mysql_section['db.username']
            password = mysql_section['db.password']
            dbname = mysql_section['db.dbname']
            charset = mysql_section['db.charset']
            self.conn = pymysql.connect(host=host, port=port, user=username, passwd=password, db=dbname, charset=charset)
            self.conn.autocommit(True)
            self.cursor = self.conn.cursor()
        else:
            raise FileNotFoundError('database.cfg mysql section not found!!!')

    # 数据库连接关闭
    def close(self):
        if self.cursor:
            self.cursor.close()
            print('---> 关闭游标')
        if self.conn:
            self.conn.close()
            print('---> 关闭连接')

    # noinspection SpellCheckingInspection
    def insert(self, upsert_sql):
        try:
            if upsert_sql:
                self.cursor.execute(upsert_sql)
                return True
            else:
                return False
        except Exception:
            print('error sql:', upsert_sql)
            traceback.print_exc()

    # noinspection SpellCheckingInspection,PyBroadException
    def insert_many(self, upsert_sql_list):
        try:
            if upsert_sql_list:
                for upsert_sql in upsert_sql_list:
                    try:
                        self.cursor.execute(upsert_sql)
                    except Exception:
                        print('error sql:', upsert_sql)
                        self.conn.rollback()
                        traceback.print_exc()
                        return False
                return True
            return False
        except Exception:
            self.conn.rollback()
            traceback.print_exc()

    def query(self, query_sql):
        try:
            if query_sql:
                self.cursor.execute(query_sql)
                stock_tuple_tuple = self.cursor.fetchall()
                return stock_tuple_tuple
            else:
                return None
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type, exc_value, exc_traceback, 'sql error:', query_sql)
            return None

    def query_all_security_codes(self):
        sql = "select security_code, exchange_code " \
              "from tquant_security_info " \
              "where security_type = 'STOCK'"
        return self.query(sql)

    def get_calendar_max_the_date(self):
        """
        查询交易日表中最大交易日日期
        :return:
        """
        sql = "select max(the_date) max_the_date from tquant_calendar_info"
        the_date = self.query(sql)
        if the_date is not None and len(the_date) > 0:
            max_the_date = the_date[0][0]
            return max_the_date
        return None

    def get_batch_list_security_codes(self, batch_size):
        tuple_security_codes = self.query_all_security_codes()
        if tuple_security_codes is not None and len(tuple_security_codes) > 0:
            batch_list = []
            size = len(tuple_security_codes)
            # 分组后余数
            remainder = size % batch_size
            if remainder > 0:
                remainder = 1
            # 分组数，取整数，即批量的倍数
            multiple = size // batch_size
            total = remainder + multiple
            print('size:', size, 'batch:', batch_size, 'remainder:', remainder, 'multiple:', multiple, 'total:', total)
            i = 0
            while i < total:
                # 如果是最后一组，则取全量
                if i == total - 1:
                    temp_tuple = tuple_security_codes[i * batch_size:size]
                else:
                    temp_tuple = tuple_security_codes[i * batch_size:(i + 1) * batch_size]
                batch_list.append(temp_tuple)
                i += 1
            return batch_list
        return None

    def get_batch_list_except_security_codes(self):
        sql = "select c.security_code, c.exchange_code " \
              "from " \
              "( " \
              "select a.security_code, a.exchange_code, a.k_count, b.avg_count ," \
              "b.ma, (a.k_count-b.avg_count + 1) diff " \
              "from " \
              "( " \
              "select security_code, exchange_code, count(*) k_count " \
              "from tquant_stock_day_kline " \
              "group by security_code, exchange_code" \
              ") a " \
              "left join " \
              "( " \
              "select security_code, exchange_code, ma, count(*) avg_count " \
              "from tquant_stock_average_line " \
              "group by security_code, exchange_code, ma" \
              ") b " \
              "on a.security_code = b.security_code and b.exchange_code = a.exchange_code " \
              "having (a.k_count-b.avg_count + 1) != b.ma ) c " \
              "group by c.security_code, c.exchange_code "
        tuple_security_codes = self.query(sql)
        if tuple_security_codes is not None and len(tuple_security_codes) > 0:
            return tuple_security_codes
        return None

    def get_day_kline_except_security_codes(self):
        sql = "select security_code, exchange_code " \
              "from " \
              "( " \
              "select security_code, exchange_code " \
              "from tquant_stock_day_kline " \
              "where close is null or close <= 0 " \
              "or open is null or open <= 0 " \
              "or high <= 0 or high is null " \
              "or low <= 0 or low is null " \
              "group by security_code, exchange_code " \
              ") a"
        tuple_security_codes = self.query(sql)
        if tuple_security_codes is not None and len(tuple_security_codes) > 0:
            return tuple_security_codes
        return None

    def get_stock_day_kline(self, security_code, exchange_code, decline_ma_the_date):
        sql = "select the_date, close, amount, vol " \
              "from tquant_stock_day_kline " \
              "where security_code = {security_code} " \
              "and exchange_code = {exchange_code} "
        max_the_date = None
        if decline_ma_the_date is not None:
            sql += "and the_date >= {max_the_date} "
            max_the_date = decline_ma_the_date.strftime('%Y-%m-%d')
        sql += "order by the_date asc "
        sql = sql.format(security_code=Utils.quotes_surround(security_code),
                         exchange_code=Utils.quotes_surround(exchange_code),
                         max_the_date=Utils.quotes_surround(max_the_date)
                         )
        result = self.query(sql)
        return result

    def get_previous_average_line(self, ma, security_code, exchange_code, the_date):
        sql = "select close_pre_avg, amount_pre_avg, vol_pre_avg, price_pre_avg from tquant_stock_average_line " \
              "where security_code = {security_code} " \
              "and exchange_code = {exchange_code} and ma = {ma} and the_date < {the_date} " \
              "order by the_date desc limit 1".format(security_code=Utils.quotes_surround(security_code),
                                                      exchange_code=Utils.quotes_surround(exchange_code),
                                                      ma=ma,
                                                      the_date=Utils.quotes_surround(the_date.strftime('%Y-%m-%d')))
        previous_data = self.query(sql)
        return previous_data

    def get_average_line(self, ma, security_code, exchange_code, decline_ma_the_date):
        sql = "select the_date, " \
              "close_avg_chg, amount_avg_chg, vol_avg_chg, " \
              "price_avg_chg, amount_flow_chg, vol_flow_chg " \
              "from tquant_stock_average_line " \
              "where security_code = {security_code} " \
              "and exchange_code = {exchange_code} " \
              "and ma = {ma} " \
              "and close_avg_chg is not null " \
              "and amount_avg_chg is not null " \
              "and vol_avg_chg is not null " \
              "and price_avg_chg is not null " \
              "and amount_flow_chg is not null " \
              "and vol_flow_chg is not null "
        max_the_date = None
        if decline_ma_the_date is not None:
            sql += "and the_date >= {max_the_date} "
            max_the_date = decline_ma_the_date.strftime('%Y-%m-%d')
        sql += "order by the_date asc "
        sql = sql.format(security_code=Utils.quotes_surround(security_code),
                         exchange_code=Utils.quotes_surround(exchange_code),
                         max_the_date=Utils.quotes_surround(max_the_date),
                         ma=ma
                         )
        result = self.query(sql)
        return result

    def get_day_kline_max_the_date(self, security_code, exchange_code):
        sql = "select max(the_date) max_the_date from tquant_stock_day_kline " \
              "where security_code = {security_code} " \
              "and exchange_code = {exchange_code} " \
              "and previous_close is not null and close_change_percent is not null "
        the_date = self.query(sql.format(security_code=Utils.quotes_surround(security_code),
                                         exchange_code=Utils.quotes_surround(exchange_code)
                                        )
                              )
        if the_date:
            max_the_date = the_date[0][0]
            return max_the_date
        return None

    def get_average_line_max_the_date(self, ma, security_code, exchange_code):
        sql = "select max(the_date) max_the_date from tquant_stock_average_line " \
              "where security_code = {security_code} " \
              "and exchange_code = {exchange_code} " \
              "and ma = {ma}"
        the_date = self.query(sql.format(security_code=Utils.quotes_surround(security_code),
                                         exchange_code=Utils.quotes_surround(exchange_code),
                                         ma=ma
                                         )
                              )
        if the_date:
            max_the_date = the_date[0][0]
            return max_the_date
        return None

    def get_average_line_decline_max_the_date(self, ma, average_line_max_the_date):
        if average_line_max_the_date is not None and average_line_max_the_date != '':
            sql = "select min(the_date) from (select the_date from tquant_calendar_info " \
                  "where the_date <= {average_line_max_the_date} " \
                  "order by the_date desc limit {ma}) a"
        else:
            sql = "select min(the_date) from tquant_calendar_info"
        the_date = self.query(sql.format(average_line_max_the_date=Utils.quotes_surround(str(average_line_max_the_date)),
                                                   ma=ma)
                                        )
        if the_date is not None and the_date != '':
            decline_ma_the_date = the_date[0][0]
            return decline_ma_the_date
        return None

    def get_average_line_avg_max_the_date(self, ma, security_code, exchange_code):
        sql = "select max(the_date) max_the_date from tquant_stock_average_line " \
              "where security_code = {security_code} " \
              "and exchange_code = {exchange_code} " \
              "and ma = {ma} " \
              "and close_avg_chg is not null " \
              "and amount_avg_chg is not null " \
              "and vol_avg_chg is not null " \
              "and price_avg_chg is not null " \
              "and amount_flow_chg is not null " \
              "and vol_flow_chg is not null " \
              "and close_avg_chg_avg is not null " \
              "and amount_avg_chg_avg is not null " \
              "and vol_avg_chg_avg is not null " \
              "and price_avg_chg_avg is not null " \
              "and amount_flow_chg_avg is not null " \
              "and vol_flow_chg_avg is not null "
        the_date = self.query(sql.format(security_code=Utils.quotes_surround(security_code),
                                                   exchange_code=Utils.quotes_surround(exchange_code),
                                                   ma=ma
                                         )
                              )
        if the_date:
            max_the_date = the_date[0][0]
            return max_the_date
        return None

    def get_average_line_avg_decline_max_the_date(self, ma, average_line_avg_max_the_date):
        if average_line_avg_max_the_date is not None and average_line_avg_max_the_date != '':
            sql = "select min(the_date) from (select the_date from tquant_calendar_info " \
                  "where the_date <= {average_line_max_the_date} " \
                  "order by the_date desc limit {ma}) a"
        else:
            sql = "select min(the_date) from tquant_calendar_info"
        the_date = self.query(sql.format(average_line_max_the_date=Utils.quotes_surround(str(average_line_avg_max_the_date)),
                                         ma=ma
                                         )
                              )
        if the_date is not None and the_date != '':
            decline_ma_the_date = the_date[0][0]
            return decline_ma_the_date
        return None

    def get_day_kline_exist_max_the_date(self, security_code, exchange_code):
        sql = "select max(the_date) from tquant_stock_day_kline " \
              "where security_code = {security_code} and exchange_code = {exchange_code}"
        sql = sql.format(security_code=Utils.quotes_surround(security_code),
                         exchange_code=Utils.quotes_surround(exchange_code))
        the_date = self.query(sql)
        if the_date is not None and len(the_date) > 0:
            the_date = the_date[0][0]
            return the_date
        return None