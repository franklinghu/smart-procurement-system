# 智能工业品采购系统 (Procurement System)

> MVP 开发中 | 技术栈：Vue 3 + FastAPI + PostgreSQL

## 快速开始

### 前端
```bash
cd frontend
npm install
npm run dev
```

### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 项目结构

```
procurement-system/
├── frontend/          # Vue 3 前端
│   ├── src/
│   │   ├── api/      # API 接口
│   │   ├── assets/   # 静态资源
│   │   ├── components/ # 公共组件
│   │   ├── router/  # 路由配置
│   │   ├── store/   # 状态管理
│   │   ├── utils/   # 工具函数
│   │   └── views/   # 页面视图
│   └── package.json
├── backend/          # FastAPI 后端
│   ├── app/
│   │   ├── api/     # API 路由
│   │   ├── core/    # 核心配置
│   │   ├── models/  # 数据模型
│   │   ├── schemas/ # Pydantic schemas
│   │   └── services/# 业务逻辑
│   └── requirements.txt
└── docs/             # 文档
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Element Plus + Vite |
| 后端 | Python FastAPI + SQLAlchemy |
| 数据库 | PostgreSQL + Redis |
| 部署 | Docker |

## 开发规范

- 分支命名：`feature/功能名`、`bugfix/问题描述`
- Commit：`[模块] 描述`
- 代码Review后合并

---

**版本**：v0.1.0 | **状态**：开发中