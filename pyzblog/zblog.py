#-*- coding=utf-8 -*-

import pymysql
import phpserialize
import logging

class ZBlog(object):
    __TABLES = dict(ZBP_CATEGORY='category',
                    ZBP_COMMENT='comment',
                    ZBP_CONFIG='config', 
                    ZBP_MEMBER='member',
                    ZBP_MODULE='module',
                    ZBP_POST='post',
                    ZBP_TAG='tag',
                    ZBP_UPLOAD='upload')

    def __init__(self, user, password, db, host='localhost', charset='utf8', prefix='zbp_'):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    db=db,
                                    charset=charset)
        self.curs = self.conn.cursor()
        self.prefix = prefix
        for k in self.__TABLES:
            self.__setattr__(k, prefix + self.__TABLES[k])
    
    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_val, exec_tb):
        self.close()

    def close(self):
        self.conn.commit()
        
        self.curs.close()
        self.conn.close()

    def add_table(self, key, table_name, prefix=None):
        if prefix is None:
            prefix = self.prefix
        self.__setattr__(key, prefix + table_name)

    def each_content(self, table_name, fields, prefix=None):
        if prefix is None:
            prefix = self.prefix
        if isinstance(fields, str):
            fields = [fields]
        sql = 'SELECT ' + ', '.join(['`' + f + '`' for f in fields]) + 'FROM `%s`' % (prefix + table_name)
        self.curs.execute(sql)
        for row in self.curs.fetchall():
            yield row

    def all_contents(self, table_name, fields, prefix=None):
        return [r for r in self.each_content(table_name, fields, prefix)]

    def reload_system_config(self):
        sql = 'SELECT `conf_Value` FROM `%s` WHERE `conf_Name`=\'system\' LIMIT 1' % self.ZBP_CONFIG
        self.curs.execute(sql)
        sys_conf = self.curs.fetchone()
        sys_conf_dict = phpserialize.loads(sys_conf.encode())
        for k in sys_conf_dict:
            pass

