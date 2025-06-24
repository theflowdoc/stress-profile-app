# stress_profile_app.py
import streamlit as st
from datetime import datetime
import io

st.set_page_config(page_title="Stress Profile Test", layout="centered")
st.title("🧠 Personalized Stress Profile Test")

# Ask for name
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello **{name.title()}**! Welcome to your stress profile test.")

    st.markdown("""
    **Instructions:**
    - Rate each statement from 0 (Never) to 10 (Almost Always).
    - Be honest — this is for your personal reflection.
    """)

    scale = {
        0: "Never", 1: "Almost never", 2: "Rarely", 3: "Very infrequently", 4: "Infrequently",
        5: "Sometimes", 6: "Occasionally", 7: "Often", 8: "Frequently",
        9: "Very frequently", 10: "Almost always"
    }

    statements = [
        "I feel used up at the end of the day.",
        "I wish I could be as happy as other people seem to be.",
        "I try to do two or three things at once, rather than taking one thing at a time.",
        "If I could stop worrying so much, I would accomplish a lot more.",
        "I don't seem to get the same kind of lasting satisfaction from time with friends.",
        "I feel low on energy or unable to get things done.",
        "I feel many people see me as more successful than I am.",
        "I hold feelings in instead of expressing them openly.",
        "When something stressful is coming up, I focus on how it could go poorly.",
        "I don't feel close to or accepted by those around me.",
        "I tire quickly.",
        "My leisure time doesn't reflect my creative side.",
        "I tend to interrupt or finish sentences for others.",
        "Worrisome thoughts keep returning when I try to forget them.",
        "I don’t handle disagreements as well as I’d like.",
        "I get the flu or a cold.",
        "The way I organize my time doesn’t reflect my interests.",
        "I get uneasy when I’m waiting.",
        "I struggle with decisions, worrying if I’ve missed alternatives.",
        "I feel I should spend more time with my family."
    ]

    stress_types = {
        "Basket Case": [1, 6, 11, 16],
        "Drifter": [2, 7, 12, 17],
        "Speed Freak": [3, 8, 13, 18],
        "Worry Wart": [4, 9, 14, 19],
        "Loner": [5, 10, 15, 20]
    }

    responses = {}
    for i, statement in enumerate(statements, 1):
        st.markdown(f"**{i}. {statement}**")
        responses[i] = st.slider("Your rating", 0, 10, 5, key=f"q{i}")
        st.markdown("---")  # optional visual divider

    if st.button("Get My Results"):
        total_stress_score = 0
        type_scores = {}

        def interpret(score):
            if score <= 11:
                return "✅ Positive: Build on strengths."
            elif 12 <= score <= 15:
                return "⚠️ Early Warning Signs: Take preventive measures."
            else:
                return "🚨 Elevated Risk: Take corrective action now."

        for s_type, questions in stress_types.items():
            score = sum(responses[q] for q in questions)
            type_scores[s_type] = score
            total_stress_score += score

        total_msg = interpret(total_stress_score)

        st.subheader("🧾 Your Results")
        st.markdown(f"**Total Stress Score:** `{total_stress_score} / 200`")
        st.markdown(f"**Interpretation:** {total_msg}")

        st.markdown("### Stress Type Scores:")
        for s_type, score in type_scores.items():
            st.markdown(f"- **{s_type}**: {score} → {interpret(score)}")

        # Generate report text
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output = io.StringIO()
        output.write(f"Stress Profile Test Results\n")
        output.write(f"Name: {name.title()}\n")
        output.write(f"Date: {timestamp}\n")
        output.write("=" * 40 + "\n\n")
        output.write(f"Total Stress Score: {total_stress_score} / 200\n")
        output.write(f"Interpretation: {total_msg}\n\n")
        output.write("Stress Type Scores:\n")
        for s_type, score in type_scores.items():
            output.write(f"- {s_type}: {score} → {interpret(score)}\n")
        output.write("\nYour Responses:\n")
        for i, value in responses.items():
            output.write(f"{i}. {statements[i-1]} = {value} ({scale[value]})\n")
        output.write("\nFor deeper insight, contact Shannon Levee at slevee72@gmail.com\n")

        # Provide download button
        st.download_button(
            label="📥 Download My Report",
            data=output.getvalue(),
            file_name=f"Stress_Profile_{name.title().replace(' ', '_')}.txt",
            mime="text/plain"
        )
