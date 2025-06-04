import io
import contextlib
import re

def band_to_grade(band):
    grade_map = {
        6: "A",
        5: "B+",
        4: "B",
        3: "C",
        2: "D",
        1: "F"
    }
    return grade_map.get(band, "Ungraded")

def deep_lit_review(essay):
    ao_scores = {"AO1": 0, "AO2": 0, "AO3": 0}
    feedback = {"AO1": [], "AO2": [], "AO3": []}

    output = io.StringIO()
    with contextlib.redirect_stdout(output):

        # AO1 - Critical Personal Response
        if re.search(r'\bI (think|feel|believe|interpret|noticed|realized)\b', essay, re.IGNORECASE):
            ao_scores["AO1"] += 1
            feedback["AO1"].append("Shows personal engagement with the text.")
        if re.search(r'\b(meaning|suggests|implies|portrays|reveals|reflects)\b', essay, re.IGNORECASE):
            ao_scores["AO1"] += 1
            feedback["AO1"].append("Attempts interpretation or thematic commentary.")

        # AO2 - Language/Form/Structure
        if re.search(r'\b(metaphor|simile|alliteration|enjambment|diction|syntax|tone|structure|form|caesura|imagery|contrast)\b', essay, re.IGNORECASE):
            ao_scores["AO2"] += 1
            feedback["AO2"].append("Identifies and analyzes literary/structural techniques.")
        if re.search(r'\b(conveys|emphasizes|creates|enhances|juxtaposes|evokes|reinforces)\b', essay, re.IGNORECASE):
            ao_scores["AO2"] += 1
            feedback["AO2"].append("Explains effects of techniques on meaning or reader response.")

        # AO3 - Contextual Understanding
        if re.search(r'\b(context|historical|Victorian|Romantic|colonial|feminist|author|society|era)\b', essay, re.IGNORECASE):
            ao_scores["AO3"] += 1
            feedback["AO3"].append("Demonstrates awareness of literary or historical context.")
        if re.search(r'\b(influenced|reflected|mirror|represents|critique|criticize|challenge)\b', essay, re.IGNORECASE):
            ao_scores["AO3"] += 1
            feedback["AO3"].append("Connects text to broader societal or authorial commentary.")

        total_score = sum(ao_scores.values())
        band = min(6, max(1, total_score))
        grade = band_to_grade(band)

        print("\n📊 AICE Literature Essay – PROFESSIONAL REVIEW")
        print(f"Grade Estimate: {grade} (Band {band}/6)")
        print("------------------------------------------")

        print("\n🔎 Skill Breakdown:")
        for ao, score in ao_scores.items():
            print(f"- {ao}: {score}/2")
            for comment in feedback[ao]:
                print(f"   • {comment}")

        print("\n📐 Structure & Style Analysis:")
        paragraphs = essay.strip().count("\n\n") + 1
        if paragraphs < 3:
            print("- Essay may lack full structure (fewer than 3 body paragraphs).")
        else:
            print("- Essay shows clear structure and paragraphing.")

        if any(len(s.split()) > 30 for s in essay.split('.')):
            print("- Consider varying sentence lengths for better pacing and clarity.")
        else:
            print("- Sentence length and variation are well controlled.")

        if "I think" in essay and "the reader" in essay:
            print("- Balances personal interpretation with audience/reader awareness.")

        print("\n🧾 Summary:")
        if band >= 5:
            print("✅ Strong literary engagement, critical insight, and contextual integration.")
        elif band >= 3:
            print("⚠️ Reasonable interpretation with some use of techniques and context.")
        else:
            print("❌ Limited engagement with meaning or context. Focus on deepening analysis and structure.")

        print("\n🎯 Suggestions:")
        print("- Integrate 2–3 well-selected quotes per paragraph and zoom into technique.")
        print("- Explore historical/literary context to strengthen interpretations.")
        print("- Link authorial methods to reader impact and thematic development.")

    return output.getvalue()
