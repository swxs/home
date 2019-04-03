### **简要描述：**

创建Column

### **请求URL：**

`/api/Column/create/`

### **请求方式：**

POST

### **类型：**

---
#### dtype
|值|原名|备注|
|:--|:--|:--|
|1|int||
|2|string||
|3|float||
|4|object||
|5|longtext||
|6|datetime||
|7|datetime_y||
|8|datetime_q||
|9|datetime_m||
|10|datetime_w||
|11|datetime_wd||
|12|datetime_d||

---
#### ttype
|值|原名|备注|
|:--|:--|:--|
|1|普通||
|2|计算||
|3|分组||


### **请求参数：**

|参数名|参数类型|备注|
|:--|:--|:--|
|col|str|真正的列名|
|realcol|str|原始未处理的列名|
|readablecol|str|展示的列名|
|worktable_id|objectid|工作表id|
|is_visible|boolean|是否可见|
|is_unique|boolean|是否唯一字段|
|dtype|int||
|ttype|int||
|expression|str|表达式|
|value_group_id_list|str|分组字段id|
