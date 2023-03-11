import streamlit as st
from math import ceil
from datetime import datetime
from datetime import timedelta

default_start_date = '2021/10/09'
start = datetime.strptime(default_start_date, '%Y/%m/%d')


def calc_lease(mileage, annual_mileage=10000, term=3, overage_cost=0.25, start=start):
    date_format = '%Y-%m-%d'
    length_years = term
    length_days = ceil(length_years * 365.25)
    annual_mileage = annual_mileage
    total_mileage = length_years * annual_mileage
    cost_per_extra_mile = overage_cost
    allowed_overage = 200
    end = start + timedelta(days=length_days)
    allowed_miles_per_day = (annual_mileage * length_years) / length_days
    today = datetime.now().date()
    days_elapsed = today - start
    days_left = end - today
    miles_driven_per_day = mileage / days_elapsed.days
    expected_mileage = days_elapsed.days * allowed_miles_per_day
    miles_remaining = total_mileage - mileage
    new_miles_per_day = miles_remaining / days_left.days
    projected_final_mileage = miles_driven_per_day * days_left.days + mileage
    overage_miles = projected_final_mileage - (annual_mileage * length_years)
    overage_cost = (overage_miles - allowed_overage) * cost_per_extra_mile

    results = {
        "Expected Current Mileage": "{:.1f}".format(expected_mileage),
        "Projected Final Mileage": "{:.1f}".format(projected_final_mileage),
        "Projected Overage (Miles)": "{:.1f}".format(overage_miles),
        "Projected Overage Cost": "${:.2f}".format(overage_cost),
        "Miles Allowed/Day": "{:.1f}".format(allowed_miles_per_day),
        "Miles Driven/Day": "{:.1f}".format(miles_driven_per_day),
        "Updated Miles Allowed/Day": "{:.1f}".format(new_miles_per_day),
        "Days Elapsed": days_elapsed.days,
        "Days Left": days_left.days,

    }
    return results


st.header("Lease Calculator")

with st.form('Lease Information'):
    mileage = st.number_input('Current Mileage', value=0, min_value=0)
    annual_mileage = st.number_input('Annual Allowed Mileage', min_value=10000, max_value=15000)
    term = st.slider('Term (years)', value=3, max_value=3, min_value=1) 
    overage_cost = st.number_input('Overage Cost per Mile', value=0.25, min_value=0.0)
    start_str = st.date_input('Lease Start Date', value=start)

    submitted = st.form_submit_button("Submit")
    if submitted:
        for key, value in calc_lease(mileage, annual_mileage, term, overage_cost, start_str).items():
            st.text(key)
            st.text(value)

