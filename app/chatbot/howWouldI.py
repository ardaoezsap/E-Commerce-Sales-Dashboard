from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI



class DashboardQuery(BaseModel):
    country: Optional[str] = Field(
        default=None,
        description="Filter by country (e.g., Mexico, Canada, Germany)."
    )
    product_category: Optional[str] = Field(
        default=None,
        description="Filter by product category (e.g., Office Supplies, Technology, Furniture)."
    )
    start_date: Optional[str] = Field(
        default=None,
        description="Start date in YYYY-MM-DD format."
    )
    end_date: Optional[str] = Field(
        default=None,
        description="End date in YYYY-MM-DD format."
    )
    tab: Optional[str] = Field(
        default=None,
        description="Which tab to show, e.g., Sales Overview, Product Performance, etc."
    )


countries = [
    "United States", "France", "Germany", "El Salvador", "Guatemala", "Nicaragua",
    "Belgium", "South Africa", "India", "Hong Kong", "Democratic Republic of the Congo",
    "Spain", "Russia", "China", "Niger", "Qatar", "New Zealand", "Mexico", "Malaysia",
    "Poland", "Madagascar", "Iraq", "Cuba", "Colombia", "Saudi Arabia", "Egypt", "Brazil",
    "Iran", "Ukraine", "Japan", "Morocco", "United Kingdom", "Cameroon", "Chile", "Ghana",
    "Trinidad and Tobago", "Canada", "Chad", "Bulgaria", "Bangladesh", "Djibouti",
    "Uruguay", "Singapore", "Italy", "Czech Republic", "Zambia", "Bolivia", "Angola",
    "Australia", "Tanzania", "Norway", "Sierra Leone", "Hungary", "Austria", "Uzbekistan",
    "Romania", "Kyrgyzstan", "Belarus", "Mongolia", "Georgia", "Syria", "Croatia", "Israel",
    "Guinea-Bissau", "Somalia", "Tunisia", "Mali", "Algeria", "Kenya", "Mozambique",
    "Senegal", "Guadeloupe", "Finland", "Taiwan", "Jamaica", "Switzerland", "Azerbaijan",
    "Lesotho", "Afghanistan", "Cote d'Ivoire", "Bahrain", "Benin", "Moldova", "Jordan",
    "Rwanda", "Libya", "Togo", "Nepal", "Estonia", "Albania", "Slovakia", "Sudan",
    "Guinea", "Republic of the Congo", "Liberia", "Eritrea", "Lebanon",
    "Bosnia and Herzegovina", "Barbados", "Martinique", "Namibia", "Cambodia", "Ecuador",
    "Central African Republic", "Paraguay", "Mauritania", "Armenia", "Gabon",
    "Sri Lanka", "Macedonia", "Ethiopia", "Turkey", "Nigeria", "Kazakhstan", "Lithuania",
    "Ireland", "Netherlands", "Pakistan", "South Korea", "Philippines", "Vietnam",
    "Indonesia", "Venezuela", "Panama", "Dominican Republic", "Zimbabwe",
    "Myanmar (Burma)", "Thailand", "Honduras", "United Arab Emirates", "Tajikistan"
]

tabs = ["Sales Overview", "Product Performance", "Customer Insights", "Sales Forecasting", "Regional Analysis",
        "Order Analysis"]


def ask_question(question):
    llm = ChatOpenAI(model="gpt-4o",
                     api_key="here is you key")

    structured_llm = llm.with_structured_output(DashboardQuery)

    response = structured_llm.invoke(question)
    is_valid = False

    while not is_valid:
        if response.country not in countries:
            print(f"Error: Country: {response.country}")
            question += f" {response.country} is not a valid country. Please try again."
            response = structured_llm.invoke(question)
            print("-------------------")
            print(response._dict_)
            continue
        if response.product_category not in ["Office Supplies", "Technology", "Furniture"]:
            print(f"Error: Product Category: {response.product_category}")
            question += f" {response.product_category} is not a valid product category. Please try again. Select between Office Supplies, Technology, Furniture"
            response = structured_llm.invoke(question)
            print("-------------------")
            print(response._dict_)
            continue
        if response.start_date and response.end_date:
            pass
        if response.tab not in tabs:
            print("-------------------")
            print(f"Error: Tab: {response.tab}")
            question += f" {response.tab} is not a valid tab. Please try again. Select between {', '.join(tabs)}"
            response = structured_llm.invoke(question)
            continue
        is_valid = True

    response.start_date = datetime.strptime("2020-01-01", "%Y-%m-%d").date()
    response.end_date = datetime.strptime("2023-12-31", "%Y-%m-%d").date()

    return response
