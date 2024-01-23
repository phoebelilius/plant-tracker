import streamlit as st

from plant_tracker.common import format_time_difference
from plant_tracker.db import Database
from plant_tracker.db.mongo import MongoDatabase


def water_plant(name: str):
    db.water_plant(name)
    # show success message
    st.success("Watered plant!", icon="✅")
    pass


@st.cache_resource
def connect_to_db():
    # Ensure we are connected to the database
    db: Database = MongoDatabase()
    return db


if __name__ == "__main__":
    db = connect_to_db()

    st.header("Plant Tracker")
    tab_view, tab_add = st.tabs(["View plants", "Add a new plant"])

    with tab_view:
        st.header("View Plants")
        plants = db.get_plants()
        for plant in plants:
            with st.expander(plant["name"]):
                st.write(f"Species: {plant['species']}")
                st.write(f"Watering Schedule: {plant['watering_schedule']}")
                st.write(
                    f"Last Watered: {format_time_difference(plant['last_watered'])}"
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"💧 Water", key=f"water-{plant['name']}"):
                        water_plant(plant["name"])
                with col2:
                    if st.button(
                        f"Delete", key=f"delete-{plant['name']}", type="primary"
                    ):
                        db.delete_plant(plant["name"])
                        # show success message
                        st.success("Deleted plant!", icon="✅")
        # add a refresh button
        if st.button("Refresh"):
            st.rerun()

    with tab_add:
        st.header("Add Plant")
        name = st.text_input("Name")
        species = st.text_input("Species")
        watering_schedule = st.text_input("Watering Schedule")
        if st.button("Add"):
            db.add_plant(name, species, watering_schedule)
            # show success message
            st.success("Added plant!", icon="✅")
