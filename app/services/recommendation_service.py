def generate_recommendations(weak_subjects, momentum_score, coding_activity):
    
    recommendations = []

    for subject in weak_subjects:

        recommendations.append(f"Focus on {subject} this week")

    if coding_activity < 30:

        recommendations.append("Solve at least 5 coding problems this week")

    if momentum_score < 60:

        recommendations.append("Increase study consistency to improve momentum")

    if momentum_score > 80:

        recommendations.append("Great progress! Maintain your current learning pace")

    return {
        "recommendations": recommendations
    }