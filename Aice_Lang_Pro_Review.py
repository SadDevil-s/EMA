import io
import contextlib
import re

def band_to_grade(band):
    return {
        6: "A",
        5: "B+",
        4: "B",
        3: "C",
        2: "D",
        1: "F"
    }.get(band, "Ungraded")

def deep_lang_review(essay):
    ao1, ao2, ao3 = 0, 0, 0
    feedback = {"AO1": [], "AO2": [], "AO3": []}

    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        # AO1: Personal voice & argument
        if re.search(r"\b(I|we|my|our|me|us)\b", essay, re.IGNORECASE):
            ao1 += 1
            feedback["AO1"].append("Personal voice is present.")
        if re.search(r"\b(think|believe|feel|in my opinion|clearly|strongly)\b", essay, re.IGNORECASE):
            ao1 += 1
            feedback["AO1"].append("Argumentative tone or stance established.")

        # AO2: Language and rhetorical analysis
        if re.search(r"\b(tricolon|hyperbole|rhetorical question|anecdote|repetition|contrast|humour|irony|listing|emotive language)\b", essay, re.IGNORECASE):
            ao2 += 1
            feedback["AO2"].append("Rhetorical devices identified or used effectively.")
        if re.search(r"\b(appeals|evokes|persuade|reinforce|undermine|challenge|tone|voice|register|style)\b", essay, re.IGNORECASE):
            ao2 += 1
            feedback["AO2"].append("Effect of techniques explained or analyzed.")

        # AO3: Context and genre conventions
        if re.search(r"\b(speech|letter|blog|article|column|audience|tone|purpose|register|genre)\b", essay, re.IGNORECASE):
            ao3 += 1
            feedback["AO3"].append("Genre conventions are acknowledged or applied.")
        if re.search(r"\b(formal|informal|colloquial|persuasive|narrative|descriptive)\b", essay, re.IGNORECASE):
            ao3 += 1
            feedback["AO3"].append("Appropriate register/style is used for the task.")

        total = ao1 + ao2 + ao3
        band = min(6, max(1, total))
        grade = band_to_grade(band)

        print("\n📊 AICE English Language – PROFESSIONAL REVIEW")
        print(f"Grade Estimate: {grade} (Band {band}/6)")
        print("--------------------------------------------")

        print("\n🔍 Skill Breakdown:")
        print(f"- AO1 (Personal Voice / Argument): {ao1}/2")
        for f in feedback["AO1"]:
            print(f"   • {f}")
        print(f"\n- AO2 (Language/Rhetoric Analysis): {ao2}/2")
        for f in feedback["AO2"]:
            print(f"   • {f}")
        print(f"\n- AO3 (Context & Genre): {ao3}/2")
        for f in feedback["AO3"]:
            print(f"   • {f}")

        print("\n📐 Structure & Style Notes:")
        paragraphs = essay.count("\n\n") + 1
        if paragraphs < 3:
            print("- Essay may be underdeveloped (less than 3 full paragraphs).")
        else:
            print("- Structure looks solid with paragraph development.")

        if any(len(s.split()) > 35 for s in essay.split('.')):
            print("- Consider shortening long sentences for clarity.")
        else:
            print("- Sentences are properly punctuated and clear.")

        print("\n🧾 Summary:")
        if band >= 5:
            print("✅ Sophisticated argument, language analysis, and genre awareness.")
        elif band >= 3:
            print("⚠️ Developing voice and structure. Build in more analysis.")
        else:
            print("❌ Basic or unclear argument. Review tone, audience, and genre conventions.")

        print("\n🎯 Suggestions:")
        print("- Clarify your position/argument early and reinforce it in conclusion.")
        print("- Use a variety of rhetorical strategies for effect (triples, contrast, etc.).")
        print("- Maintain consistent tone that fits the audience and form.")

    return output.getvalue()
