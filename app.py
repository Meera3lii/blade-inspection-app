import streamlit as st
from yolo_runner import run_inference
from report_generator import generate_report

st.set_page_config(page_title="Blade Inspection AI", layout="wide")
st.title("Automated Blade Inspection Report")
st.write("Upload one or more turbine blade images to generate a formal defect inspection report.")

uploaded_files = st.file_uploader(
    "Upload blade image(s)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"{len(uploaded_files)} image(s) uploaded. Click the button to begin.")

    if st.button("▶ Run Inspection"):

        uploaded_files = sorted(uploaded_files, key=lambda f: f.name)

        all_results = []

        st.subheader("Step 1 — Defect Detection")
        with st.spinner("Running YOLO on all images..."):
            for file in uploaded_files:
                image_bytes = file.read()
                result = run_inference(image_bytes, file.name)
                all_results.append(result)

        cols = st.columns(min(len(all_results), 3))
        for i, result in enumerate(all_results):
            with cols[i % 3]:
                st.image(
                    result["annotated_image"],
                    caption=f"{result['filename']} — {len(result['detections'])} defect(s) found",
                    use_column_width=True
                )

        st.subheader("Step 2 — Generating Inspection Report")
        with st.spinner("Claude is writing the report..."):
            report = generate_report(all_results)

        st.success("Report generated successfully.")

        st.subheader("Inspection Report")
        st.markdown(report)

        st.download_button(
            label="⬇ Download Report",
            data=report,
            file_name="blade_inspection_report.md",
            mime="text/markdown"
        )