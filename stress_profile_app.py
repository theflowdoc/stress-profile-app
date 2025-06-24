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
    - Select the option that best reflects how often each statement has been true for you over the past year.
    - Be honest — this is for your personal reflection.
    """)

    # Rating labels (used instead of numbers)
    rating_labels = [
        "Never", "Almost never", "Rarely", "Very infrequently", "Infrequently",
        "Sometimes", "Occasionally", "Often", "Frequently", "Very frequently", "Almost always"
    ]

    # Updated 20 statements
    statements = [
        "I feel used up at the end of the day.",
        "I wish I could be as happy as other people seem to be.",
        "I try to do two or three things at once, rather than taking one thing at a time.",
        "If I could stop worrying so much, I would accomplish a lot more.",
        "I don't seem to get the same kind of lasting satisfaction that I used to from the time I spend with friends.",
        "I feel low on energy, exhausted, tired, or unable to get things done.",
        "I feel that many people see me as being a lot more successful than I really feel I have been.",
        "I tend to hold my feelings inside, rather than expressing them openly.",
        "When something difficult or stressful is coming up, I find myself thinking about all the ways things can go poorly for me.",
        "I don't feel really close to or accepted by the people around me, both family and friends.",
        "I tire quickly.",
        "I feel that my leisure time and recreational life don't express the really creative side of me.",
        "I tend to anticipate others in conversation (interrupting, finishing sentences for the other person), rather than listening well and letting the other person finish speaking.",
        "Whenever I try to put a worrisome thought out of my mind, it comes right back.",
        "I don't handle conflicts or disagreements with people as well as I'd like to.",
        "I get the flu or a cold.",
        "The ways I organize and use my time aren't a very accurate reflection of my interests.",
        "I get uneasy when I'm waiting.",
        "Decisions are hard for me because I spend a lot of time wondering if I've thought of all the alternatives.",
        "I feel I should be spending more time with my family."
    ]

    # Mapping to stress types
    stress_types = {
        "Basket Case": [1, 6, 11, 16],
        "Drifter": [2, 7, 12, 17],
        "Speed Freak": [3, 8, 13, 18],
        "Worry Wart": [4, 9, 14, 19],
        "Loner": [5, 10, 15, 20]
    }

    # Collect responses
    responses = {}
    for i, statement in enumerate(statements, 1):
        st.markdown(f"**{i}. {statement}**")
        selected_label = st.selectbox("Your rating", rating_labels, index=5, key=f"q{i}")
        responses[i] = rating_labels.index(selected_label)
        st.markdown("---")

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

        # Calculate type scores
        for s_type, questions in stress_types.items():
            score = sum(responses[q] for q in questions)
            type_scores[s_type] = score
            total_stress_score += score

        total_msg = interpret(total_stress_score)

        # Show results
        st.subheader("🧾 Your Results")
        st.markdown(f"**Total Stress Score:** `{total_stress_score} / 200`")
        st.markdown(f"**Interpretation:** {total_msg}")

        st.markdown("### Stress Type Scores:")
        for s_type, score in type_scores.items():
            st.markdown(f"- **{s_type}**: {score} → {interpret(score)}")

        # Generate report
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
            output.write(f"{i}. {statements[i-1]} = {value} ({rating_labels[value]})\n")
        output.write("\nFor deeper insight, contact Shannon Levee at slevee72@gmail.com\n")

        # Download button
        st.download_button(
            label="📥 Download My Report",
            data=output.getvalue(),
            file_name=f"Stress_Profile_{name.title().replace(' ', '_')}.txt",
            mime="text/plain"
        )
