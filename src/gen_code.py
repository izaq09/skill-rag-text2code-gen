import argparse
from pathlib import Path

from google import genai
from google.genai import types
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma

from utils import get_embedding_function, get_logger

logger = get_logger(__name__)

DB_PATH = Path("chroma")

PROMPT_TEMPLATE = """
Generate commands with reference to the following context:

{context}

---

The cell is {cell}.
The instances in this cell are {instances}.
The nets present in the cell are {nets}.

---

Generate a procedure based on the above context: {prompt}
"""


def parse_args():
    """
    Procedure to parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate code from LLM")
    parser.add_argument(
        "--cell",
        type=str,
        required=True,
        help="Cell name to generate code for (e.g., 'cell1', 'cell2', etc.)",
    )
    parser.add_argument(
        "--instances",
        type=str,
        required=True,
        help="Comma-separated list of instances to generate code for (e.g., 'instance1,instance2')",
    )
    parser.add_argument(
        "--nets",
        type=str,
        required=True,
        help="Comma-separated list of nets to generate code for (e.g., 'net1,net2')",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Prompt to use for code generation (e.g., 'instance1 to abut with instance2')",
    )
    return parser.parse_args()


def preprocess_prompt(cell, instances, nets, prompt):
    """
    Preprocess the prompt to ensure it is suitable for code generation.
    """
    logger.info("Preprocessing prompt for code generation...")

    db = Chroma(
        persist_directory=str(DB_PATH), embedding_function=get_embedding_function()
    )

    results = db.similarity_search_with_score(prompt, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    return prompt_template.format(
        context=context_text, cell=cell, instances=instances, nets=nets, prompt=prompt
    )


def inference(prompt):
    """
    Perform inference to generate code based on the provided prompt.
    """
    logger.info("Starting inference for code generation...")

    client = genai.Client()

    return client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        config=types.GenerateContentConfig(
            system_instruction="You are the best Cadence SKILL language programmer"
        ),
        contents=prompt,
    ).text


def gen_code(cell, instances, nets, prompt):
    """
    Generate code based on the provided cell, instances, nets, and prompt.
    """

    # Preprocess the prompt to ensure it is suitable for code generation
    prompt = preprocess_prompt(cell, instances, nets, prompt)

    # Return the output of the inference function
    return inference(prompt)


if __name__ == "__main__":
    args = parse_args()
    gen_code_result = gen_code(
        args.cell, args.instances.split(","), args.nets.split(","), args.prompt
    )
    logger.info(f"Generated code:\n{gen_code_result}")
