import streamlit as st
import litellm
import trio
import os

# Configure your API keys here or via system environment variables
# os.environ["OPENAI_API_KEY"] = "your-openai-key"
# os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"

litellm.drop_params = True

# 1. ASYNCHRONOUS ENGINE WORKERS
async def call_llm(model_path, system_prompt, user_prompt):
    try:
        response = await litellm.acompletion(
            model=model_path,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices.message.content
    except Exception as e:
        return f"Error from {model_path}: {str(e)}"

async def run_parallel_orchestration(selected_models, user_prompt, prompts_dict):
    outputs = {}
    
    # Dynamically build async functions for toggled models
    async def task_wrapper(model_key, model_path, sys_prompt):
        outputs[model_key] = await call_llm(model_path, sys_prompt, user_prompt)

    async with trio.open_nursery() as nursery:
        if "ChatGPT" in selected_models:
            nursery.start_soon(task_wrapper, "ChatGPT", "openai/gpt-4o", prompts_dict["ChatGPT"])
        if "Claude" in selected_models:
            nursery.start_soon(task_wrapper, "Claude", "anthropic/claude-3-5-sonnet", prompts_dict["Claude"])
            
    return outputs

def generate_synthesis(synthesis_model_path, user_prompt, engine_outputs):
    # Formulate a dynamic prompt containing only the active responses
    context_str = ""
    for model_name, model_out in engine_outputs.items():
        context_str += f"\n--- {model_name.upper()} PERSPECTIVE ---\n{model_out}\n"
        
    synthesis_prompt = f"""
    You are an AI Product Moderator and Project Manager. 
    The user is trying to build a product based on this original prompt: "{user_prompt}"
    
    You have gathered perspectives from the active models:
    {context_str}
    
    Your task is to merge, clean, and synthesize these active outputs into one comprehensive Master Blueprint. 
    Ensure technical insights are seamlessly balanced with strategic narratives.
    """
    
    response = litellm.completion(
        model=synthesis_model_path,
        messages=[{"role": "user", "content": synthesis_prompt}]
    )
    return response.choices.message.content

# 2. STREAMLIT UI SETUP
st.set_page_config(layout="wide", page_title="AI Moderator Orchestrator")
st.title("🤖 AI Moderator Orchestrator")

# 3. SIDEBAR CONFIGURATION (Toggles and Selectors)
st.sidebar.header("🎛️ Model Controls")

# Checkboxes to select active models
st.sidebar.subheader("1. Active Perspectives")
run_chatgpt = st.sidebar.checkbox("Include ChatGPT (gpt-4o)", value=True)
run_claude = st.sidebar.checkbox("Include Claude (claude-3-5-sonnet)", value=True)

# Map human selections to internal states
selected_engines = []
if run_chatgpt: selected_engines.append("ChatGPT")
if run_claude: selected_engines.append("Claude")

# Dropdown to choose who synthesizes the final report
st.sidebar.subheader("2. Synthesis Engine")
synth_choice = st.sidebar.selectbox(
    "Choose who blends the outputs:",
    ["ChatGPT (gpt-4o)", "Claude (claude-3-5-sonnet)"]
)
synth_model_path = "openai/gpt-4o" if "ChatGPT" in synth_choice else "anthropic/claude-3-5-sonnet"

# Pre-defined system identities
SYSTEM_PROMPTS = {
    "ChatGPT": "You are a creative, customer-obsessed Product Strategy Consultant. Focus on human emotion, pitch messaging, and product value propositions.",
    "Claude": "You are a strict, deeply technical Principal Systems Architect. Focus on production infrastructure, code architecture, and database schemas."
}

# 4. MAIN CHAT INTERFACE
user_input = st.text_area("Enter your product prompt or update:", height=150, placeholder="e.g., How do we structure the user authentication flow?")

if st.button("Run Orchestration pipeline", type="primary"):
    if not user_input.strip():
        st.warning("Please enter a prompt first.")
    elif not selected_engines:
        st.error("Please toggle on at least one model in the sidebar.")
    else:
        with st.spinner("Processing your orchestration pipeline..."):
            # Step 1: Run active models in parallel
            raw_responses = trio.run(run_parallel_orchestration, selected_engines, user_input, SYSTEM_PROMPTS)
            
            # Step 2: Generate synthesis
            final_blend = generate_synthesis(synth_model_path, user_input, raw_responses)
            
            # Step 3: Dynamic Tab UI generation
            tab_names = ["🎯 Unified Synthesis"] + [f"📦 {name} Raw" for name in raw_responses.keys()]
            ui_tabs = st.tabs(tab_names)
            
            # Populate synthesis tab
            with ui_tabs[0]:
                st.markdown(f"### 🏆 Combined Master Blueprint (Synthesized by {synth_choice})")
                st.write(final_blend)
                
            # Populate individual raw data tabs dynamically
            for idx, (model_name, output_text) in enumerate(raw_responses.items(), start=1):
                with ui_tabs[idx]:
                    st.markdown(f"### Current data from {model_name}")
                    st.write(output_text)
import logging
# Suppress Streamlit's internal thread warnings
logging.getLogger("streamlit.runtime.scriptrunner_shared").setLevel(logging.ERROR)
