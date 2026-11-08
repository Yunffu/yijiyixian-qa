# 一季一鲜 · 接口自动化测试工程

> 面向 [`Yunffu/yijiyixian-v2`](https://github.com/Yunffu/yijiyixian-v2)（一季一鲜助农电商平台）的
> **接口自动化测试工程**：以「业务不变量」为断言主轴，同一套测试 harness 对照
> **Node 原版 SUT** 与 **Python/FastAPI 重写版 SUT**，验证迁移是否保持语义等价。

| | |
|---|---|
| 项目名称 | 一季一鲜接口自动化测试工程 |
| 角色 | 独立开发（用例设计 → 脚本实现 → 缺陷定位 → 回归维护） |
| 被测对象 | HTTP 接口（Express 原版 / FastAPI 重写版） |
| 技术栈 | Python + pytest + requests + FastAPI + SQLite + PyJWT + bcrypt |
| 仓库 | `Yunffu/yijiyixian-qa` |
| 关联仓库 | [`yijiyixian`](https://github.com/Yunffu/yijiyixian)（v1 存档） / [`yijiyixian-v2`](https://github.com/Yunffu/yijiyixian-v2)（完善版） |

---

## 1. 核心思路：断言不变量，而不是断言状态码

只断言 HTTP 200 抓不到真正的业务缺陷。本工程以 **5 条业务不变量** 为主断言轴，
每条不变量都能同时表达为「响应字段断言」和「数据库终态断言」：

| # | 不变量 | 含义 |
|---|---|---|
| 1 | **库存守恒** | 初始库存 = 期末库存 + 所有有效订单数量之和（取消的订单要回滚） |
| 2 | **金额守恒** | `total_price = 单价 × 数量`，且取自**下单时价格快照** |
| 3 | **库存非负** | 任何路径下 `stock >= 0`，并发下不超卖 |
| 4 | **订单归属** | 只能读取/取消自己的订单（横向越权走不通） |
| 5 | **状态机合法迁移** | `pending → cancelled` 合法；`cancelled → cancelled` 非法 |

---

## 2. 已定位的高危缺陷（在 v1 上实测复现）

| # | 缺陷 | 复现证据 |
|---|---|---|
| 1 | `quantity` 无正整数校验 → 负数令库存虚增 | 库存 999 → **1004**（`server.js:329 / 377`） |
| 2 | `total_price` 返回单价而非「单价 × 数量」，且 `price` 为 TEXT | `quantity=2` → `total_price="¥1288"`（`server.js:387`） |
| 3 | 库存扣减「读-判-写」未 await 且无事务 → 并发超卖 | 12 并发抢 5 件库存 → **12 单全成功、stock = -7** |

详细复现脚本与数据库前后快照见 `docs/` 与 `spec/`。

---

## 3. 目录结构

```
一季一鲜测试工程/
├── docs/
│   ├── 链路-认养下单.md          # 全链路图（带文件行号），吃透阶段的产出
│   └── 学习笔记-01-python.md     # D1 Python 速通笔记 + 动手任务
├── harness/                      # 与 SUT 无关的公共断言/夹具层
├── spec/cases/                   # 用例矩阵（参数化数据）
├── sut_py/                       # Python/FastAPI 重写版 SUT
├── sql/                          # 对账 SQL
├── perf/                         # 压测脚本
├── trace/                        # trace 记录（本地，不入库）
├── report/                       # Allure 风格报告（本地，不入库）
├── scratch/                      # 临时脚本与个人笔记
└── requirements.txt
```

---

## 4. 版权与使用声明

- 本测试工程是作者**对自己作品**（一季一鲜助农电商平台）的质量建设，版权归两位作者共同所有。
- 被测产品的**创意、内容、素材等一切权利归两位作者共同所有**，**严禁商用、严禁抄袭创意**；
  完整条款见 [`yijiyixian` 仓库的 LICENSE](https://github.com/Yunffu/yijiyixian/blob/main/LICENSE)。
- 本仓库仅供学习、研究与非商业展示；引用须标注作者与出处。

---

## 5. 快速开始

```bash
python -m venv .venv && source .venv/Script/activate   # Windows
pip install -r requirements.txt

# 读数据脚本（D1 练手）
python scratch/day01.py
```

---

## 5. 计划中的能力

- [ ] pytest fixture 事务回滚（跑前跑后 DB 行数一致）
- [ ] `@pytest.mark.parametrize("sut", ["node", "python"])` 双 SUT 参数化
- [ ] 轨迹断言（tool_called / max_tool_calls）
- [ ] record / replay 回放 + `pass^k` 稳定性
- [ ] 失败归因分类（规划 / 事实 / 工具选择 / 权限 / 超时 / 评分器）
- [ ] GitHub Actions CI
