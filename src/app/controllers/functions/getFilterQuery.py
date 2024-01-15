def getFilterQuery(url,websites,contract_types,companies,years,months,dates,regions,departments,cities):
    if websites:
        if len(websites)==1:
            url += f"(website='{websites[0]}')"
        else:
            url += '('
            url += ' or '.join([f"website='{website}'" for website in websites])
            url += ')'
        url += ' and '

    if contract_types:
        if len(contract_types)==1:
            url += f"(contract_type='{contract_types[0]}')"
        else:
            url += '('
            url += ' or '.join([f"contract_type='{contract_type}'" for contract_type in contract_types])
            url += ')'
        url += ' and '

    if companies:
        if len(companies)==1:
            url += f"(company='{companies[0]}')"
        else:
            url += '('
            url += ' or '.join([f"company='{company}'" for company in companies])
            url += ')'
        url += ' and '

    if years:
        if len(years)==1:
            url += f"(year='{years[0]}')"
        else:
            url += '('
            url += ' or '.join([f"year='{year}'" for year in years])
            url += ')'
        url += ' and '

    if months:
        if len(months)==1:
            url += f"(month='{months[0]}')"
        else:
            url += '('
            url += ' or '.join([f"month='{month}'" for month in months])
            url += ')'
        url += ' and '

    if dates:
        if len(dates)==1:
            url += f"(date='{dates[0]}')"
        else:
            url += '('
            url += ' or '.join([f"date='{date}'" for date in dates])
            url += ')'
        url += ' and '

    if regions:
        if len(regions)==1:
            url += f"(region='{regions[0]}')"
        else:
            url += '('
            url += ' or '.join([f"region='{region}'" for region in regions])
            url += ')'
        url += ' and '

    if departments:
        if len(departments)==1:
            url += f"(department='{departments[0]}')"
        else:
            url += '('
            url += ' or '.join([f"department='{department}'" for department in departments])
            url += ')'
        url += ' and '

    if cities:
        if len(cities)==1:
            url += f"(d_city.city='{cities[0]}')"
        else:
            url += '('
            url += ' or '.join([f"d_city.city='{city}'" for city in cities])
            url += ')'
        url += ' and '

    if "and" in url.strip()[-3:]:
        url = url.strip()[:-4]

    return url