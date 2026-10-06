prompt_template = """
You are an expert at creating questions based on social sciences material and documentation.
Your goal is to prepare a researcher for their exam and interview questions.
You will do this by asking questions about the text below:

------------
{text}
------------

Create 10 high-quality questions from the provided text.

Focus on important concepts, facts, findings, statistics, arguments,
and conclusions.

Make sure not to lose any important information. Do not generate unnecessary or repetitive questions.

Ignore copyright notices, licensing terms, disclaimers, acknowledgements,
tables of contents, and other front matter. Ask only about the subject
matter of the document.

Format rules:
- Number the questions 1 to 10.
- Put each question on a single line.
- Use plain text only: no bold, no markdown, no headings.

Use plain ASCII characters only: straight quotes, normal hyphens, normal spaces.

Questions:
"""


refine_template = """
You are an expert at creating practice questions based on social sciences material and documentation.

Your task is to maintain and improve an existing list of practice questions.

Here is the CURRENT QUESTION LIST:
----------------
{existing_answers}
----------------

Here is NEW CONTEXT from the document:
----------------
{text}
----------------

Instructions:
1. Review the current question list against the new context.
2. Keep questions that already cover important information.
3. Improve an existing question only when the new context provides important additional information.
4. Add new questions only when the new context contains important information that is not already covered.
5. Remove or combine redundant questions.
6. Ignore copyright notices, licensing terms, disclaimers, and other front
matter. Do not keep questions about them.
7. The final output MUST contain 10 questions.
8. Do NOT ask the user for the existing questions.
9. Do NOT explain your process.
10. Output ONLY the numbered questions, one per line, in plain text with no bold or markdown.

Use plain ASCII characters only: straight quotes, normal hyphens, normal spaces.

Final questions:
"""


answer_template = """You are helping a researcher prepare for an exam and interview.
Answer the question using only the context below.

Rules:
- Answer in 3 to 5 sentences.
- Include specific facts or statistics from the context when they exist.
- Answer only what the question asks. Do not repeat statistics that belong to other topics.
- If the context doesn't contain the answer, reply exactly: "Not found in the document."
- Use plain text only, with no bold or markdown formatting.
- Do not add an introduction or a closing remark.

Use plain ASCII characters only: straight quotes, normal hyphens, normal spaces.

Context:
{context}

Question: {question}

Answer:"""