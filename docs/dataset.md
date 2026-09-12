# Meykkural – Dataset Documentation

## 1. Purpose

The dataset is used to train, validate, and evaluate the Meykkural voice deepfake detection system.

The dataset should contain both:

- Bonafide / genuine human speech
- Spoof / synthetic / manipulated speech

The primary objective is to teach the detection system to distinguish authentic speech from artificially generated or manipulated speech.

---

## 2. Dataset Classes

The basic classification structure is:

```text
Dataset
│
├── bonafide/
│   ├── speaker_001/
│   ├── speaker_002/
│   └── ...
│
└── spoof/
    ├── speaker_001/
    ├── speaker_002/
    └── ...