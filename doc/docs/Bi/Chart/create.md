### **简要描述：**

创建Chart

### **请求URL：**

`/api/bi/Chart/create/`

### **请求方式：**

POST

### **类型：**

---
#### ttype
|值|原名|备注|
|:--|:--|:--|
|1|柱状图||
|2|堆积柱状图||
|3|百分比堆积柱状图||
|4|条形图||
|5|堆积条形图||
|6|百分比堆积条形图||
|7|柱状折线图||
|8|堆积柱状折线图||
|9|折线图||
|10|折线阴影图||
|11|堆积折线图||
|12|饼图||
|13|雷达图||
|14|散点图||
|15|地图||
|16|仪表盘||
|17|指标卡||
|18|表格||
|19|富文本||
|20|私人定制||


### **请求参数：**

|参数名|参数类型|备注|
|:--|:--|:--|
|name|str||
|title|str||
|worktable_id|objectid||
|is_drilldown|boolean||
|ttype|int||
|range_region_type_id|objectid||
|base_option|dict||
|next_chart_id|objectid||
|prev_chart_id|objectid||
|custom_attr|dict||
|markline|list||

[返回目录](../base.md)

