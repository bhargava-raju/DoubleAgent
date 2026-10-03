"""DoubleAgent's first UI (Lesson 1.5). Run it with:

    uv run streamlit run src/doubleagent/ui/app.py

Streamlit re-runs this whole script top to bottom on every interaction (C#: think of
Blazor Server re-rendering, where `st.session_state` is the state that survives).
The tests in tests/module01/test_ui.py drive this page with Streamlit's AppTest and
replace `backend.answer`/`backend.compare`, so always call them as `backend.<name>(...)`.
"""

import asyncio  # noqa: F401  (you will need it)

import streamlit as st

from doubleagent.scorecard import PRICES  # noqa: F401  (model choices)
from doubleagent.ui import backend  # noqa: F401

st.set_page_config(page_title="DoubleAgent", page_icon="🕵️")
st.title("DoubleAgent")

# TODO (1.5), in this order:
#
# 1. Guardrail: if backend.config_error() returns a message, show it with st.error(...)
#    and call st.stop() so nothing else renders. (Tip: the walrus operator `:=`.)
#
# 2. Sidebar (`with st.sidebar:`):
#      - a model st.selectbox over the PRICES keys, defaulting to "claude-opus-5-5"
#      - a "Max agent turns" st.slider from 1 to 10, default 5
#      - a "New conversation" st.button with key="new_conversation" that empties the history
#
# 3. Make sure st.session_state.history exists (a list of dicts: role, content, tool_calls).
#
# 4. Two tabs: chat, scores = st.tabs(["Chat", "Scorecard"])
#
#    Chat tab:
#      - replay the history: one st.chat_message(role) per turn with st.markdown(content);
#        for assistant turns with tool calls, an st.expander listing each tool name with st.code
#      - question := st.chat_input("Ask about a supplier"):
#          append the user turn, call backend.answer(...) inside st.spinner via asyncio.run,
#          append the assistant turn (answer + tool_calls), then st.rerun()
#
#    Scorecard tab:
#      - st.text_area for the task, st.text_input for comma-separated keywords,
#        st.multiselect for models
#      - an st.button("Run comparison", key="run_comparison") that calls backend.compare(...)
#        and shows the rows in st.dataframe and cost per model in st.bar_chart

raise NotImplementedError("Lesson 1.5: build the UI")
