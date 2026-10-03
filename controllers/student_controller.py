from typing import Optional, Tuple
from database.supabase_client import get_supabase_client
from models.student import Student


class StudentController:

    @staticmethod
    def get_student_by_auth_id(auth_user_id: str) -> Optional[Student]:
        client = get_supabase_client()
        try:
            response = (
                client.table("students")
                .select("*")
                .eq("auth_user_id", auth_user_id)
                .limit(1)
                .execute()
            )
            if response.data and len(response.data) > 0:
                return Student.from_dict(response.data[0])
            return None
        except Exception as e:
            print(f"[StudentController] Error fetching profile: {e}")
            return None

    @staticmethod
    def update_student_profile(
        student: Student, new_name: str, new_course: str
    ) -> Tuple[bool, str]:
        if not new_name or not new_name.strip():
            return False, "Student name cannot be empty."
        if not new_course or not new_course.strip():
            return False, "Course cannot be empty."

        clean_name = new_name.strip()
        clean_course = new_course.strip()

        client = get_supabase_client()
        try:
            response = (
                client.table("students")
                .update({"name": clean_name, "course": clean_course})
                .eq("id", student.student_id)
                .execute()
            )
            if response.data:
                student.update_info(clean_name, clean_course)
                return True, "Profile updated successfully!"
            else:
                return False, "Failed to update profile. Please try again."
        except Exception as e:
            return False, f"Database error updating profile: {str(e)}"