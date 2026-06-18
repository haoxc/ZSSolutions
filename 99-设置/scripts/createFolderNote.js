module.exports = async (params) => {
    // 从 QuickAdd 获取核心 API
    const { quickAddApi, app, templater } = params;
    // 使用 new Notice() 需要确保 app 对象可用，这里它在 params 中

    // --- 配置区域 ---
    const TEMPLATE_PATH = "99-设置/zTemplates/--Normal/TPL-Folder Note.md"; 
    // ----------------

    // 1. 获取用户输入的文件夹名称
    const folderName = await quickAddApi.inputPrompt("输入新文件夹名称:");
    if (!folderName) return; // 如果用户取消，则停止执行

    // 2. 计算目标路径：确保在新文件夹和新笔记中使用相同的名称
    const activeFile = app.workspace.getActiveFile();
    const parentPath = activeFile ? activeFile.parent.path : "";
    
    const targetFolderPath = (parentPath === "/" || parentPath === "") ? folderName : `${parentPath}/${folderName}`;
    const targetNotePath = `${targetFolderPath}/${folderName}.md`;

    // 3. 创建文件夹（Obsidian API 会自动处理重复创建的错误）
    try {
        await app.vault.createFolder(targetFolderPath);
    } catch (err) {
        console.log(`文件夹 ${targetFolderPath} 可能已存在，跳过创建。`);
        // 注意：这里移除了旧的 quickAddApi.info() 调用
    }

    // 4. 读取并处理模板文件内容
    let processedTemplateContent = "";
    try {
        const templateFile = app.vault.getAbstractFileByPath(TEMPLATE_PATH);
        if (!templateFile) {
            throw new Error(`找不到模板文件: ${TEMPLATE_PATH}`);
        }
        console.debug("模版文件:"+ templateFile);
        const templateContents = await app.vault.read(templateFile);
        processedTemplateContent =templateContents;
        //processedTemplateContent = await templater.parseTemplate(templateContents);
    } catch (err) {
        // !!! 关键修复在这里 !!! 替换为 new Notice()
        new Notice(`无法应用模板: ${err.message}. 创建空笔记。`, 5000);
        processedTemplateContent = `# ${folderName}\n\n`;
    }
    
    // 5. 使用模板内容创建笔记
    
    console.debug("内容:"+processedTemplateContent);
    await app.vault.create(targetNotePath, processedTemplateContent);
    
    // 6. 打开新创建的笔记
    const newFile = app.vault.getAbstractFileByPath(targetNotePath);
    if (newFile) {
        await app.workspace.getLeaf().openFile(newFile);
    }
};
