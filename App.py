#Importing relevant packages and libraries
import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt


# Defining filepath locally
file_path = '/Users/markushenriksson/Desktop/Data/Python/Projects/ds-master/data/assignments_datasets/KIVA'

# Changing to the correct file and changing to the the working directory
os.chdir(file_path)

# Loading datasets
try: #Try function to do specific command with exceptions
    # Different parts of the dataset
    df_part_0 = pd.read_csv('kiva_loans_part_0.csv')
    df_part_1 = pd.read_csv('kiva_loans_part_1.csv')
    df_part_2 = pd.read_csv('kiva_loans_part_2.csv')

    # Concatonating the subdatasets
    df_combined = pd.concat([df_part_0, df_part_1, df_part_2], ignore_index=True)

    # Displaying dataset header 
    st.title("KIVA Loans Dataset Visualization")
    st.write("### Data Preview")
    st.dataframe(df_combined.head())

except FileNotFoundError as e:
    st.error(f"File not found: {e}")
except Exception as e:
    st.error(f"An error occurred: {e}")

# Introduction

# KIVA Loans Distribution Dashboard

st.markdown("""
            Welcome to the KIVA Loans Distribution Dashboard. In the context of global financial inclusion, understanding the dynamics of microfinance is crucial for both lenders and policymakers. This dashboard explores the distribution and impact of microloans across various countries and sectors, highlighting key patterns in funding allocation. Through detailed data visualizations, we provide insights into how these loans support economic activities, the demographics of borrowers, and the repayment trends that influence the sustainability of microfinance initiatives. Our aim is to facilitate informed decision-making that enhances the effectiveness of financial aid and fosters economic development in underserved communities
""")
with st.expander("📊 **Objective**"):
                 st.markdown("""
At the heart of this dashboard is the mission to visually decode data, equipping financial analysts and policymakers with insights to address these critical queries:

- Which countries and sectors are most significantly impacted by microloan distributions?
- What factors contribute to the varying success rates of these loans across different regions and sectors?
- Based on the observed trends, what strategies could be pivotal in enhancing the effectiveness of microloans and ensuring financial stability for borrowers?
Through interactive visualizations, this dashboard reveals the intricate patterns of loan allocations and repayments, aiming to support strategic decisions that enhance financial inclusivity and foster sustainable economic growth in underrepresented communities.
"""
)

                             
# Tutorial Expander
with st.expander("How to Use the Dashboard 📚"):
    st.markdown("""
    1. **Filter Data** - Use the sidebar filters to narrow down specific data sets.
    2. **Visualize Data** - From the dropdown, select a visualization type to view patterns.
    3. **Insights & Recommendations** - Scroll down to see insights derived from the visualizations and actionable recommendations.
    """)


# Sidebar filter for Sectors without any preselected options
sectors = df_combined['sector'].unique().tolist() #Sectors are unique and listed correctly (tolist)
selected_sector = st.sidebar.multiselect(
    "Select Sectors 🏦", 
    sectors, #Filterlist opens 
    default=[] #No preselection
)

# Sidebar filter for Countries without any preselected options
countries = df_combined['country'].unique().tolist()
selected_countries = st.sidebar.multiselect(
    "Select Countries 🌍", 
    countries, 
    default=[]
)

# Apply the filters only if selections are made
if selected_sector:
    df_combined = df_combined[df_combined['sector'].isin(selected_sector)]

if selected_countries:
    df_combined = df_combined[df_combined['country'].isin(selected_countries)]

# Check if any filters are applied
if not selected_sector and not selected_countries:
    st.warning("Please select at least one sector or country from the sidebar to view data.")
    st.stop()

# Filter the dataset based on selected sectors and countries
filtered_df = df_combined[df_combined['sector'].isin(selected_sector) & df_combined['country'].isin(selected_countries)]

# Sidebar filter: Loan Amount Range
min_loan_amount = int(filtered_df['loan_amount'].min())
max_loan_amount = int(filtered_df['loan_amount'].max())
loan_amount_range = st.sidebar.slider("Select Loan Amount Range 💵", min_loan_amount, max_loan_amount, (min_loan_amount, max_loan_amount))
filtered_df = filtered_df[(filtered_df['loan_amount'] >= loan_amount_range[0]) & (filtered_df['loan_amount'] <= loan_amount_range[1])] #Checking if amounts are greater than or less than boundaries.

# Sidebar filter: Repayment Interval
repayment_intervals = filtered_df['repayment_interval'].unique().tolist() #unique and listed correctly (tolist)
selected_repayment_interval = st.sidebar.multiselect("Select Repayment Intervals 🕰️", repayment_intervals, default=repayment_intervals) #Creating dropdown menu with options selected by default
if not selected_repayment_interval: #Conditional warning and stop if nothing is chosen
    st.warning("Please select a repayment interval from the sidebar ⚠️")
    st.stop() #Stops if nothing is selected
filtered_df = filtered_df[filtered_df['repayment_interval'].isin(selected_repayment_interval)] #Only show the data from which kinds of repayments has been chosen. Isin checks which value is in the column so it can be included or not included.

# Displaying the filtered dataset
st.title("Filtered KIVA Loans Dataset")
st.dataframe(filtered_df.head())

# Displaying the Loan Analysis header
st.header("Loan Analysis 📊")

# Dropdown to select the type of visualization
visualization_option = st.selectbox(
    "Select Visualization 🎨", 
    ["Loan Amount by Country", 
     "Loan Amount by Sector", 
     "Repayment Interval Distribution", 
     "Funded Amount by Gender"]
)

# Visualizations based on user selection
if visualization_option == "Loan Amount by Country":
    # Bar chart for loan amount by country
    chart = alt.Chart(df_combined).mark_bar().encode(
        x='country:N',
        y='sum(loan_amount):Q',
        tooltip=['country', 'sum(loan_amount)']
    ).properties(
        title='Loan Amount by Country'
    )
    st.altair_chart(chart, use_container_width=True)

elif visualization_option == "Loan Amount by Sector":
    # Bar chart for loan amount by sector
    chart = alt.Chart(df_combined).mark_bar().encode(
        x='sector:N',
        y='sum(loan_amount):Q',
        tooltip=['sector', 'sum(loan_amount)']
    ).properties(
        title='Loan Amount by Sector'
    )
    st.altair_chart(chart, use_container_width=True)

elif visualization_option == "Repayment Interval Distribution":
    # Pie chart for repayment interval distribution
    pie_data = df_combined['repayment_interval'].value_counts().reset_index()
    pie_data.columns = ['repayment_interval', 'count']
    
    chart = alt.Chart(pie_data).mark_arc().encode(
        theta='count:Q',
        color='repayment_interval:N',
        tooltip=['repayment_interval', 'count']
    ).properties(
        title='Repayment Interval Distribution',
        width=300,
        height=300
    )
    st.altair_chart(chart, use_container_width=True)

elif visualization_option == "Funded Amount by Gender":
    # Boxplot for funded amount by gender
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_combined, x='borrower_genders', y='funded_amount', palette='Set2')
    plt.xlabel('Borrower Gender')
    plt.ylabel('Funded Amount')
    plt.title('Funded Amount by Gender')
    st.pyplot(plt)

    import streamlit as st

# Insights from Visualization Section Expander
with st.expander("Insights from Visualization 🧠"):
    st.markdown("""
    1. **Loan Distribution by Country** - The 'Loan Amount by Country' plot showcases which countries receive the most funding and may indicate regions with higher economic activities or needs.
    2. **Sector Funding Insights** - The 'Loan Amount by Sector' visualization reveals which sectors are receiving more loans, potentially indicating areas of economic focus or need.
    3. **Repayment Dynamics** - The 'Repayment Interval Distribution' chart provides insights into the preferred repayment structures, which could suggest financial stability or instability depending on the intervals' lengths.
    4. **Gender and Funding** - The 'Funded Amount by Gender' box plot may highlight disparities or equities in funding between different genders.
    """)

# Recommendations Expander
with st.expander("Recommendations for Action 🌟"):
    st.markdown("""
    - 🌍 **Targeted Funding Initiatives:** Increase funding to countries that are underrepresented in loan distributions to balance economic opportunities.
    - 🌱 **Sector-Specific Strategies:** Enhance support for sectors that are crucial for economic development but are receiving less funding.
    - ⏳ **Flexible Repayment Options:** Offer more flexible repayment plans to support borrowers in more volatile sectors or unstable economic conditions.
    - 👫 **Gender Equality in Funding:** Ensure equitable funding opportunities across genders and promote programs that support underfunded groups.
    """)


import altair as alt

# Loan by country and sector 
def plot_country_sector_stacked_chart():
    country_sector_count = df_combined.groupby(['country', 'sector']).size().reset_index(name='counts')
    chart = alt.Chart(country_sector_count).mark_bar().encode(
        x='country:N',
        y=alt.Y('counts:Q', stack='normalize'),
        color='sector:N',
        tooltip=['country', 'sector', 'counts']
    ).properties(
        title='Number of Loans by Country and Sector'
    )
    st.altair_chart(chart, use_container_width=True)

st.header("Number of Loans by Country and Sector")
plot_country_sector_stacked_chart()

# Insights from Visualization Section Expander
with st.expander("Insights from Visualization 🧠"):
    st.markdown("""
    1. **Geographic Loan Distribution** - The 'Number of Loans by Country and Sector' visualization showcases how loan distribution varies across countries and sectors, indicating regions with high funding needs and sector activity.
    2. **Sector Focus** - This chart highlights which sectors are more actively funded in specific countries, potentially pointing to targeted economic development initiatives.
    3. **Country-Specific Economic Support** - Observing the sectors that receive more loans in particular countries can give insights into the economic policies or market demands driving these trends.
    4. **Diversity of Funding** - The stacked nature of the chart shows the diversity of sector funding within each country, illustrating which sectors might be underserved or overemphasized.
    """)

# Recommendations Expander
with st.expander("Recommendations for Action 🌟"):
    st.markdown("""
    - 🌍 **Balanced Sector Funding:** Encourage balanced funding across sectors in each country to ensure no sector is left behind, especially those critical for sustainable development.
    - 🌱 **Support for Emerging Sectors:** Identify and support emerging sectors that have lower representation in loan distributions but are vital for future economic resilience.
    - 📊 **Data-Driven Policies:** Utilize data insights to shape economic policies that specifically target sectors and regions identified as needing more support or investment.
    - 🤝 **International Collaboration:** Foster partnerships between countries to support sectors that have high potential but low funding, sharing expertise and financial resources.
    """)

def plot_country_loan_boxplot():
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df_combined, x='country', y='loan_amount', palette='Set3')
    plt.xticks(rotation=90)
    plt.title('Distribution of Loan Amounts by Country')
    plt.xlabel('Country')
    plt.ylabel('Loan Amount')
    st.pyplot(plt)

st.header("Loan Amount Distribution by Country")
plot_country_loan_boxplot()

# Insights from Visualization Section Expander
with st.expander("Insights from Visualization 🧠"):
    st.markdown("""
    1. **Loan Amount Variability** - The 'Distribution of Loan Amounts by Country' boxplot illustrates the variability and range of loan amounts in each country, highlighting economic disparities or financial strategies.
    2. **Median Loan Amount** - Observing the median loan amount in each country can provide insights into the typical financial support provided, which may reflect the local economic conditions or the effectiveness of microfinance initiatives.
    3. **Outliers and Extremes** - The presence of outliers can indicate either exceptionally high or low loan amounts, which might suggest unique economic activities or specific needs of borrowers that are not typical.
    4. **Equitable Funding** - Comparison across countries can shed light on whether funding is equitably distributed based on needs and economic conditions.
    """)

# Recommendations Expander
with st.expander("Recommendations for Action 🌟"):
    st.markdown("""
    - 📈 **Adjust Funding Caps and Floors:** Consider adjusting the minimum and maximum loan amounts allowed in countries with high variability to ensure that loans are accessible and tailored to actual needs.
    - 🔍 **Investigate Outliers:** Further investigate the reasons behind outliers in loan amounts to better understand unique needs or possible adjustments in lending practices.
    - 💸 **Scale Funding Based on Median Needs:** Adjust loan amounts based on the median needs of each country to ensure that the support matches local economic realities.
    - 🌍 **Promote Equitable Distribution:** Strive for a more equitable distribution of loan amounts, focusing on countries that may be underfunded or overfunded relative to their economic status.
    """)

# Normalize 'borrower_genders' column
df_combined['borrower_genders'] = df_combined['borrower_genders'].str.lower().str.strip()

# This code handles multible genders per loan, if needed
# Split each loan by comma and counts unique gender
# Turns multible borrowers into seperate columns
gender_counts = df_combined['borrower_genders'].str.split(', ').explode().value_counts()

# Creation of pie chart 
fig, ax = plt.subplots()
ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Vizualisation
st.title("Loan Distribution by Gender")
st.pyplot(fig)

# Insights from Visualization Section Expander
with st.expander("Insights from Visualization 🧠"):
    st.markdown("""
    1. **Gender Participation** - The 'Loan Distribution by Gender' pie chart provides a clear view of the gender breakdown among loan recipients, highlighting the involvement level of each gender in loan programs.
    2. **Inclusivity** - This visualization can help assess the inclusivity of the lending program, indicating whether there is a balanced representation of genders among borrowers.
    3. **Targeted Outreach** - By understanding which gender is less represented in receiving loans, stakeholders can design outreach programs that specifically address these disparities.
    4. **Cultural and Economic Factors** - The distribution may also reflect broader societal factors, such as cultural norms or economic barriers that affect gender participation in financial activities.
    """)

# Recommendations Expander
with st.expander("Recommendations for Action 🌟"):
    st.markdown("""
    - 🌟 **Enhance Gender Equality Programs:** Implement or strengthen programs that promote gender equality in loan access, ensuring that all genders have equal opportunities to receive financial support.
    - 👥 **Customized Financial Products:** Develop financial products tailored to the underrepresented gender, considering their specific needs and circumstances.
    - 📊 **Data-Driven Decision Making:** Use these insights to inform policy decisions and advocacy efforts aimed at creating a more equitable lending environment.
    - 🌐 **Community Engagement:** Engage with communities to understand and overcome the social, cultural, or economic barriers that prevent equal gender participation in lending.
    """)


# Calculating top 10 countries by total funded amount
top_10_countries = df_combined.groupby('country')['funded_amount'].sum().nlargest(10).index

# Filtering data for only these top 10 countries
data_filtered = df_combined[df_combined['country'].isin(top_10_countries)]

# Visualization
st.title("Distribution of Funded Amounts in Top 10 Countries by Sector")

# Create the plot
plt.figure(figsize=(16, 10))
sns.histplot(data=data_filtered, x='funded_amount', hue='sector', palette='gist_rainbow', multiple='stack', kde=True)
plt.title('Distribution of Funded Amounts in Top 10 Countries, Color-Visualized by Sector')
plt.xlabel('Funded Amount')
plt.ylabel('Frequency')

# Display the plot in Streamlit
st.pyplot(plt)

# Insights from Visualization Section Expander
with st.expander("Insights from Visualization 🧠"):
    st.markdown("""
    1. **Sector Funding Variability** - This visualization showcases how different sectors within the top 10 countries vary in terms of funded amounts. This indicates not only the sectors that attract more funding but also those that might be underfunded.
    2. **Economic Priorities** - The distribution of funded amounts by sector can reveal the economic priorities of a region. Sectors with higher funding levels are likely seen as more vital to the country's economic development or stability.
    3. **Funding Gaps** - Observing where the funding peaks and troughs can highlight potential gaps in funding allocation, which could represent opportunities for more balanced economic support.
    4. **Impact of Sectoral Funding** - The presence of significant funding in certain sectors might drive economic trends and employment rates within those sectors, shaping the economic landscape of the country.
    """)

# Recommendations Expander
with st.expander("Recommendations for Action 🌟"):
    st.markdown("""
    - **Balanced Sector Development:** Encourage investment in underfunded sectors to ensure balanced economic growth across all areas. This might involve government incentives, private investment opportunities, or international aid focus.
    - **Targeted Economic Policies:** Develop and implement economic policies that target sectors identified as crucial but underfunded, ensuring they receive the necessary attention and resources.
    - **Data-Driven Funding Strategies:** Utilize data insights from the visualization to allocate resources more efficiently, ensuring that funding decisions are guided by actual sector needs and potential for impact.
    - **Enhance Transparency in Funding:** Promote greater transparency in how funds are allocated to different sectors to foster a more equitable distribution of resources and improve public trust.
    """)