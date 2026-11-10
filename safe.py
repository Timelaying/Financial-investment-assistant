import streamlit as st


def render_safely(name, render, *args):
    """Run one tab, and show a notice instead of crashing the whole page.

    Several tabs depend on third-party data sources (Finviz, Yahoo Finance,
    CNBC) that can refuse or rate-limit requests from cloud hosts. Without
    this, one failing request aborts the script and every later tab goes blank.
    """
    try:
        render(*args)
    except Exception as exc:  # noqa: BLE001 - show any failure to the visitor
        st.warning(
            f"{name} could not load right now ({type(exc).__name__}). "
            "The data provider may be limiting requests from this host. "
            "Please try again in a few minutes."
        )
