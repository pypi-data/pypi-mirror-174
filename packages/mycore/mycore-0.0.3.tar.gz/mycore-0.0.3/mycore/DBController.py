import sqlite3
import logging
import time
import os
import json
import numpy as np


def project_root_path(project_name=None):
    """ 获取工程目录
    :param project_name:
    :return:
    """
    project_path = os.path.abspath(os.path.dirname(__file__))
    if project_path.find('\\') != -1: separator = '\\'  # Windows
    if project_path.find('/') != -1: separator = '/'  # Mac、Linux、Unix
    root_path = project_path[
                :project_path.find(f'{project_name}{separator}') + len(f'{project_name}{separator}')]
    return root_path


def now():
    return int(time.time() * 1000)


def logger(root, module):
    local_logger = logging.getLogger('') # 创建日志 logger 对象
    local_logger.setLevel(logging.INFO) # 设置日志等级
    ami_log = logging.FileHandler(f"{root}/{module}/logger/{module}.log", 'a', encoding='utf-8') # 追加写入文件
    ami_log.setLevel(logging.INFO) # 向文件输出日志级别
    formatter = logging.Formatter( # 向文件输出的日志信息格式
        '%(asctime)s - %(filename)s - line:%(lineno)d - %(levelname)s - %(message)s -%(process)s')
    ami_log.setFormatter(formatter)
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.INFO)
    console_log.setFormatter(formatter)
    local_logger.addHandler(ami_log) # 加载文件到logger对象中
    local_logger.addHandler(console_log)
    return local_logger


def create_file(dir):
    print(dir)
    with open(dir, 'w', encoding='utf-8') as new_file:
        print("")


class DBController():
    project = ""
    module = ""
    root = ""
    db_name = ""
    db_dir = ""
    log_dir = ""
    conn = None
    result = {}
    L = None
    isMeta = False

    def __init__(self, project, module, db_name):  ## 初始化DB_Controller
        self.project = project
        self.module = module
        self.db_name = db_name
        self.root = project_root_path(project)
        self.db_dir = f"{self.root}/{module}/data"

    def get_logger(self):
        self.log_dir = f"{self.root}/{self.module}/logger"
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
            create_file(f"{self.log_dir}/{self.module}.log")
        else:
            self.L = logger(self.root, self.module)

    def create_connection(self):
        """ 连接数据库
        :param name: 数据库名称
        :return: True or False
        """
        try:
            if not os.path.exists(self.db_dir):
                os.mkdir(self.db_dir)
                create_file(f"{self.db_dir}/{self.db_name}.db")
            self.conn = sqlite3.connect(f"{self.db_dir}/{self.db_name}.db", timeout=10)
            self.init_all()
            self.L.info(f"database {self.db_name} is connected successfully on {now()}")
        except Exception as e:
            self.L.error(e)
            return False
        finally:
            return True

    def init_all(self):
        """ 初始化元数据表
        :return:
        """
        try:
            tables = self.query_tables()
            if tables is None or not tables:
                self.create_metatable()
            self.isMeta = True if 'Metadata' in self.query_tables() else False
            if not self.isMeta:
                self.create_metatable()
            self.L = self.get_logger()
        except Exception as e:
            self.L.error(e)
            return False
        finally:
            return True

    def query_tables(self):
        """ 查询数据库下所有的表
        :return:
        """
        try:
            cur = self.conn.cursor()
            cur.execute(f"select name from sqlite_master where type='table' order by name")
            result = cur.fetchall()
            return [x[0] for x in result]
        except Exception as e:
            self.L.error(e)

    def create_metatable(self):
        """ 创建元数据表
        :return:
        """
        try:
            cursor_ins = self.conn.cursor()
            exe_str = f"CREATE TABLE IF NOT EXISTS Metadata " \
                      f"(id integer PRIMARY KEY AUTOINCREMENT NOT NULL," \
                      f" tablename text UNIQUE, field_list text, type_list text," \
                      f" size_list text, memo text, cretime Integer )"
            cursor_ins.execute(exe_str)
            self.L.info(f"Metatable of {self.db_name} is create successful at {now()}")
            cursor_ins.close()
        except Exception as e:
            self.L.error(e)
            return False
        finally:
            self.conn.commit()
            return True

    def create_table(self, table_name, field_list=None, type_list=None, size_list=None):
        """ 创建数据库表 自动增加主键id
        :param size_list:
        :param type_list:
        :param field_list:
        :param table_name: 表名称
        :return: True or False
        """
        try:
            meta_list = ["id", "tablename", "field_list", "type_list", "size_list", "memo", "cretime"]
            cursor_ins = self.conn.cursor()
            cdt_list = []
            for i, field in enumerate(field_list):
                cdt_list.append(f" {field_list[i]} {type_list[i]} {size_list[i]}")
            exe_str = f"CREATE TABLE IF NOT EXISTS '{table_name}' " \
                      f"(id integer PRIMARY KEY AUTOINCREMENT NOT NULL, {','.join(cdt_list)} )"
            meta_exe = f" INSERT INTO Metadata ({','.join(meta_list)} ) VALUES " \
                       f"(NULL, '{table_name}', '{json.dumps(field_list)}', '{json.dumps(type_list)}', " \
                       f"'{json.dumps(size_list)}', '', {now()} )"
            cursor_ins.execute(meta_exe)
            cursor_ins.execute(exe_str)
            self.L.info(f"table {table_name} of {self.db_name} is create successful at {now()}")
            cursor_ins.close()
        except Exception as e:
            self.L.error(e)
            return False
        finally:
            self.conn.commit()
            return True

    def alter_table_column(self, name, field_list, type_list):
        """ 已有表基础上增加列
        :param name:
        :param field_list:
        :param type_list:
        :return:
        """
        try:
            cursor_ins = self.conn.cursor()
            field_str = []
            for i, x in enumerate(field_list):
                field_str.append(f"{field_list[i]} {type_list[i]}")
            exe_sql = f"ALTER TABLE '{name}' add {','.join(field_str)}"
            cursor_ins.execute(exe_sql)
            self.L.info(f"table {name} executes a sql {exe_sql}")
            cursor_ins.close()
        except Exception as e:
            self.L.error(e)
        finally:
            self.conn.commit()
            return True

    def delete_table(self, table_name):
        """ 删除数据库表
        :param table_name: 表名称
        :return: True or False
        """
        try:
            cursor_ins = self.conn.cursor()
            exe_sql = f"DROP TABLE '{table_name}'"
            cursor_ins.execute(exe_sql)
            self.L.info(f"table {table_name} of {self.db_name} is drop successfully at {now()}")
            cursor_ins.close()
        except Exception as e:
            self.L.error(e)
            return False
        finally:
            self.conn.commit()
            return True

    def query_items(self, name, cdt_fields=None, cdt_vals=None):
        """ 查询记录
        :param cdt_vals: 查询条件列表
        :param cdt_fields: 查询字段列表
        :param name: 表名称
        :return: 查询到的集合 (后续考虑给定size)
        """
        try:
            cursor_ins = self.conn.cursor()
            exe_sql = f"SELECT * FROM '{name}' "
            cds_list = []
            for i, x in enumerate(cdt_fields):
                if "<" in str(cdt_vals[i]) or ">" in str(cdt_vals[i]) or "=" in str(cdt_vals[i]) or "!=" in str(
                        cdt_vals[i]):
                    cds_list.append(f" {cdt_fields[i]}{cdt_vals[i]} ")
                else:
                    cds_list.append(f" {cdt_fields[i]} LIKE '%{cdt_vals[i]}%' ")
            cds_sql = f" WHERE {'AND'.join(cds_list)}"
            # print(exe_sql + cds_sql)
            cursor_ins.execute(exe_sql + cds_sql)
            self.result = cursor_ins.fetchall()
            cursor_ins.close()
            return self.result
        except Exception as e:
            self.L.error(e)

    def query_page_items(self, name, cdc_fields=None, cdc_vals=None, limit=0, offset=0):
        """ 查询记录
        :param offset:
        :param limit:
        :param cdc_vals:
        :param name: 表名称
        :param cdc_fields: 查询字段列表
        :return: 查询到的集合 (后续考虑给定size)
        """
        cursor_ins = self.conn.cursor()
        result = {}
        try:
            exe_sql = f"SELECT * FROM '{name}' "
            cds_sql = " WHERE " if len(cdc_fields) > 0 else " "
            for i, x in enumerate(cdc_fields):
                if "<" in str(cdc_vals[i]) or ">" in str(cdc_vals[i]) or "=" in str(cdc_vals[i]) or "!=" in str(
                        cdc_vals[i]):
                    cds_sql += (" AND " if i > 0 else "" + f" {cdc_fields[i]} {cdc_vals[i]}")
                else:
                    cds_sql += (" AND " if i > 0 else "" + f" {cdc_fields[i]} LIKE '%{cdc_vals[i]}%'")
            appendix = f" LIMIT {limit} OFFSET {offset}"
            # print(exe_sql + cds_sql + appendix)
            cursor_ins.execute(exe_sql + cds_sql + appendix)
            # L.info('table ' + name + ' executes a query: ' + exe_sql + cds_sql)
            result = cursor_ins.fetchall()
        except Exception as e:
            self.L.error(e)
        finally:
            cursor_ins.close()
            return result

    def query_items_json(self, name, cdc_fields=None, cdc_vals=None):
        cursor_ins = self.conn.cursor()
        result_all = []
        try:
            val_data = self.query_items(name, cdc_fields, cdc_vals)
            fld_data = self.query_items("Metadata", ["tablename"], [f"='{name}'"])
            if len(fld_data) > 0 and len(val_data) > 0:
                fld_list = json.loads(fld_data[0][2])
                for i in range(len(val_data)):
                    result = {}
                    val_list = val_data[i]
                    for j, item in enumerate(fld_list):
                        result[fld_list[j]] = val_list[j + 1]
                    result["id"] = val_list[0]
                    result_all.append(result)
            # L.info('table ' + name + ' executes a query and return json.......... ')
        except Exception as e:
            self.L.error(e)
        finally:
            cursor_ins.close()
            return result_all

    def insert_item(self, name, value_list):
        """ 插入一条记录
        :param name: 表名称
        :param field_list: 表字段
        :param value_list: 表数据
        :return: True or False
        """
        try:
            cursor_ins = self.conn.cursor()
            exe_sql = f"INSERT INTO '{name}' VALUES (NULL, {','.join(['?' if x == 0.0 else x for x in np.zeros(len(value_list))])})"
            cursor_ins.execute(exe_sql, value_list)
            retId = cursor_ins.lastrowid
            self.L.info(f"table {name} inserts and value with id = {retId}")
            cursor_ins.close()
        except Exception as e:
            self.L.error(e)
            return -1
        finally:
            self.conn.commit()
            return retId

    def insert_item_retjson(self, name, value_list):
        """ 插入一条记录，返回json对象
        :param name: 表名称
        :param value_list: 表数据
        :return: True or False
        """
        local_result = {}
        try:
            cursor_ins = self.conn.cursor()
            exe_sql = f"INSERT INTO {name} VALUES (NULL, {','.join(['?' if x == 0.0 else x for x in np.zeros(len(value_list))])})"
            cursor_ins.execute(exe_sql, value_list)
            field_list = json.loads(
                cursor_ins.execute(f"SELECT * FROM Metadata WHERE tablename = '{name}'").fetchall()[0][2])
            local_result["id"] = cursor_ins.lastrowid
            for i, x in enumerate(field_list):
                local_result[field_list[i]] = value_list[i]
            self.L.info(f"table {name} inserts value with id = {cursor_ins.lastrowid}")
            cursor_ins.close()
        except Exception as e:
            self.L.error(e)
        finally:
            self.conn.commit()
            return local_result

    def insert_many_items(self, name, data_list):
        """ 插入多条记录
        :param name:
        :param data_list:
        :return:
        """
        try:
            cursor_ins = self.conn.cursor()
            fields = self.field_list if name == "Metadata" else json.loads(
                self.query_items("Metadata", ["tablename"], [f"='{name}'"])[0][2])
            exe_sql = f"INSERT INTO '{name}' (id, {','.join(fields)} ) VALUES " \
                      f"(NULL, {','.join(['?' if x == 0.0 else x for x in np.zeros(len(fields))])})"
            # print(exe_sql)
            cursor_ins.executemany(exe_sql, data_list)
            self.L.info(f"table {name} inserts many values with last id is {cursor_ins.lastrowid}")
            cursor_ins.close()
        except Exception as e:
            self.L.error(e)
            return False
        finally:
            self.conn.commit()
            return True

    def update_items(self, name, update_fields, value_list, cdt_fields, cdt_vals):
        try:
            cursor_ins = self.conn.cursor()
            upd_list, cdt_list = [], []
            for i, x in enumerate(update_fields):
                if x != 'id':
                    upd_list.append(f"{update_fields[i]} = '{str(value_list[i])}'")
            for i, x in enumerate(cdt_list):
                if "<" in str(cdt_vals[i]) or ">" in str(cdt_vals[i]) or "=" in str(cdt_vals[i]) or "!=" in str(
                        cdt_vals[i]):
                    cdt_list.append(f" {cdt_fields[i]}{cdt_vals[i]} ")
                else:
                    cdt_list.append(f" {cdt_fields[i]} LIKE '%{cdt_vals[i]}%' ")
            exe_sql = f"UPDATE '{name}' SET {' AND '.join(upd_list)} WHERE {' AND '.join(cdt_list)}"
            # print(exe_sql)
            cursor_ins.execute(exe_sql)
            self.L.info(f"table {name} executes an update {exe_sql}")
            cursor_ins.close()
        except Exception as e:
            self.L.error(e)
            return False
        finally:
            self.conn.commit()
            return True

    def update_items_retjson(self, name, json_data):
        try:
            cursor_ins = self.conn.cursor()
            update_fields, value_list = list(json_data.keys()), list(json_data.values())
            exe_sql, cds_sql = f"UPDATE '{name}' SET ", f" WHERE id = {json_data['id']} " if len(value_list) > 0 else " "
            cds_list = []
            for i, x in enumerate(update_fields):
                if x != 'id':
                    cds_list.append(f"{update_fields[i]} = '{str(value_list[i])}'")
            upd_sql = f"{','.join(cds_list)}"
            cursor_ins.execute(exe_sql + upd_sql + cds_sql)
            update_val = cursor_ins.execute(f"SELECT * FROM '{name}' {cds_sql}").fetchall()[0]
            update_col_list = [d[0] for d in cursor_ins.description]
            self.result = dict(zip(update_col_list, update_val))
            self.L.info(f"table {name} executes an update {exe_sql + upd_sql + cds_sql}")
        except Exception as e:
            self.L.error(e)
        finally:
            return self.result

    def delete_items(self, name, delete_fields=None, value_list=None):
        try:
            cursor_ins = self.conn.cursor()
            dlt_list = []
            for i, x in enumerate(delete_fields):
                if "<" in str(value_list[i]) or ">" in str(value_list[i]) or "=" in str(value_list[i]) or "!=" in str(
                        value_list[i]):
                    dlt_list.append(f" {delete_fields[i]}{value_list[i]} ")
                else:
                    dlt_list.append(f" {delete_fields[i]} LIKE '%{value_list[i]}%' ")
            dlt_sql = f"WHERE {' AND '.join(dlt_list)}" if len(delete_fields) > 0 else ""
            exe_sql = f"DELETE FROM '{name}' {dlt_sql}"
            cursor_ins.execute(exe_sql)
            self.L.info(f"table {name} executes an delete {exe_sql}")
            cursor_ins.close()
        except Exception as e:
            self.L.error(e)
            return False
        finally:
            self.conn.commit()
            return True
