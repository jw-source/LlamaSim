import gradio as gr
from network import Network
import pandas as pd

agent_network = None

def generate_agents(population, num_agents, context_size):
    global agent_network 
    agent_network = Network(population, num_agents, context_size)
    agents_df = pd.DataFrame({
        "Identity": agent_network.identities
    })
    return agents_df

def start_groupchat(prompt, chat_type, rounds):
    global agent_network
    if agent_network is None:
        return [], gr.update(value="Please generate agents before starting the group chat.")
    else:
        conversation_logs = agent_network.group_chat(prompt, chat_type, rounds)
        conversation_pairs = []
        for i in range(0, len(conversation_logs), 2):
            user_msg = conversation_logs[i]
            if i+1 < len(conversation_logs):
                bot_msg = conversation_logs[i+1]
            else:
                bot_msg = ""
            conversation_pairs.append((user_msg, bot_msg))
        return conversation_pairs, gr.update(value="")

with gr.Blocks() as demo:
    gr.Markdown("# LlamaPoll")

    with gr.Tab("Generate Agents"):
        with gr.Column():
            with gr.Row():
                population_input = gr.Textbox(
                    label="Population",
                    value="Students at Carnegie Mellon University",
                    lines=2
                )
                num_agents_input = gr.Number(
                    label="Number of Agents", value=10
                )
                memory_size_input = gr.Number(
                    label="Memory Size", value=4000
                )
            generate_agents_button = gr.Button("Generate Agents")

            gr.Markdown("### Agents Dashboard")
            agents_table = gr.Dataframe(headers=["Identity"], interactive=False)

    with gr.Tab("Groupchat"):
        with gr.Column():
            with gr.Row():
                prompt_input = gr.Textbox(
                    label="Prompt",
                    value="Kamala Harris is showing up to the Purnell Center today!",
                    lines=2
                )
                chat_type_input = gr.Radio(
                    label="Chat Type",
                    choices=["round_robin", "random"],
                    value="random"
                )
                rounds_input = gr.Number(
                    label="Number of Rounds", value=1
                )
            groupchat_button = gr.Button("Start Groupchat")
            gr.Markdown("### Groupchat History")
            conversation = gr.Chatbot(label="Conversation")
            error_message = gr.Textbox(value="", visible=False, interactive=False)

    with gr.Tab("Predict"):
        pass

    generate_agents_button.click(
        fn=generate_agents,
        inputs=[
            population_input,
            num_agents_input,
            memory_size_input,
        ],
        outputs=[agents_table],
    )

    groupchat_button.click(
        fn=start_groupchat,
        inputs=[
            prompt_input,
            chat_type_input,
            rounds_input,
        ],
        outputs=[conversation, error_message],
    )

demo.launch()
