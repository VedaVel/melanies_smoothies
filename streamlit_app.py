# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col 
import requests
 

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie !:cup_with_straw:")
st.write(
    """Choose your fruits you want in your custom smoothie.
    """
)
#Enter Customer Name
name_of_order = st.text_input('Name on Smoothie:', '')
st.write('The name on your Smoothie will be:',name_of_order )

#Select Fruits from table
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto five fruits:'
     ,my_dataframe
     ,max_selections = 5
    )
#st.write('You selected:', ingredients_list)
if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '
        #New Section to display nutrition information
          fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
          fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
      my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_of_order +"""')"""
       time_to_insert = st.button('Submit')
    # This if statement executes when submit button has a value
    if time_to_insert:
    #if  ingredients_string: The if statement executes when ingredients_string has value
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '+ name_of_order+ '!', icon="✅")


