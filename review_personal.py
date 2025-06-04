import re
import io
import contextlib

def band_to_grade(band):
    return {
        6: "A",
        5: "A-",
        4: "B+",
        3: "B",
        2: "C",
        1: "D"
    }[band]

def deep_personal_review(essay):
    ao1, ao2, ao3 = 0, 0, 0
    feedback = {"AO1": [], "AO2": [], "AO3": []}

    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        # AO1 – Personal Voice / Reflection
        if re.search(r'\b(I|me|my|mine|myself|reflect|learned|grew|realized|discovered)\b', essay, re.IGNORECASE):
            ao1 += 2
            feedback["AO1"].append("Strong personal reflection and voice.")
        else:
            feedback["AO1"].append("Needs stronger personal insight or storytelling.")

        # AO2 – Structure & Coherence
        if essay.count("\n\n") >= 3:
            ao2 += 1
            feedback["AO2"].append("Well-structured and coherent.")
        if any(len(s.split()) > 30 for s in essay.split(".")):
            feedback["AO2"].append("Watch for sentence length. Some are overly long.")
        else:
            ao2 += 1
            feedback["AO2"].append("Good variation in sentence structure.")

        # AO3 – Language & Emotional Effect
        if re.search(r'\b(emotion|fear|joy|hope|struggle|challenge|growth|identity)\b', essay, re.IGNORECASE):
            ao3 += 2
            feedback["AO3"].append("Emotional depth and strong expression.")
        else:
            feedback["AO3"].append("Try to deepen the emotional/empathic connection.")

        total = ao1 + ao2 + ao3
        band = min(6, max(1, total))
        grade = band_to_grade(band)

        print("📋 Personal Narrative Review:")
        print(f"Estimated Grade: {grade} (Band {band}/6)\n")

        print("🔍 Breakdown:")
        print(f"- AO1 (Voice & Insight): {ao1}/2")
        for fb in feedback["AO1"]:
            print(f"   • {fb}")
        print(f"- AO2 (Structure): {ao2}/2")
        for fb in feedback["AO2"]:
            print(f"   • {fb}")
        print(f"- AO3 (Language & Emotion): {ao3}/2")
        for fb in feedback["AO3"]:
            print(f"   • {fb}")

        print("\n🧠 Summary:")
        if band >= 5:
            print("✅ Powerful and engaging narrative. Excellent emotional tone and writing flow.")
        elif band >= 3:
            print("⚠️ Good ideas, but could use stronger reflection and refinement in structure.")
        else:
            print("❌ Needs deeper personal focus and improved organization.")

    return output.getvalue()
