---
tags: [工具]
description: //-------------------------------------------
type: note
create-date: 2026-03-01
---

<%*
//-------------------------------------------
// 实践指南: 
// 1. 确保变量定义统一 (aspectName)
// 2. 使用 Templater 原生日期函数
//-------------------------------------------
    
const aspectName = "学习笔记";  
const aspectPINYIN = "xxbj";  


// 1. 确认笔记标题
let originalTitle = tp.file.title.trim();
let subject = originalTitle;
const defaultNames = ["未命名", "untitled", "无标题"];

if (!originalTitle || defaultNames.includes(originalTitle.toLowerCase())) {
     subject = await tp.system.prompt("请输入笔记主题:", "", true);
     if (!subject) return; // 用户取消则退出
} else if (originalTitle.includes("-")) {
     // 提取横杠后的内容或处理逻辑
     subject = originalTitle.split("-").pop(); 
}

// 2. 获取当前日期 (YYMMDD 格式)
const dateString = tp.date.now("YYMMDD");

// 3. 获取领域并确定新文件名
let domainId = await tp.system.prompt("请输入领域代码 (如: ART, MATH):", "", true) || "";
let newFileName = `${aspectName}(${dateString})-${subject}`;

// 执行重命名
if (tp.file.title !== newFileName) {
    await tp.file.rename(newFileName);
}

try {
    // 4. 配置 Frontmatter
    let yaml = `---\n`;
    yaml += `aliases:\n`;
    
    // 别名逻辑
    if (domainId) {
        yaml += `  - "${aspectName}(${aspectPINYIN})://${domainId}/${subject}"\n`;
    }
    //yaml += `  - "${aspectName}:${subject}"\n`;
    
    // 元信息
    yaml += `domain: "${domainId}"\n`;
    yaml += `category: "${aspectName}"\n`;
    yaml += `tags:\n`;
    if (domainId) {
        yaml += `  - ${aspectName}/${domainId}\n`;    
    }
    else {
        yaml += `  - ${aspectName}\n`;
    }
    
    yaml += `description: ""\n`;
    yaml += `created: ${tp.date.now("YYYY-MM-DD HH:mm")}\n`;
    yaml += `---\n`;

    tR += yaml;

    // 5. 动态生成正文结构
    tR += `\n## 内容\n- \n`;

} catch (e) {
    console.error("生成 YAML 时出错:", e);
    new Notice("YAML 生成失败，请检查控制台");
}
%>
