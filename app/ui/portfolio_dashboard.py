import streamlit as st
from ..models.portfolio import PortfolioAnalytics
from ..models.opportunity import Opportunity


def show_portfolio_dashboard(opportunities: List[Opportunity]):
    analytics = PortfolioAnalytics(opportunities)

    st.title("Portfolio Analytics")

    # Exposure by symbol
    st.subheader("Exposure by Symbol")
    symbol_exposure = analytics.get_symbol_exposure()
    st.bar_chart(symbol_exposure)

    # Greeks summary
    st.subheader("Greeks Summary")
    greeks = analytics.get_greeks_summary()
    st.write(f"Delta: {greeks.delta:.2f}")
    st.write(f"Gamma: {greeks.gamma:.2f}")
    st.write(f"Theta: {greeks.theta:.2f}")
    st.write(f"Vega: {greeks.vega:.2f}")

    # Concentration warnings
    st.subheader("Concentration Warnings")
    warnings = analytics.get_concentration_warnings()
    if warnings:
        for warning in warnings:
            st.warning(warning)
    else:
        st.success("No significant concentration warnings")

    # Net premium at risk
    st.subheader("Net Premium at Risk")
    st.write(f"${analytics.get_net_premium_at_risk():.2f}")

    # Stress test
    st.subheader("Stress Test")
    stress_results = analytics.stress_test()
    st.write("10% stress test results:")
    st.write(stress_results)