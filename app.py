import streamlit as st
from yolo_runner import run_inference
from report_generator import generate_report

st.set_page_config(
    page_title="Blade Inspection AI",
    layout="wide",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #F0F4FA;
}
[data-testid="stSidebar"] {
    background-color: #0047BA;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
#MainMenu, footer { visibility: hidden; }

.header-card {
    background: linear-gradient(135deg, #0047BA 0%, #002F85 100%);
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 28px;
    color: white;
}
.header-card h1 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 6px 0;
    color: white;
}
.header-card p {
    font-size: 1rem;
    margin: 0;
    opacity: 0.85;
    color: white;
}

.step-header {
    background-color: #0047BA;
    color: white;
    padding: 10px 18px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    margin: 24px 0 14px 0;
}

.metric-row {
    display: flex;
    gap: 16px;
    margin: 16px 0;
}
.metric-card {
    background: white;
    border-radius: 10px;
    padding: 16px 24px;
    flex: 1;
    text-align: center;
    border-top: 4px solid #0047BA;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.metric-card .value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #0047BA;
}
.metric-card .label {
    font-size: 0.8rem;
    color: #666;
    margin-top: 4px;
}

[data-testid="stFileUploader"] {
    background: white;
    border-radius: 10px;
    padding: 12px;
}

.stButton > button {
    background-color: #0047BA;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 32px;
    font-size: 1rem;
    font-weight: 600;
    width: 100%;
    transition: background 0.2s;
}
.stButton > button:hover {
    background-color: #003494;
    color: white;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Blade Inspection AI")
    st.markdown("---")
    st.markdown("**Pipeline**")
    st.markdown("YOLOv8 → Claude API → Report")

st.markdown("""
<div class="header-card">
    <h1>Automated Blade Inspection System</h1>
    <p>Upload turbine blade images — YOLOv8 detects defects, Claude writes the formal inspection report.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="step-header">Step 1 — Upload Blade Images</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload one or more turbine blade images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} image(s) ready for inspection.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run = st.button("Run Inspection")

    if run:
        uploaded_files_sorted = sorted(uploaded_files, key=lambda f: f.name)
        all_results = []

        st.markdown('<div class="step-header">Step 2 — Defect Detection (YOLOv8)</div>', unsafe_allow_html=True)

        with st.spinner("Running YOLOv8 defect detection..."):
            for file in uploaded_files_sorted:
                image_bytes = file.read()
                result = run_inference(image_bytes, file.name)
                all_results.append(result)

        total_images = len(all_results)
        total_defects = sum(len(r["detections"]) for r in all_results)
        blades_with_defects = sum(1 for r in all_results if r["detections"])

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="value">{total_images}</div>
                <div class="label">Images Analysed</div>
            </div>
            <div class="metric-card">
                <div class="value">{blades_with_defects}</div>
                <div class="label">Blades with Defects</div>
            </div>
            <div class="metric-card">
                <div class="value">{total_defects}</div>
                <div class="label">Total Detections</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(min(len(all_results), 3))
        for i, result in enumerate(all_results):
            defect_count = len(result["detections"])
            status = "Defect Detected" if defect_count > 0 else "No Defects"
            with cols[i % 3]:
                st.image(
                    result["annotated_image"],
                    caption=f"{result['filename']} — {status}",
                    use_container_width=True
                )

        st.markdown('<div class="step-header">Step 3 — Generating Inspection Report (Claude)</div>',
                    unsafe_allow_html=True)

        with st.spinner("Claude is writing the formal inspection report..."):
            report = generate_report(all_results)

        st.success("Inspection report generated successfully.")

        st.markdown(report)

        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="Download Inspection Report",
                data=report,
                file_name="blade_inspection_report.md",
                mime="text/markdown",
            )