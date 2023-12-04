def get_partial_result_string(
        sent_choices,
        correct_choices,
        question_type,
        question_text):
    result_string = ""
    if question_type == "SC":
        result_string += f"Вопрос: \"{question_text}\" \n"
        if sent_choices[0] == correct_choices[0]:
            result_string += f"Выбранный ответ: \n{correct_choices[0]}\n был верен\n\n"
        else:
            result_string += f"Выбранный ответ: \n{correct_choices[0]}\n был неверен\n\n"
    elif question_type == "MC":
        result_string += f"Вопрос: \"{question_text}\" \n"
        for choice in sent_choices:
            if choice in correct_choices:
                result_string += f"Выбранный ответ: \n{choice}\n был верен\n"
                result_string += "|||"
            else:
                result_string += f"Выбранный ответ: \n{choice}\n был неверен\n"
                result_string += "|||"
    return result_string


def get_result_string(questions_set, sent_data):
    result_string = ""
    for question in questions_set:
        question_id = question.id
        question_text = question.question_text
        question_type = question.question_type
        correct_choices = question.choices.filter(
            is_correct=True).only('choice_text')
        sent_choices = sent_data[str(question_id)]
        result_string += get_partial_result_string(
            sent_choices, correct_choices, question_type, question_text)
    return result_string
