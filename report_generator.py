import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
def generate_report(all_results: list) -> str:

    findings_text = ""
    for result in all_results:
        fname = result["filename"]
        dets = result["detections"]

        if dets:
            det_lines = "\n".join(
                f"  - Defect detected (confidence: {d['confidence']})"
                for d in dets
            )
            findings_text += f"\nImage: {fname}\n{det_lines}\n"
        else:
            findings_text += f"\nImage: {fname}\nNo defects detected.\n"

    prompt = f"""You are a certified aerospace blade inspection engineer writing an official inspection report.

You have been given the output of an automated YOLOv8 defect detection system for one or more turbine blade images.
Write a formal, structured inspection report based ONLY on the detections listed below.

STRICT RULES:
- Do NOT invent or assume any defects that are not listed in the detections.
- If an image has no detections, write exactly: "No defects detected. Blade appears serviceable."
- Use the exact image filename as the section header for each blade.
- Keep the tone formal, technical, and professional throughout.

USE THIS EXACT STRUCTURE FOR EVERY IMAGE:

**[filename]**

1. Defect Summary
   List each detection with its confidence score. If none, state "No defects detected."

2. Finding Description
   One paragraph describing the finding in plain engineering language.

3. Recommended Action
   Choose exactly one of:
   - "No action required"
   - "Monitor at next scheduled inspection"
   - "Remove from service for detailed inspection"
   - "Immediate removal from service"

DETECTION DATA:
{findings_text}

Write the complete inspection report now:"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text