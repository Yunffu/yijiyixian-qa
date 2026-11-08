# 学习笔记 01 · Python（第一天只需要这 3 样）

> 2026-11-08 · D1 · 目标：**看懂**就行，不用会写。今天不学 FastAPI，不学 pytest。
> 判读标准：下面 §4 的三道题你能**在纸上写出伪代码 / 说出思路**，就算过。

---

## 1. f-string —— 把变量塞进字符串

**Python**
```python
name = "云南古树核桃认养"
price = "¥688"
print(f"商品：{name}，价格：{price}")
```

**JS 里你项目里对应的写法**
```js
console.log(`商品：${name}，价格：${price}`);
```

| 要点 | 说明 |
|---|---|
| `f"..."` 前面那个 **f 是必须的**，漏了就会原样打印 `{name}` | |
| `{}` 里可以放变量，也可以放表达式：`f"{price * 2}"` | |
| 调试时常用：`print(f"user_id={user_id}, token={token[:8]}")` | 切片 `[:8]` = 只取前 8 个字符 |

---

## 2. 字典取值 —— 和 JS 的区别在"取不到会怎样"

**Python**
```python
d = {"id": "fa001", "price": "¥688"}
print(d["id"])        # 正常
print(d.get("stock")) # 取不到 -> None（不报错）
print(d["stock"])     # 取不到 -> KeyError（会崩）
```

**JS**
```javascript
d.id;        // undefined
d["stock"];  // undefined
```

| | 取不到时 |
|---|---|
| Python `d["k"]` | **抛 KeyError，程序崩** |
| Python `d.get("k")` | 返回 `None`，程序继续 |
| JS `d.k` | 返回 `undefined` |

> ⚠️ **这条是 Python 和 JS 最大的日常差异之一。** 写自动化脚本时，从接口返回的 JSON 里取字段，
> 用 `.get()` 比 `["x"]` 安全得多——**接口没返回某个字段时，脚本不该直接崩掉，而是让断言失败并说清缺了什么**。

---

## 3. 列表遍历 —— 两种写法，别混

```python
products = [{"id": "fa001", "price": 688}, {"id": "fa002", "price": 1288}]

# 写法 A：只要值
for p in products:
    print(p["id"])

# 写法 B：要下标 / 位置
for i, p in enumerate(products):
    print(i, p["id"])
```

**JS**
```javascript
products.forEach((p, i) => console.log(p.id));
```

| 场景 | 用哪个 |
|---|---|
| 只关心每个商品本身 | 写法 A |
| 报错信息里要写"第 3 个商品失败了" | 写法 B（`enumerate`） |

> 💡 **这就是测试脚本里最常见的需求**：断言失败时要能说清"是哪一个"。

---

## 4. 今日练习（**先自己写，别看答案**）

> 规则：写在纸上或记事本里，写完再往下看。这三题对应后面 D2/D6 会用到的能力。

**第 1 题（字典 + f-string）**
接口返回：
```json
{"products": [{"id": "fa001", "name": "云南古树核桃认养", "price": "¥688", "stock": 999}]}
```
写一段 Python，把**第一个商品的 id 和价格**打印成这一行：
```
[fa001] ¥688
```
提示：`data["products"][0]` 拿到第一个商品。

**第 2 题（`.get` vs `[]`）**
下面这段代码，在商品没有 `stock` 字段时会发生什么？打印出什么？
```python
p = {"id": "fa001", "price": "¥688"}
print(p.get("stock", 0))
print(p["stock"])
```
先说结论，再说明理由。

**第 3 题（enumerate）**
有一个用例列表：
```python
cases = [
    {"name": "数量为0", "expect": 400},
    {"name": "数量为负数", "expect": 400},
    {"name": "数量超大", "expect": 400},
]
```
写一段循环，**只把 expect 不是 200 的用例打印出来**，并且打印格式是：
```
[2/3] 数量超大 -> expect 400
```
（第几个 / 总共几个，用例名，期望值）

---

## 5. 今天可以直接跑的 5 行脚本

把它存成 `scratch/day01.py`，跑一下，看懂每一行：

```python
import sqlite3
con = sqlite3.connect("../一季一鲜助农电商平台源代码/源代码/backend/db.sqlite")
for row in con.execute("SELECT id, name, price, stock FROM products LIMIT 3"):
    print(f"[{row[0]}] {row[1]}  {row[2]}  库存={row[3]}")
con.close()
```

**逐行解释**（对照你项目里的 JS）：

| Python | 你项目里对应的 JS | 说明 |
|---|---|---|
| `import sqlite3` | `const db = require('./database')` | 引一个库进来 |
| `sqlite3.connect(path)` | `new sqlite3.Database(path)` | 打开数据库文件 |
| `con.execute("SELECT ...")` | `db.all("SELECT ...", params, cb)` | 执行 SQL |
| `for row in con.execute(...)` | `db.all(..., (err, rows) => rows.forEach(...))` | 遍历结果集；**row 是元组**（tuple），用 `row[0]` 取第 1 列 |
| `f"[{row[0]}] ..."` | `` `[${row[0]}]` `` | 拼字符串 |
| `con.close()` | — | 关连接 |

> 📌 顺手记住一个差异：**Python 的 SQL 是"同步"的**（`execute` 直接拿到结果），JS 的 `db.all` 是**回调**（要等）。
> 这就是为什么 Python 脚本读数据比 JS 直觉得多，也是我们后面写对账 SQL 会很快的原因。

---

## 6. 今天的自检（能答就是过）

1. `f"{x}"` 里的 `f` 忘了写会怎样？
2. `d["k"]` 和 `d.get("k")` 在 key 不存在时分别发生什么？
3. `for i, p in enumerate(xs)` 里 `i` 是什么？
4. `con.execute(...)` 返回的东西能直接 `for` 吗？
5. Python 里取到的每一行是 dict 还是 tuple？（→ 这决定你写 `row["id"]` 还是 `row[0]`）

答不上来的不要紧，记下来，D2 开头我们再讲一遍。

---

## 7. 明天要用的（先知道存在就行）

| 明天要用 | 现在知道它是什么 |
|---|---|
| `sqlite3.Row` | 让 `row["id"]` 也能用（默认是 tuple，只能 `row[0]`） |
| `with sqlite3.connect(...) as con:` | 退出时自动提交/回滚 → 事务 |
| 事务 | 一组操作要么全成功要么全失败 → **并发超卖缺陷的解药就在这** |
