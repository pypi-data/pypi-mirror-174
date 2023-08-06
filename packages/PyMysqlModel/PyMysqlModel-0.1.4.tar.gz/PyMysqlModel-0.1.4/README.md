# PyMysqlModel

#### Description
基于 pymysql 的模型创建及使用 

内置 create、all、update、delete、filter、get 等常用方法

安装

```python
pip install PyMysqlModel
```

example 目录下为示例程序



# 使用介绍

#### 连接数据库

```python
from PyMysqlModel import Model

# database=None,
# user=None,
# password=None,
# host="localhost", 默认
# port=3306, 默认
# charset="utf8" 默认
# 连接数据库     指定   数据库名             用户   密码
student = Model(database="model_test",user="root",password=123)

# 读取目录下 settings 配置文件连接数据库
# 推荐
student = Model()

# 表名
table_name = "student_tb"

# 表字段
# 支持原生 sql 语句
student_table_fields = [
    "name varchar(20)",  # 一个字符串为一个字段
    "age int",
    "gender enum('男','女')",
    "phone varchar(11)",
]

# 连接表
# 当该表不存在时 则会自动创建该表
# 注意：当表存在时，但表字段不一致时，无法操作该表
# 推荐删除该表(注意备份表数据)，并重新运行，自动创建该表，
student.link_table(table_name,student_table_fields)
```

#### 添加数据 create

```python
# 添加数据
name = "张三1"
age = "18"
gender = 1
phone = "17613355211"

# 添加数据
# 接受一个 NULL 空 字段类型允
flag = student.create(name=name,age=age,gender=gender,phone=phone)

print(f"是否成功标志：{flag}")
# 添加成功 return True
# 添加失败 return False

# 关键字传参 位置随便
flag = student.create(age=age,name=name,phone=phone,gender=gender)

# 接受 NULL 空字段类型
# 不传，或传入一个 None
flag = student.create(name=name,gender=gender,phone=phone)
flag = student.create(name=name,age=None,gender=gender,phone=phone)

# 每张表 自带自增 id
# 可以指定
flag = student.create(id=66,name=name,age=age,gender=gender,phone=phone)
```

#### 修改数据 update

```python
from PyMysqlModel import Model

student = Model()

# 表名
table_name = "student_tb"
# 表字段
student_table_fields = [
    "name varchar(20)",  # 一个字符串为一个字段
    "age int",
    "gender enum('男','女')",
    "phone varchar(11)",
]

student.link_table(table_name,student_table_fields)


# 修改数据
# 修改后的数据
pk = 3
name = "李四"
age = 21
gender = 2
phone = "17613355211"

# 目前仅支持 根据 id 修改数据
# 传入要修改数据项的 id
# 其他字段为修改后的值
# id 字段为必传项

# 修改全部
flag = student.update(id=pk,name=name, age=age, gender=gender, phone=phone)
print(f"是否成功标志：{flag}")

# 修改 age 为 None
flag = student.update(id=pk,name=name, age=None, gender=gender, phone=phone)

# 修改部分字段
flag = student.update(id=pk,name=name, phone=phone)
```

#### 删除数据 delete

```python
# 删除数据
pk = 1
name = "张三"

# 根据 id 删除
num = student.delete(id=pk)
print(f"删除数据的条数：{num}")

# num： 返回删除数据的条数

# 根据条件删除
num = student.delete(id=pk,name=name)
```

#### 查询数据 all

```python
# 获取所有数据
data = student.all() # 查询全部
# result： 返回查询结果列表， list 类型

print(f"查询结果：{data}")
for i in data:
    print(i)


# 获取指定字段值
data = student.all("id","name") # 查询指定字段1

print(f"查询结果：{data}")
for i in data:
    print(i)
```

#### 查询数据 filter

```python
# 根据表字段进行过滤查询
name = "张三"
age = 18

# 查询条件为 and 关系
result = student.filter(name=name,age=age)
# result： 返回查询列表， list 类型
print(f"查询结果：{result}")
for i in result:
    print(i)

# 指定查询结果字段
result = student.filter("id","name",age=age)
print(f"查询结果：{result}")
```

#### 查询数据 get

```python
# 根据表字段进行过滤查询
name = "张三"
age = 18

# 查询条件为 and 关系
result = student.get(name=name,age=age)
# result： 返回第一条数据，dict 类型

print(f"查询结果：{result}")
```
