# Industrial Event Stream Simulator

A lightweight industrial software project that simulates machine-state events, stores them in a SQLite database, and exposes operational metrics through a FastAPI backend.

## Project Summary

This project demonstrates backend engineering patterns relevant to industrial software platforms and manufacturing data systems. It simulates machine events, captures them in a relational database, and surfaces operational data through API endpoints for reporting and analytics.

## Why I Built This

I built this project to strengthen and demonstrate backend software engineering skills in an industrial context. It reflects patterns commonly used in manufacturing software systems, including machine-state modeling, event-driven data capture, downtime tracking, and production metrics reporting.

## Tech Stack

- Python
- FastAPI
- SQLite

## Architecture

```text
Machine Simulator → SQLite Event Store → FastAPI → Metrics Endpoints
<img width="936" height="1011" alt="image" src="https://github.com/user-attachments/assets/538751ab-fe5d-4e78-961c-1a6067cf96d1" />

