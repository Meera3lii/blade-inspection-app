# Blade Inspection AI

Automated turbine blade defect inspection using YOLOv8 + Claude API.

Upload one or more blade images and receive a formal engineering inspection report.

## How It Works

1. User uploads blade images via the web interface
2. YOLOv8 model runs defect detection on each image
3. Detections are sent to Claude API with a structured prompt
4. Claude generates a formal inspection report
5. Report is displayed and available to download

## Setup

1. Clone the repository
   git clone https://github.com/Meera3lii/blade-inspection-app.git
   cd blade-inspection-app

2. Install dependencies
   pip install -r requirements.txt

3. Add your trained model
   Place your best.pt file in the root folder

4. Set your Anthropic API key
   Windows: set ANTHROPIC_API_KEY=your_key_here

5. Run the app
   streamlit run app.py

## Model

- Architecture: YOLOv8n
- Trained on: 461 blade images (70/20/10 split)
- Classes: 1 (Defect)
- mAP@0.5: 98.1%
- Precision: 90.4% | Recall: 90.9%

## Project Structure

```
BladeInspectionApp/
├── app.py                 ← Streamlit frontend
├── yolo_runner.py         ← YOLO inference
├── report_generator.py    ← Claude API report generation
├── best.pt                ← Trained YOLOv8 model
├── requirements.txt
└── README.md
```
