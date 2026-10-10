# node.js
简单一句话：

> **Node.js 不是一门新的编程语言，它是让 JavaScript 可以在浏览器之外（比如你的电脑服务器上）运行的一个环境（Runtime）。**

为了让你彻底理解，我们从几个关键角度来拆解：

### 1. JavaScript 的“解放”

在 Node.js 出现之前，JavaScript 就像一个被“关在”浏览器里的囚犯。它只能在网页上做一些交互（比如点击按钮弹出窗口、修改页面内容）。它的能力受限于浏览器的“沙盒”（一个安全限制环境）。

Node.js 打破了这道墙。它把 Chrome 浏览器的强大心脏——**V8 引擎**——拿出来，装到了一个独立的环境里，并赋予了它访问文件系统、网络、操作系统等底层能力。

所以，你现在可以像用 Python 或 Java 一样，用 JavaScript 来写后端服务、命令行工具、甚至控制硬件。

### 2. Chrome V8 引擎 = 超级跑车发动机

Node.js 的核心是 Chrome 的 V8 引擎。这是一个用 C++ 编写的、超快的 JavaScript 解释器。
- 它像一辆高性能跑车的发动机。
- 而 Node.js 就是为这台发动机配套的底盘、方向盘、座椅和油箱，让它能真正上路行驶。

### 3. 两大核心特性（为什么 Node.js 这么火）

- **非阻塞、异步 I/O**：想象你去奶茶店点单。
    - **传统方式（如传统 PHP/Apache）**：店员（服务器）必须等你付款、做好程序运行完，才能服务下一位客人。客人多了就要排队。
    - **Node.js 的方式**：店员（Node.js 事件循环）记下你的单子，告诉你“做好了叫你”，然后立刻去服务下一位客人。等你的奶茶做好了，它就会通知你来拿。**这就是“非阻塞”**，它能同时处理成千上万个请求，效率极高，尤其适合聊天应用、在线游戏、实时数据推送等场景。

- **单线程 + 事件循环**：
    - 虽然是单线程（同一时间只做一件事），但通过刚才提到的“异步”机制，它不会卡在等待一件事完成上。
    - 它就是一个极致高效的“项目经理”，把任务分发出去，自己只负责协调和等待结果，利用等待时间去处理新的任务。

### 在你当前学习 *JavaScript* 的语境下：

你现在看到的 `Javascript.md` 笔记，是学习这门语言的核心语法。
- 学习过程中，你主要是在**浏览器**里测试和运行这些代码。
- 将来你进阶到后端开发时，**Node.js** 就是你运行同样用 JavaScript 写的后端代码的平台。

### 总结一下 Node.js = ?

| 特质 | 类比 |
| :--- | :--- |
| **本质** | JavaScript 的运行环境（Runtime） |
| **核心** | Chrome V8 引擎 |
| **主要特点** | 事件驱动、非阻塞 I/O、轻量高效 |
| **能做什么** | 构建后端 API、Web 服务器、命令行工具 (CLI)、实时应用 |
| **为什么学** | 让你能用一门语言 (JS) 搞定前后端全栈开发，发展前景极大 |

所以，**Node.js 就是 JavaScript 从浏览器走向服务器、从“前端小工”变成“全栈工程师”的最关键一步。**


# 什么是javascript
在浏览器中的实现包含有三个部分：
- ECMAScript，核心语言
- DOM，文档对象模型，将文档分解为树索引，用于操作文档
- BOM，浏览器对象模型，提供一个浏览器操作接口，操作浏览器窗口

借助Node.js，可以使javascript在服务器端运行，进行后端开发。


## script标签
### 标签位置
- 将script标签放在head文件下，就意味着要等将所有js文件下载完以后，才能加载body主体，渲染整个界面。
- 将 script 放在 body 底部，可以让 HTML 内容先被解析和渲染，然后再下载并执行 JavaScript，从而减少用户等待白屏的时间。这是利用了脚本放置位置的优化，而非 JavaScript 的异步特性。

## 不同类型脚本
**defer**

**async**

**动态加载脚本**



# 语法
// 单行注释
/*      多行注释


## 变量

**var**关键字（函数作用域）、**let**声明（块作用域）
通过var来定义变量，在js中变量可以随意进行更改。
```javascript
var mess="sdf"

var a=0,
	b=6,
	c=5, //定义多个变量
```

作用域区别：
`let` 只存活于它所在的 `{ }` 块内，`var` 存活于整个函数。这也是为什么现代 JavaScript 开发中 **推荐优先使用 `let` 和 `const`** 而不是 `var`。

在循环中的不同：
```javascript
// var —— 循环结束后 i 仍然存在
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100); // 输出 3, 3, 3
}
console.log(i); // 3 （i 泄露到全局）

// let —— 每个迭代都有自己的块作用域
for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log(j), 100); // 输出 0, 1, 2
}
console.log(j); // ❌ ReferenceError: j is not defined
```

**const**声明
全局变量，且在声明时必须同时初始化变量。

## 数据类型
- undefined类型，当变量使用var或let声明却没有初始化后，就是这个类型
- Null，无
- Boolean，布尔类型：true，false
- Number类型，可作为类型转换函数，将其他类型转为数字类型：空字符串“”-->0 、数字字符串“00011”-->11、bool"true"-->1
- String类型，字符串变量一旦创建后就不可以进行修改，可以通过String函数或.toString()方法，将其他类型进行转换。
	字符串插值（通过$()进行插值）:let value=5;  ‘a = $(value)’
	raw属性，它返回模板字面量的**原始形式**——即不对转义序列（如 `\n`、`\t`、`\uXXXX`）进行解释。
	**标签函数**，通过构造函数对字符串进行插值
```JavaScript
	function myTag(strings, ...values) {
  console.log(strings); // ["Hello ", " world ", ""]
  console.log(values);  // ["Alice", 2024]
  // 可以自定义如何拼接
  return strings.reduce((acc, str, i) => acc + str + (values[i] || ''), '').toUpperCase();
}

const name = "Alice";
const year = 2024;
const result = myTag`Hello ${name} world ${year}`;
console.log(result); // "HELLO ALICE WORLD 2024"
```
- Symbol符号类型，
- Object对象类型

## 操作符
- 加性操作。++a：先加后操作；a++：先操作再加
- 乘，*
- 指数，**
- 除，/
- 关系，>,<,=
- 条件，let a=(b>c) ? 1:2;  a的取值，真为1，假为2


## 语句
- while
- for；
```javascript
for(let i=0;i<5;i++){

}
```
- for-in 语句，这是一个迭代语句，用于遍历枚举对象中的**属性**。
	主要用于遍历**普通对象**的属性名（字符串形式）。
	会遍历**原型链**上的可枚举属性（通常需要用 `hasOwnProperty()` 过滤）。
```javascript
const obj = { a: 1, b: 2, c: 3 };

for (let key in obj) {
  console.log(key); // "a", "b", "c"
}

// 数组上的 for-in 会遍历出索引（字符串）
const arr = [10, 20, 30];
arr.custom = 'hello';
for (let index in arr) {
  console.log(index, arr[index]); 
  // "0" 10, "1" 20, "2" 30, "custom" "hello"
}
```
- for-of语句，用法:
	只能用于可迭代对象：Array、String、Map、Set、arguments、NodeList、生成器等。
	直接获取集合的每个值，不关心键。
	不会遍历原型属性。
	不能用于普通对象（除非手动实现迭代器
	与for-in的区别：
	**`for...in` 取键，`for...of` 取值。  
	对象用 `in`，数组用 `of`。**
```javascript
const arr = [10, 20, 30];

for (let value of arr) {
  console.log(value); // 10, 20, 30
}

const str = "abc";
for (let ch of str) {
  console.log(ch); // "a", "b", "c"
}

// 普通对象不能使用
const obj = { a: 1 };
for (let val of obj) { // TypeError: obj is not iterable
  console.log(val);
}

```
 #### 什么是 **iterable（可迭代）**？

可迭代（iterable）是指对象实现了 **迭代器协议（Iterator Protocol）**，即它具有一个 `[Symbol.iterator]` 方法，该方法返回一个迭代器对象（iterator）。迭代器对象必须有一个 `next()` 方法，每次调用返回 `{ value: ..., done: boolean }`。

简单理解：**可迭代对象就是可以被「依次取出一个一个值」的对象**。常见的可迭代对象有：

- 数组（`Array`）
- 字符串（`String`）
- `Map`、`Set`
- `arguments` 对象
- `NodeList`（DOM 节点列表）
- 生成器（Generator）
普通对象（`{ a: 1, b: 2 }`）本身不提供 `[Symbol.iterator]` 方法，所以不是可迭代对象，无法用 `for...of` 遍历。


- **标签语句**，一种给语句起名字的语法，主要用于控制循环流（嵌套循环的 break 和 continue 定位跳转）。
`break` 与 `continue` 在标签中的区别

| 语句               | 行为                                 |
| ---------------- | ---------------------------------- |
| `break outer`    | **完全退出**标签 `outer` 所在的整个语句         |
| `continue outer` | 跳过当前迭代，**跳回**标签 `outer` 所在循环的下一次迭代 |
```javascript
outer: for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    if (j === 1) {
      continue outer;  // 跳过 i=1 的整轮外部迭代
    }
    console.log(`i=${i}, j=${j}`);
  }
}
```

- with语句，with语句的用处是将代码作用域设置为特定的对象，就是在with语句内，调用指定对象的属性可以不加对象名引用
```javascript
//原
let qs = location.search.substring(1); 
let hostName = location.hostname; 
let url = location.href;


with(location) { 
let qs = search.substring(1); 
let hostName = hostname; 
let url = href; 
}
```

## 函数
用function创建
```javascript
function fun(num1,num2){
	return num1+nunm2;
}
```



# 集合引用类型
## object
通过new的方法创建以及构造函数
```javascript
//new方式
let person = new Object(); 
person.name = "Nicholas"; 
person.age = 29;

//构造函数方式
let person = { 
	name: "Nicholas", 
	age: 29 
};
```
**取属性方式：** 
```javascript
person.name
person[属性]
```

## Array
数组中的每个槽位可以存储任意类型的数据，并且是动态大小，自动增长。
- 创建数组
```javascript
	let a= new Array([1,2,3,4],[1,2,2,2]);
	let a=[1,2,3]; //直接创建
	a[0];
	
	Array.from  //from方法
```
- 数组索引，0开始
- array对象都有栈方法（push,pop）和队列方法（push、shift取第一项）
- 排序方法 .sort()   .reverse()逆序

### 操作方法
**concat**
进行数组拼接。
```javascript
let a=[1,2];
a.concat([1,2,3]) //a=[1,2,1,2,3]
```

## 定型数组




## map键值对
```javascript
let a=new map([
	["key1","value1"],
	["key2","value2"],
]);

for (let key of a.keys()){
	alert(key);
}
```


## set


# 迭代器


# 速通版
## 数组与对象

### **对象**
对象可直接创建
```javascript
const project = {  
	name: "EEG Agent",  
	status: "running",  
	subjectCount: 20  
};  
  
console.log(project.name);
```
对象索引
对象的创建又可以理解成创建的map实例，通过键值对索引
```javascript
project.name
project["name"]
Object.keys(project) //返回对象的键列表     ['name', 'status', 'subjectCount']
Object.values(project) //返回值列表    ['EEG Agent', 'running', 20]
Object.entries(project) //将键值对转化为二维的数组返回    [Array(2), Array(2), Array(2)]
```

### **数组**

#### map方法，用于做批量转换
```javascript
// 示例：将数字数组中的每个元素都乘以2
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(num => num * 2);
// doubled: [2, 4, 6, 8, 10]

// 示例：提取对象数组中的特定属性
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' }
];
const names = users.map(user => user.name);
// names: ['Alice', 'Bob']
```

#### filter筛选方法
```javascript
// 示例：筛选出偶数
const numbers = [1, 2, 3, 4, 5, 6];
const evens = numbers.filter(num => num % 2 === 0);
// evens: [2, 4, 6]

// 示例：筛选出成年人
const people = [
  { name: 'Alice', age: 17 },
  { name: 'Bob', age: 25 },
  { name: 'Charlie', age: 19 }
];
const adults = people.filter(person => person.age >= 18);
```

#### reduce 汇总
对数组中的每个元素执行回调函数，将其结果汇总为单个值。
```javascript
array.reduce(callback(accumulator, currentValue, currentIndex, array), initialValue)
```
参数解析
1. **callback**​ - 对每个数组元素执行的函数
    - **accumulator**​ (累加器)：累积回调的返回值
    - **currentValue**​ (当前值)：数组中正在处理的当前元素
    - **currentIndex**​ (可选)：当前元素的索引
    - **array**​ (可选)：调用 reduce 的数组
2. **initialValue**​ (可选)：作为第一次调用 callback 时 accumulator 的初始值
    - 如果没有提供，则使用数组的第一个元素作为初始值
    - 空数组调用 reduce 时必须提供初始值

```javascript
// 示例：计算数组元素的总和
const numbers = [1, 2, 3, 4, 5];
const sum = numbers.reduce((accumulator, current) => {
  return accumulator + current;
}, 0);
// 0是accumulator的初始值
// sum: 15

// 示例：统计元素出现次数
const fruits = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple'];
const fruitCount = fruits.reduce((acc, fruit) => {
  acc[fruit] = (acc[fruit] || 0) + 1;
  return acc;
}, {});
// fruitCount: { apple: 3, banana: 2, orange: 1 }
// 将accumulator初始化为一个空{}
```

#### find() - 找一个
返回数组中满足回调函数的**第一个元素**的值，否则返回 `undefined`。
```javascript
// 示例：查找第一个大于10的元素
const numbers = [5, 12, 8, 130, 44];
const found = numbers.find(num => num > 10);
// found: 12

// 示例：查找特定id的用户
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' }
];
const user = users.find(u => u.id === 2);
// user: { id: 2, name: 'Bob' }
```

#### some() - 是否存在

测试数组中是否**至少有一个元素**通过了回调函数的测试。
```javascript
// 示例：检查数组中是否有偶数
const numbers = [1, 3, 5, 7, 8];
const hasEven = numbers.some(num => num % 2 === 0);
// hasEven: true

// 示例：检查是否有未成年人
const people = [
  { name: 'Alice', age: 20 },
  { name: 'Bob', age: 17 },
  { name: 'Charlie', age: 25 }
];
const hasMinor = people.some(person => person.age < 18);
// hasMinor: true
```

#### **every() - 是否全部满足**

测试数组中的**所有元素**是否都通过了回调函数的测试。
```javascript
// 示例：检查数组中的所有数字是否都大于0
const numbers = [1, 2, 3, 4, 5];
const allPositive = numbers.every(num => num > 0);
// allPositive: true

// 示例：检查是否所有人都成年
const people = [
  { name: 'Alice', age: 20 },
  { name: 'Bob', age: 18 },
  { name: 'Charlie', age: 25 }
];
const allAdults = people.every(person => person.age >= 18);
// allAdults: true
```

#### **push() - 添加**

向数组的末尾添加一个或多个元素，并返回新的长度。
```javascript
// 示例：向数组添加元素
const fruits = ['apple', 'banana'];
const newLength = fruits.push('orange');
// fruits: ['apple', 'banana', 'orange']
// newLength: 3

// 示例：添加多个元素
fruits.push('grape', 'mango');
// fruits: ['apple', 'banana', 'orange', 'grape', 'mango']
```

####  **includes() - 是否包含**

判断数组是否包含某个元素，返回布尔值。

```javascript
// 示例：检查数组是否包含特定元素
const fruits = ['apple', 'banana', 'orange'];
const hasBanana = fruits.includes('banana');
// hasBanana: true

const hasGrape = fruits.includes('grape');
// hasGrape: false

// 从指定索引开始查找
const numbers = [1, 2, 3, 4, 5];
const hasThreeFromIndex2 = numbers.includes(3, 2);
// hasThreeFromIndex2: true
```

#### **sort() - 排序**

对数组元素进行排序，并返回排序后的数组。**注意：会改变原数组！**

```javascript
// 示例：数字排序（注意默认按字符串Unicode排序）
const numbers = [10, 2, 5, 1, 9];
numbers.sort();
// numbers: [1, 10, 2, 5, 9] ❌ 这不是我们想要的数字排序

// 正确的数字排序
numbers.sort((a, b) => a - b);
// 升序: [1, 2, 5, 9, 10]

numbers.sort((a, b) => b - a);
// 降序: [10, 9, 5, 2, 1]

// 字符串排序
const fruits = ['banana', 'apple', 'orange', 'grape'];
fruits.sort();
// fruits: ['apple', 'banana', 'grape', 'orange']

// 对象数组排序
const users = [
  { name: 'Bob', age: 25 },
  { name: 'Alice', age: 20 },
  { name: 'Charlie', age: 30 }
];

// 按年龄升序排序
users.sort((a, b) => a.age - b.age);

// 按名字字母顺序排序
users.sort((a, b) => a.name.localeCompare(b.name));
```
要按数字大小正确排序，需要传入一个**比较函数（compare function）**。

**比较函数 (a, b) => a - b**

比较函数接收两个参数，代表数组中正在比较的两个元素。它必须返回一个**数字**：

- 如果返回值 **< 0**，表示 `a` 应该排在 `b` **前面**（即 `a` 小于 `b`）。
- 如果返回值 **> 0**，表示 `a` 应该排在 `b` **后面**（即 `a` 大于 `b`）。
- 如果返回值 **=== 0**，表示 `a` 和 `b` 相等，顺序不变。

`(a, b) => a - b` 的计算结果：

- 当 `a < b` 时，`a - b < 0` → `a` 排在 `b` 前 → **升序**。
- 当 `a > b` 时，`a - b > 0` → `a` 排在 `b` 后 → 也是升序。
- 当 `a === b` 时，`a - b = 0` → 位置不变。

所以 `numbers.sort((a, b) => a - b)` 实现了**数字升序排序**（从小到大）

## 操作符
### 算术运算
```txt
+    // 加法
-    // 减法
*    // 乘法
/    // 除法
%    // 取余（求模）
**   // 幂运算（指数）
++   // 自增
--   // 自减
```

### 比较运算
```txt
==   // 相等（会类型转换）
===  // 严格相等（值和类型都相同）  不会进行类型转换
!=   // 不相等  会进行类型转换
!==  // 严格不相等
>    // 大于
<    // 小于
>=   // 大于等于
<=   // 小于等于

"1"!=1  //false
"1"!==1 //true
```

### 逻辑运算
```
&&   // 逻辑与（AND）
||   // 逻辑或（OR）
!    // 逻辑非（NOT）
??   // 空值合并
?.   // 可选链
```

### 箭头函数
=>：箭头函数，是用于定义函数的一种简洁的方式
```javascript
// 传统函数
function add(a, b) {
  return a + b;
}

// 箭头函数
const add = (a, b) => {
  return a + b;
};

// 1. 当只有一个参数时，可以省略括号
const double = num => num * 2;

// 2. 当函数体只有一条返回语句时，可以省略大括号和 return
const square = x => x * x;  // 隐式返回 x*x

// 3. 无参数的箭头函数
const sayHello = () => "Hello!";

// 4. 返回对象时，需要加括号
const getPerson = () => ({ name: "Alice", age: 25 });

// 5. 多行函数体需要大括号
const calculate = (x, y) => {
  const sum = x + y;
  const diff = x - y;
  return { sum, diff };
};
```

### 展开运算符...
可以将数组、对象等可迭代的对象进行展开，**只需输入...加上变量名**
```JavaScript
const a = [1, 2];  
const b = [3, 4];  
const c = [...a, ...b]; // c=[1,2,3,4]

const oldData = { name: "EEG Agent", status: "pending" };  
  
const newData = {  
...oldData,  
status: "running"  
};

```

## 解构赋值
数组结构
```javascript
const arr = [1, 2, 3];  
const [a, b] = arr;
console.log(a); // 输出: 1
console.log(b); // 输出: 2

const user = {  
name: "张俊",  
major: "生物医学工程"  
};  
  
const { name, major } = user;

```

## 模块化
导出函数
```javascript
// utils.js
export function formatTime(time) {
  return time.toString();
}
```
导入
```javascript
// main.js
import { formatTime } from "./utils.js";
```


## 异步编程

异步编程用在面对很多耗时任务时，会对主线程造成阻塞，所以异步编程的核心思想是：
> 遇到耗时任务，不阻塞主线程，先把任务交出去，等结果回来后再继续处理。

先看看同步代码和异步代码的区别：
- 同步代码：一步一步地执行
```javascript
console.log("1");

console.log("2");

console.log("3");
//输出：
1
2
3
```

- 异步代码：用一个定时器的例子展示，定时器的语句不会造成阻塞：
```javascript
console.log("1");

//设置定时器，延时1秒，执行箭头函数()=>{}
setTimeout(() => {
  console.log("2");
}, 1000);

console.log("3");
//输出
1
3
2
```

### javascript异步的三种写法

- 回调函数
- promise
- async / await
#### 回调函数

回调函数是：
> 把一个函数作为参数传给另一个函数，等事情做完了以后再调用它

举个例子📝
```javascript
function getData(callback) {
  setTimeout(() => {
    const data = "服务器返回的数据";
    callback(data);
  }, 1000);
}

getData((result) => {
  console.log(result);
});
```
在这个例子中，getData将箭头函数作为callback传入；去执行callback(data)，当定时器结束后，在执行callback(data)，也就是打印输出data。

执行逻辑是：
```
getData 开始执行
遇到 setTimeout，开启异步等待
1 秒后拿到 data
调用 callback(data)
```

**callback的问题：回调地狱**
如果当多个异步任务以来前一个结果：
```javascript
login((user) => {
  getUserInfo(user.id, (info) => {
    getUserOrders(info.id, (orders) => {
      getOrderDetail(orders[0].id, (detail) => {
        console.log(detail);
      });
    });
  });
});
```
也就是说，当回调形成嵌套以后，层级会越陷越深，且代码会变得不以维护。

因此，也就有了promise

#### promise

promise可以理解为：
> 一个的代表未来结果的对象

它有三种状态：
- pending：等待中
- fulfilled：成功
- rejected：失败

举个例子来说明promise：
```javascript
const p = new Promise((resolve, reject) => {
  setTimeout(() => {
    const success = true;

    if (success) {
      resolve("请求成功");
    } else {
      reject("请求失败");
    }
  }, 1000);
});
```
resolve和reject是 Promise 构造函数传入的两个参数。它们的作用是控制 Promise 的状态转换，从而让异步操作的结果可以被 .then() / .catch() 等后续方法处理。

**resolve**
- **将 Promise 状态从 `pending`（等待中）变为 `fulfilled`（成功）**。
- 可以传递一个值（通常是异步操作成功的结果），这个值会被 `.then()` 的回调函数接收。
- `resolve` 只能被调用一次，之后再次调用 `resolve` 或 `reject` 都不会生效（Promise 状态一旦改变就不可逆转）。
**reject**
- **将 Promise 状态从 `pending`（等待中）变为 `rejected`（失败）**。
- 可以传递一个错误原因（通常是 Error 对象或错误信息），这个值会被 `.catch()` 或 `.then()` 的第二个回调函数接收。
- 同样，`reject` 也只能被调用一次，且一旦状态变为 rejected，就不能再改变。

使用promise，接收resolve和reject
```javascript
p.then((result) => {
  console.log(result);
}).catch((error) => {
  console.log(error);
});
```
通过promise参数返回值的方式，避免了造成回调嵌套的局面，显式的给出了异步的结果，使异步代码变得可链式调用。

**下面介绍promise接收的详细用法：**

- .then()处理成功
```javascript
function getData() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve("数据来了");
    }, 1000);
  });
}

getData().then((data) => {
  console.log(data);
});
```

- .catch()处理失败
```javascript
function getData() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      reject("网络错误");
    }, 1000);
  });
}

getData()
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.log("出错了：", error);
  }); 
```
**完全可以直接在 Promise 后面只写 `.catch()` 而不写 `.then()`**，这是完全合法的 JavaScript 语法。

- .finally()无论成功失败都会执行
```javascript
getData()
  .then((data) => {
    console.log("成功：", data);
  })
  .catch((error) => {
    console.log("失败：", error);
  })
  .finally(() => {
    console.log("请求结束");
  });
```

> promise的链式调用

通过下面这个例子来介绍一下来链式调用
```javascript
login() //执行login()这个promise对象
  .then((user) => {   //login中成功，resolve会将user传递出来
    return getUserInfo(user.id);//return的是一个promise对象
  })
  .then((info) => {  //getUserInfo这个promise成功，会传出info
    return getOrders(info.id);
  })
  .then((orders) => {
    console.log(orders);
  })
  .catch((error) => {
    console.log("流程出错：", error);
  });
```
上述例子演示的流程是：
```
先登录
再获取用户信息
再获取订单
```

#### async/await

async/await是promise的语法糖🍬它让异步代码写起来更像是同步代码

什么是语法糖?
一个编程术语，指**一种语法上的便捷写法，它不提供新功能，只是让代码更简洁、更易读、更符合直觉**。

比如：
promise写法：
```javascript
getData()
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.log(error);
  });
```

可以改成：
```javascript
async function main() {
  try {
    const data = await getData();
    console.log(data);
  } catch (error) {
    console.log(error);
  }
}

main();
```

**async是什么**？
只要给函数前面加了async，这个函数就会返回promise
比如：
```javascript
async function test() {
  return 123;
}

console.log(test());
//输出的结果是：
Promise { 123 }
//要通过.then()获得结果
test().then((res) => {
  console.log(res);
});
```

或者通过下面这种语句调用test：
```javascript
async function main(){
	const res = await test();
	console.log(res);
}
main();
```

**await是什么**
await只能在async函数中使用
> await的意思是，等这个promise结束后，将结果取出来。相当于就是调用.then()，将resolve的值取出来

比如下面这个例子：
```javascript
function getData() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve("数据来了");
    }, 1000);
  });
}

async function main() {
  console.log("开始");

  const data = await getData();

  console.log(data);
  console.log("结束");
}

main();

//输出：
开始
数据来了
结束
```

**async/await的错误处理**

promise失败时，用try...catch捕获，**接收reject**
```javascript
function getData() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      reject("服务器异常");
    }, 1000);
  });
}

async function main() {
  try {
    const data = await getData();
    console.log(data);
  } catch (error) {
    console.log("捕获错误：", error);
  }
}

main();
```

### 一个例子：fetch
fetch的作用是

> 浏览器请求后端api时常用fetch

以下是完整的写法：
```javascript
async function getUser() {
  try {
    const response = await fetch("https://jsonplaceholder.typicode.com/users/1");

    if (!response.ok) {
      throw new Error("请求失败，状态码：" + response.status);
    }

    const data = await response.json();

    console.log("用户数据：", data);
  } catch (error) {
    console.log("请求出错：", error.message);
  }
}

getUser();
```

在真实fetch中需要注意：
```
fetch 只有网络层失败才会自动 reject
HTTP 404 / 500 不会自动进入 catch
所以需要自己判断 response.ok
```

### 串行异步和并行异步

**串行异步**
后一个任务依赖前一个任务，就串行。
```javascript
async function main() {
  const user = await login();
  const info = await getUserInfo(user.id);
  const orders = await getOrders(info.id);

  console.log(orders);
}
```

**并行异步**
如果多个任务互不依赖，更好的写法应该并行。
```javascript
async function main() {
  const [user, products, news] = await Promise.all([
    getUser(),
    getProducts(),
    getNews()
  ]);

  console.log(user, products, news);
}
```
像这样，三个请求会同时的发出

其中：

- promise.all，用于多个异步任务全部成功后再继续。全部成功，才成功，只要一个失败，整体失败。

- promise.allSettled，用于不管成功失败，都拿到每个任务的结果
比如：
```javascript
async function main() {
  const results = await Promise.allSettled([
    getUser(),
    getProducts(),
    getNews()
  ]);

  console.log(results);
}

main();

//结果为：
[
  { status: "fulfilled", value: "用户数据" },
  { status: "rejected", reason: "商品接口失败" },
  { status: "fulfilled", value: "新闻数据" }
]
```

- Promise.race，谁先完成就用谁。
比如用于处理链接超时：
```javascript
function timeout(ms) {
  return new Promise((_, reject) => { //只传出reject
    setTimeout(() => {
      reject(new Error("请求超时"));
    }, ms);
  });
}

async function main() {
  try {
    const result = await Promise.race([
      fetch("https://jsonplaceholder.typicode.com/users/1"),
      timeout(3000)
    ]);

    console.log(result);
  } catch (error) {
    console.log(error.message);
  }
}

main();
```

### 事件循环Event Loop

在js中的任务大致可以分为：
- 同步任务，正常的语句
- 微任务 microtask，Promise.then / await 后面的代码
- 宏任务 macro，setTimeout / setInterval

执行顺序：
```
同步任务 → 微任务 → 宏任务
```

通过一个例子理解下：
```javascript
console.log("1");

setTimeout(() => {
  console.log("2");
}, 0);

Promise.resolve().then(() => {
  console.log("3");
});

console.log("4");
//输出：
1
4
3
2
```
await后面的代码也是微任务：
```javascript
async function test() {
  console.log("A");

  await Promise.resolve();

  console.log("B");
}

console.log("1");

test();

console.log("2");
//输出：
1
A
2
B
```

# 速通react💪

**什么是react?**

> React 是一个用于构建用户界面的 **JavaScript 库**，由 Facebook 团队开发并开源。它的核心思想是通过组件化、声明式的方式来高效地构建交互式 UI。

React 本质就一句话：

**用 JavaScript 函数描述页面长什么样；当数据变了，React 自动重新渲染页面。**















