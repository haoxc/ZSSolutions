---
aliases:
tags:
description:
type:
ref-url:
create-date: 2026-06-23 09:33
---

> 自动汇聚 `20-解决方案` 中标记 `#PJX/JBFG/todo` 的列表项。

```dataview
TABLE WITHOUT ID
	L.text AS 事项, 
    file.link AS 来源
FROM "03-项目课题/26.0618-数智化生产支撑系统(JBFG)/20-解决方案/方案产出-V5"
FLATTEN file.lists AS L
WHERE   contains(L.tags, "PJX/JBFG/todo")
```
