### **简要描述：**

更新CacheChart

### **请求URL：**

`/api/bi/CacheChart/update/<CacheChart_id>/`

### **请求方式：**

PATCH

### **类型：**

---
#### ttype
|值|原名|备注|
|:--|:--|:--|
|1|图表展示||
|2|图表下载||
|3|筛选器展示||

---
#### status
|值|原名|备注|
|:--|:--|:--|
|1|未完成||
|2|成功||
|3|失败||


### **请求参数：**

|参数名|参数类型|备注|
|:--|:--|:--|
|chart_id|objectid||
|data_filter_id|objectid||
|ttype|int||
|key|str||
|value|str||
|status|int||

[返回目录](../base.md)