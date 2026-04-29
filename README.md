# SizeRight: Industrial Service & Maintenance Order System

A full-stack industrial reporting tool designed to streamline complex uniform and facility service orders, automated reporting, and maintenance tracking.

## Features 
Dynamic Form Entry: Real-Time addition of Facility Items and Wearers with reactive state management.
Complex Logic: Handles ABUS tracking, Systematic Replacment rates, and Delivery Variations.
Automated PDF Generation: Generates a professionnally formatted order form with a calculated grand total.
Responsive UI: A mobile-friendly design sticky footer designed for high efficiency data entry.
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
## Disclaimer
This application is an independent prototype developed for educational purposes and workflow optimization. It is not an official corporate application and is intended for portfolio demonstration.