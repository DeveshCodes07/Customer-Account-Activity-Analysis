"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Reusable Tailwind CSS UI Component Library
File: src/ui.py
"""

import streamlit as st
import streamlit.components.v1 as components

def render_tailwind_header(title: str, subtitle: str, badge_text: str = "FinEdge Analytics", category: str = "Enterprise Edition"):
    """
    Renders an institutional executive hero header with Tailwind CSS via iframe.
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; background-color: transparent; }}
        </style>
    </head>
    <body>
        <div class="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 rounded-2xl p-6 text-white shadow-lg border border-slate-800">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-300 border border-blue-500/30">
                            {badge_text}
                        </span>
                        <span class="text-xs text-slate-400 font-medium tracking-wide uppercase">
                            {category}
                        </span>
                    </div>
                    <h1 class="text-2xl font-bold tracking-tight text-white mb-1">
                        {title}
                    </h1>
                    <p class="text-sm text-slate-300 max-w-2xl">
                        {subtitle}
                    </p>
                </div>
                <div class="flex items-center gap-3">
                    <div class="text-right hidden sm:block">
                        <div class="text-xs text-slate-400">System Status</div>
                        <div class="text-xs font-semibold text-emerald-400 flex items-center justify-end gap-1">
                            <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
                            SQLite Engine Online
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=135, scrolling=False)

def render_kpi_card(title: str, value: str, delta: str = None, is_positive: bool = True, icon: str = "📊", subtext: str = None):
    """
    Renders a single high-impact KPI metric card styled with Tailwind CSS.
    """
    delta_html = ""
    if delta:
        if is_positive:
            pill_color = "bg-emerald-50 text-emerald-700 border-emerald-200"
            arrow = "▲"
        else:
            pill_color = "bg-rose-50 text-rose-700 border-rose-200"
            arrow = "▼"
        delta_html = f"""
        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-semibold border {pill_color}">
            {arrow} {delta}
        </span>
        """
        
    subtext_html = f'<div class="text-xs text-slate-500 mt-1">{subtext}</div>' if subtext else ""
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; background-color: transparent; }}
        </style>
    </head>
    <body>
        <div class="bg-white rounded-xl p-5 border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <div class="flex justify-between items-start mb-2">
                <span class="text-xs font-medium uppercase tracking-wider text-slate-500">{title}</span>
                <span class="text-lg">{icon}</span>
            </div>
            <div class="flex items-baseline justify-between gap-2">
                <div class="text-2xl font-bold tracking-tight text-slate-900">{value}</div>
                {delta_html}
            </div>
            {subtext_html}
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=125, scrolling=False)

def render_kpi_row_4(kpis: list):
    """
    Renders a 4-column row of KPI cards using Tailwind Grid inside a single iframe for optimal alignment.
    kpis is a list of dicts: [{'title': ..., 'value': ..., 'delta': ..., 'is_positive': ..., 'icon': ..., 'subtext': ...}, ...]
    """
    cards_html = ""
    for k in kpis:
        delta_html = ""
        if k.get("delta"):
            is_pos = k.get("is_positive", True)
            pill = "bg-emerald-50 text-emerald-700 border-emerald-200" if is_pos else "bg-rose-50 text-rose-700 border-rose-200"
            arrow = "▲" if is_pos else "▼"
            delta_html = f'<span class="inline-flex items-center gap-0.5 px-2 py-0.5 rounded text-xs font-semibold border {pill}">{arrow} {k["delta"]}</span>'
        
        sub = f'<p class="text-xs text-slate-400 mt-1">{k.get("subtext", "")}</p>' if k.get("subtext") else ""
        
        cards_html += f"""
        <div class="bg-white rounded-xl p-4 border border-slate-200/80 shadow-sm">
            <div class="flex justify-between items-center text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">
                <span>{k['title']}</span>
                <span class="text-base">{k.get('icon', '📈')}</span>
            </div>
            <div class="flex items-baseline justify-between">
                <span class="text-2xl font-bold tracking-tight text-slate-900">{k['value']}</span>
                {delta_html}
            </div>
            {sub}
        </div>
        """
        
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 4px; background-color: transparent; }}
        </style>
    </head>
    <body>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {cards_html}
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=120, scrolling=False)

def render_insight_box(title: str, message: str, level: str = "info"):
    """
    Renders an executive insight callout box with Tailwind styling.
    level: 'info', 'warning', 'success', 'danger'
    """
    themes = {
        "info": {"bg": "bg-blue-50", "border": "border-blue-400", "title": "text-blue-900", "text": "text-blue-800", "icon": "ℹ️"},
        "warning": {"bg": "bg-amber-50", "border": "border-amber-400", "title": "text-amber-900", "text": "text-amber-800", "icon": "⚠️"},
        "success": {"bg": "bg-emerald-50", "border": "border-emerald-400", "title": "text-emerald-900", "text": "text-emerald-800", "icon": "✅"},
        "danger": {"bg": "bg-rose-50", "border": "border-rose-400", "title": "text-rose-900", "text": "text-rose-800", "icon": "🚨"}
    }
    cfg = themes.get(level, themes["info"])
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 2px; background-color: transparent; }}
        </style>
    </head>
    <body>
        <div class="{cfg['bg']} border-l-4 {cfg['border']} rounded-r-xl p-4 shadow-sm">
            <div class="flex items-start gap-3">
                <span class="text-lg">{cfg['icon']}</span>
                <div>
                    <h4 class="text-sm font-semibold {cfg['title']} mb-0.5">{title}</h4>
                    <p class="text-xs {cfg['text']} leading-relaxed">{message}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=85, scrolling=False)

def render_alert_banner(alert_title: str, alert_message: str):
    """
    Renders a prominent, high-priority alert banner for critical banking thresholds.
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 2px; background-color: transparent; }}
        </style>
    </head>
    <body>
        <div class="bg-red-50 border border-red-300 rounded-xl p-4 shadow-sm flex items-center gap-3">
            <div class="flex-shrink-0 h-10 w-10 bg-red-100 rounded-full flex items-center justify-center text-red-600 text-xl font-bold">
                ⚠️
            </div>
            <div>
                <h4 class="text-sm font-bold text-red-900">{alert_title}</h4>
                <p class="text-xs text-red-700 leading-tight mt-0.5">{alert_message}</p>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=90, scrolling=False)
