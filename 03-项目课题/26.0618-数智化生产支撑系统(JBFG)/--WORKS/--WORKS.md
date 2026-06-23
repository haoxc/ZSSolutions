---
aliases:
tags:
description:
type:
ref-url:
create-date: 2026-06-23 09:33
---

> 自动汇聚 `课题-业务需求管理` 中标记 `#S06/todo/继远/接口确认` 的列表项。

```dataview
TABLE WITHOUT ID
	L.text AS 事项, 
    file.link AS 来源
FROM "-Workspaces/课题-业务需求管理"
FLATTEN file.lists AS L
WHERE   contains(L.tags, "S06/todo/继远/接口确认")
```
