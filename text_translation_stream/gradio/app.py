import asyncio

import httpx

import gradio as gr

languages = [
    "Arabic",
    "English",
    "French",
    "German",
    "Hindi",
    "Indonesian",
    "Japanese",
    "Javanese",
    "Korean",
    "Mandarin Chinese",
    "Portuguese",
    "Russian",
    "Spanish",
    "Turkish",
    "Urdu"
]

examples = {"gradio": [["Japanese", "German", "Spanish"],
                       "Building apps with Gradio is fun!"],
            "langchain": [["Russian", "Arabic", "French"],
                          "LangChain is awesome!!!"]}


async def process_stream(language, text):
    url = "http://langchain_backend:8000/translate/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "language": language,
        "text": text
    }

    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, headers=headers, json=data) as response:
            response.raise_for_status()  # Ensure we handle bad status codes
            response_text = ""
            async for chunk in response.aiter_text():
                if chunk:
                    response_text += chunk
                    await asyncio.sleep(0.02)  # Simulate processing delay
                    yield response_text  # Yield each chunk here

with gr.Blocks() as demo:
    gr.Markdown("# Text Translation App")
    with gr.Row():
        text_input = gr.Textbox(lines=10, label="Original Text",
                                info="Write a text that you want to get translated")
        translation_output = gr.Textbox(
            lines=10, label="Translation", info="Your translation will show up here")
    with gr.Row():
        language_input = gr.Dropdown(
            choices=languages, value="Japanese",
            label="Target Languages", multiselect=True,
            info="Select one or more languages to translate the original text"
        )
    with gr.Row():
        submit_button = gr.Button("Submit")
        submit_button.click(
            process_stream,
            inputs=[language_input, text_input],
            outputs=translation_output,
            queue=True
        )

    gr.Examples(
        examples=[examples['gradio'], examples['langchain']],
        inputs=[language_input, text_input])

# Launch the app
demo.launch(server_name="0.0.0.0", server_port=7860)
