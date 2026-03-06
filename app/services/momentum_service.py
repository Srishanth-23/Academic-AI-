def calculate_momentum(attendance, marks, coding_activity):
    
    score = (
        attendance * 0.4 +
        marks * 0.4 +
        min(coding_activity, 100) * 0.2
    )

    if score > 75:
        trend = "Improving"

    elif score >= 50:
        trend = "Stable"

    else:
        trend = "Declining"

    return {
        "momentum_score": round(score, 2),
        "trend": trend
    }