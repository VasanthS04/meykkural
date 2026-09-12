# Meykkural System Architecture

## 1. Overview

Meykkural is an AI-powered voice authenticity and deepfake detection platform.

The system is designed to analyze speech audio and estimate whether the audio is:

- Genuine human speech
- Suspicious speech
- AI-generated speech
- Voice-cloned speech
- Potentially manipulated audio

The platform supports both:

1. Uploaded audio analysis
2. Real-time audio monitoring

---

# 2. High-Level Architecture

```text
                    ┌─────────────────────────┐
                    │       User / Admin       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     React Frontend      │
                    │                         │
                    │  Live Monitor           │
                    │  Voice Analysis         │
                    │  Model Intelligence     │
                    │  Security Alerts        │
                    └────────────┬────────────┘
                                 │
                    HTTP / WebSocket
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      FastAPI Backend     │
                    └────────────┬────────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               │                 │                 │
               ▼                 ▼                 ▼
        Audio Processing     Feature Extraction   Privacy
               │                 │
               │                 ▼
               │          ┌─────────────────┐
               │          │ ML Model Layer  │
               │          └────────┬────────┘
               │                   │
               │     ┌─────────────┼─────────────┐
               │     │             │             │
               │     ▼             ▼             ▼
               │   AASIST       RawNet2       XLS-R
               │   ProS-DD      Conformer      ECAPA
               │
               └──────────────────┐
                                  ▼
                         ┌─────────────────┐
                         │ Score Fusion    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Calibration     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Risk Engine     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Security Alert  │
                         └─────────────────┘