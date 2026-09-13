# 图表设计规范

## 通用原则
1. **矢量图优先**：PDF/EPS 格式，避免低分辨率 PNG
2. **字体一致**：图中文字大小与正文接近（通常 8-10pt）
3. **颜色可区分**：色盲友好配色，避免仅靠颜色区分（加形状/线型）
4. **图例清晰**：legend 不遮挡数据，优先放在空白区域
5. **坐标轴标注**：每个轴有标签和单位
6. **caption 在下方**：figure 的 caption 放在图下面

## 学术配色方案
\definecolor{tol1}{RGB}{51,34,136}     % 靛蓝
\definecolor{tol2}{RGB}{17,119,51}     % 绿
\definecolor{tol3}{RGB}{204,102,119}   % 玫红
\definecolor{tol4}{RGB}{136,34,85}     % 紫红
\definecolor{tol5}{RGB}{68,170,153}    % 青
\definecolor{tol6}{RGB}{221,204,119}   % 黄

## 模板
### pgfplots 折线图（双曲线）/ pgfplots 分组柱状图（带 error bar）/ 通用流程图（TikZ）
