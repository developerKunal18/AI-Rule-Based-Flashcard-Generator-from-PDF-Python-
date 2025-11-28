# 📚 PDF Flashcard Generator – Python Project

## 💡 Overview
The **PDF Flashcard Generator** automatically converts any PDF (notes, textbook chapter, research paper, article, etc.) into study flashcards.

It uses a **rule-based AI approach** (no external APIs) to:
- Extract text from PDF  
- Detect important sentences  
- Identify key terms  
- Create **cloze-style (fill-in-the-blank)** flashcards  
- Optionally generate **multiple-choice questions (MCQs)** with distractors  
- Export everything to `flashcards.json`

This tool is perfect for students, note-takers, self-learners, and anyone preparing for exams.

---

## 🚀 Features
- 📄 Extracts text from any PDF file  
- ✂️ Splits content into clean sentences  
- 🧠 Identifies important keywords using word-frequency scoring  
- 📝 Generates cloze (fill-in-the-blank) flashcards  
- 🔀 Optional MCQ mode with auto-generated distractors  
- 💾 Saves flashcards in JSON format for Anki/Quizlet import  
- ⚙ Fully configurable (card count, distractors, difficulty)  
- 💻 Pure Python — only `PyPDF2` required  

---

## 🧠 Concepts Used
- Rule-based NLP  
- Keyword scoring using frequency analysis  
- Regex text cleaning  
- Cloze deletion generation  
- Automatic MCQ question creation  
- JSON data formatting  
- PDF parsing  

---