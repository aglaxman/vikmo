# 🚗 Sales Order & Inventory Lite – VIKMO

## 📌 Project Overview

This project is a **Sales Order & Inventory Management System** built using **Django** and **Django REST Framework**.

It simulates a simplified backend of the **VIKMO B2B auto-parts distribution platform**, where dealers place orders for products and the system manages stock levels automatically.

The system ensures:

- **Inventory tracking**
- **Order validation**
- **Automatic stock deduction**
- **Controlled order status transitions**

---

# ✨ Features Implemented

## 📦 Product Management

- Create and manage products  
- Each product has a **unique SKU**
- Store **pricing information**
- Search products by **SKU or product name**

---

## 👨‍💼 Dealer Management

- Manage dealer/customer information
- Dealers can **place multiple orders**
- Store dealer **contact details**

---

## 📊 Inventory Tracking

- Maintain **stock quantity for each product**
- Inventory can be **manually adjusted**
- Stock automatically updates when **orders are confirmed**

---

## 🧾 Order Management

- Dealers can create **orders with multiple items**
- Orders maintain **price at the time of purchase**
- Order numbers are **automatically generated**

Example order number:

```
ORD-20260312-0001
```

---

## 🔄 Order Status System

Orders follow a strict workflow:

```
Draft → Confirmed → Delivered
```

| Status | Description |
|------|-------------|
| **Draft** | Order can be edited |
| **Confirmed** | Stock deducted and order locked |
| **Delivered** | Final state – order completed |

Invalid status transitions are **rejected with errors**.

---

# ⚙️ Business Logic Implementation

## ✔ Stock Validation

When confirming an order:

- System checks **available inventory**
- If requested quantity exceeds stock → confirmation fails

Example error:

```
Insufficient stock for Brake Pad. Available: 5, Requested: 10
```

---

## 📉 Stock Deduction

Stock deduction happens **only when order status changes**:

```
Draft → Confirmed
```

This ensures:

- Draft orders **do not affect stock**
- Only confirmed purchases **reduce inventory**

Database **atomic transactions** prevent race conditions.

---

## ✏️ Order Editing Rules

| Order Status | Editable |
|--------------|---------|
| Draft | ✅ Yes |
| Confirmed | ❌ No |
| Delivered | ❌ No |

Editing confirmed or delivered orders returns an **error**.

---

# 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Framework | Django |
| API Framework | Django REST Framework |
| Database | SQLite |
| API Testing | Postman |

---

# ⚡ Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/vikmo-assignment.git
cd vikmo-assignment
```

---

## 2. Create Virtual Environment

```bash
python -m venv env
```

Activate environment:

### Windows

```bash
env\Scripts\activate
```

### Mac / Linux

```bash
source env/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5. Run Server

```bash
python manage.py runserver
```

Server will run at:

```
http://127.0.0.1:8000/
```

---

# 📁 Project Structure

```
project/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── project_name/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── app_name/
    ├── models.py
    ├── views.py
    ├── serializers.py
    ├── urls.py
```
# 📷 Project Snapshots

| Products | Dealers |
|----------|---------|
| <img src="https://github.com/user-attachments/assets/4eb1e718-cfea-4e48-86e6-f0472bb77cb5" width="500"/> | <img src="https://github.com/user-attachments/assets/a1a35dc0-4dad-4bbf-81a3-08444e1d9c15" width="500"/> |

| Orders | Inventory |
|--------|-----------|
| <img src="https://github.com/user-attachments/assets/85e339d5-4fa5-4266-9d02-222e72b625e1" width="500"/> | <img src="https://github.com/user-attachments/assets/9a64f158-fd98-4d70-82d3-b1008fbd1f70" width="500"/> |
---

# 📌 Assumptions

- Each product has **one inventory record**
- Stock deduction occurs **only on order confirmation**
- Confirmed orders **cannot be modified**
- Delivered orders represent **final transactions**
- Historical order prices **remain unchanged even if product prices change**

---

# 🚀 Future Improvements

- Authentication & role-based permissions  
- Inventory audit logs  
- Pagination and filtering  
- Order reporting features  
- Automated tests  
- Docker deployment  

---

# 👨‍💻 Author

**Laxmanna A Goudar**

VIKMO Fresher Developer Assignment
