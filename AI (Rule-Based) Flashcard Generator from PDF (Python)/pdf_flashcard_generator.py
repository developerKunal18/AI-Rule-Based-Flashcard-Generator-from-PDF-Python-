import re
import json
import random
from pathlib import Path
from collections import Counter
from typing import List, Tuple
import PyPDF2

# ---------- Utilities ----------
def extract_text_from_pdf(pdf_path: str) -> str:
    text = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            ptext = page.extract_text()
            if ptext:
                text.append(ptext)
    return "\n".join(text)

def split_to_sentences(text: str) -> List[str]:
    # crude sentence splitter (keeps abbreviations naive)
    text = text.replace("\n", " ")
    # split on period/question/exclamation followed by space and uppercase (heuristic)
    sentences = re.split(r'(?<=[\.\?\!])\s+(?=[A-Z0-9])', text)
    cleaned = [s.strip() for s in sentences if len(s.strip()) > 30]  # ignore very short sentences
    return cleaned

def word_scores(text: str) -> Counter:
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())  # words length>=4
    return Counter(words)

def pick_keyword(sentence: str, global_scores: Counter) -> Tuple[str, str]:
    # choose candidate words from sentence and prefer globally important words
    candidates = re.findall(r"\b[a-zA-Z]{4,}\b", sentence)
    if not candidates:
        return None, None
    candidates = list(dict.fromkeys([w.lower() for w in candidates]))  # preserve order, unique
    # score by frequency in document (global_scores) and word length
    best = max(candidates, key=lambda w: (global_scores.get(w,0), len(w)))
    return best, best  # (keyword, answer)

# ---------- Flashcard generation ----------
def make_cloze(sentence: str, keyword: str) -> str:
    # Replace only first occurrence of the keyword (case-insensitive)
    pattern = re.compile(re.escape(keyword), flags=re.IGNORECASE)
    cloze = pattern.sub("_____", sentence, count=1)
    return cloze

def generate_distractors(correct: str, global_vocab: List[str], n=3) -> List[str]:
    # simple distractor generator: pick random words of similar length from vocab
    candidates = [w for w in global_vocab if w.lower() != correct.lower() and abs(len(w)-len(correct))<=2]
    chosen = random.sample(candidates, k=min(n, len(candidates))) if candidates else []
    return chosen

def generate_flashcards_from_pdf(pdf_path: str, max_cards=30, make_mcq=False, distractors=3):
    text = extract_text_from_pdf(pdf_path)
    sentences = split_to_sentences(text)
    scores = word_scores(text)
    vocab = [w for w,_ in scores.most_common(500)]
    cards = []
    used_sentences = set()

    for s in sorted(sentences, key=lambda x: -len(x)):  # prefer longer sentences first
        if len(cards) >= max_cards:
            break
        kw, answer = pick_keyword(s, scores)
        if not kw:
            continue
        # avoid trivial words
        if kw.lower() in {"this","that","these","those","which","where","when","what","there","their"}:
            continue
        cloze = make_cloze(s, kw)
        if cloze == s:
            # replacement failed
            continue
        if s in used_sentences:
            continue
        used_sentences.add(s)

        card = {"type":"cloze", "prompt": cloze, "answer": answer}
        if make_mcq:
            distract = generate_distractors(answer, vocab, n=distractors)
            options = distract + [answer]
            random.shuffle(options)
            card = {"type":"mcq", "prompt": cloze, "answer": answer, "options": options}
        cards.append(card)

    return cards

def save_flashcards(cards: List[dict], out_file="flashcards.json"):
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(cards)} cards to {out_file}")

# ---------- CLI ----------
def main():
    print("\n📚 PDF → Flashcard Generator (Day 46)\n")
    pdf_path = input("Enter path to PDF file (e.g., notes.pdf): ").strip()
    if not Path(pdf_path).exists():
        print("❌ File not found.")
        return
    try:
        max_cards = int(input("Number of cards to generate (default 20): ") or "20")
    except:
        max_cards = 20
    mcq = input("Create multiple-choice cards? (y/N): ").strip().lower() == "y"
    distractors = 3
    if mcq:
        try:
            distractors = int(input("Number of distractors per MCQ (default 3): ") or "3")
        except:
            distractors = 3

    cards = generate_flashcards_from_pdf(pdf_path, max_cards=max_cards, make_mcq=mcq, distractors=distractors)
    if not cards:
        print("⚠ No cards generated — try a different document or increase sentence length threshold.")
        return
    save_flashcards(cards)
    # print sample
    print("\n🔎 Sample cards:")
    for i,c in enumerate(cards[:5], start=1):
        print(f"\nCard {i}:")
        print("Prompt:", c["prompt"])
        if c["type"] == "mcq":
            print("Options:", c["options"])
        print("Answer:", c["answer"])

if __name__ == "__main__":
    main()
