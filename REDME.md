# 🏨 Hotel Management System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/UI-PyQt6-green.svg)](https://pypi.org/project/PyQt6/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Build-Stable-success.svg)]()

A powerful and modern **Hotel Management System** built using **PyQt6** and **MySQL**.  
It provides two main portals — **Booking Portal** for guests and **Management Portal** for administrators/staff — with a clean UI, animated interactions, and robust database operations.

---

## 🧭 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Requirements](#requirements)
5. [Project Structure](#project-structure)
6. [Setup & Installation](#setup--installation)
7. [How to Run](#how-to-run)
8. [Screenshots](#screenshots)
9. [Future Enhancements](#future-enhancements)
10. [Author](#author)
11. [License](#license)

---

## 🧾 Overview

This Hotel Management System enables seamless **room booking**, **guest management**, and **hotel administration** from a single interface.

- The **Booking Portal** simplifies guest bookings and payment handling.  
- The **Management Portal** offers comprehensive tools for staff to manage bookings, customers, and reports.  
- The system generates **PDF invoices** for every booking and allows **search & filter operations** for quick data access.

It’s a complete end-to-end desktop solution for medium and small hotels.

---

## 🌟 Features

### 🏠 Booking Portal
- User-friendly room booking system.
- Real-time room availability check.
- Guest detail entry and stay duration tracking.
- Instant **PDF invoice generation** upon booking confirmation.
- Smooth loading animations using `spinner.gif`.

### 🛠️ Management Portal
- Secure admin login with password toggle (`Eye_open.svg`, `Eye_close.svg`).
- Add, update, and delete room and booking records.
- **Search and filter** functions for rooms, customers, and bookings.
- Manage check-ins, check-outs, and cancellations.
- Status indicators for database connectivity.
- Window control icons for custom frameless design (`maximize.svg`, `minimize.svg`, `restore.svg`, `close.svg`).

---

## 🧰 Technology Stack

| Component | Technology |
|------------|-------------|
| **Programming Language** | Python 3.10+ |
| **UI Framework** | PyQt6 |
| **Database** | MySQL |
| **Database Connector** | PyMySQL |
| **Scheduler** | schedule |
| **UI Assets** | SVG, PNG, GIF |
| **Invoice Generation** | ReportLab or FPDF (PDF creation library) |

---

## 📋 Requirements

### 📦 Python Packages

Install all dependencies with:

```bash
pip install PyQt6 pymysql schedule reportlab
