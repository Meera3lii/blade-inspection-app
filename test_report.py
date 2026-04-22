from report_generator import generate_report

fake_results = [
    {
        "filename": "blade_01.jpg",
        "detections": [
            {"class": "Defect", "confidence": 0.848},
            {"class": "Defect", "confidence": 0.712}
        ]
    },
    {
        "filename": "blade_02.jpg",
        "detections": []
    }
]

report = generate_report(fake_results)
print(report)