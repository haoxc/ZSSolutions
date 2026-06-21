// Second pass: fix remaining ASCII blocks that didn't match in first pass
const fs = require('fs');
const file = process.argv[2];
let content = fs.readFileSync(file, 'utf-8');
let lines = content.split('\n');

const remainingMap = new Map();

function add(key, type, ...codeLines) {
  const block = ['```' + type, ...codeLines, '```'];
  remainingMap.set(key, block);
}

// Physical deployment (first line: "中心云（集团侧）")
add('中心云（集团侧）', 'mermaid',
'flowchart TB',
'    subgraph 中心云["中心云（集团侧）"]',
'    GPU["GPU 集群<br/>AI 训练"]',
'    BD["大数据集群<br/>ClickHouse/Postgres"]',
'    DASH["全局驾驶舱"]',
'    end',
'    subgraph 边缘["场站边缘（冀北基地）"]',
'    direction LR',
'    Z1["安全I区·控制区<br/>GOOSE暂态≤100ms<br/>防误保护·本地兜底"]',
'    Z2["安全II区·非控生产区<br/>IEC104实时采集<br/>Redis缓存·GPU边缘推理<br/>AGC/AVC·断网自持≥2h"]',
'    Z3["安全III区·管理信息区<br/>三维Web门户<br/>工单/报表/大屏"]',
'    end',
'    中心云 -.广域网4G/5G/专线.-> 边缘',
'    Z1 -->|正向隔离装置·物理单向| Z2',
'    Z2 -->|防火墙| Z3',
'    边缘 --> DEV["设备层：风机SCADA/光伏监控/储能EMS/SVG升压站/摄像头/无人机"]',
'    style Z1 fill:#c00000,color:#fff',
'    style Z2 fill:#ed7d31,color:#fff',
'    style Z3 fill:#1f4e79,color:#fff'
);

// AI engine (first line contains "边缘端（场站 II 区 GPU）")
add('边缘端（场站 II 区 GPU）', 'mermaid',
'flowchart LR',
'    subgraph 边缘["边缘端·场站II区GPU"]',
'    E1["实时CV推理"]',
'    E2["告警生成"]',
'    E3["边缘模型热更新"]',
'    end',
'    subgraph 云["云端·中心云GPU集群"]',
'    C1["模型训练/微调"]',
'    C2["版本管理+AB测试"]',
'    C3["数据集管理"]',
'    end',
'    subgraph 业务["业务端·III区运维门户"]',
'    B1["人工复核"]',
'    B2["标注反馈"]',
'    B3["闭环追踪"]',
'    end',
'    边缘 <-->|USDF标准API<br/>gRPC同步/Kafka异步| 云',
'    云 <--> 业务',
'    style 边缘 fill:#ed7d31,color:#fff',
'    style 云 fill:#1f4e79,color:#fff',
'    style 业务 fill:#2e7d32,color:#fff'
);

// fig4-0: 五大业务子系统
add('五大业务子系统', 'mermaid',
'flowchart TB',
'    USDF["数字孪生底座 USDF"]',
'    USDF --> F1["F1 一体化场站【建】<br/>三维建模·数据接入·低代码组态"]',
'    USDF --> F2["F2 协同优化【控】<br/>有功无功协同·暂态控制·三道防误"]',
'    USDF --> F3["F3 透明场站【评】<br/>并网性能·发电性能·跟构网对比"]',
'    F1 --> BUS{统一数据总线}',
'    F2 --> BUS',
'    F3 --> BUS',
'    BUS --> F4["F4 智能运维【检】<br/>升压站·光伏·线路·储能 AI巡检"]',
'    BUS --> F5["F5 数字运维【管】<br/>360°监控·智能诊断·运维门户"]',
'    F4 --> LOOP["闭环反馈"]',
'    F5 --> LOOP',
'    LOOP -.预测性维护驱动.-> USDF',
'    style USDF fill:#1f4e79,color:#fff',
'    style BUS fill:#ed7d31,color:#fff',
'    style LOOP fill:#2e7d32,color:#fff'
);

// Alert-to-workorder sequence
add('告警→工单闭环', 'mermaid',
'sequenceDiagram',
'    participant AI as AI引擎/规则引擎',
'    participant WO as 工单中心',
'    participant OP as 运维人员',
'    participant RV as 审核人',
'    AI->>WO: 告警触发（等级+设备+图像）',
'    WO->>OP: 自动派单（类型+班组+时限）',
'    OP->>OP: 现场处置（拍照+记录）',
'    OP->>WO: 结果回传（处置结果+图像）',
'    WO->>RV: 提交待审核',
'    RV->>RV: 复核+修正（不覆盖原始数据）',
'    RV->>WO: 审核通过',
'    WO->>WO: 关闭归档（全流程日志入库）'
);

// Risk heatmap (Vega-Lite) - use substring that works with both × and x
add('风险热力图', 'vega-lite',
'{',
'  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",',
'  "title": "风险分布热力图（数字=风险项数）",',
'  "data": {"values": [',
'    {"维度": "技术风险", "等级": "阻断", "数量": 2},',
'    {"维度": "技术风险", "等级": "高", "数量": 5},',
'    {"维度": "技术风险", "等级": "低", "数量": 1},',
'    {"维度": "业务风险", "等级": "阻断", "数量": 2},',
'    {"维度": "业务风险", "等级": "高", "数量": 3},',
'    {"维度": "业务风险", "等级": "低", "数量": 0},',
'    {"维度": "实施风险", "等级": "阻断", "数量": 1},',
'    {"维度": "实施风险", "等级": "高", "数量": 3},',
'    {"维度": "实施风险", "等级": "低", "数量": 1}',
'  ]},',
'  "mark": "rect",',
'  "encoding": {',
'    "x": {"field": "维度", "type": "nominal", "axis": {"title": null, "labelAngle": 0}},',
'    "y": {"field": "等级", "type": "nominal", "sort": ["阻断","高","低"], "axis": {"title": null}},',
'    "color": {"field": "数量", "type": "quantitative", "scale": {"scheme": "reds"}},',
'    "tooltip": [{"field": "维度"}, {"field": "等级"}, {"field": "数量"}]',
'  }',
'}'
);

// Process
const newLines = [];
let i = 0;
let replacedCount = 0;

while (i < lines.length) {
  const line = lines[i];

  if (line.trim() === '```' && (i + 1 < lines.length) &&
      !lines[i + 1].trim().startsWith('```') &&
      !lines[i + 1].startsWith('mermaid') &&
      !lines[i + 1].startsWith('vega-lite') &&
      !lines[i + 1].startsWith('gantt') &&
      !lines[i + 1].startsWith('sequenceDiagram') &&
      !lines[i + 1].startsWith('flowchart') &&
      !lines[i + 1].startsWith('{')) {

    const blockStart = i;
    i++;
    const blockContentLines = [];
    while (i < lines.length && lines[i].trim() !== '```') {
      blockContentLines.push(lines[i]);
      i++;
    }
    const blockEnd = i;

    const firstLine = (blockContentLines[0] || '').trim();
    let matched = false;

    for (const [key, replacement] of remainingMap) {
      if (firstLine.includes(key)) {
        newLines.push(...replacement);
        matched = true;
        replacedCount++;
        console.log(`Replaced: ${key} (was: ${firstLine.substring(0, 60)})`);
        break;
      }
    }

    if (!matched) {
      newLines.push(lines[blockStart]);
      newLines.push(...blockContentLines);
      newLines.push(lines[blockEnd]);
    }
    i++;
  } else {
    newLines.push(line);
    i++;
  }
}

fs.writeFileSync(file, newLines.join('\n'), 'utf-8');
console.log(`\nDone. ${replacedCount} blocks replaced. Total lines: ${newLines.length}`);
