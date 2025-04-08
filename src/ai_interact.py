import logging

import ollama


def ask_ai(prompt: str) -> str:
    # TODO: how to set a random seed?
    logging.info(f"AI request={prompt}")
    try:
        response = ollama.generate(model='cas/discolm-mfto-german:latest', prompt=prompt, options={"top_k": 20})
    except Exception as e:
        logging.error("Exception during ollama request. Did you forgot to start the service?", exc_info=True)
        raise Exception("Exception during ollama request") from e
    response_text = response['response']
    logging.info(f"AI response={response_text}")
    return response_text
