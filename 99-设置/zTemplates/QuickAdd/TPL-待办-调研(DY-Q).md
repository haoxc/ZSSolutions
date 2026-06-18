---
tags: [工具]
description: //模板变量
type: note
create-date: 2025-11-15
---

<%*
//模板变量
const fileType = "调研"; //🚨修改当前主题
const fileType_c_abbr = "dy"; //🚨修改当前主题

//获取用户输入的主题（必填）
//const userTopic = await tp.system.prompt("请输入笔记主题（必填）:", "", true);
const userTopic= tp.file.title
if (!userTopic.trim()) {
  return; // 空主题时直接终止执行
}

const fileTitle = fileType +"-" + userTopic.trim();
await tp.file.rename(fileTitle);

//配置 Frontmatter
const title = userTopic;
const creationDate = tp.date.now("YYYY-MM-DD HH:mm");
const abbr= `"abbr:${fileType}/${userTopic}(${fileType_c_abbr}-)"`;
//const statusOptions = ["Draft", "Published", "In Review"];
//const status = await tp.system.suggester(statusOptions, statusOptions, false, "选择状态");


// 构建包含动态数据的 YAML 字符串
	//status: ${status}
const metaData = `---
title: ${title}
aliases: 
  - ${abbr}
tags: 
  - ${fileType}
  - hxc/TODO
created: ${creationDate}
description: 
---`;

// 将 YAML 字符串添加到笔记内容中
tR += metaData;

//动态生成内容生成内容和结构
const content = `
`;
tR+= content;
%>
## 内容
