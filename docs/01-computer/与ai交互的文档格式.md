# 与 AI 交互的文档格式
<div class="section-intro" markdown="1">

>因为LLM的对象是文本，所以对于一些非文本的数据对象（比如公式，图片），gpt一般都是生成的代码生成这些数据，所以在用ai生成一些数据，但并不完全满意的时候，是有必要会这些语言，这样可以直接在ai生成的基础上自己上手改。

</div>


我在这里汇总我目前知道的，待发现有其他的再补充：

- 数学公式用的**latex**
- 图片用的**svg**
- 文本用的**markdown**


[Markdown 语法详细教程](Markdown语法详细教程.md)

svg:

```
<svg width="800" height="500"
     viewBox="0 0 800 500"
     xmlns="http://www.w3.org/2000/svg">

    <!-- 矩形 -->
    <rect
        x="50"
        y="50"
        width="200"
        height="100"
        rx="15"
        fill="#4F8EF7"
    />

    <!-- 圆 -->
    <circle
        cx="400"
        cy="100"
        r="50"
        fill="white"
        stroke="#7C3AED"
        stroke-width="4"
    />

    <!-- 线 -->
    <line
        x1="250"
        y1="100"
        x2="350"
        y2="100"
        stroke="#333"
        stroke-width="3"
    />

    <!-- 文字 -->
    <text
        x="150"
        y="110"
        text-anchor="middle"
        font-size="20"
        fill="white">
        EEG Input
    </text>

</svg>
```


