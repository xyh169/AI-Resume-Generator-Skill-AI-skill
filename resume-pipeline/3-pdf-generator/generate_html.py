import sys

with open(r"f:/MY Darling RooM/py脚本/GitHub/Blue-Purple-Resume-Builder v2.0.0/GitHub_Export/resume-pipeline/3-pdf-generator/resources/template_1page.css", "r", encoding="utf-8") as f:
    css_content = f.read()

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        {css_content}
        body {{ font-family: Arial, "Microsoft YaHei", "微软雅黑", SimSun, "宋体", sans-serif; font-size: 10pt; line-height: 1.5; }}
        .a4-page {{ padding: 10mm 15mm 10mm 15mm; }}
        .header h1 {{ font-size: 16pt; }}
        .header p {{ font-size: 9.5pt; margin: 1px 0; }}
        .section-title h2 {{ font-size: 12pt; }}
        .item-title {{ font-size: 10.5pt; }}
        .item {{ margin-bottom: 5px; }}
        .section-title {{ margin: 3px 0 2px 0; padding: 2px 18px 2px 8px; }}
        .section-content {{ margin-bottom: 2px; }}
        ul {{ margin: 1px 0; }}
        li {{ margin-bottom: 1px; }}
    </style>
</head>
<body>
    <div class="a4-page">
        <!-- Header -->
        <div class="header">
            <h1>王XX</h1>
            <p><strong>电话</strong>: 13800138000 | <strong>邮箱</strong>: wangxx@example.com | <strong>政治面貌</strong>: 中共党员</p>
            <p><strong>求职意向</strong>: 高校实验技术岗 | <strong>研究方向</strong>: 分子诊断、POCT (体外诊断)</p>
        </div>

        <div class="section">
            <div class="section-title"><h2>教育背景</h2></div>
            <div class="section-content">
                <div class="item edu-item">
                    <div class="edu-header">
                        <div><span class="edu-school">AA大学</span> | <span class="edu-major">生物化学与分子生物学</span><span class="edu-detail">博士（主攻分子诊断、POCT）</span></div>
                        <div class="item-date">2020.09 - 2025.06</div>
                    </div>
                </div>
                <div class="item edu-item">
                    <div class="edu-header">
                        <div><span class="edu-school">BB大学</span> | <span class="edu-major">生物学（分子病毒学）</span><span class="edu-detail">硕士</span></div>
                        <div class="item-date">2017.09 - 2020.07</div>
                    </div>
                </div>
                <div class="item edu-item">
                    <div class="edu-header">
                        <div><span class="edu-school">CC大学</span> | <span class="edu-major">包装工程</span><span class="edu-detail">本科</span></div>
                        <div class="item-date">2013.09 - 2017.06</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title"><h2>个人优势与岗位匹配度</h2></div>
            <div class="section-content">
                <div class="item">
                    <ul>
                        <li><span class="k">扎实的 IVD 科研经验与平台建设能力</span>：具有生物化学与分子生物学博士学位，主攻分子诊断与 POCT 领域。曾在导师指导下从零到一主导搭建了全自动核酸检测系统，精通相关仪器操作与维护，具备极强的实验室硬件平台建设和运行管理能力。</li>
                        <li><span class="k">管理协调与学生指导及培训能力</span>：作为重点课题子负责人全面统筹课题进度、协调跨学科团队，具有指导师弟师妹及团队成员正确使用实验室相关仪器和软件的丰富实战经验。</li>
                        <li><span class="k">强烈的责任心、服务意识及团队精神</span>：担任社团副主席期间包揽千人级活动，热心参与公共事务建设。富有极强的团队合作精神与服务意识，能够高效承担实验室行政、课程开发以及日常运维工作。</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title"><h2>项目经历与实验平台经验</h2></div>
            <div class="section-content">
                <div class="item">
                    <div class="item-header">
                        <div><span class="item-title">一体化全自动核酸检测系统的研发</span><span class="item-org">| 子课题负责人</span></div>
                        <div class="item-date">博士阶段</div>
                    </div>
                    <ul>
                        <li><span class="k">实验平台建设与硬件维护</span>：主导研发了一台基于磁珠法的微流控全自动核酸检测集成设备，深度参与底层方法构建与卡盒设计。熟悉各类生命科学分析仪器的日常安全守则、使用规范与维护校准准则。</li>
                        <li><span class="k">实验室管理统筹与课程规划</span>：长期负责实验组内跨学科团队运转，规范实验操作安全及制度；不仅出色拔高自身研究产出，还承担起辅导本科生及硕士生开展基础实验设计的指导工作，课题顺利验收。</li>
                        <li><span class="k">软件维护与配套数字系统研发</span>：参与边缘 AI 算法（YOLOv11n）优化，攻克仪器低成本数据读取难题。本人熟练掌握数据处理及 Python 编程技能，可直接输出实验室各类信息化管理或实验平台软件的开发与维保支持。</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title"><h2>实习经历</h2></div>
            <div class="section-content">
                <div class="item">
                    <div class="item-header">
                        <div><span class="item-title">DD资本管理有限公司</span><span class="item-org">| 投资助理</span></div>
                        <div class="item-date">2022.04 - 2022.09</div>
                    </div>
                    <ul>
                        <li><span class="k">生物技术平台与项目评估</span>：利用生物及分子诊断硕博背景与跨界视野，评估早期生物技术与医疗器械初创，输出系统性行业调研分析报告以辅助高层投资决策依据。</li>
                        <li><span class="k">校企资源桥接与孵化服务</span>：深度挖掘并衔接高校内优质潜力实验项目至创投资源，推动高壁垒科研成果和硬件平台朝商业应用落地。</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title"><h2>校园经历</h2></div>
            <div class="section-content">
                <div class="item">
                    <div class="item-header">
                        <div><span class="item-title">AA大学123社团</span><span class="item-org">| 副主席兼荣誉创投事业部主席</span></div>
                        <div class="item-date">2022.04 - 2023.03</div>
                    </div>
                    <ul>
                        <li><span class="k">大型活动统筹与服务意识</span>：全面负责社团日常架构运转，成功策划并落地纳新、知识分享会及20周年大型校庆配套活动，展现一流校际统筹和公共服务能力。</li>
                        <li><span class="k">资源整合与外部联络沟通</span>：独立邀请到5家头部一线投资机构及浙大系孵化器专家，举办逾10场高规格闭门圆桌交流，为渴望技术变现或创业的同学建立了强力跳板通道。</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title"><h2>成果与荣誉</h2></div>
            <div class="section-content section-2col">
                <div class="item">
                    <div class="item-desc"><strong>核心学术成果与专利</strong></div>
                    <ul>
                        <li>以第一作者发表高水平 SCI 论文2篇（Q1区，其中 Small Methods IF=12.1）；另有2篇一作文章在投。</li>
                        <li>针对实验仪器底层持有一项“集成核酸提取与检测装置”国家授权发明专利（除导师团队外署名第一）。</li>
                    </ul>
                </div>
                <div class="item">
                    <div class="item-desc"><strong>所获荣誉奖项</strong></div>
                    <ul>
                        <li><span class="k">2025年</span>：荣获 AA大学优秀毕业研究生称号。</li>
                        <li><span class="k">博硕期间</span>：多次荣获校级“五好研究生”、“优秀研究生”，及黄子源奖学金。</li>
                        <li><span class="k">本科期间</span>：连续两年获批校级三等学业奖学金。</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

with open(r"f:/MY Darling RooM/py脚本/GitHub/Blue-Purple-Resume-Builder v2.0.0/GitHub_Export/resume-pipeline/3-pdf-generator/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated HTML.")
