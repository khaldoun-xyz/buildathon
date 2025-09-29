import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


APP_TITLE = "Cologne AI Buildathon — Oct 18"
EVENT_DATE = "October 18, 2025"
EVENT_CITY = "Cologne, Germany"
EVENT_TAGLINE = "A one-day sprint to build AI apps"
REGISTRATION_LIMIT = 30


def ensure_data_dir() -> Path:
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_rsvp_csv_path() -> Path:
    return ensure_data_dir() / "rsvps.csv"


def load_rsvps() -> pd.DataFrame:
    csv_path = get_rsvp_csv_path()
    if csv_path.exists():
        try:
            return pd.read_csv(csv_path)
        except Exception:
            return pd.DataFrame(columns=["timestamp", "name", "email", "affiliation", "role", "interests"]) 
    return pd.DataFrame(columns=["timestamp", "name", "email", "affiliation", "role", "interests"]) 


def append_rsvp(record: dict) -> None:
    csv_path = get_rsvp_csv_path()
    df_existing = load_rsvps()
    df_new = pd.DataFrame([record])
    df_all = pd.concat([df_existing, df_new], ignore_index=True)
    df_all.to_csv(csv_path, index=False)


def render_header():
    st.set_page_config(page_title=APP_TITLE, page_icon="🤖", layout="wide")
    st.title(APP_TITLE)
    st.subheader(f"{EVENT_CITY} · {EVENT_DATE}")
    st.caption(EVENT_TAGLINE)


def render_hero():
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown(
            """
            Join developers, researchers, product builders, and students for a focused day of rapid prototyping.
            Bring an idea, form a team, ship an MVP by evening. Demos, feedback, and community — all in one day.
            """
        )
        st.markdown("- Hands-on building, not talks")
        st.markdown("- Team up or go solo")
        st.markdown("- Demos and prizes at the end")
        st.markdown("- All skill levels welcome")
        st.write("")
        st.link_button("RSVP Now", "#rsvp", type="primary")
    with col2:
        st.metric("Target participants", f"{REGISTRATION_LIMIT}")


def render_agenda():
    st.markdown("---")
    st.header("Agenda")
    agenda = [
        ("09:00", "Check-in, coffee"),
        ("10:00", "Kickoff and problem pitches"),
        ("10:30", "Tips on using AI assistants"),
        ("11:00", "Building starts"),
        ("17:00", "Demos"),
        ("18:00", "Group vote and closing"),
    ]
    for time_str, item in agenda:
        st.markdown(f"**{time_str}** — {item}")


def render_faq():
    st.markdown("---")
    st.header("FAQ")
    with st.expander("Who should attend?"):
        st.write("Builders of all kinds: engineers, designers, PMs, researchers, students.")
    with st.expander("Do I need a team?"):
        st.write("No. Team formation happens on the day, and solo builders are welcome.")
    with st.expander("What should I bring?"):
        st.write("Laptop, charger, and an idea. We'll handle the rest.")


def render_contact():
    st.markdown("---")
    st.header("Contact")
    st.write("Questions or sponsorship inquiries: email ")
    st.code("alex.gansmann@hey.com")


def render_rsvp():
    st.markdown("---")
    st.header("RSVP")
    st.markdown("<a id='rsvp'></a>", unsafe_allow_html=True)

    rsvps = load_rsvps()
    if len(rsvps) >= REGISTRATION_LIMIT:
        st.warning("RSVPs have reached capacity. You can still join the waitlist.")

    with st.form("rsvp_form", clear_on_submit=True):
        name = st.text_input("Full name", placeholder="Ada Lovelace")
        email = st.text_input("Email", placeholder="ada@example.com")
        affiliation = st.text_input("Affiliation (company/school)")
        role = st.selectbox("Primary role", ["Engineer", "Researcher", "Designer", "Product", "Student", "Other"])
        interests = st.text_area("What do you want to build?", height=100)
        submitted = st.form_submit_button("Submit RSVP")

        if submitted:
            if not name or not email:
                st.error("Please provide at least your name and email.")
            else:
                record = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "name": name.strip(),
                    "email": email.strip().lower(),
                    "affiliation": affiliation.strip(),
                    "role": role,
                    "interests": interests.strip(),
                }
                try:
                    append_rsvp(record)
                    st.success("Thanks! We'll be in touch with details.")
                except Exception as e:
                    st.error(f"Could not save your RSVP: {e}")


def main():
    render_header()
    render_hero()
    render_agenda()
    render_faq()
    render_rsvp()
    render_contact()


if __name__ == "__main__":
    main()


