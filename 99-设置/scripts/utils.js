function getParentFolderFrontMatter(tp) {
    let frontmatter = null;
    // 1. 获取父目录路径 (true 代表相对库根目录的路径)
    const fullPath = tp.file.folder(true);
    console.debug("fullPath: " + fullPath);
	
	// 将字符串按 / 分割成数组，删除最后一个元素，再拼接回去
	let parentPath = fullPath.split("/").slice(0, -1).join("/");
	

    // 2. 提取文件夹名称
    // 处理根目录情况：如果 fullPath 为空，说明在根目录
    const folderName = parentPath ? parentPath.split("/").pop() : app.vault.getName();
    console.log("FolderName: " + folderName);


    // 3. 构建目标文件路径
    // 使用条件判断拼接路径，防止根目录出现 // 情况
    const targetPath = parentPath ? `${parentPath}/${folderName}.md` : `${folderName}.md`;
    
    const file = app.vault.getAbstractFileByPath(targetPath);
	console.log("targetPath: " + targetPath);

    if (file && file instanceof tp.obsidian.TFile) {
        // 4. 获取该文件的缓存
        const cache = app.metadataCache.getFileCache(file);
        frontmatter = cache?.frontmatter || null;
    } else {
        // 如果找不到文件，建议仅在调试时 log，或 Notice 提醒
        console.warn("未找到对应的 Folder Note: " + targetPath);
		new Notice("未找到对应的 Folder Note: " + targetPath);
    }
    return frontmatter;
} 

function getFolderNoteFrontMatter(tp) {
    let frontmatter = null;

    // 1. 获取父目录路径 (true 代表相对库根目录的路径)
    const fullPath = tp.file.folder(true);
    console.debug("fullPath: " + fullPath);

    // 2. 提取文件夹名称
    // 处理根目录情况：如果 fullPath 为空，说明在根目录
    const folderName = fullPath ? fullPath.split("/").pop() : app.vault.getName();
    console.log("FolderName: " + folderName);

    // 3. 构建目标文件路径
    // 使用条件判断拼接路径，防止根目录出现 // 情况
    const targetPath = fullPath ? `${fullPath}/${folderName}.md` : `${folderName}.md`;
    
    const file = app.vault.getAbstractFileByPath(targetPath);
	console.log("targetPath: " + targetPath);

    if (file && file instanceof tp.obsidian.TFile) {
        // 4. 获取该文件的缓存
        const cache = app.metadataCache.getFileCache(file);
        frontmatter = cache?.frontmatter || null;
        
        //const mtime = file.stat.mtime;
        //console.log("找到 Folder Note:", targetPath);
        //console.log("YAML信息:", frontmatter);
    } else {
        // 如果找不到文件，建议仅在调试时 log，或 Notice 提醒
        console.warn("未找到对应的 Folder Note: " + targetPath);
		new Notice("未找到对应的 Folder Note: " + targetPath);
    }

    return frontmatter;
}

module.exports = {
    getFolderNoteFrontMatter,
	getParentFolderFrontMatter
};