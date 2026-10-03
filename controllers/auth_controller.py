import re
from typing import Tuple
import streamlit as st
from database.supabase_client import get_supabase_client, reset_supabase_client
from models.student import Student
from controllers.student_controller import StudentController


class AuthController:

    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return bool(re.match(pattern, email.strip()))

    @staticmethod
    def register_student(
        name: str, email: str, course: str, password: str, confirm_password: str
    ) -> Tuple[bool, str]:
        if not name or not name.strip():
            return False, "Please enter your full name."
        if not email or not email.strip():
            return False, "Please enter your email address."
        if not AuthController.is_valid_email(email):
            return False, "Please enter a valid email address (e.g., student@university.edu)."
        if not course or not course.strip():
            return False, "Please enter your course or degree program."
        if not password:
            return False, "Please enter a password."
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        if password != confirm_password:
            return False, "Passwords do not match. Please re-enter."

        clean_name = name.strip()
        clean_email = email.strip().lower()
        clean_course = course.strip()

        client = get_supabase_client()

        try:
            auth_response = client.auth.sign_up({
                "email": clean_email,
                "password": password,
                "options": {
                    "data": {
                        "name": clean_name,
                        "course": clean_course,
                    }
                }
            })

            user = auth_response.user
            if not user or not user.id:
                return False, "Registration failed: Could not create user account."

            auth_user_id = str(user.id)

            try:
                profile_payload = {
                    "auth_user_id": auth_user_id,
                    "name": clean_name,
                    "email": clean_email,
                    "course": clean_course,
                }
                client.table("students").insert(profile_payload).execute()
            except Exception as profile_err:
                err_str = str(profile_err).lower()
                if "duplicate" in err_str or "unique" in err_str:
                    return False, "An account with this email already exists."
                print(f"[AuthController] Note during student insert: {profile_err}")

            return True, "Account created successfully! You can now log in with your credentials."

        except Exception as e:
            error_message = str(e).lower()
            if "already registered" in error_message or "user already exists" in error_message:
                return False, "An account with this email is already registered. Please log in."
            elif "rate limit" in error_message:
                return False, "Authentication rate limit reached. Please wait a moment before trying again."
            return False, "Unable to create your account. Please check your information and try again."

    @staticmethod
    def login_student(email: str, password: str) -> Tuple[bool, str]:
        if not email or not email.strip():
            return False, "Please enter your email address."
        if not password:
            return False, "Please enter your password."

        clean_email = email.strip().lower()
        client = get_supabase_client()

        try:
            auth_response = client.auth.sign_in_with_password({
                "email": clean_email,
                "password": password,
            })

            user = auth_response.user
            if not user or not user.id:
                return False, "Invalid email or password."

            auth_user_id = str(user.id)

            student = StudentController.get_student_by_auth_id(auth_user_id)

            if not student:
                meta = getattr(user, "user_metadata", {}) or {}
                name = meta.get("name", clean_email.split("@")[0].capitalize())
                course = meta.get("course", "General Student")

                try:
                    insert_res = client.table("students").insert({
                        "auth_user_id": auth_user_id,
                        "name": name,
                        "email": clean_email,
                        "course": course,
                    }).execute()
                    if insert_res.data:
                        student = Student.from_dict(insert_res.data[0])
                except Exception as db_err:
                    print(f"[AuthController] Profile auto-creation fallback error: {db_err}")

            if not student:
                student = Student(
                    student_id=None,
                    auth_user_id=auth_user_id,
                    name=clean_email.split("@")[0].capitalize(),
                    email=clean_email,
                    course="General Student",
                )

            st.session_state.logged_in = True
            st.session_state.student = student
            st.session_state.auth_user_id = auth_user_id

            return True, f"Welcome back, {student.name}!"

        except Exception as e:
            err_msg = str(e).lower()
            if "invalid" in err_msg or "credentials" in err_msg or "grant" in err_msg:
                return False, "Invalid email or password. Please check your credentials."
            elif "email not confirmed" in err_msg:
                return False, "Your email is not confirmed yet. In your Supabase Dashboard, disable 'Confirm email' for instant local testing."
            return False, f"Login failed: {str(e)}"

    @staticmethod
    def logout_student():
        reset_supabase_client()
        st.session_state.clear()
        st.rerun()