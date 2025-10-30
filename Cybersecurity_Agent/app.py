import gradio as gr

from backend import get_cyber_answer


APP_TITLE = "Cybersecurity AI Assistant"


def answer_fn(message, history):
    _ = history  # history not used in backend, kept for chat interface compatibility
    return get_cyber_answer(message or "")


dark = gr.themes.Soft(
    primary_hue="blue",
    neutral_hue="slate",
).set(
    body_background_fill="*neutral_900",
    body_text_color="white",
    background_fill_primary="*neutral_900",
    block_background_fill="*neutral_850",
    input_background_fill="*neutral_800",
    button_secondary_background_fill="*neutral_800",
)


with gr.Blocks(theme=dark, css="""
.wrap { max-width: 1100px; margin: 0 auto; }
.chat-container { height: 70vh; }
.controls { display: flex; gap: 12px; align-items: center; }
footer { display: none !important; visibility: hidden; }
""") as demo:
    with gr.Column(elem_classes=["wrap"]):
        gr.Markdown(f"## {APP_TITLE}")
        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(height=520, elem_classes=["chat-container"], show_copy_button=True)
        with gr.Row():
            with gr.Column(scale=8):
                msg = gr.Textbox(
                    placeholder="Type your cybersecurity question...",
                    lines=2,
                    label=None,
                )
            with gr.Column(scale=2):
                send = gr.Button("Send", variant="primary")
        def user_submit(user_message, chat_history):
            if not user_message or not user_message.strip():
                return gr.update(value=""), chat_history
            chat_history = chat_history + [(user_message, None)]
            return gr.update(value=""), chat_history

        def bot_respond(chat_history):
            user_message = chat_history[-1][0]
            answer = answer_fn(user_message, chat_history)
            chat_history[-1] = (user_message, answer)
            return chat_history

        send.click(user_submit, [msg, chatbot], [msg, chatbot]).then(
            bot_respond, [chatbot], [chatbot]
        )
        msg.submit(user_submit, [msg, chatbot], [msg, chatbot]).then(
            bot_respond, [chatbot], [chatbot]
        )


if __name__ == "__main__":
    demo.launch(show_api=False)


