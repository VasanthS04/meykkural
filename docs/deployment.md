# Meykkural – Deployment Guide

## 1. Overview

Meykkural consists of:

- React + Vite frontend
- Python + FastAPI backend
- AI inference pipeline
- Audio processing
- WebSocket communication
- Optional WebRTC/VoIP integration

The deployment architecture is:

```text
User Browser
     │
     ▼
Frontend
React + Vite
     │
     │ HTTPS / WSS
     ▼
FastAPI Backend
     │
     ▼
Audio Processing
     │
     ▼
AI Models
     │
     ▼
Risk Engine
     │
     ▼
Detection Result
