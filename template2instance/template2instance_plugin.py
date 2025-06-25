def validate_language_codes(lang_code: str) -> bool:
    """
    This function checks if the given language code is valid.

    Parameters
    ----------
    lang_code : str
        The language code to check

    Returns
    -------
    bool
        True if the language code is valid, False otherwise
    """
    valid_codes = [ 'ar', 'bg', 'bn', 'ca', 'cak', 'cs', 'cy', 'da', 'de', 
                   'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'he',
                   'hi', 'hi_IN', 'hr', 'hu', 'id', 'it', 'ja', 'ko', 'lt',
                   'lv', 'mk', 'nb_NO', 'ne', 'nl', 'pl', 'pt', 'pt_BR', 
                   'pt_PT', 'ro', 'ru', 'si', 'sk', 'sl', 'sq', 'sr', 
                   'sr@latin', 'sr_RS', 'sv', 'ta', 'te', 'tr', 'uk_UA', 'ur', 
                   'vi', 'zh_CN', 'zh_TW' ]
    return lang_code in valid_codes