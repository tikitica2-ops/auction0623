import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def get_bid_ratio_trend_chart():
    """
    Generates a Line Chart showing the monthly trend of bid-to-appraisal ratios.
    """
    months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
    ratios = [78.5, 79.2, 81.0, 80.4, 82.1, 83.5, 84.0, 83.2, 85.6, 88.1, 90.5, 89.2]
    
    df = pd.DataFrame({
        "월": months,
        "낙찰가율(%)": ratios
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["월"],
        y=df["낙찰가율(%)"],
        mode="lines+markers",
        line=dict(color="#6366F1", width=3),
        marker=dict(size=8, color="#A855F7"),
        name="낙찰가율"
    ))
    
    fig.update_layout(
        title={
            "text": "📊 2025년 전국 아파트 낙찰가율 추이",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 16, "family": "Outfit, Noto Sans KR"}
        },
        xaxis_title="기준 월",
        yaxis_title="낙찰가율 (%)",
        yaxis=dict(range=[70, 100]),
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def get_property_distribution_chart():
    """
    Generates a Donut Chart showing the distribution of auction property types.
    """
    labels = ["아파트", "빌라/다세대", "상가/오피스텔", "토지/임야"]
    values = [42.5, 28.0, 18.5, 11.0]
    colors = ["#6366F1", "#A855F7", "#06B6D4", "#64748B"]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=1.5)),
        textinfo="percent+label",
        hoverinfo="label+value+percent"
    )])
    
    fig.update_layout(
        title={
            "text": "🏢 경매 매물 종류별 점유 분포",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 16, "family": "Outfit, Noto Sans KR"}
        },
        template="plotly_white",
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def get_regional_volume_chart():
    """
    Generates a Grouped Bar Chart showing total auction volume vs successful bids by region.
    """
    regions = ["서울", "경기", "인천", "부산", "대구"]
    total_volumes = [340, 480, 210, 190, 150]
    bids = [122, 158, 68, 59, 41]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=regions,
        y=total_volumes,
        name="진행 건수",
        marker_color="#6366F1"
    ))
    fig.add_trace(go.Bar(
        x=regions,
        y=bids,
        name="낙찰 건수",
        marker_color="#A855F7"
    ))
    
    fig.update_layout(
        title={
            "text": "📍 주요 지역별 진행 vs 낙찰 건수 비교",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 16, "family": "Outfit, Noto Sans KR"}
        },
        xaxis_title="지역",
        yaxis_title="건수",
        barmode="group",
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

if __name__ == "__main__":
    # Smoke test of chart builders
    fig1 = get_bid_ratio_trend_chart()
    fig2 = get_property_distribution_chart()
    fig3 = get_regional_volume_chart()
    print("Plotly chart builders initialized successfully.")
