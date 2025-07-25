import re

def clean_json_response(response_text: str) -> str:
    """
    Clean the LLM response to ensure valid JSON
    
    Args:
        response_text (str): Raw response from LLM
        
    Returns:
        str: Cleaned JSON string
    """
    # Remove any text before the first {
    start_idx = response_text.find('{')
    if start_idx != -1:
        response_text = response_text[start_idx:]
    
    # Remove any text after the last }
    end_idx = response_text.rfind('}')
    if end_idx != -1:
        response_text = response_text[:end_idx + 1]
    
    return response_text

def map_seniority_level(experience_level: str) -> int:
    """
    Map experience level to numeric seniority level
    
    Args:
        experience_level (str): Experience level string
        
    Returns:
        int: Numeric seniority level
    """
    experience_level = experience_level.lower()
    if 'entry' in experience_level or 'junior' in experience_level:
        return 1
    elif 'mid' in experience_level:
        return 2
    elif 'senior' in experience_level:
        return 3
    elif 'lead' in experience_level or 'principal' in experience_level:
        return 4
    else:
        return 2  # Default to mid-level