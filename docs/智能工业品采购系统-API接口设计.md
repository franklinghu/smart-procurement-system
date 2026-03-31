# 智能工业品采购系统 - API 接口设计

**版本**: 1.0
**日期**: 2026-03-30

---

## 一、接口总体设计

### 1.1 接口规范

- **协议**: HTTP/RESTful + WebSocket（实时通知）
- **数据格式**: JSON
- **编码**: UTF-8
- **认证方式**: JWT Bearer Token
- **版本管理**: URL路径版本化 `/api/v1/`

### 1.2 响应格式

**成功响应**
```json
{
  "code": 0,
  "message": "success",
  "data": { },
  "timestamp": "2026-03-30T10:00:00Z"
}
```

**错误响应**
```json
{
  "code": 1001,
  "message": "参数错误",
  "details": { },
  "timestamp": "2026-03-30T10:00:00Z"
}
```

### 1.3 公共错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 参数错误 |
| 1002 | 缺少必填参数 |
| 1003 | 参数格式错误 |
| 2001 | 未授权 |
| 2002 | Token过期 |
| 2003 | 权限不足 |
| 3001 | 资源不存在 |
| 3002 | 资源已存在 |
| 4001 | 业务逻辑错误 |
| 5001 | 系统内部错误 |

---

## 二、用户服务 API (User Service)

**基础路径**: `/api/v1/users`

### 2.1 认证管理

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /auth/login | 账号密码登录 |
| POST | /auth/logout | 登出 |
| POST | /auth/refresh | 刷新Token |
| POST | /auth/mfa/verify | MFA验证 |

**登录请求**
```json
POST /api/v1/users/auth/login
{
  "username": "admin",
  "password": "encrypted_password"
}
```

**登录响应**
```json
{
  "code": 0,
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "expires_in": 7200,
    "token_type": "Bearer",
    "user": {
      "id": "uuid",
      "username": "admin",
      "real_name": "管理员",
      "role": "tenant_admin",
      "tenant_id": "uuid"
    }
  }
}
```

### 2.2 用户管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 获取用户列表 |
| GET | /{id} | 获取用户详情 |
| POST | / | 创建用户 |
| PUT | /{id} | 更新用户 |
| DELETE | /{id} | 删除用户 |
| PUT | /{id}/password | 修改密码 |
| PUT | /{id}/status | 更新用户状态 |

---

## 三、商品服务 API (Goods Service)

**基础路径**: `/api/v1/goods`

### 3.1 商品管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 获取商品列表 |
| GET | /{id} | 获取商品详情 |
| POST | / | 创建商品 |
| PUT | /{id} | 更新商品 |
| DELETE | /{id} | 删除商品 |
| GET | /categories | 获取商品分类 |
| GET | /search | 搜索商品 |

**商品列表响应**
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "id": "uuid",
        "name": "M8x25mm 六角螺栓",
        "code": "BOLT-M8-25",
        "category_name": "紧固件 > 螺栓",
        "unit": "pcs",
        "images": ["url1", "url2"],
        "status": "active"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}
```

### 3.2 供应商管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /suppliers | 获取供应商列表 |
| GET | /suppliers/{id} | 获取供应商详情 |
| POST | /suppliers | 创建供应商 |
| PUT | /suppliers/{id} | 更新供应商 |
| DELETE | /suppliers/{id} | 删除供应商 |

---

## 四、比价服务 API (Price Service)

**基础路径**: `/api/v1/prices`

### 4.1 比价查询

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /compare |发起比价请求 |
| GET | /compare/{task_id} | 获取比价结果 |
| POST | /compare/refresh | 强制刷新价格 |

**比价请求**
```json
POST /api/v1/prices/compare
{
  "goods_name": "M8x25mm 六角螺栓",
  "goods_spec": "GB/T 5783",
  "quantity": 100,
  "platforms": ["zkh", "west", "jd"]
}
```

**比价响应**
```json
{
  "code": 0,
  "data": {
    "task_id": "uuid",
    "status": "completed",
    "results": [
      {
        "platform": "zkh",
        "platform_name": "震坤行",
        "price": 8.50,
        "original_price": 10.00,
        "discount_rate": 15.0,
        "stock_status": "in_stock",
        "stock_quantity": 10000,
        "moq": 10,
        "delivery_days": 2,
        "supplier_name": "震坤行自营",
        "product_url": "https://...",
        "cached_at": "2026-03-30T09:00:00Z"
      },
      {
        "platform": "west",
        "platform_name": "西域",
        "price": 8.80,
        "stock_status": "in_stock",
        "moq": 20,
        "delivery_days": 3
      },
      {
        "platform": "jd",
        "platform_name": "京东工业品",
        "price": 9.20,
        "stock_status": "in_stock",
        "moq": 1,
        "delivery_days": 1
      }
    ],
    "sorted_by": "comprehensive",
    "best_match": {
      "platform": "zkh",
      "reason": "价格最低 + 交货快"
    }
  }
}
```

### 4.2 价格缓存

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /cache/{goods_id} | 获取缓存价格 |
| DELETE | /cache/{goods_id} | 清除缓存 |

---

## 五、采购服务 API (Purchase Service)

**基础路径**: `/api/v1/purchases`

### 5.1 采购申请

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /orders | 获取采购申请列表 |
| GET | /orders/{id} | 获取采购申请详情 |
| POST | /orders | 创建采购申请 |
| PUT | /orders/{id} | 更新采购申请 |
| DELETE | /orders/{id} | 删除采购申请 |
| POST | /orders/{id}/submit | 提交审批 |
| POST | /orders/{id}/withdraw | 撤回申请 |

**创建采购申请**
```json
POST /api/v1/purchases/orders
{
  "goods_id": "uuid",
  "goods_name": "M8x25mm 六角螺栓",
  "goods_spec": "GB/T 5783",
  "supplier_id": "uuid",
  "supplier_name": "震坤行",
  "quantity": 100,
  "unit_price": 8.50,
  "total_amount": 850.00,
  "delivery_place": "上海市嘉定区工厂",
  "payment_method": "monthly",
  "department": "生产部",
  "project_name": "产线改造项目",
  "usage_desc": "产线设备维护",
  "is_urgent": false
}
```

**采购申请响应**
```json
{
  "code": 0,
  "data": {
    "id": "uuid",
    "order_no": "PR-20260330-001",
    "status": "pending",
    "current_approver": {
      "id": "uuid",
      "name": "部门经理"
    },
    "created_at": "2026-03-30T10:00:00Z"
  }
}
```

### 5.2 审批流程

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /approvals | 获取待审批列表 |
| GET | /approvals/{order_id} | 获取审批详情 |
| POST | /approvals/{order_id}/approve | 审批通过 |
| POST | /approvals/{order_id}/reject | 审批驳回 |
| POST | /approvals/{order_id}/transfer | 转交审批 |

**审批请求**
```json
POST /api/v1/purchases/approvals/{order_id}/approve
{
  "comment": "同意采购，请及时跟进交货"
}
```

### 5.3 审批配置

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /workflows | 获取审批流程列表 |
| GET | /workflows/{id} | 获取流程详情 |
| POST | /workflows | 创建审批流程 |
| PUT | /workflows/{id} | 更新审批流程 |
| DELETE | /workflows/{id} | 删除审批流程 |

---

## 六、通知服务 API (Notify Service)

**基础路径**: `/api/v1/notifications`

### 6.1 消息通知

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 获取通知列表 |
| GET | /{id} | 获取通知详情 |
| PUT | /{id}/read | 标记已读 |
| PUT | /read-all | 全部标记已读 |
| DELETE | /{id} | 删除通知 |

### 6.2 消息模板

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /templates | 获取模板列表 |
| POST | /templates | 创建模板 |
| PUT | /templates/{id} | 更新模板 |

---

## 七、ERP对接服务 API (ERP Service)

**基础路径**: `/api/v1/erp`

### 7.1 ERP配置

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /configs | 获取ERP配置列表 |
| GET | /configs/{id} | 获取配置详情 |
| POST | /configs | 创建ERP配置 |
| PUT | /configs/{id} | 更新ERP配置 |
| DELETE | /configs/{id} | 删除配置 |
| POST | /configs/{id}/test | 测试连接 |

**创建ERP配置**
```json
POST /api/v1/erp/configs
{
  "erp_type": "yongyou_u8",
  "erp_name": "用友U8",
  "api_url": "https://erp.company.com/api",
  "account": "001",
  "app_key": "xxx",
  "app_secret": "xxx",
  "field_mapping": {
    "order_no": "PO_PurchaseOrder",
    "supplier_code": "Supplier_Code",
    "goods_code": "Inventory_Code",
    "quantity": "Quantity"
  }
}
```

### 7.2 订单同步

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /sync/orders | 获取同步记录 |
| POST | /sync/orders/{order_id} | 手动同步订单 |
| GET | /sync/logs/{order_id} | 获取同步日志 |

### 7.3 同步状态

| 状态 | 说明 |
|------|------|
| pending | 待同步 |
| syncing | 同步中 |
| success | 同步成功 |
| failed | 同步失败 |

---

## 八、多租户管理 API

**基础路径**: `/api/v1/tenants` (仅超级管理员)

### 8.1 租户管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 获取租户列表 |
| GET | /{id} | 获取租户详情 |
| POST | / | 创建租户 |
| PUT | /{id} | 更新租户 |
| DELETE | /{id} | 删除租户 |
| POST | /{id}/activate | 激活租户 |
| POST | /{id}/disable | 禁用租户 |

---

## 九、WebSocket 实时通知

**WebSocket 路径**: `/ws/notifications`

### 9.1 连接认证

```
ws://host/ws/notifications?token=eyJhbGc...
```

### 9.2 消息类型

| 事件 | 说明 |
|------|------|
| notification.new | 新通知 |
| approval.pending | 待审批提醒 |
| approval.result | 审批结果通知 |
| erp.sync.status | ERP同步状态变更 |
| price.alert | 价格异常提醒 |

**WebSocket 消息格式**
```json
{
  "type": "notification.new",
  "data": {
    "id": "uuid",
    "title": "新的采购审批",
    "content": "您有一笔采购申请需要审批",
    "link_url": "/purchase/approvals/xxx"
  },
  "timestamp": "2026-03-30T10:00:00Z"
}
```

---

## 十、分页与过滤

### 10.1 分页参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| page | 页码 | 1 |
| page_size | 每页数量 | 20 |
| max_page_size | 最大每页数量 | 100 |

### 10.2 排序参数

| 参数 | 说明 |
|------|------|
| sort_by | 排序字段 |
| order | 排序方式：asc/desc |

### 10.3 过滤参数

| 参数 | 说明 | 示例 |
|------|------|------|
| status | 状态过滤 | status=active |
| created_at_start | 创建时间起 | created_at_start=2026-01-01 |
| created_at_end | 创建时间止 | created_at_end=2026-12-31 |
| keyword | 关键词搜索 | keyword=螺栓 |

---

## 十一、安全设计

### 11.1 认证

- 所有API需携带JWT Token
- Token有效期：2小时（access_token）
- 刷新Token有效期：7天

### 11.2 权限控制

- 基于RBAC的权限模型
- 接口级别权限校验
- 数据级别租户隔离

### 11.3 限流

- 登录接口：5次/分钟
- 查询接口：60次/分钟
- 写操作接口：30次/分钟

### 11.4 审计日志

- 记录所有管理操作
- 记录敏感数据访问
- 日志保留≥1年

---

## 十二、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0 | 2026-03-30 | 初始版本 |

---

*API接口设计完成*