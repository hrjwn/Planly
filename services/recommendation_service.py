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
