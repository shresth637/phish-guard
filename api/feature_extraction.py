import urllib.parse
import re

def extract_features(url: str, required_features: list):
    """
    Extracts 15 structural and ratio-based features from the URL string.
    """
    if not url.startswith('http'):
        url = 'http://' + url
    
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.split(':')[0]
    
    # Base counts
    url_len = len(url)
    num_letters = sum(c.isalpha() for c in url)
    num_digits = sum(c.isdigit() for c in url)
    num_special = len(re.findall(r'[^a-zA-Z0-9]', url))
    
    # Subdomain and TLD calculations
    domain_parts = domain.split('.')
    tld_length = len(domain_parts[-1]) if len(domain_parts) > 1 else 0
    subdomains = max(0, len(domain_parts) - 2)

    extracted = {
        'URLLength': url_len,
        'DomainLength': len(domain),
        'IsDomainIP': 1 if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain) else 0,
        'TLDLength': tld_length,
        'NoOfSubDomain': subdomains,
        'NoOfLettersInURL': num_letters,
        'LetterRatioInURL': num_letters / url_len if url_len > 0 else 0,
        'NoOfDegitsInURL': num_digits,  # Deliberate dataset typo
        'DegitRatioInURL': num_digits / url_len if url_len > 0 else 0,
        'NoOfEqualsInURL': url.count('='),
        'NoOfQMarkInURL': url.count('?'),
        'NoOfAmpersandInURL': url.count('&'),
        'NoOfOtherSpecialCharsInURL': num_special,
        'SpacialCharRatioInURL': num_special / url_len if url_len > 0 else 0, # Deliberate dataset typo
        'IsHTTPS': 1 if parsed.scheme == 'https' else 0,
    }
    
    # Map features in the exact order expected by the AI model
    final_features = [extracted.get(feat, 0.0) for feat in required_features]
    return [final_features]