import os
from io import StringIO
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


APP_TITLE = "Build with AI in Cologne — Oct 18"
EVENT_DATE = "October 18, 2025"
EVENT_CITY = "Cologne, Germany"
EVENT_TAGLINE = "Build a software product in one day."
REGISTRATION_LIMIT = 20


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
            return pd.DataFrame(columns=["timestamp", "name", "email", "phone", "inviter"]) 
    return pd.DataFrame(columns=["timestamp", "name", "email", "phone", "inviter"]) 


def append_rsvp(record: dict) -> None:
    csv_path = get_rsvp_csv_path()
    df_existing = load_rsvps()
    df_new = pd.DataFrame([record])
    df_all = pd.concat([df_existing, df_new], ignore_index=True)
    df_all.to_csv(csv_path, index=False)


def render_header():
    st.set_page_config(
        page_title="Build with AI in Cologne - Oct 18, 2025", 
        page_icon="🐒", 
        layout="wide"
    )
    
    # Add Open Graph meta tags for better social sharing
    st.markdown("""
    <meta property="og:title" content="Build with AI in Cologne - Oct 18, 2025">
    <meta property="og:description" content="Build a software product in one day using AI.">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Build with AI in Cologne - Oct 18, 2025">
    <meta name="twitter:description" content="Build a software product in one day using AI.">
    """, unsafe_allow_html=True)
    
    st.title(APP_TITLE)
    st.subheader(f"{EVENT_CITY} · {EVENT_DATE}")
    st.caption(EVENT_TAGLINE)


def render_hero():
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown(
            """
            We invite you to join us in this one-day challenge.  
            Out of 5 product specifications, we will try to build as many 
            products as we can within 6 hours.
            """
        )
        st.markdown("- Get free access to AI coding assistants.")
        st.markdown("- Build & deploy as many products as you can in 6 hours.")
        st.markdown("- Go solo or join a team.")
        st.markdown("- No preparation required. Just come and have fun.")
    with col2:
        current = len(load_rsvps())
        seats_left = max(REGISTRATION_LIMIT - current, 0)
        st.metric("Seats left", f"{seats_left}")

def render_rsvp():
    st.header("Reserve your spot now")
    st.markdown("<a id='rsvp'></a>", unsafe_allow_html=True)

    # Try to get passphrase from secrets first, then environment
    expected_pass = ""
    try:
        if hasattr(st, "secrets") and st.secrets:
            expected_pass = st.secrets.get("INVITE_PASSPHRASE", "")
    except Exception:
        pass
    
    if not expected_pass:
        expected_pass = os.getenv("INVITE_PASSPHRASE", "")
    
    expected_pass = expected_pass.strip()

    if not expected_pass:
        st.info("Registration is currently closed. Organisers have not enabled invites yet.")
        return

    if "invite_ok" not in st.session_state:
        st.session_state["invite_ok"] = False

    st.text_input("Invite passphrase", type="password", key="invite_pass_input")
    if st.button("Verify invite"):
        entered = (st.session_state.get("invite_pass_input") or "").strip()
        if entered == expected_pass:
            st.session_state["invite_ok"] = True
            st.success("Invite confirmed. Registration unlocked below.")
        else:
            st.session_state["invite_ok"] = False
            st.error("Incorrect code. Please try again or contact the organisers.")

    rsvps = load_rsvps()
    if len(rsvps) >= REGISTRATION_LIMIT:
        st.warning("RSVPs have reached capacity. You can still join the waitlist.")

    if not st.session_state.get("invite_ok"):
        st.info("Enter your invite code to register.")
        return

    with st.form("rsvp_form", clear_on_submit=True):
        name = st.text_input("Full name", placeholder="Ada Lovelace")
        email = st.text_input("Email", placeholder="ada@example.com")
        phone = st.text_input("Phone number", placeholder="optional")
        inviter = st.text_input("Who invited you to this event?")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name or not email:
                st.error("Please provide name and email.")
            else:
                record = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "name": name.strip(),
                    "email": email.strip().lower(),
                    "phone": phone.strip(),
                    "inviter": inviter.strip(),
                }
                try:
                    append_rsvp(record)
                    st.success("Thanks! We'll be in touch with details.")
                except Exception as e:
                    st.error(f"Could not save your RSVP: {e}")


def render_agenda():
    st.markdown("---")
    st.header("Agenda")
    agenda = [
        ("09:00", "Check-in, coffee"),
        ("09:30", "Kickoff"),
        ("10:00", "Tips on using AI assistants"),
        ("11:00", "Building starts"),
        ("17:00", "Demos"),
        ("18:00", "Group vote and closing"),
    ]
    for time_str, item in agenda:
        st.markdown(f"**{time_str}** — {item}")


def render_faq():
    st.markdown("---")
    st.header("FAQ")
    with st.expander("Why this event?"):
        st.write("""AI is changing how we work. We feel it.
            What used to take us a day, we now complete within an hour.
            Yet, AI coding assistants and all the tools surrounding them
            are changing so rapidly that we want to take some time to play around
            with new developments and catch up on new ideas.
            The original inspiration for this event is the Buildathon 
            that took place in California in August 2025 (https://www.buildathon.ai/).
            """)
    with st.expander("Where will the event take place?"):
        st.write("""We're still in the process of figuring that out. 
            The event will definitely take place in Cologne or a place very close to Cologne.
            We'll send you the exact location before the event.""")
    with st.expander("Do I need a team?"):
        st.write("No. Team formation happens on the day, and solo builders are welcome.")
    with st.expander("What should I bring?"):
        st.write("Laptop, charger and fun. We'll handle the rest.")
    with st.expander("Do I need to bring a product idea?"):
        st.write("""No, we provide you with a list of product specifications. 
            A product specification is a short text description of a product. 
            It's a list of features and requirements. This is a simplified example: 
            
            Create a web app that tracks tasks. 
            - Constraint: A task can have several states.
            """)
    with st.expander("Who are we?"):
        st.write("""We are data scientists & machine learning specialists 
            that realise AI projects at work. 
            The algorithms we deployed have significantly impacted our organisations.""") 

    
def render_contact():
    st.markdown("---")
    st.header("Contact")
    st.write("Questions? Send an email to Alex:")
    st.code("alex.gansmann@hey.com")



def render_registrations():
    st.markdown("---")

    # Try secrets first, then environment
    admin_pass = ""
    try:
        if hasattr(st, "secrets") and st.secrets:
            admin_pass = st.secrets.get("ADMIN_PASSPHRASE", "")
    except Exception:
        pass
    if not admin_pass:
        admin_pass = os.getenv("ADMIN_PASSPHRASE", "")
    admin_pass = admin_pass.strip()

    if not admin_pass:
        st.info("Admin access is disabled. Set ADMIN_PASSPHRASE to enable.")
        return

    if "admin_ok" not in st.session_state:
        st.session_state["admin_ok"] = False

    st.text_input("", type="password", key="admin_pass_input")
    if st.button("Go"):
        entered = (st.session_state.get("admin_pass_input") or "").strip()
        st.session_state["admin_ok"] = (entered == admin_pass)
        if st.session_state["admin_ok"]:
            st.success("Access granted.")
        else:
            st.error("Incorrect admin passphrase.")

    if not st.session_state.get("admin_ok"):
        return

    df = load_rsvps()
    st.subheader("Current RSVPs")
    if df.empty:
        st.write("No registrations yet.")
        return
    st.dataframe(df, use_container_width=True)

    csv_buf = StringIO()
    df.to_csv(csv_buf, index=False)
    st.download_button("Download CSV", data=csv_buf.getvalue(), file_name="rsvps.csv", mime="text/csv")



def main():
    # Simple routing using query param: ?page=registrations
    try:
        params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
    except Exception:
        params = {}

    page_val = params.get("page", "")
    if isinstance(page_val, list):
        page_val = page_val[0] if page_val else ""
    page = (page_val or "").strip().lower()

    render_header()
    if page == "registrations":
        render_registrations()
        return

    render_hero()
    render_rsvp()
    render_agenda()
    render_faq()
    render_contact()


if __name__ == "__main__":
    main()


