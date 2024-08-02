import re
from .models import StudentReview,QuestionDetail
from openai import OpenAI
import base64
import requests
import os
import re
# OpenAI API Key
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# some fixes

def extract_review_details(response_text):
    # Extract general information
    student_name_match = re.search(r'"student_name": "([^"]+)"', response_text)
    book_name_match = re.search(r'"book_name": "([^"]+)"', response_text)
    final_score_match = re.search(r'"final_score": (\d+)', response_text)
    incorrect_answers_count_match = re.search(r'"incorrect_answers_count": (\d+)', response_text)
    student_name = student_name_match.group(1) if student_name_match else ''
    book_name = book_name_match.group(1) if book_name_match else ''
    final_score = int(final_score_match.group(1)) if final_score_match else 0
    incorrect_answers_count = int(incorrect_answers_count_match.group(1)) if incorrect_answers_count_match else 0

    # Updated regex to match "reason" and "correct_answer"
    incorrect_answers_details = []
    questions_matches = re.findall(
        r'"question_number": (\d+),.*?"reason": "([^"]+)",.*?"correct_answer": "([^"]+)"', response_text, re.DOTALL)


    for match in questions_matches:
        question_number = int(match[0])
        reason = match[1]  # Now correctly named to match the expected output
        correct_answer = match[2]  # Now correctly named to match the expected output

        incorrect_answer_detail = {
            "question_number": question_number,
            "reason": reason,  # Updated to match the expected output
            "correct_answer": correct_answer  # Updated to match the expected output
        }
        incorrect_answers_details.append(incorrect_answer_detail)

    # Create structured response
    structured_response = {
        "review": {
            "student_name": student_name,
            "book_name": book_name,
            "results": {
                "final_score": final_score,
                "incorrect_answers_count": incorrect_answers_count,
                "incorrect_answers_details": incorrect_answers_details
            }
        }
    }

    return structured_response



# automatically save
def save_review_to_db(response_data, user):
    # Create and save the StudentReview instance
    student_review = StudentReview(
        user=user,
        student_name=response_data['review']['student_name'],
        book_name=response_data['review']['book_name'],
        final_score=response_data['review']['results']['final_score'],
        incorrect_answers_count=response_data['review']['results']['incorrect_answers_count']
    )
    student_review.save()

    # Create and save the QuestionDetail instances
    for detail in response_data['review']['results']['incorrect_answers_details']:
        question_detail = QuestionDetail(
            user=user,
            student_review=student_review,
            question_number=detail['question_number'],
            reason=detail['reason'],  # Matches the key used in extract_review_details
            correct_answer=detail['correct_answer']  # Matches the key used in extract_review_details
        )
        question_detail.save()


# extract exam image papers

import base64
import openai

def encode_image(image_path):
    return base64.b64encode(image_path).decode("utf-8")

def extract_exam_text(image_paths):
    base64_images = [encode_image(path) for path in image_paths]

    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    messages = [
        {"role": "system", "content": "You are a helpful assistant that responds in Markdown."},
        {"role": "user", "content": [
            {"type": "text", 
            "text": '''
                   I have uploaded images of student exam papers. Please follow these detailed instructions to extract and organize the content:

                    1. **Identify and Categorize Question Types:**
                    - **Multiple Choice Questions (MCQs):** Extract questions with several options where only one is correct. These typically include a prompt followed by a list of options labeled with letters (e.g., A, B, C) or numbers. Extract the options and note which one is marked as the student's choice.
                    - **True/False Questions:** Extract questions that require a 'True' or 'False' answer. These often present a statement that needs validation. Extract the statement and the student's answer.
                    - **Short Answer Questions:** Extract questions that require brief, specific responses. These questions usually request a short piece of information or explanation. Extract the question and the student's response.
                    - **Essay Questions:** Extract questions that require detailed responses. These questions prompt for extensive answers or discussions. Extract the question and the student's complete essay or response.
                    - **Fill-in-the-Blank Questions:** Extract questions with blanks that need to be filled in with specific words or phrases. Extract the question and the student's answers for the blanks.
                    - **Matching Questions:** Extract questions requiring matching items from two lists, involving pairs of statements or items. Extract the question and the student's matching pairs or selections.

                    2. **Extracting Questions and Answers:**
                    - For each identified question type, extract the text of the question clearly.
                    - For MCQs and matching questions, extract and list the answer options or pairs, and indicate the student's selected options or pairs.
                    - For questions that require answers (short answer, essay, fill-in-the-blank), extract both the questions and the student's responses.
                    - Ensure that each student's response is placed directly after its corresponding question.

                    3. **Organize and Format the Extracted Content:**
                    - Present each question type in its own section or format for clarity.
                    - Group each question with its respective student answer(s) immediately following it.
                    - Maintain the order of appearance as closely as possible to the original exam paper.
                    - Ensure continuity if the exam spans multiple pages, keeping questions and answers in the correct sequence.

                    4. **Provide Contextual Information (if possible):**
                    - Include student name , subject name ,exam marks , school name all header info please .

                   WARNING : Your response should only be the exam not other extra text intro or outro please

                   Thank you !
                    
            
                '''}
        ] + [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            for base64_image in base64_images
        ]}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.0,
    )

    return response.choices[0].message.content