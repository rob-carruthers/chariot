import streamlit as st
import requests
import os

url = os.environ.get("API_URL", None)
st.session_state["return_value"] = ""

if url:
    st.markdown("""
    # Chariot

    Enter a journey request below. For example:

    _I would like to go to Manor House from Turnpike Lane, please_
    """)

    with st.form("form"):
        journey_query = st.text_area("Where would you like to go?")
        def journey_request(query):
            """
            Perform a journey request based on user input.
            """
            if query:
                response = requests.get(url, params={"query": query}, timeout=10).json()
                output = []
                duration = response.get("duration", None)
                if duration:
                    if duration == 1:
                        output.append("Your journey will last about 1 minute.")
                    else:
                        output.append(f"Your journey will last about {duration} minutes.")

                legs = response.get("legs", None)
                if legs:
                    if legs[0]:
                        summary = legs[0].get("summary", "")
                        if summary:
                            summary = summary.split(" to ")[0].strip()
                        departure = legs[0].get("departure_station", "")
                        arrival = legs[0].get("arrival_station", "")
                        interchange = legs[0].get("interchange_duration", 0)
                        output.append(f"First, take the {summary} from {departure} to {arrival}.")

                        if interchange == 1:
                            output.append(f"Your change at {arrival} will take {interchange} minute.")
                        if interchange > 1:
                            output.append(f"Your change at {arrival} will take {interchange} minutes.")


                    for leg in legs[1:]:
                        summary = leg.get("summary", "")
                        if summary:
                            summary = summary.split(" to ")[0].strip()
                        departure = leg.get("departure_station", "")
                        arrival = leg.get("arrival_station", "")
                        interchange = leg.get("interchange_duration", 0)
                        output.append(f"At {departure}, take the {summary} from {departure} to {arrival}.")

                        if interchange == 1:
                            output.append(f"Your change at {arrival} will take {interchange} minute.")
                        if interchange > 1:
                            output.append(f"Your change at {arrival} will take {interchange} minutes.")

                st.session_state["return_value"] = "\n\n".join(output)

        st.form_submit_button("Go!", on_click=journey_request(journey_query), type="primary")

    result = st.markdown(st.session_state["return_value"])


else:
    st.markdown("""
    # Chariot

    `API_URL` is not set!
    """)
