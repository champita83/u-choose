import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gpt_response(history, riddle=False, insight=False):
    system_prompt = "You are Alex, a gentle, insightful guide who helps users explore internal conflicts. You use Socratic questioning to help users identify assumptions behind their desires and actions. Do not mention Theory of Constraints or technical methods. Use metaphors or riddles only if appropriate. Speak in a natural, conversational tone."

    messages = [{"role": "system", "content": system_prompt}]
    for entry in history:
        role = "user" if entry["role"] == "user" else "assistant"
        messages.append({"role": role, "content": entry["content"]})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    return response['choices'][0]['message']['content'].strip()
