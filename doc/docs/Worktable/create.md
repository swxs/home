### **简要描述：**

创建Worktable

### **请求URL：**

`/api/Worktable/create/`

### **请求方式：**

POST

### **类型：**

---
#### engine
|值|原名|备注|
|:--|:--|:--|
|1|pandas引擎||
|2|Kylin引擎||

---
#### status
|值|原名|备注|
|:--|:--|:--|
|1|停用||
|2|启用||


### **请求参数：**

|参数名|参数类型|备注|
|:--|:--|:--|
|name|str|名称|
|datasource_id|objectid||
|engine|int||
|status|int||
|description|str|描述|
