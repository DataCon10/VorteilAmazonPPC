# scripts/peel.py
from typing import List, Dict

def peel_keywords(
    search_term_data: List[Dict],
    acos_threshold: float = 20.0,
    conversion_rate_threshold: float = 0.05
) -> List[str]:
    """
    Filters high-performing keywords from auto campaign search term data.

    Args:
        search_term_data (List[Dict]): A list of dictionaries representing search term performance.
            Each dictionary should have at least the keys:
                - 'keyword': the search term.
                - 'acos': the advertising cost of sales percentage.
                - 'conversion_rate': the conversion rate as a float (e.g., 0.05 for 5%).
        acos_threshold (float): Maximum acceptable ACOS (default is 20%).
        conversion_rate_threshold (float): Minimum conversion rate required (default is 5%).

    Returns:
        List[str]: A list of high-performing keywords.
    
    Example:
        >>> dummy_data = [
        ...     {"keyword": "crochet hooks", "acos": 18.5, "conversion_rate": 0.06},
        ...     {"keyword": "cheap crochet hooks", "acos": 30.0, "conversion_rate": 0.03},
        ...     {"keyword": "ergonomic crochet hooks", "acos": 15.0, "conversion_rate": 0.07}
        ... ]
        >>> peel_keywords(dummy_data)
        ['crochet hooks', 'ergonomic crochet hooks']
    """
    high_performers = []
    for term in search_term_data:
        try:
            keyword = term["keyword"]
            acos = float(term.get("acos", 100))
            conv_rate = float(term.get("conversion_rate", 0))
        except (KeyError, ValueError):
            continue

        if acos <= acos_threshold and conv_rate >= conversion_rate_threshold:
            high_performers.append(keyword)
    return high_performers
