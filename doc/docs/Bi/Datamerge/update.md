### **简要描述：**

更新Datamerge

### **请求URL：**

`/api/bi/Datamerge/update/<Datamerge_id>/`

### **请求方式：**

PATCH

### **类型：**

---
#### how
|值|原名|备注|
|:--|:--|:--|
|1|内联||
|2|左联||
|3|右联||
|4|外联||
|5|上下||


### **请求参数：**

|参数名|参数类型|备注|
|:--|:--|:--|
|source_worktable_id|objectid||
|source_column_id_list|list||
|remote_worktable_id|objectid||
|remote_column_id_list|list||
|how|int||

[返回目录](../base.md)