import re
from datetime import date
from dateutil.parser import parse


class ChatData:

    def __init__(self):
        self.country = None
        self.product_category = None
        self.start_date = None
        self.end_date = None
        self.tab = None


def ask_question(user_input: str) -> ChatData:

    print("DEBUG: Received user_input =", user_input)

    data = ChatData()

    found_dates = []

    year_range_pattern = r"(\d{4})\s*[-–—]\s*(\d{4})"
    year_range_matches = re.findall(year_range_pattern, user_input)
    if year_range_matches:
        for yr1, yr2 in year_range_matches:
            print(f"DEBUG: Found year range {yr1}-{yr2}")
            # Convert to an actual start/end date
            start_yr = int(yr1)
            end_yr = int(yr2)
            start_dt = date(start_yr, 1, 1)
            end_dt = date(end_yr, 12, 31)
            found_dates.append((start_dt, end_dt))

    date_pattern = r"\b(\d{4}[-/]\d{2}[-/]\d{2})\b"
    full_date_strings = re.findall(date_pattern, user_input)
    if full_date_strings:
        for ds in full_date_strings:
            try:
                parsed = parse(ds, yearfirst=True).date()
                print(f"DEBUG: Found exact date {ds} => {parsed}")
                found_dates.append(parsed)
            except ValueError:
                print(f"DEBUG: Could not parse exact date {ds}")

    single_year_pattern = r"\b(?<![-/])(\d{4})(?![-/])\b"
    single_year_matches = re.findall(single_year_pattern, user_input)
    if single_year_matches:
        for yr in single_year_matches:
            print(f"DEBUG: Found single year {yr}")
            y = int(yr)
            start_of_year = date(y, 1, 1)
            end_of_year = date(y, 12, 31)
            found_dates.append((start_of_year, end_of_year))

    all_pairs = []
    for item in found_dates:
        if isinstance(item, tuple):
            # We already have (start, end)
            all_pairs.append(item)
        else:
            # It's a single date
            all_pairs.append((item, None))

    if not all_pairs:
        print("DEBUG: No date specified. Resetting dates to full range.")
        data.start_date = date(2020, 1, 1)
        data.end_date = date(2023, 12, 31)
    else:
        expanded_dates = []
        for s, e in all_pairs:
            if s and e:
                expanded_dates.extend([s, e])
            elif s:
                expanded_dates.append(s)

        if len(expanded_dates) >= 2:
            data.start_date = expanded_dates[0]
            data.end_date = expanded_dates[1]
        else:
            data.start_date = expanded_dates[0]

    possible_countries = [
        "United States",
        "France",
        "Germany",
        "El Salvador",
        "Guatemala",
        "Nicaragua",
        "Belgium",
        "South Africa",
        "India",
        "Hong Kong",
        "Democratic Republic of the Congo",
        "Spain",
        "Russia",
        "China",
        "Niger",
        "Qatar",
        "New Zealand",
        "Mexico",
        "Malaysia",
        "Poland",
        "Madagascar",
        "Iraq",
        "Cuba",
        "Colombia",
        "Saudi Arabia",
        "Egypt",
        "Brazil",
        "Iran",
        "Ukraine",
        "Japan",
        "Morocco",
        "United Kingdom",
        "Cameroon",
        "Chile",
        "Ghana",
        "Trinidad and Tobago",
        "Canada",
        "Chad",
        "Bulgaria",
        "Bangladesh",
        "Djibouti",
        "Uruguay",
        "Singapore",
        "Italy",
        "Czech Republic",
        "Zambia",
        "Bolivia",
        "Angola",
        "Australia",
        "Tanzania",
        "Norway",
        "Sierra Leone",
        "Hungary",
        "Austria",
        "Uzbekistan",
        "Romania",
        "Kyrgyzstan",
        "Belarus",
        "Mongolia",
        "Georgia",
        "Syria",
        "Croatia",
        "Israel",
        "Guinea-Bissau",
        "Somalia",
        "Tunisia",
        "Mali",
        "Algeria",
        "Kenya",
        "Mozambique",
        "Senegal",
        "Guadeloupe",
        "Finland",
        "Taiwan",
        "Jamaica",
        "Switzerland",
        "Azerbaijan",
        "Lesotho",
        "Afghanistan",
        "Cote d'Ivoire",
        "Bahrain",
        "Benin",
        "Moldova",
        "Jordan",
        "Rwanda",
        "Libya",
        "Togo",
        "Nepal",
        "Estonia",
        "Albania",
        "Slovakia",
        "Sudan",
        "Guinea",
        "Republic of the Congo",
        "Liberia",
        "Eritrea",
        "Lebanon",
        "Bosnia and Herzegovina",
        "Barbados",
        "Martinique",
        "Namibia",
        "Cambodia",
        "Ecuador",
        "Central African Republic",
        "Paraguay",
        "Mauritania",
        "Armenia",
        "Gabon",
        "Sri Lanka",
        "Macedonia",
        "Ethiopia",
        "Turkey",
        "Nigeria",
        "Kazakhstan",
        "Lithuania",
        "Ireland",
        "Netherlands",
        "Pakistan",
        "South Korea",
        "Philippines",
        "Vietnam",
        "Indonesia",
        "Venezuela",
        "Panama",
        "Dominican Republic",
        "Zimbabwe",
        "Myanmar (Burma)",
        "Thailand",
        "Honduras",
        "United Arab Emirates",
        "Tajikistan",
    ]
    data.country = []

    user_specified_countries = any(
        c.lower() in user_input.lower() for c in possible_countries
    )

    if not user_specified_countries:
        data.country = None
        print("DEBUG: No country specified. Resetting country filter.")
    else:
        # Otherwise, parse countries as usual
        for c in possible_countries:
            if c.lower() in user_input.lower():
                data.country.append(c)
                print(f"DEBUG: Matched country => {c}")
    possible_categories = ["Furniture", "Technology", "Office Supplies"]
    data.product_category = []

    for cat in possible_categories:
        if cat.lower() in user_input.lower():
            data.product_category.append(cat)
            print(f"DEBUG: Matched category => {cat}")

    if not data.product_category:
        data.product_category = None

    recognized_tabs = {
        "sales overview": "Sales Overview",
        "product performance": "Product Performance",
        "customer insights": "Customer Insights",
        "sales forecasting": "Sales Forecasting",
        "regional analysis": "Regional Analysis",
        "order analysis": "Order Analysis",
    }
    data.tab = None
    for keyword, tab_name in recognized_tabs.items():
        if keyword in user_input.lower():
            data.tab = tab_name
            print(f"DEBUG: Matched tab => {tab_name}")
            break

    print(
        "DEBUG: Final parsed ChatData =>",
        {
            "country": data.country,
            "product_category": data.product_category,
            "start_date": data.start_date,
            "end_date": data.end_date,
            "tab": data.tab,
        },
    )
    print("DEBUG: Done parsing.\n")

    return data
