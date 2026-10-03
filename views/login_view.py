import streamlit as st
from controllers.auth_controllers import AuthController


def render_login_view():
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0 1.5rem 0;">
            <div style="display: inline-block; padding: 4px 14px; background-color: #FCE8F0; color: #C95A8D; border-radius: 20px; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.8rem;">
                Academic Planner
            </div>
            <h1 style="font-size: 2.8rem; font-weight: 700; margin-bottom: 0.3rem; color: #D96C9D; letter-spacing: -0.02em;">
                PLANLY
            </h1>
            <p style="font-size: 1.1rem; color: #3B3036; margin-bottom: 0.4rem; font-weight: 600;">
                Student Workload & Task Management System
            </p>
            <p style="font-size: 0.92rem; color: #8A737D; max-width: 520px; margin: 0 auto 0.8rem auto; line-height: 1.5;">
                Stay organized, manage your workload, and keep track of your academic progress in one place.
            </p>
            <div style="font-size: 0.82rem; color: #C95A8D; font-style: italic; letter-spacing: 0.02em;">
                Plan your work. Track your progress.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, col_center, _ = st.columns([1, 1.8, 1])

    with col_center:
        st.markdown(
            """
            <div style="background-color: #FFFFFF; border: 1px solid #F3B6CF; border-radius: 16px; padding: 0.5rem 1.8rem 1.8rem 1.8rem; box-shadow: 0 4px 16px rgba(217, 108, 157, 0.08); margin-bottom: 1.5rem;">
            """,
            unsafe_allow_html=True,
        )

        tab_login, tab_register = st.tabs(["Log In", "Create Account"])

        with tab_login:
            st.markdown(
                """
                <div style="padding: 0.8rem 0 0.5rem 0;">
                    <div style="font-size: 1.15rem; font-weight: 600; color: #3B3036; margin-bottom: 0.2rem;">Welcome Back</div>
                    <div style="font-size: 0.85rem; color: #8A737D;">Sign in with your academic credentials to view your tasks.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.form(key="login_form", clear_on_submit=False):
                email = st.text_input(
                    "Email Address",
                    placeholder="student@planly.edu",
                    key="login_email",
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password",
                )

                submit_login = st.form_submit_button(
                    "Log In", use_container_width=True, type="primary"
                )

                if submit_login:
                    success, message = AuthController.login_student(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

        with tab_register:
            st.markdown(
                """
                <div style="padding: 0.8rem 0 0.5rem 0;">
                    <div style="font-size: 1.15rem; font-weight: 600; color: #3B3036; margin-bottom: 0.2rem;">Create Account</div>
                    <div style="font-size: 0.85rem; color: #8A737D;">Register your student account to organize deadlines and workloads.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.form(key="register_form", clear_on_submit=False):
                name = st.text_input(
                    "Full Name",
                    placeholder="e.g., Hariette Reyes",
                    key="reg_name",
                )
                email = st.text_input(
                    "Email Address",
                    placeholder="e.g., hariette@planly.edu",
                    key="reg_email",
                )
                course = st.text_input(
                    "Course / Degree Program",
                    placeholder="e.g., BS Computer Science",
                    key="reg_course",
                )
                password = st.text_input(
                    "Password (minimum 6 characters)",
                    type="password",
                    placeholder="Create a password",
                    key="reg_password",
                )
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter password",
                    key="reg_confirm_password",
                )

                submit_register = st.form_submit_button(
                    "Create Account", use_container_width=True, type="primary"
                )

                if submit_register:
                    success, message = AuthController.register_student(
                        name=name,
                        email=email,
                        course=course,
                        password=password,
                        confirm_password=confirm_password,
                    )
                    if success:
                        st.success(message)
                        st.info("Your account is ready. Please switch to the Log In tab to sign in.")
                    else:
                        st.error(message)

        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("Demo Accounts for Evaluation"):
            st.markdown(
                """
                <div style="font-size: 0.85rem; color: #3B3036; line-height: 1.6;">
                    <b>Sample Student Accounts:</b>
                    <ul style="margin: 0.4rem 0 0.6rem 1.2rem; padding: 0;">
                        <li><b>Hariette Pelipas:</b> <code>hariette@gmail.edu</code> | Pass: <code>d1pelipas</code> (Medium Workload)</li>
                        <li><b>Alex Rivera:</b> <code>alex@planly.edu</code> | Pass: <code>Planly123!</code> (Low Workload)</li>
                        <li><b>Bea Santos:</b> <code>bea@planly.edu</code> | Pass: <code>Planly123!</code> (High Workload)</li>
                    </ul>
                    <i>You may also create a new student account using the Create Account tab above.</i>
                </div>
                """,
                unsafe_allow_html=True,
            )