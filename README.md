# Industrial Event Stream Simulator

A lightweight industrial software project that simulates machine-state events, stores them in a relational database, and exposes operational metrics through a FastAPI backend.

## Why I built this

This project demonstrates backend engineering patterns relevant to industrial software platforms:

- machine-state event modeling
- real-time operational data capture
- downtime analysis
- production metrics APIs
- manufacturing-style reporting workflows

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite

## Architecture

```text
Machine Simulator → SQLite Event Store → FastAPI → Metrics Endpoints
