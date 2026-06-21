// Replace ASCII fenced code blocks with Mermaid/Vega equivalents in V3
const fs = require('fs');
const path = require('path');

const file = 'C:/Users/haoxc/HXC_DATA/80_Knowledges/ZSSolutions/03-项目课题/26.0618-数智化生产支撑系统(JBFG)/20-解决方案/方案产出-V3/v3-冀北风光储数智化生产支撑与数字孪生解决方案.md';
let content = fs.readFileSync(file, 'utf-8');

// Map: first_line_substring → replacement block
// We identify ASCII blocks by their first content line
const replacements = [
  // fig2-1: SCQA
  {
    marker: 'SCQA 分析框架',
    replace: `\`\`\`mermaid
flowchart TB
    S["S 现状<br/>冀北基地多系统并行<br/>风机SCADA·光伏监控·储能EMS<br/>各自独立·坐标系不统一"]
    C["C 挑战<br/>数据:百万测点 | 实时:≤1s | 可靠:10000h"]
    Q["Q 问题<br/>如何在单一平台中<br/>同时解决三个痛点？"]
    A["A 答案<br/>USDF 空间对象操作系统<br/>三通道分流：P1暂态·P2稳态·P3历史"]
    S --> C --> Q --> A
    style S fill:#a6a6a6,color:#fff
    style C fill:#c00000,color:#fff
    style Q fill:#ed7d31,color:#fff
    style A fill:#1f4e79,color:#fff
\`\`\``
  },
  // Digital twin tree (in §2.2)
  {
    marker: '数字孪生（三维可视化 + 实时数据驱动）',
    replace: `\`\`\`mermaid
flowchart LR
    DT["数字孪生<br/>三维可视化+实时数据驱动"]
    DT --> F1["F1 一体化场站【建】"]
    DT --> F2["F2 协同优化【控】"]
    DT --> F3["F3 透明场站【评】"]
    DT --> F4["F4 智能运维【检】"]
    DT --> F5["F5 数字运维【管】"]
    style DT fill:#1f4e79,color:#fff
\`\`\``
  },
  // §3.2 逻辑四层
  {
    marker: '展示层    三维 Web 门户',
    replace: `\`\`\`mermaid
flowchart TB
    subgraph L4["展示层"]
    P1["三维 Web 门户 / 大屏 / 移动端 / 运维门户"]
    end
    subgraph L3["业务层"]
    B1["F1 一体化场站│F2 协同优化│F3 透明场站│F4 智能运维│F5 数字运维"]
    end
    subgraph L2["平台层 (USDF)"]
    U1["对象注册 + 空间参照 + 属性标准化 + 拓扑关系"]
    U2["Kafka + ClickHouse + Postgres+PostGIS + Redis"]
    end
    subgraph L1["采集层"]
    C1["IEC104 / Modbus TCP / GOOSE / RTSP-GB28181 / MQTT"]
    end
    L4 -->|RESTful API (APISIX)| L3 -->|gRPC + Kafka| L2 -->|统一采集适配器| L1
    style L2 fill:#1f4e79,color:#fff
\`\`\``
  },
  // §3.2 物理部署拓扑
  {
    marker: '物理部署拓扑（三级）',
    replace: `\`\`\`mermaid
flowchart TB
    subgraph 中心云["中心云（集团侧）"]
    GPU["GPU 集群<br/>AI 训练"]
    BD["大数据集群<br/>ClickHouse/Postgres"]
    DASH["全局驾驶舱"]
    end
    subgraph 边缘["场站边缘（冀北基地）"]
    direction LR
    Z1["安全I区·控制区<br/>GOOSE暂态≤100ms<br/>防误保护·本地兜底"]
    Z2["安全II区·非控生产区<br/>IEC104实时采集<br/>Redis缓存·GPU边缘推理<br/>AGC/AVC·断网自持≥2h"]
    Z3["安全III区·管理信息区<br/>三维Web门户<br/>工单/报表/大屏"]
    end
    中心云 -.广域网4G/5G/专线.-> 边缘
    Z1 -->|正向隔离装置·物理单向| Z2
    Z2 -->|防火墙| Z3
    边缘 --> DEV["设备层：风机SCADA/光伏监控/储能EMS/SVG升压站/摄像头/无人机"]
    style Z1 fill:#c00000,color:#fff
    style Z2 fill:#ed7d31,color:#fff
    style Z3 fill:#1f4e79,color:#fff
\`\`\``
  },
  // §3.5 AI引擎架构
  {
    marker: 'AI 引擎三层架构',
    replace: `\`\`\`mermaid
flowchart LR
    subgraph 边缘["边缘端·场站II区GPU"]
    E1["实时CV推理"]
    E2["告警生成"]
    E3["边缘模型热更新"]
    end
    subgraph 云["云端·中心云GPU集群"]
    C1["模型训练/微调"]
    C2["版本管理+AB测试"]
    C3["数据集管理"]
    end
    subgraph 业务["业务端·III区运维门户"]
    B1["人工复核"]
    B2["标注反馈"]
    B3["闭环追踪"]
    end
    边缘 <-->|USDF标准API<br/>gRPC同步/Kafka异步| 云
    云 <--> 业务
    style 边缘 fill:#ed7d31,color:#fff
    style 云 fill:#1f4e79,color:#fff
    style 业务 fill:#2e7d32,color:#fff
\`\`\``
  },
  // §3.6 四层治理体系
  {
    marker: '四层治理体系',
    replace: `\`\`\`mermaid
flowchart BT
    L1["① 主数据管理（USDF已有）<br/>全局唯一ID+标准属性集+生命周期+拓扑关系"]
    L2["② 元数据目录<br/>场站→区域→设备→部件→测点，五级目录+搜索"]
    L3["③ 数据血缘<br/>测点→Kafka Topic→时序表→API字段，全链路可追溯"]
    L4["④ 数据质量<br/>完整性校验/时效性监控/异常值检测/质量报告"]
    L1 --> L2 --> L3 --> L4
    style L1 fill:#1f4e79,color:#fff
    style L4 fill:#2e7d32,color:#fff
\`\`\``
  },
  // §3.7 四层运维监控 (keep as is since V2 presents this as a table)
  // §3.8 系统完整架构
  {
    marker: '系统完整架构',
    replace: `\`\`\`mermaid
flowchart TB
    P["展示层<br/>三维Web门户(Cesium+Three.js)/大屏/移动端/运维门户"]
    B["业务层<br/>F1场站平台│F2协同优化│F3透明场站│F4智能运维│F5数字运维"]
    U["USDF平台层<br/>对象注册/空间参照/属性标准化/拓扑关系<br/>Kafka(≥32分区)·ClickHouse+PostGIS·Postgres·Redis<br/>P1暂态(GOOSE)│P2稳态(IEC104)│P3历史(API)"]
    C["采集层·统一采集适配器<br/>IEC104/Modbus/GOOSE/RTSP-GB28181/MQTT"]
    D["设备层：风机SCADA/光伏监控/储能EMS/SVG/视频"]
    M["运维监控（跨层贯通）<br/>Prometheus+SkyWalking+ELK → Grafana/审计库/AlertManager"]
    P -->|RESTful·APISIX| B -->|gRPC+Kafka| U --> C --> D
    M -.贯通.- U
    style P fill:#2e75b6,color:#fff
    style B fill:#ed7d31,color:#fff
    style U fill:#1f4e79,color:#fff
    style C fill:#a6a6a6,color:#fff
    style M fill:#70ad47,color:#fff
\`\`\``
  },
  // fig4-0: 五大业务子系统闭环全景
  {
    marker: '五大业务子系统闭环全景图',
    replace: `\`\`\`mermaid
flowchart TB
    USDF["数字孪生底座 USDF"]
    USDF --> F1["F1 一体化场站【建】<br/>三维建模·数据接入·低代码组态"]
    USDF --> F2["F2 协同优化【控】<br/>有功无功协同·暂态控制·三道防误"]
    USDF --> F3["F3 透明场站【评】<br/>并网性能·发电性能·跟构网对比"]
    F1 --> BUS{统一数据总线}
    F2 --> BUS
    F3 --> BUS
    BUS --> F4["F4 智能运维【检】<br/>升压站·光伏·线路·储能 AI巡检"]
    BUS --> F5["F5 数字运维【管】<br/>360°监控·智能诊断·运维门户"]
    F4 --> LOOP["闭环反馈"]
    F5 --> LOOP
    LOOP -.预测性维护驱动.-> USDF
    style USDF fill:#1f4e79,color:#fff
    style BUS fill:#ed7d31,color:#fff
    style LOOP fill:#2e7d32,color:#fff
\`\`\``
  },
  // §4.4 告警工单闭环时序
  {
    marker: '告警工单闭环时序',
    replace: `\`\`\`mermaid
sequenceDiagram
    participant AI as AI引擎/规则引擎
    participant WO as 工单中心
    participant OP as 运维人员
    participant RV as 审核人
    AI->>WO: 告警触发（等级+设备+图像）
    WO->>OP: 自动派单（类型+班组+时限）
    OP->>OP: 现场处置（拍照+记录）
    OP->>WO: 结果回传（处置结果+图像）
    WO->>RV: 提交待审核
    RV->>RV: 复核+修正（不覆盖原始数据）
    RV->>WO: 审核通过
    WO->>WO: 关闭归档（全流程日志入库）
\`\`\``
  },
  // fig5-1: 四层 SLA (ASCII → Vega-Lite)
  {
    marker: '四层 SLA 延迟预算与数据通路',
    replace: `\`\`\`vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "title": "四层 SLA 延迟边界（对数轴，毫秒）",
  "data": {"values": [
    {"层级": "L0 暂态(GOOSE直通)", "延迟ms": 100, "场景": "紧急调频/防误保护"},
    {"层级": "L1 实时(采集→Kafka→Redis→API)", "延迟ms": 1000, "场景": "实时监控/告警推送"},
    {"层级": "L2 近实时(含三维渲染)", "延迟ms": 3000, "场景": "三维交互/驾驶舱"},
    {"层级": "L3 历史(时序库聚合)", "延迟ms": 5000, "场景": "报表/趋势/AI训练"}
  ]},
  "mark": {"type": "bar"},
  "encoding": {
    "y": {"field": "层级", "type": "nominal", "sort": "-x", "axis": {"title": null}},
    "x": {"field": "延迟ms", "type": "quantitative", "scale": {"type": "log"}, "axis": {"title": "延迟上限 (ms, 对数轴)"}},
    "color": {"field": "层级", "type": "nominal", "legend": null, "scale": {"range": ["#c00000", "#ed7d31", "#1f4e79", "#2e7d32"]}},
    "tooltip": [{"field": "场景"}, {"field": "延迟ms"}]
  }
}
\`\`\``
  },
  // fig6-1: 甘特图
  {
    marker: '项目实施甘特图（4 个月，三阶段交付）',
    replace: `\`\`\`mermaid
gantt
    title 冀北风光储数智化项目实施计划（4个月）
    dateFormat YYYY-MM-DD
    axisFormat %m月
    section 一阶段·平台底座
    USDF底座+统一采集适配器      :a1, 2026-07-01, 30d
    Kafka+ClickHouse+PG数据平台 :a2, 2026-07-01, 30d
    F1.2 三维可视化基础场景      :a3, 2026-07-15, 30d
    F5.1 360°实时监控           :a4, 2026-07-15, 30d
    M1 平台底座可用(百万测点验证) :milestone, m1, 2026-07-31, 0d
    section 二阶段·核心业务
    F2 功率协同优化             :b1, 2026-08-01, 40d
    F3 构网型透明场站           :b2, 2026-08-01, 40d
    F4 智能运维(四区)           :b3, 2026-08-01, 45d
    F5.2-5.3 诊断+门户          :b4, 2026-08-10, 35d
    M2 核心业务上线             :milestone, m2, 2026-09-15, 0d
    section 三阶段·联调上线
    P2增强功能+全功能联调        :c1, 2026-09-16, 30d
    性能压测(500并发/百万测点)   :c2, 2026-09-20, 25d
    等保测评+UAT               :c3, 2026-10-01, 25d
    M3 联调完成                 :milestone, m3, 2026-10-20, 0d
    M4 正式上线                 :milestone, m4, 2026-10-31, 0d
\`\`\``
  },
  // fig7-1: 风险热力图 (ASCII → Vega-Lite)
  {
    marker: '风险热力图（18 项风险 x 三维度）',
    replace: `\`\`\`vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "title": "风险分布热力图（数字=风险项数）",
  "data": {"values": [
    {"维度": "技术风险", "等级": "阻断", "数量": 2},
    {"维度": "技术风险", "等级": "高", "数量": 5},
    {"维度": "技术风险", "等级": "低", "数量": 1},
    {"维度": "业务风险", "等级": "阻断", "数量": 2},
    {"维度": "业务风险", "等级": "高", "数量": 3},
    {"维度": "业务风险", "等级": "低", "数量": 0},
    {"维度": "实施风险", "等级": "阻断", "数量": 1},
    {"维度": "实施风险", "等级": "高", "数量": 3},
    {"维度": "实施风险", "等级": "低", "数量": 1}
  ]},
  "mark": "rect",
  "encoding": {
    "x": {"field": "维度", "type": "nominal", "axis": {"title": null, "labelAngle": 0}},
    "y": {"field": "等级", "type": "nominal", "sort": ["阻断","高","低"], "axis": {"title": null}},
    "color": {"field": "数量", "type": "quantitative", "scale": {"scheme": "reds"}},
    "tooltip": [{"field": "维度"}, {"field": "等级"}, {"field": "数量"}]
  }
}
\`\`\``
  },
  // fig8-1: 报价构成 (ASCII → Vega-Lite)
  {
    marker: '报价构成（220 万元含税）',
    replace: `\`\`\`vega-lite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
  "title": "项目报价构成（220万元含税）",
  "data": {"values": [
    {"项目": "定制开发", "金额": 93},
    {"项目": "三维建模", "金额": 40},
    {"项目": "硬件设备", "金额": 28},
    {"项目": "软件平台", "金额": 23},
    {"项目": "实施培训", "金额": 16},
    {"项目": "运维质保", "金额": 11},
    {"项目": "GIS数据", "金额": 9}
  ]},
  "mark": {"type": "arc", "innerRadius": 60, "stroke": "#fff"},
  "encoding": {
    "theta": {"field": "金额", "type": "quantitative"},
    "color": {"field": "项目", "type": "nominal", "scale": {"range": ["#1f4e79","#2e75b6","#ed7d31","#a6a6a6","#70ad47","#ffc000","#9e480e"]}},
    "tooltip": [{"field": "项目"}, {"field": "金额", "title": "金额(万元)"}]
  }
}
\`\`\``
  }
];

// Process replacements
let replaced = 0;
for (const r of replacements) {
  // Find ASCII fenced block containing the marker
  const pattern = new RegExp(
    '\`\`\`\\n[\\s\\S]*?' + r.marker.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '[\\s\\S]*?\\n\`\`\`',
    'g'
  );
  const match = content.match(pattern);
  if (match) {
    content = content.replace(match[0], r.replace);
    replaced++;
    console.log(`Replaced: ${r.marker}`);
  } else {
    console.log(`NOT FOUND: ${r.marker}`);
  }
}

fs.writeFileSync(file, content, 'utf-8');
console.log(`\nDone. ${replaced}/${replacements.length} replacements made.`);
