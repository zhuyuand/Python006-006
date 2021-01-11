学习笔记
- 安装
• 注意系统平台
arch
cat /etc/etc/redhat-release
• 注意mysql的版本
（企业版、 社区版、 MariaDB）, 一般选择社区版
(无网)
https://downloads.mysql.com/archives/community/
解压
tar zxvf mysql-5.7.31-1.el7.x86_64.rpm-bundle.tar
安装
yum install *.rpm
• 注意安装后避免yum自动更新
注意： 有网环境使用  ， https://www.cnblogs.com/gnool/p/7689354.html
yum remove mysql57-connunity-release-el7-10.noarch  (删除:索引")
• 注意数据库的安全
启动mysql服务
systemctl start mysqld.service
systemctl status mysqld.service
systemctl enable mysqld.service
登陆数据库
grep 'password' /var/log/mysqld.log | head -1
mysql -uroot -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_PASSWORD123';
SHOW VARIABLES LIKE 'validate_password%';
set global validate_password_policy=0;
set global validate_password_length=6;
ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';
远程连接
use mysql;
select user,host from user;
grant all privileges on *.* to 'root'@'%' identified by '123456' with grant option;
database testdb  账号 testuser 密码 testpass
GRANT ALL PRIVILEGES ON testdb.* TO 'testuser'@'%' IDENTIFIED BY 'testpass';
flush privileges;
- 正确使用mysql字符集
show variables like '%character%';   查看字符集
show variables like 'collation_%';  查看校对规则
mysql中utf8不是UTF-8字符集，utf8最多占3个字节，而utf-8占4个字节
vim /etc/my.cnf
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/5.7/en/server-configuration-defaults.html
[client]
default-character-set=utf8mb4
[mysql]
default-character-set=utf8mb4
[mysqld]
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
interactive_timeout=28800 # 针对交互式连接超时时间
wait_timeout=28800 #  针对非交互式连接超时时间
max_connections=10000  # mysql最大连接数量
character_set_server=utf8mb4 # mysql基字符集设置
init_connect='SET NAMES utf8mb4'  # 服务器为每个连接的客户端执行的字符串
character_set_client_handshake=FALSE
collation_server=utf8mb4_unicode_ci  # 校对规则（存储表的时候需要大小写敏感），大小写不敏感 cs敏感
python多种方式连接数据库
pymysql
import pymysql
host = '106.15.187.5'
user = 'root'
password = '123456'
database = 'demo'
port = 3306
charset = 'utf8mb4'
connection = pymysql.connect(host=host, user=user, password=password, database=database, port=port, charset=charset)
try:
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = '''insert into users (email, password) VALUES (%s, %s)'''
        cursor.execute(sql, ('10', '1234'))
    connection.commit()
except Exception as e:
    print(f'fetch error {e}')
finally:
    connection.close()
sqlalchemy core
from sqlalchemy import create_engine, MetaData, Integer, String, Table, Column, ForeignKey
import pymysql
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
info = 'mysql+pymysql://root:123456@106.15.187.5:3306/demo'
# 开启调试模式
engine = create_engine(info, echo=True)
# 创建元数据
meta_data = MetaData(engine)
# 每张表必须有个关键字
book_table = Table(
    'book', meta_data,
    Column('id', Integer, primary_key=True),
    Column('name', String(20))
)
author_table = Table(
    'author', meta_data,
    Column('id', Integer, primary_key=True),
    Column('book_id', None, ForeignKey('book.id')),
    Column('author_name', String(20), nullable=False)
)
try:
    meta_data.create_all()
except Exception as e:
    print(f'fetch error {e}')
sqlalchemy orm
from sqlalchemy import create_engine, Table, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
engine = create_engine(
    'mysql+pymysql://root:123456@106.15.187.5:3306/demo',
    echo=True)
Base = declarative_base(engine)
class BookTable(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True)
class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    book_id = Column(None, ForeignKey('book.id'))
    # 唯一、不可为空
    name = Column(String(20), nullable=True, unique=True)
    create_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    updata_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
try:
    Base.metadata.create_all()
except Exception as e:
    print(f'fetch error {e}')
sqlalchemy 
from sqlalchemy import and_, or_, not_
from sqlalchemy import func
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base(engine)
class BookTable(Base):
    __tablename__ = 'book'
    book_id = Column(Integer(), primary_key=True)
    book_name = Column(String(20), index=True)
    def __repr__(self):
        return self.__class__.__name__ + \
            '(' + ', '.join(f'{k}: {v}' for k, v in self.__dict__.items() if not k.startswith('_')) + ')'
class AuthorTable(Base):
    __tablename__ = 'author'
    user_id = Column(Integer(), autoincrement=True, primary_key=True)
    author_name = Column('name', String(20), unique=True, nullable=True)
    create_on = Column(DateTime(), default=datetime.now)
    update_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
 # 新建表格
 try:
    Base.metadata.create_all()
 except Exception as e:
    print(f'fetch error {e}')
 from sqlalchemy.orm import sessionmaker
# 创建会话
SessionClass = sessionmaker(bind=engine)
session = SessionClass()
# 增
book = BookTable(book_name='一千零一夜')
print(book)
session.add(book)
# 查
print(session.query(BookTable.book_id).all())
# all first（取第一个， 没有none） one（必须一个） sclar(0/1个)
# 倒叙
res = session.query(BookTable.book_id, BookTable.book_name).order_by(BookTable.book_id.desc())
# 聚合函数
res = session.query(BookTable).filter(BookTable.book_id == 9).first()
res = session.query(func.count(BookTable.book_id)).first()
# 删除 
res = session.query(BookTable).filter(or_(BookTable.book_id == 1,
                                          BookTable.book_id == 9)).delete()
# 改
res = session.query(BookTable).filter(BookTable.book_id == 7).update({BookTable.book_name: '1234111'})
session.commit()
连接池
import pymysql
# pip3 install DBUtils
from dbutils.pooled_db import PooledDB
db_config = {
    "host": "server1",
    "port": 3306,
    "user": "testuser",
    "passwd": "testpass",
    "db": "testdb",
    "charset": "utf8mb4",
    "maxconnections": 0,   # 连接池允许的最大连接数
    "mincached": 4,        # 初始化时连接池中至少创建的空闲的链接,0表示不创建
    "maxcached": 0,        # 连接池中最多闲置的链接,0不限制
    "maxusage": 5,        # 每个连接最多被重复使用的次数,None表示无限制
    "blocking": True       # 连接池中如果没有可用连接后是否阻塞等待
    #  True 等待; False 不等待然后报错
}
spool = PooledDB(pymysql, **db_config)
conn = spool.connection()
cur = conn.cursor()
SQL = "select * from bookorm;"
cur.execute(SQL)
f = cur.fetchall()
print(f)
cur.close()
conn.close()
DDL
• 创建数据库
create database 数据库名;
• 切换数据库
use 数据库名字;
• 查看表名
show tables;
• 查看表的信息
show create table 表名；
• 简单描述表结构，字段类型
desc tabl_name;
（显示表结构，字段类型，主键，是否为空等属性，但不显示外键。）
DQL
书写循序
SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY …LIMIT
执行顺序
1. FROM 
2. where
3. GROUP BY
4. HAVING
5. SELEECT
6. ORDER BY
7. LIMIT
join关键连接
• 左连接 
select * from table1  left join table2 on table1.id = table2.id
类似
# 内连接
for i in table1:
    for j in table2:
        if i.id = j.id
            ...
for i in table1:
    for j in table2:
        if i.id = i.id:
            ... 
        else
            ... null
• 内连接
select * from table1  left join table2 on table1.id = table2.id
Select * from TableA a where Not Exists (Select * from TableB b where a.id=b.id and a.name=b.name);
1. Not Exists 用在where之后，且后面紧跟子查询语句（带括号）；
2. Not Exists(Exists) 并不关心子查询的结果具体是什么，只关心子查询有没有结果；
3. 这条语句的意思，把TableA的记录逐条代入到子查询，如果子查询结果集为空，说明不存在，那么这条TableA的记录出现在最终结果集，否则被排除；
• 用法：
Select * from TableA a where Not Exists (Select 1 from TableB);
这条语句子查询无论什么情况下都不为空，导致最终的结果集为空，因为TableA中每条记录对应的子查询都有结果集，表示都存在，所以最终结果集为空；
函数
sum(case when 80 <= score and score < 90 then 1 else 0 end) / count(*)
参考资料
https://kangroo.gitee.io/ajcg/#/table-ddl