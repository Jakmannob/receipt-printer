import json

question_file = "Quizfragen.md"
question_output = "quizfragen.json"
questions = []
with open(question_file, "r") as infile:
    for line in infile.readlines():
        question = dict()
        question["question"] = line.split("?")[0].strip() + "?"
        question["answer"] = ("?".join(line.split("?")[1:])).strip().lower()
        questions.append(question)

with open(question_output, "w", encoding="utf8") as outfile:
    json.dump(questions, outfile, sort_keys=True, indent=4, ensure_ascii=False)
