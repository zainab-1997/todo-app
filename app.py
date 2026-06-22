import streamlit as st
from datetime import date
from database import init_db, add_task, get_active_tasks, update_task, mark_completed, archive_task

st.set_page_config(page_title="My Tasks", page_icon="📝", layout="centered")

init_db()

st.markdown("""
<style>
    .stApp {
        background-color: #EAF2FA;
    }

    h1 {
        color: #2C6E9B;
        text-align: center;
        border-bottom: 3px solid #2C6E9B;
        padding-bottom: 10px;
    }

    h3 {
        color: #2C6E9B;
    }

    label {
        font-weight: 700 !important;
        font-size: 16px !important;
        color: #1F4E6B !important;
        font-family: 'Trebuchet MS', sans-serif !important;
    }

    button[kind="secondary"], button[kind="primary"],
    div[data-testid="stButton"] button,
    div[data-testid="stFormSubmitButton"] button {
        background-color: #2C6E9B !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }

    .stTextInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1.5px solid #B8C4CE !important;
        color: #3D3D3D !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        padding: 6px;
    }

    .task-title { font-size: 17px; font-weight: 700; color: #3D3D3D; }
    .task-meta { font-size: 13px; color: #8A8A8A; margin-top: 3px; margin-bottom: 10px; }
    .priority-bar-high { border-right: 5px solid #E07A5F; padding-right: 12px; }
    .priority-bar-medium { border-right: 5px solid #E9C46A; padding-right: 12px; }
    .priority-bar-low { border-right: 5px solid #94A89A; padding-right: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("📝 My Tasks")

with st.container(border=True):
    st.subheader("Add a New Task")

    with st.form("add_task_form", clear_on_submit=True):
        title = st.text_input("Task Title")
        due_date = st.date_input("Due Date", min_value=date.today())
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])

        submitted = st.form_submit_button("Add Task")

        if submitted:
            success, message = add_task(title, due_date.isoformat(), priority)
            if success:
                st.success(message)
            else:
                st.error(message)

st.divider()

st.subheader("My Tasks")

tasks = get_active_tasks()

if not tasks:
    st.info("No tasks yet")
else:
    for task in tasks:
        task_id, task_title, task_due_date, task_priority, is_completed = task

        priority_bar = {"High": "priority-bar-high", "Medium": "priority-bar-medium", "Low": "priority-bar-low"}.get(task_priority, "")
        title_html = f"<s>{task_title}</s>" if is_completed else task_title

        with st.container(border=True):
            st.markdown(f"""
                <div class="{priority_bar}">
                    <div class="task-title">{title_html}</div>
                    <div class="task-meta">📅 {task_due_date} &nbsp;|&nbsp; 🏷️ {task_priority}</div>
                </div>
            """, unsafe_allow_html=True)

            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                if not is_completed:
                    if st.button("✅ Done", key=f"complete_{task_id}", use_container_width=True):
                        mark_completed(task_id)
                        st.rerun()
            with btn_col2:
                if st.button("✏️ Edit", key=f"edit_{task_id}", use_container_width=True):
                    st.session_state[f"editing_{task_id}"] = True
            with btn_col3:
                if st.button("🗑️ Delete", key=f"delete_{task_id}", use_container_width=True):
                    archive_task(task_id)
                    st.rerun()

        if st.session_state.get(f"editing_{task_id}", False):
            with st.form(f"edit_form_{task_id}"):
                new_title = st.text_input("New Title", value=task_title)
                new_due_date = st.date_input("New Due Date", value=date.fromisoformat(task_due_date))
                new_priority = st.selectbox(
                    "New Priority",
                    ["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(task_priority)
                )
                save = st.form_submit_button("Save Changes")

                if save:
                    success, message = update_task(task_id, new_title, new_due_date.isoformat(), new_priority)
                    if success:
                        st.session_state[f"editing_{task_id}"] = False
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)