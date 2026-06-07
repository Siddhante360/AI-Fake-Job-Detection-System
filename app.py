import streamlit as st
import torch

from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification
)

from rules import calculate_risk


@st.cache_resource
def load_model():

    tokenizer = DistilBertTokenizer.from_pretrained("model")

    model = DistilBertForSequenceClassification.from_pretrained(
        "model"
    )

    model.eval()

    return tokenizer, model


tokenizer, model = load_model()


st.set_page_config(
    page_title="AI Fake Job Detector",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI-Powered Fake Job Detection System")

st.markdown("""
This system combines:

✅ DistilBERT Deep Learning Model

✅ Fraud Detection Rules

✅ Risk Scoring Engine

✅ Explainable AI Indicators
""")


# ==================================================
# TWO COLUMN DASHBOARD
# ==================================================

left_col, right_col = st.columns([1, 1])

with left_col:

    st.subheader("📄 Job Description")

    job_text = st.text_area(
        "Paste Job Description",
        height=350
    )

    analyze = st.button(
        "🔍 Analyze Job",
        use_container_width=True
    )


if analyze:

    if len(job_text.strip()) == 0:

        st.warning("Please enter a job description.")

    else:

        inputs = tokenizer(
            job_text,
            truncation=True,
            padding="max_length",
            max_length=512,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = model(**inputs)

            probabilities = torch.softmax(
                outputs.logits,
                dim=1
            )

            prediction = torch.argmax(
                probabilities,
                dim=1
            ).item()

            confidence = probabilities[0][prediction].item()

        risk_score, reasons, category, breakdown = calculate_risk(job_text)

        with right_col:

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Risk Score",
                risk_score
            )

            metric2.metric(
                "Category",
                category
            )

            metric3.metric(
                "Confidence",
                f"{confidence*100:.1f}%"
            )

            st.divider()

            # =====================================
            # FINAL VERDICT
            # =====================================

            st.subheader("🚦 Final Verdict")

            if category == "HIGH RISK FRAUD":

                final_verdict = "FRAUD ALERT"

                st.error(
                    "🚨 FRAUD ALERT: High Risk Job Posting Detected"
                )

            elif category == "SUSPICIOUS":

                final_verdict = "SUSPICIOUS JOB"

                st.warning(
                    "🟠 SUSPICIOUS JOB: Verify Before Applying"
                )

            elif prediction == 1:

                final_verdict = "FAKE JOB"

                st.error(
                    f"🚨 Fake Job Detected | Confidence: {confidence*100:.2f}%"
                )

            else:

                final_verdict = "REAL JOB"

                st.success(
                    f"✅ Real Job Detected | Confidence: {confidence*100:.2f}%"
                )

            # =====================================
            # RISK SCORE
            # =====================================

            st.subheader("📊 Risk Score")

            st.progress(risk_score / 100)

            st.write(f"Risk Score: {risk_score}/100")

            # =====================================
            # RISK CATEGORY
            # =====================================

            st.subheader("🏷 Risk Category")

            if category == "HIGH RISK FRAUD":

                st.error("🔴 HIGH RISK FRAUD")

            elif category == "SUSPICIOUS":

                st.warning("🟠 SUSPICIOUS")

            elif category == "LOW SUSPICION":

                st.info("🟡 LOW SUSPICION")

            else:

                st.success("🟢 SAFE")

            # =====================================
            # AI MODEL OUTPUT
            # =====================================

            st.subheader("🤖 AI Model Prediction")

            if prediction == 1:

                st.write(
                    f"DistilBERT Prediction: Fake Job ({confidence*100:.2f}%)"
                )

            else:

                st.write(
                    f"DistilBERT Prediction: Real Job ({confidence*100:.2f}%)"
                )

            # =====================================
            # RISK INDICATORS
            # =====================================

            st.subheader("⚠ Risk Indicators")

            if len(reasons) > 0:

                for reason in reasons:

                    st.write("•", reason)

            else:

                st.success(
                    "No suspicious indicators detected."
                )

            # =====================================
            # RISK BREAKDOWN
            # =====================================

            with st.expander("📈 Risk Breakdown"):

                if len(breakdown) > 0:

                    for item, points in breakdown.items():

                        st.write(
                            f"• {item} : +{points} points"
                        )

                else:

                    st.write(
                        "No risk factors detected."
                    )

            # =====================================
            # RECOMMENDATION
            # =====================================

            st.subheader("💡 Recommendation")

            if category == "HIGH RISK FRAUD":

                st.error(
                    "Avoid applying. This posting contains multiple fraud indicators."
                )

            elif category == "SUSPICIOUS":

                st.warning(
                    "Verify company credentials, website, and recruiter before applying."
                )

            elif category == "LOW SUSPICION":

                st.info(
                    "Proceed with caution and verify the company independently."
                )

            else:

                st.success(
                    "No major fraud indicators detected."
                )

            # =====================================
            # ANALYSIS SUMMARY
            # =====================================

            with st.expander("📝 Analysis Summary"):

                st.info(
                    f"""
Final Verdict: {final_verdict}

Risk Category: {category}

Risk Score: {risk_score}/100

Detected Indicators: {len(reasons)}

Model Confidence: {confidence*100:.2f}%
"""
                )