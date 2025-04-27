# AirKey

**AirKey** is a gesture-driven password authentication system using Leap Motion, MongoDB, and Arduino feedback.

## Features
- Real-time Leap Motion gesture capture (frame segmentation + swipe detection)
- MongoDB Atlas integration for user/password lookups and access logging
- Arduino serial feedback via `pySerial`
- Modular, well-documented Python package

## Installation

```bash
git clone https://github.com/nehanmohammed19/Air-Key.git
cd Air-Key
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
