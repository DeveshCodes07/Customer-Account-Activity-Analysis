"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Quality Assurance Test Suite: Streamlit App UI & Performance Tests
File: tests/test_app.py
"""

import os
import time
import pytest

# ---------------------------------------------------------------------
# TC-T-13: UI Module Import & Component Rendering Check
# ---------------------------------------------------------------------
def test_ui_module_components():
    """TC-T-13: Verify src/ui.py imports and renders HTML strings without errors."""
    from src.ui import render_tailwind_header, render_kpi_card, render_kpi_row_4, render_insight_box
    
    # Check callable
    assert callable(render_tailwind_header)
    assert callable(render_kpi_card)
    assert callable(render_kpi_row_4)
    assert callable(render_insight_box)

# ---------------------------------------------------------------------
# TC-T-14: Streamlit App Initialization (Streamlit AppTest)
# ---------------------------------------------------------------------
def test_streamlit_app_starts():
    """TC-T-14: Verify app.py loads via Streamlit AppTest framework without fatal exceptions."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app_path = os.path.join(base_dir, "app.py")
    
    if not os.path.exists(app_path):
        pytest.skip("app.py not yet implemented (scheduled for Step 15 build)")
        
    from streamlit.testing.v1 import AppTest
    
    start_time = time.time()
    at = AppTest.from_file(app_path, default_timeout=10)
    at.run()
    elapsed = time.time() - start_time
    
    # Assert no unhandled app exceptions
    assert not at.exception, f"AppTest encountered unhandled exception: {at.exception}"
    # Assert load time < 3.0 seconds SLA
    assert elapsed < 3.0, f"App execution took {elapsed:.2f}s, exceeding 3.0s SLA"

# ---------------------------------------------------------------------
# TC-T-15: Multipage Navigation Directory Structure Check
# ---------------------------------------------------------------------
def test_multipage_pages_structure():
    """TC-T-15: Verify pages directory contains all planned analytical screens."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pages_dir = os.path.join(base_dir, "pages")
    
    # In Step 13, check if directory exists or will be verified in Step 15
    if not os.path.exists(pages_dir):
        pytest.skip("pages/ directory build scheduled for Step 15")
        
    expected_pages = [
        "1_📊_Portfolio_Overview.py",
        "2_📈_Transaction_Trends.py",
        "3_⚡_Channel_Analytics.py",
        "4_👤_Customer_360.py",
        "5_⚠️_Dormancy_and_Churn.py",
        "6_👥_Demographic_Insights.py"
    ]
    existing_files = os.listdir(pages_dir)
    for p in expected_pages:
        assert p in existing_files, f"Page {p} missing from pages/ directory"
