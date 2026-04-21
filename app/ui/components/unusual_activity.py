import streamlit as st
from typing import List
from app.models.unusual_activity import UnusualActivitySignal


def display_unusual_activity_signals(signals: List[UnusualActivitySignal]):
    """Display unusual activity signals in a Streamlit UI."""
    st.subheader("Unusual Activity Signals")
    
    if not signals:
        st.write("No unusual activity detected.")
        return
    
    for signal in signals:
        with st.expander(f"{signal.symbol} - {signal.signal_type}"):
            st.write(f"Score: {signal.score:.2f}")
            st.write(f"Value: {signal.value:.2f}")
            st.write(f"Baseline Value: {signal.baseline_value:.2f}")
            st.write(f"Timestamp: {signal.timestamp}")