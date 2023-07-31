import openai

OPEN_AI_KEY = "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"
openai.api_key = OPEN_AI_KEY

# specify the chatgpt engine of the application
model_engine = "text-davinci-003"


def get_book_suggestion_from_ai(prompt):
    """
        Get response from chatgpt based on the prompt given and returns the response
    :param prompt:
    :return:
    """
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    response = completion.choices[0].text
    return response
