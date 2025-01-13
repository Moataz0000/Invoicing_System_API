# Invoice Management System

A Django-based Invoice Management System that allows users to create, manage, and export invoices. Users can also manage clients, export invoices as PDF or CSV, and send invoices via email.

## Features

- **Invoice Management**: Create, read, update, and delete invoices.
- **Client Management**: Add, edit, and delete clients.
- **Export Invoices**: Export invoices as PDF or CSV.
- **Email Invoices**: Send invoices directly via email.
- **Authentication**: Secure API endpoints with token-based authentication.
- **User-Specific Data**: Users can only access their own invoices.

## Technologies Used

- **Backend**: Django, Django Rest Framework (DRF)
- **Database**: SQLite (default), PostgreSQL (production-ready)
- **Authentication**: Token Authentication
- **Export Libraries**: ReportLab (PDF), Pandas (CSV)


### API Endpoints

| Endpoint                              | Method | Description                              |
|---------------------------------------|--------|------------------------------------------|
| `/api/register/`                      | POST   | Register a new user                      |
| `/api/api-token-auth/`                | POST   | Obtain an authentication token           |
| `/api/invoices/`                      | GET    | List all invoices (user-specific)        |
| `/api/invoices/`                      | POST   | Create a new invoice                     |
| `/api/invoices/<invoice_id>/`         | GET    | Retrieve a specific invoice              |
| `/api/invoices/<invoice_id>/`         | PUT    | Update a specific invoice                |
| `/api/invoices/<invoice_id>/`         | DELETE | Delete a specific invoice                |
| `/api/invoices/<invoice_id>/pdf/`     | GET    | Export an invoice as PDF                 |
| `/api/invoices/<invoice_id>/csv/`     | GET    | Export an invoice as CSV                 |
| `/api/clients/`                       | GET    | List all clients (user-specific)         |
| `/api/clients/`                       | POST   | Create a new client                      |
| `/api/clients/<client_id>/`           | GET    | Retrieve a specific client               |
| `/api/clients/<client_id>/`           | PUT    | Update a specific client                 |
| `/api/clients/<client_id>/`           | DELETE | Delete a specific client                 |


## Invoice As A PDF

![Screenshot from 2025-01-13 09-30-37](https://github.com/user-attachments/assets/bba5380d-abb8-4ff0-af43-11ed3fefdaac)
