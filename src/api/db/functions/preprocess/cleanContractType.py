def cleanContractType(contract_type):
    return_value = ""
    contract_type_lower = contract_type.lower()
    if '|' in contract_type_lower or '/' in contract_type_lower or 'ou' in contract_type_lower.split() or 'et' in contract_type_lower.split():
        return_value='Mixed contract'
    elif 'emploi permanent' in contract_type_lower or 'cdi' in contract_type_lower:
        return_value='Permanent contract' 
    elif 'emploi temporaire' in contract_type_lower or 'cdd' in contract_type_lower:
        return_value='Fixed-term contract' 
    elif 'stag' in contract_type_lower:
        return_value='Internship'
    elif 'altern' in contract_type_lower:
        return_value='Apprenticeship'
    elif 'interim' in contract_type_lower or 'intérim' in contract_type_lower:
        return_value='Temporary Work'        
    else:
        return_value="Unreferenced"

    return return_value
