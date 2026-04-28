#Unifirst Order & Maintenance Order Entry System

A full-stack industrial reporting tool designed to streamline complex uniform and facility service orders.

## Features 
Dynamic Form Entry: Real-Time addition of Facility Items and Wearers.
Complex Logic: Handles ABUS tracking, Systematic Replacment rates, and Delivery Variations.
Automated PDF Generation: Generates a professionnally formatted Unifirst order form with a calculated grand total.
Responsive UI: A sticky footer designed for high efficiency data entry.
## Tech Stack
Frontend: Angular 17+ (Standalone Components), Bootstrap 5.
Backend: FastAPI (Python 3.x), Uvicorn
PDF Engine: ReportLab
State Management: Reactive Forms & ngModel
## Installation
Backend: 
-'cd size-right-backend'
-'pip install fastapi uvicorn reportlab pydantic'
-'uvicorn main:app --reload'
Frontend:
-'cd size-right-frontend'
-'npm install'
-'npm install file-saver'
-'ng serve'