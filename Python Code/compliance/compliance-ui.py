import streamlit as st
import requests
import json
import pandas as pd

FLASK_API_URL = "http://127.0.0.1:5000/call_api"

st.set_page_config(layout="wide")
st.title("Compliance- AI")

st.subheader("Add Input Name")

col1, col2 = st.columns(2)

type_options = ["Individual", "Entity", "Vessel", "Aircraft"]
selected_type = col1.selectbox("Type", type_options)

name = col1.text_input("Name *")
address1 = col1.text_input("Address1")
address2 = col1.text_input("Address2")
city = col2.text_input("City *")
state = col2.text_input("State")
zip_code = col2.text_input("Zip Code")
country = col2.text_input("Country *")

if st.button("Submit"):
    if not name:
        st.error("Name is required")
    
    if not city:
        st.error("City is required")

    if not country:
        st.error("Country is required")

    query_data = {
        "type": selected_type,
        "name": name,
        "address1": address1,
        "address2": address2,
        "city": city,
        "state": state,
        "zipCode": zip_code,
        "country": country,
        "skipScanning": "no"
    }


    try:
        payload = {"query": [query_data]}
        headers = {'Content-Type' : 'application/json'}
        response = requests.post(FLASK_API_URL, json = payload, headers = headers)
        # Raise exception for bad code status
        response.raise_for_status()

        st.subheader("AI System Response:")
        response_data = response.json()

        if isinstance(response_data, dict) and "body" in response_data:
            try:
                body_data = response_data['body']['body']
                if isinstance(body_data, dict) and "Response" in body_data:
                    response_content = body_data["Response"]
                    main_response_data = {k: v for k, v in response_content.items() if k != 'Match_Details'}
                    if main_response_data:
                        num_cols = len(main_response_data)
                        cols = st.columns(num_cols if num_cols > 0 else 1)
                        col_index = 0
                        for key, value in main_response_data.items():
                            cols[col_index % num_cols].metric(key.replace("_", " ").title(), value)
                            col_index += 1

                        if "Description" in main_response_data:
                            st.subheader("Description:")
                            st.write(main_response_data["Description"])
                        st.markdown("---")
                        # df_main = pd.DataFrame([main_response_data])
                        # st.subheader("Main Response:")
                        # st.dataframe(df_main)
                    else:
                        st.info("No main response data to display (excluding Match_Details).")

                    # Display matching details information
                    if "Match_Details" in response_content:
                        match_details_list = response_content['Match_Details']
                        if isinstance(match_details_list, list):
                            match_data_for_df = []
                            for match in match_details_list:
                                base_match_data = {
                                    "Type": match.get("Type", ""),
                                    "Input Name": match.get("Matching_Data_From_Input", ""),
                                    "Address": match.get("Address", ""),
                                    "Hits": match.get("Number_of_Hits", ""),
                                    "Percentage Score": match.get("Percentage_Score", ""),
                                    # Add other relevant fields directly from the 'match' dictionary
                                    **{k: v for k, v in match.items() if k not in ['Type', 'Matching_Data_From_Input', 'Address', 'Number_of_Hits', 'Percentage_Score', 'Reviewer', 'Approver', 'Additional_Matches']},
                                    "Reviewer": match.get("Reviewer", ""),
                                    "Approver": match.get("Approver", "")
                                }
                                match_data_for_df.append(base_match_data)

                                if "Additional_Matches" in match and isinstance(match["Additional_Matches"], list):
                                    for additional_match in match["Additional_Matches"]:
                                        additional_match_data = {
                                            "Type": match.get("Type", ""),
                                            "Name": additional_match.get("Name", ""),
                                            "Address": "",
                                            "Score": additional_match.get("Score", ""),
                                            "Reviewer": "",
                                            "Approver": "",
                                            **{f"Additional Matches_{k.replace(' ', '_').title()}": v for k, v in additional_match.items() if k not in ['Name', 'Score', 'SDN_Entry', 'Terrorist_Affiliation', 'Terrorist_Designation', 'Why_Not_100%', 'Current_Location_Discrepancy', 'Origin_Country']}
                                        }
                                        match_data_for_df.append(additional_match_data)

                            if match_data_for_df:
                                match_df = pd.DataFrame(match_data_for_df)
                                st.subheader("Match Details:")
                                st.dataframe(match_df)
                            else:
                                st.info("No matching details found.")
                            
                            # data_for_match_df = []
                            # for match_detail in match_details_list:
                            #     flattened_detail = {}
                            #     for key, value in match_detail.items():
                            #         if isinstance(value, list):
                            #             for i, item in enumerate(value):
                            #                 if isinstance(item, dict):
                            #                     for sub_key, sub_value in item.items():
                            #                         flattened_detail[f"{key}_{i}_{sub_key}"] = sub_value
                            #                 else:
                            #                     flattened_detail[f"{key}_{i}"] = str(item)
                            #         else:
                            #             flattened_detail[key] = value
                            #     data_for_match_df.append(flattened_detail)

                            # if data_for_match_df:
                            #     match_df = pd.DataFrame(data_for_match_df)
                            #     st.subheader("Matching Details:")
                            #     st.dataframe(match_df)
                            # else:
                            #     st.info("No matching details found.")
                        else:
                            st.warning("Match_Details is not a list, cannot display as a separate table.")
                            st.json(match_details_list)
                    else:
                        st.info("No 'Match_Details' found in the response.")

                else:
                    st.json(body_data)
                    st.warning("Response 'body' does not contain 'Response' or is not a dictionary, displaying as JSON.")

            except Exception as e:
                st.error(f"Could not display 'body' as a table: {e}")
                st.json(response_data['body'])
        else:
            st.json(response_data)
            st.warning("Response does not contain a 'body' dictionary or is not a dictionary itself, displaying raw JSON.")

        st.subheader("AI Response Details:")
        st.write(f"Status Code : {response.status_code}")
        st.write("Headers")
        st.json(dict(response.headers))
        st.write("AI Response :")
        st.json(dict(response_data['body']))

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the Flask API : {e}")
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON input : {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred : {e}")