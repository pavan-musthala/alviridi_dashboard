import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your dataset
df = pd.read_csv('dummy_sample.csv')

# Set up the sidebar with a custom title and description
st.sidebar.title("ALVIRIDI DASHBOARD")

# Create a dropdown with the unique company names
company_selected = st.sidebar.selectbox("☆ Select Company", ['All Companies'] + df['Company Name'].unique().tolist())

# Create a dropdown with the unique countries
country_selected = st.sidebar.selectbox("☆ Select Country", ['All Countries'] + df['Country'].unique().tolist())

# Create a dropdown with the unique funds
fund_selected = st.sidebar.selectbox("☆ Select Fund", ['All Funds'] + df['Fund'].unique().tolist())

# Filter data based on selections
filtered_data = df.copy()

if company_selected != 'All Companies':
    filtered_data = filtered_data[filtered_data['Company Name'] == company_selected]

if country_selected != 'All Countries':
    filtered_data = filtered_data[filtered_data['Country'] == country_selected]

if fund_selected != 'All Funds':
    filtered_data = filtered_data[filtered_data['Fund'] == fund_selected]

# Displaying the selected options in the main section
st.write(f"### Analyzing: **{company_selected}** in **{country_selected}** for **{fund_selected}**")

# Calculate key financial metrics for Investment Analysis
total_fund_size = filtered_data['Fund Size ($M)'].sum()
total_investment = filtered_data['Investment ($M)'].sum()
total_capital_committed = filtered_data['Total Capital Committed ($B)'].sum()
total_fund_investments = filtered_data['Fund Investments'].sum()
total_country_capital = filtered_data['Country Capital Catalyzed ($M)'].sum()
total_theme_capital = filtered_data['Theme Capital Catalyzed ($M)'].sum()

# Apply custom CSS for smaller metrics size and change font
st.markdown(
    """
    <style>
    .small-metric .stMetric {
        font-size: 10px !important;  /* Reduce the font size */
        padding: 8px !important;      /* Adjust padding */
        font-family: 'Arial', sans-serif; /* Change font */
    }
    </style>
    """, unsafe_allow_html=True
)

# Create columns to align metrics horizontally at the top
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Display financial metrics at the top with reduced size
with col1:
    st.markdown('<div class="small-metric">', unsafe_allow_html=True)
    st.metric(label="Fund Size", value=f"${total_fund_size:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="small-metric">', unsafe_allow_html=True)
    st.metric(label="Investment", value=f"${total_investment:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="small-metric">', unsafe_allow_html=True)
    st.metric(label="Total Capital Committed ($B)", value=f"${total_capital_committed:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="small-metric">', unsafe_allow_html=True)
    st.metric(label="Fund Investments", value=f"{total_fund_investments:,}")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="small-metric">', unsafe_allow_html=True)
    st.metric(label="Country Capital Catalyzed", value=f"${total_country_capital:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="small-metric">', unsafe_allow_html=True)
    st.metric(label="Theme Capital Catalyzed", value=f"${total_theme_capital:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

# Create tabs for different analyses
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Investment Analysis", "Geographic Impact Analysis", "Thematic Analysis", "Environmental Impact Analysis", "Global South Investment Focus", "Fund Performance Comparison"])

# Investment Analysis Tab
with tab1:
 st.title('Investment Analysis')

# 1. Which funds have the largest size vs. actual investment?
# Create a DataFrame with Fund size and Investment
fund_comparison = filtered_data[['Fund', 'Fund Size ($M)', 'Investment ($M)']].copy()
fund_comparison['Size vs Investment'] = fund_comparison['Fund Size ($M)'] - fund_comparison['Investment ($M)']

# Plotting Fund Size vs Investment
plt.figure(figsize=(12, 6),dpi=60)
sns.barplot(x='Fund', y='Size vs Investment', data=fund_comparison, palette='viridis')
plt.title('Fund Size vs Actual Investment')
plt.ylabel('Difference (Fund Size - Investment) ($M)')
plt.xlabel('Fund')
plt.xticks(rotation=0)
plt.tight_layout()
st.pyplot(plt)

# 2. Percentage of total capital committed that has been invested
filtered_data['Percentage Invested'] = (filtered_data['Investment ($M)'] / (filtered_data['Total Capital Committed ($B)'] * 1000)) * 100  # Convert B to M

# Plotting percentage invested
plt.figure(figsize=(12, 6),dpi=60)
sns.barplot(x='Fund', y='Percentage Invested', data=filtered_data, palette='rocket')
plt.title('Percentage of Total Capital Committed that has been Invested')
plt.ylabel('Percentage (%)')
plt.xlabel('Fund')
plt.xticks(rotation=0)
plt.tight_layout()
st.pyplot(plt)

# 3. Capital catalyzed in different countries
country_capital = filtered_data.groupby('Country')['Country Capital Catalyzed ($M)'].sum().reset_index()

# Plotting country capital catalyzed
plt.figure(figsize=(12, 6),dpi=60)
sns.barplot(x='Country Capital Catalyzed ($M)', y='Country', data=country_capital, palette='magma')
plt.title('Capital Catalyzed by Country')
plt.xlabel('Capital Catalyzed ($M)')
plt.ylabel('Country')
plt.tight_layout()
st.pyplot(plt)

# 4. Theme Capital Catalyzed Analysis
theme_capital = filtered_data.groupby('Theme')['Theme Capital Catalyzed ($M)'].sum().reset_index()

# Plotting theme capital catalyzed
plt.figure(figsize=(12, 6),dpi=60)
sns.barplot(x='Theme Capital Catalyzed ($M)', y='Theme', data=theme_capital, palette='cubehelix')
plt.title('Capital Catalyzed by Theme')
plt.xlabel('Capital Catalyzed ($M)')
plt.ylabel('Theme')
plt.tight_layout()
st.pyplot(plt)

# 5. Compare Investment ($M) with Fund Size ($M)
plt.figure(figsize=(12, 6),dpi=60)
sns.scatterplot(x='Fund Size ($M)', y='Investment ($M)', data=fund_comparison, hue='Fund', palette='deep', s=100)
plt.title('Investment vs Fund Size')
plt.xlabel('Fund Size ($M)')
plt.ylabel('Investment ($M)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(plt)

# 6. Analyze Total Capital Committed ($B) with Fund Investments
plt.figure(figsize=(12, 6),dpi=60)
sns.scatterplot(x='Total Capital Committed ($B)', y='Fund Investments', data=filtered_data, hue='Fund', palette='Paired', s=100)
plt.title('Total Capital Committed vs Fund Investments')
plt.xlabel('Total Capital Committed ($B)')
plt.ylabel('Fund Investments')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(plt)

# Geographic Impact Analysis
with tab2:
    st.write("### Geographic Impact Analysis")

    # 1. Which countries receive the most investment?
    country_investments = filtered_data.groupby('Country')['Investment ($M)'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Investment ($M)', y='Country', data=country_investments.sort_values('Investment ($M)', ascending=False), palette='viridis')
    plt.title('Total Investments by Country')
    plt.xlabel('Total Investment ($M)')
    plt.ylabel('Country')
    st.pyplot(plt)

    # 2. Number of deals made in the Global South vs. other regions
    global_south_deals = filtered_data.groupby('Global South Countries Supported')['Global South Deals Funded'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Global South Deals Funded', y='Global South Countries Supported', data=global_south_deals.sort_values('Global South Deals Funded', ascending=False), palette='magma')
    plt.title('Global South Deals Funded by Country')
    plt.xlabel('Number of Deals Funded')
    plt.ylabel('Global South Countries Supported')
    st.pyplot(plt)

    # 3. Distribution of capital across supported countries
    country_capital = filtered_data.groupby('Country')['Country Capital Catalyzed ($M)'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Country Capital Catalyzed ($M)', y='Country', data=country_capital.sort_values('Country Capital Catalyzed ($M)', ascending=False), palette='cubehelix')
    plt.title('Capital Catalyzed by Country')
    plt.xlabel('Capital Catalyzed ($M)')
    plt.ylabel('Country')
    st.pyplot(plt)

    # 4. Assess which Global South countries are receiving more deals
    global_south_deals_count = filtered_data.groupby('Country')['Global South Deals Funded'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Global South Deals Funded', y='Country', data=global_south_deals_count.sort_values('Global South Deals Funded', ascending=False), palette='crest')
    plt.title('Global South Deals Funded by Country')
    plt.xlabel('Number of Deals Funded')
    plt.ylabel('Country')
    st.pyplot(plt)

    # 5. Rank countries by the amount of capital catalyzed
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Country Capital Catalyzed ($M)', y='Country', data=country_capital.sort_values('Country Capital Catalyzed ($M)', ascending=False), palette='rocket')
    plt.title('Ranking Countries by Capital Catalyzed')
    plt.xlabel('Capital Catalyzed ($M)')
    plt.ylabel('Country')
    st.pyplot(plt)

    # 6. Analyze Global South Countries Supported with Theme
    theme_global_south = filtered_data.groupby(['Global South Countries Supported', 'Theme'])['Country Capital Catalyzed ($M)'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Country Capital Catalyzed ($M)', y='Global South Countries Supported', hue='Theme', data=theme_global_south, palette='Set2')
    plt.title('Capital Catalyzed by Theme in Global South Countries')
    plt.xlabel('Capital Catalyzed ($M)')
    plt.ylabel('Global South Countries Supported')
    plt.legend(title='Theme', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt)

# Thematic Analysis Tab
with tab3:
    st.title('Thematic Analysis')

    # 1. Which themes are attracting the most capital?
    theme_capital = filtered_data.groupby('Theme')['Theme Capital Catalyzed ($M)'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Theme Capital Catalyzed ($M)', y='Theme', data=theme_capital.sort_values('Theme Capital Catalyzed ($M)', ascending=False), palette='viridis')
    plt.title('Capital Attracted by Themes')
    plt.xlabel('Capital Attracted ($M)')
    plt.ylabel('Theme')
    plt.tight_layout()
    st.pyplot(plt)

    # 2. How do the themes vary across different countries?
    theme_country = filtered_data.groupby(['Country', 'Theme'])['Theme Capital Catalyzed ($M)'].sum().reset_index()

    plt.figure(figsize=(14, 8))
    sns.barplot(x='Theme Capital Catalyzed ($M)', y='Country', hue='Theme', data=theme_country, palette='Set2')
    plt.title('Thematic Capital Distribution Across Countries')
    plt.xlabel('Capital Attracted ($M)')
    plt.ylabel('Country')
    plt.legend(title='Theme', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # 3. Are certain themes more prevalent in the Global South?
    global_south_theme = filtered_data[filtered_data['Global South Countries Supported'].notna()]
    global_south_theme_capital = global_south_theme.groupby('Theme')['Theme Capital Catalyzed ($M)'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Theme Capital Catalyzed ($M)', y='Theme', data=global_south_theme_capital.sort_values('Theme Capital Catalyzed ($M)', ascending=False), palette='magma')
    plt.title('Capital Attracted by Themes in the Global South')
    plt.xlabel('Capital Attracted ($M)')
    plt.ylabel('Theme')
    plt.tight_layout()
    st.pyplot(plt)

    # 4. Compare Theme Capital Catalyzed ($M) with Fund
    theme_fund = filtered_data.groupby(['Fund', 'Theme'])['Theme Capital Catalyzed ($M)'].sum().reset_index()

    plt.figure(figsize=(14, 8))
    sns.barplot(x='Theme Capital Catalyzed ($M)', y='Fund', hue='Theme', data=theme_fund, palette='cubehelix')
    plt.title('Capital by Theme and Fund')
    plt.xlabel('Capital Attracted ($M)')
    plt.ylabel('Fund')
    plt.legend(title='Theme', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)


    # 5. Compare thematic investment in different regions
    theme_region = filtered_data.groupby(['Country', 'Theme'])['Theme Capital Catalyzed ($M)'].sum().reset_index()

    plt.figure(figsize=(14, 8))
    sns.barplot(x='Theme Capital Catalyzed ($M)', y='Country', hue='Theme', data=theme_region, palette='rocket')
    plt.title('Thematic Investment Distribution by Region')
    plt.xlabel('Capital Attracted ($M)')
    plt.ylabel('Country')
    plt.legend(title='Theme', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # Environmental Impact Analysis Tab
with tab4:
    st.title('Environmental Impact Analysis')

    # 1. Which funds or investments have the highest total emissions?
    total_emissions_fund = filtered_data.groupby('Fund')['Total Emissions by Fund (tons of CO2e)'].sum().reset_index()

    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Total Emissions by Fund (tons of CO2e)', y='Fund', data=total_emissions_fund.sort_values('Total Emissions by Fund (tons of CO2e)', ascending=False), palette='Blues')
    plt.title('Total Emissions by Fund')
    plt.xlabel('Total Emissions (tons of CO2e)')
    plt.ylabel('Fund')
    plt.tight_layout()
    st.pyplot(plt)

    # Pie chart for Total Emissions by Fund
    plt.figure(figsize=(12, 6),dpi=60)
    plt.pie(total_emissions_fund['Total Emissions by Fund (tons of CO2e)'], labels=total_emissions_fund['Fund'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Blues', len(total_emissions_fund)))
    plt.title('Proportion of Total Emissions by Fund')
    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
    plt.tight_layout()
    st.pyplot(plt)

    # 2. How do Scope 1, 2, and 3 emissions vary by fund?
    scope_emissions = filtered_data.melt(id_vars='Fund', 
                           value_vars=['Scope 1 Emissions (tons of CO2e)', 'Scope 2 Emissions (tons of CO2e)', 'Scope 3 Emissions (tons of CO2e)'],
                           var_name='Scope', 
                           value_name='Emissions')

    # Plotting emissions by scope and fund
    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Emissions', y='Fund', hue='Scope', data=scope_emissions, palette='pastel')
    plt.title('Scope 1, 2, and 3 Emissions by Fund')
    plt.xlabel('Emissions (tons of CO2e)')
    plt.ylabel('Fund')
    plt.legend(title='Emission Scope')
    plt.tight_layout()
    st.pyplot(plt)

    # Pie chart for Scope Emissions
    scope_summary = scope_emissions.groupby('Scope')['Emissions'].sum().reset_index()
    plt.figure(figsize=(12, 6),dpi=60)
    plt.pie(scope_summary['Emissions'], labels=scope_summary['Scope'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel', len(scope_summary)))
    plt.title('Proportion of Emissions by Scope')
    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
    plt.tight_layout()
    st.pyplot(plt)

    # 3. What are the emissions trends across different themes?
    theme_emissions = filtered_data.groupby('Theme')['Total Emissions by Fund (tons of CO2e)'].sum().reset_index()

    # Plotting total emissions by theme
    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Total Emissions by Fund (tons of CO2e)', y='Theme', data=theme_emissions.sort_values('Total Emissions by Fund (tons of CO2e)', ascending=False), palette='Reds')
    plt.title('Total Emissions by Theme')
    plt.xlabel('Total Emissions (tons of CO2e)')
    plt.ylabel('Theme')
    plt.tight_layout()
    st.pyplot(plt)

    # Pie chart for Total Emissions by Theme
    plt.figure(figsize=(12, 6),dpi=60)
    plt.pie(theme_emissions['Total Emissions by Fund (tons of CO2e)'], labels=theme_emissions['Theme'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Reds', len(theme_emissions)))
    plt.title('Proportion of Total Emissions by Theme')
    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
    plt.tight_layout()
    st.pyplot(plt)

    # 4. Combine Scope Emissions with Country
    country_scope_emissions = filtered_data.melt(id_vars='Country', 
                                   value_vars=['Scope 1 Emissions (tons of CO2e)', 'Scope 2 Emissions (tons of CO2e)', 'Scope 3 Emissions (tons of CO2e)'],
                                   var_name='Scope', 
                                   value_name='Emissions')

    # Plotting emissions by scope and country
    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Emissions', y='Country', hue='Scope', data=country_scope_emissions, palette='Set1')
    plt.title('Scope 1, 2, and 3 Emissions by Country')
    plt.xlabel('Emissions (tons of CO2e)')
    plt.ylabel('Country')
    plt.legend(title='Emission Scope')
    plt.tight_layout()
    st.pyplot(plt)

    # Pie chart for Country Scope Emissions
    country_scope_summary = country_scope_emissions.groupby('Country')['Emissions'].sum().reset_index()
    plt.figure(figsize=(12, 6),dpi=60)
    plt.pie(country_scope_summary['Emissions'], labels=country_scope_summary['Country'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('husl', len(country_scope_summary)))
    plt.title('Proportion of Emissions by Country')
    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
    plt.tight_layout()
    st.pyplot(plt)

    # 6. Compare Emissions by Fund with Theme
    fund_theme_emissions = filtered_data.groupby(['Fund', 'Theme'])['Total Emissions by Fund (tons of CO2e)'].sum().reset_index()

    # Plotting emissions by fund and theme
    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Total Emissions by Fund (tons of CO2e)', y='Fund', hue='Theme', data=fund_theme_emissions, palette='coolwarm')
    plt.title('Emissions by Fund and Theme')
    plt.xlabel('Total Emissions (tons of CO2e)')
    plt.ylabel('Fund')
    plt.legend(title='Theme', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # Global South Investment Focus Tab
with tab5:
    st.title('Global South Investment Focus')

    # 1. How much funding is flowing into Global South regions?
    total_investment = filtered_data['Investment ($M)'].sum()
    st.write(f'Total Investment in Global South: ${total_investment:.2f}M')

    # 2. What is the distribution of deals across these countries?
    deals_distribution = filtered_data.groupby('Country')['Global South Deals Funded'].sum().reset_index()

    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Global South Deals Funded', y='Country', data=deals_distribution.sort_values('Global South Deals Funded', ascending=False), palette='viridis')
    plt.title('Total Global South Deals Funded by Country')
    plt.xlabel('Number of Deals Funded')
    plt.ylabel('Country')
    plt.tight_layout()
    st.pyplot(plt)

    # 3. What are the emissions patterns associated with investments in the Global South?
    emissions_data = filtered_data[['Country', 'Total Emissions by Fund (tons of CO2e)', 'Investment ($M)']]

    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Total Emissions by Fund (tons of CO2e)', y='Country', data=emissions_data, palette='magma')
    plt.title('Total Emissions by Country in Global South')
    plt.xlabel('Total Emissions (tons of CO2e)')
    plt.ylabel('Country')
    plt.tight_layout()
    st.pyplot(plt)

    # 4. Compare Global South Deals Funded with Investment ($M)
    plt.figure(figsize=(12, 6),dpi=60)
    sns.scatterplot(x='Global South Deals Funded', y='Investment ($M)', data=filtered_data, hue='Country', palette='Set2')
    plt.title('Global South Deals Funded vs Investment ($M)')
    plt.xlabel('Global South Deals Funded')
    plt.ylabel('Investment ($M)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # 5. Combine Global South Countries Supported with Total Emissions by Fund
    emissions_by_country = filtered_data.groupby('Country')['Total Emissions by Fund (tons of CO2e)'].sum().reset_index()

    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Total Emissions by Fund (tons of CO2e)', y='Country', data=emissions_by_country.sort_values('Total Emissions by Fund (tons of CO2e)', ascending=False), palette='Blues')
    plt.title('Total Emissions by Country in the Global South')
    plt.xlabel('Total Emissions (tons of CO2e)')
    plt.ylabel('Country')
    plt.tight_layout()
    st.pyplot(plt)

    # Fund Performance Analysis Tab
with tab6:
    st.title('Fund Performance Analysis')

    # 1. How do different funds perform in terms of investment vs. size?
    fund_performance = filtered_data.groupby('Fund').agg({
        'Investment ($M)': 'sum',
        'Fund Size ($M)': 'sum',
        'Total Emissions by Fund (tons of CO2e)': 'sum'
    }).reset_index()

    # Calculate utilization ratio
    fund_performance['Utilization Ratio'] = fund_performance['Investment ($M)'] / fund_performance['Fund Size ($M)']

    # Plotting Investment vs Fund Size
    plt.figure(figsize=(12, 6),dpi=60)
    sns.scatterplot(x='Fund Size ($M)', y='Investment ($M)', hue='Fund', data=fund_performance, palette='Set1', s=100)
    plt.title('Investment vs Fund Size by Fund')
    plt.xlabel('Fund Size ($M)')
    plt.ylabel('Investment ($M)')
    plt.axline((0, 0), slope=1, color='red', linestyle='--')  # Add a line for 1:1 ratio
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # 2. Which funds are generating higher returns or catalyzing more capital?
    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Utilization Ratio', y='Fund', data=fund_performance.sort_values('Utilization Ratio', ascending=False), palette='Blues')
    plt.title('Fund Utilization Ratio')
    plt.xlabel('Utilization Ratio (Investment / Fund Size)')
    plt.ylabel('Fund')
    plt.tight_layout()
    st.pyplot(plt)

    # 3. Which funds have the lowest emissions relative to their investment size?
    fund_performance['Emissions per Investment'] = fund_performance['Total Emissions by Fund (tons of CO2e)'] / fund_performance['Investment ($M)']

    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Emissions per Investment', y='Fund', data=fund_performance.sort_values('Emissions per Investment'), palette='Reds')
    plt.title('Emissions per Investment by Fund')
    plt.xlabel('Emissions (tons of CO2e per $M Investment)')
    plt.ylabel('Fund')
    plt.tight_layout()
    st.pyplot(plt)

    # 4. Combine Fund with Total Emissions by Fund to compare environmental impacts across funds.
    plt.figure(figsize=(12, 6),dpi=60)
    sns.barplot(x='Total Emissions by Fund (tons of CO2e)', y='Fund', data=fund_performance.sort_values('Total Emissions by Fund (tons of CO2e)', ascending=False), palette='Greens')
    plt.title('Total Emissions by Fund')
    plt.xlabel('Total Emissions (tons of CO2e)')
    plt.ylabel('Fund')
    plt.tight_layout()
    st.pyplot(plt)


