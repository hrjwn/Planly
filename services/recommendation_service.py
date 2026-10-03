from typing import Dict, Any, List

class RecommendationService:

    @staticmethod
    def get_primary_recommendation(workload_level: str) -> str:
        if workload_level == "Low":
            return "Your workload is manageable. Keep your tasks organized and stay consistent."
        elif workload_level == "Medium":
            return "You have several pending tasks. Consider starting with your closest deadlines."
        elif workload_level == "High":
            return "You have many pending tasks. Try breaking larger activities into smaller steps and spreading them across different days."
        else:
            return "Keep tracking your tasks regularly to maintain a balanced academic routine."

    @staticmethod
    def get_detailed_recommendations(analysis: Dict[str, Any]) -> List[str]:
        tips = []
        workload = analysis.get("workload_level", "Low")
        overdue_count = len(analysis.get("overdue_tasks", []))
        high_priority = analysis.get("high_priority_pending", 0)
        upcoming = analysis.get("upcoming_tasks", [])

        if overdue_count > 0:
            tips.append(
                f"Attention Needed: You have {overdue_count} overdue task(s). "
                "Prioritize submitting these first or communicate with your course instructor."
            )

        if high_priority > 0:
            tips.append(
                f"Priority Focus: You have {high_priority} High-Priority task(s) pending. "
                "Reserve your peak concentration hours for these core deliverables."
            )

        due_soon = [t for t in upcoming if 0 <= t.days_until_deadline() <= 2]
        if due_soon:
            task_names = ", ".join([f"'{t.title}'" for t in due_soon[:2]])
            tips.append(
                f"Upcoming Delivery: Due within 48 hours: {task_names}. "
                "Review the project rubric and prepare submissions in advance."
            )

        if workload == "High":
            tips.append(
                "Pacing Strategy: Distribute study intervals into 25-minute focus sessions "
                "separated by short breaks to maintain stamina across multiple deadlines."
            )
        elif workload == "Medium":
            tips.append(
                "Daily Planning: Set aside 1 to 2 dedicated study blocks today to complete "
                "at least one assignment and prevent task accumulation."
            )
        else:
            tips.append(
                "Consistent Routine: With a light academic load, use this time to review "
                "upcoming syllabus topics or take scheduled rest."
            )

        tips.append(
            "Academic Balance: Consistent sleep schedules and hydration support long-term "
            "academic retention and focus."
        )

        return tips