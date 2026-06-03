# BMK Timesheet — Django + DRF

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```

Then open: http://127.0.0.1:8000/

## Pages
| URL | Description |
|-----|-------------|
| `/` | Dashboard — today's entries, monthly project hours |
| `/timesheet/` | Daily Sheet — add/edit/delete entries with project hours |
| `/projects/` | Projects — add, edit, deactivate, delete projects |
| `/employees/` | Employees — manage team members |
| `/api/` | DRF Browsable API |
| `/admin/` | Django Admin |

## API Endpoints
| Method | URL | Action |
|--------|-----|--------|
| GET/POST | `/api/projects/` | List / Create projects |
| GET/PUT/DELETE | `/api/projects/{id}/` | Retrieve / Update / Delete |
| POST | `/api/projects/{id}/toggle_active/` | Toggle active status |
| GET/POST | `/api/employees/` | List / Create employees |
| GET/POST | `/api/entries/` | List / Create timesheet entries |
| GET/PUT/DELETE | `/api/entries/{id}/` | Retrieve / Update / Delete entry |
| GET | `/api/entries/summary/?year=&month=` | Monthly summary by employee+project |
| GET | `/api/entries/weekly/?year=&week=` | Weekly entries |

## Filters
- `/api/entries/?date=2026-05-22`
- `/api/entries/?employee=1&year=2026&month_number=5`
- `/api/projects/?is_active=true`

## Data Model
- **Project**: code (BMK, ATLAS…), name, description, is_active
- **Employee**: name, is_active
- **TimesheetEntry**: date, employee, status (present/leave/holiday), task_description, total_hours  
  → auto-computes week_number, month_number, year from date
- **ProjectHours**: entry → project, hours (links hours to specific project per day)
