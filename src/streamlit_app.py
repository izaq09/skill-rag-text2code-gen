import json

import streamlit as st

st.set_page_config(layout="wide", page_title="SKILL RAG-based Text to Code Generator")

from gen_code import gen_code


def main():
    """
    Main
    """
    st.title("SKILL RAG-based Code Generator")

    col1, col2 = st.columns([0.2, 0.8])

    with col1:
        # File uploader for netlist files
        st.subheader("Upload Netlist")
        st.write("Please upload a netlist file in JSON format.")
        upload_file = st.file_uploader("Upload netlist", type=["json"])

        # Load button
        if st.button("Load File Content"):
            if upload_file is not None:
                file_content = json.loads(upload_file.getvalue().decode("utf-8"))
                st.session_state.file_content = file_content
                st.success("File content loaded successfully!")

        # If file content is loaded, display the cells and instances
        if st.session_state.get("file_content"):
            selected_cell = st.selectbox(
                "Select Cell",
                options=list(st.session_state.file_content.keys()),
                index=0,
            )
            selected_instances = st.multiselect(
                "Select Instances",
                options=list(st.session_state.file_content[selected_cell]["instances"]),
                default=list(st.session_state.file_content[selected_cell]["instances"]),
            )
            selected_nets = st.multiselect(
                "Select Nets",
                options=list(st.session_state.file_content[selected_cell]["nets"]),
                default=list(st.session_state.file_content[selected_cell]["nets"]),
            )

        with col2:
            # Initialize the session state for messages if it doesn't exist
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Write all existing messages to the chat
            for message in st.session_state.messages:
                st.chat_message(message["role"]).markdown(message["content"])

            prompt = st.chat_input(
                "Enter your prompt here...",
                disabled=not st.session_state.get("file_content"),
            )

            if prompt:
                # Add the user message to the session state
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Display the user message in the chat
                st.chat_message("user").markdown(prompt)

                # Here you would typically call your model to get a response
                # For demonstration, we'll just echo the prompt back
                response = gen_code(
                    cell=selected_cell,
                    instances=",".join(selected_instances),
                    nets=",".join(selected_nets),
                    prompt=prompt,
                )

                # Add the model's response to the session state
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

                response = f"Generated code for cell `{selected_cell}` with instances `{', '.join(selected_instances)}`:\n\n{response}"

                # Display the model's response in the chat
                st.chat_message("assistant").markdown(response)


if __name__ == "__main__":
    main()
