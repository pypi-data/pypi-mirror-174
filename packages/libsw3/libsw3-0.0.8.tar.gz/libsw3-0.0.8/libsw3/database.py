#!/usr/bin/python3
# -*- coding: utf8 -*-

__all__=["c_oracle","c_database"]

import time,base64,sys,json,urllib.request,ssl,os,datetime
import libsw3 as sw3

class c_database(object):
    def __init__(self,sconn=""):
        self.sconn=sconn
        self.connected=False
    def convconn(self,ljc):
        if ljc.find("/")>0 or ljc.find("}")>0:
            return ljc
        dh,_=os.path.splitdrive(os.getcwd())
        fn1=os.path.join(dh,"/etc","dbconn.cfg")
        fn2=os.path.join(dh,"/etc","oraconn.cfg")
        if os.path.isfile(fn1):
            f=open(fn1)
        elif os.path.isfile(fn2):
            f=open(fn2)
        else:
            sw3.swexit(-1,"无法打开连接串配置文件%s或者%s" %(fn1,fn2))
        wjnr=f.readlines()
        f.close()
        for i in wjnr:
            s=i.split()
            if len(s)<2:
                continue
            if s[0]==ljc:
                return s[1]
        return ""

class c_mysql(c_database):
    def __init__(self,sconn=""):
        pass

class c_oracle(c_database):
    def __init__(self,sconn="",yslj=False,autocommit=False,raiseExp=True):
        global cx_Oracle
        import cx_Oracle
        self.BLOB=cx_Oracle.BLOB
        self.sconn=sconn
        self.connected=False
        self.autocommit=autocommit
        self.raiseExp = raiseExp
        (not yslj) and self.connect()
    def commit(self):
        try:
            self.conn.commit()
        except cx_Oracle.DatabaseError as e:
            print("commit异常：%s" % (e))
            error, = e.args
            if error.code==28 or error.code==1012:  #未登录或者被踢出
                self.connected=False
            if self.raiseExp:
                raise  # 往上层抛
    def connect(self,sconn=""):
        if sconn!="":
            self.sconn=sconn
            self.connected=False
        if self.connected:
            c=self.conn.cursor()
            try:
                c.execute("select 1 from dual")
            except cx_Oracle.DatabaseError as e:
                self.connected=False
                print("连接数据库异常：%s" % (e))
                if self.raiseExp:
                    raise  # 往上层抛
            else:
                return
        try:
            self.conn=cx_Oracle.connect(self.convconn(self.sconn))
        except cx_Oracle.DatabaseError as e:
            sw3.swexit(1,"数据库连接%s不成功" %(self.sconn))
            error, = e.args
            if self.raiseExp:
                raise  # 往上层抛
        else:
            self.c=self.conn.cursor()
            self.connected=True
    def droptable(self,tablename):
        if self.jg1("select count(1) from user_tables where table_name = upper('%s')" %(tablename))==1:
            self.c.execute("drop table %s purge" %(tablename))
    def execute(self,ssql,*args,**kwargs):
        (not self.connected) and self.connect()
        if not self.connected:
            return
        try:
            c=self.conn.cursor()
            c.execute(ssql,*args,**kwargs)
        except cx_Oracle.DatabaseError as e:
            self.connected=False
            print("oracle执行异常：%s" % (e))
            if self.raiseExp:
                raise  # 往上层抛
            return
        return c
    def execute2(self,ssql,**kwargs):
        (not self.connected) and self.connect()
        if not self.connected:
            return
        try:
            list = []
            c = self.conn.cursor()
            c.execute(ssql, kwargs)
            col = c.description
            for item in c.fetchall():
                dict = {}
                for i in range(len(col)):
                    dict[col[i][0]] = item[i]
                list.append(dict)
        except cx_Oracle.DatabaseError as e:
            self.connected = False
            print("oracle执行异常：%s" % (e))
            if self.raiseExp:
                raise  # 往上层抛
            return
        return list
    def inslist(self,tablename,data,collist=""):
        '''在表中直接插入数据'''
        (not self.connected) and self.connect()
        if collist=="":
            ssql="insert into %s values(" %(tablename)
        else:
            ssql="insert into %s (%s) values(" %(tablename,collist)
        for i in range(len(data)):
            ssql="%s:%d," %(ssql,i)
        ssql="%s)" %(ssql[:-1])
        c=self.conn.cursor()
        c.execute(ssql,data)
    def jg1(self,ssql,*args,**kwargs):
        '''根据sql返回1条结果'''
        (not self.connected) and self.connect()
        if not self.connected:
            return
        try:
            c=self.conn.cursor()
            c.execute(ssql,*args,**kwargs)
            jg=c.fetchone()
        except cx_Oracle.DatabaseError as e:
            self.connected=False
            print("oracle执行异常：%s" % (e))
            if self.raiseExp:
                raise  # 往上层抛
            return
        c.close()
        if jg==None:
            return
        if len(jg)==1:
            return jg[0]
        else:
            return jg
    def tablecreatesql(self,tablename): #获取表的生成脚本
        c=self.conn.cursor()
        c.callproc('DBMS_METADATA.SET_TRANSFORM_PARAM',(-1, 'TABLESPACE',False))
        c.callproc("DBMS_METADATA.SET_TRANSFORM_PARAM",(-1,'STORAGE',False))
        c.callproc("DBMS_METADATA.SET_TRANSFORM_PARAM",(-1,'SEGMENT_ATTRIBUTES',False))
        c.callproc("DBMS_METADATA.SET_TRANSFORM_PARAM",(-1,'PRETTY',False))
        ssql=self.jg1("SELECT dbms_metadata.get_ddl('TABLE','%s') FROM DUAL" %(tablename.upper())).read()
        ssql='create table "%s" %s' %(tablename.upper(),ssql[ssql.find("("):])
        return ssql
    def xg(self,ssql,**kwargs): #对数据库进行修改，可自动commit
        (not self.connected) and self.connect()
        if not self.connected:
            return
        try:
            c=self.conn.cursor()
            c.execute(ssql,kwargs)
            self.autocommit and self.commit()
        except cx_Oracle.DatabaseError as e:
            self.connected=False
            print("oracle执行异常：%s" %(e))
            if self.raiseExp:
                raise  # 往上层抛
            return
        return True
