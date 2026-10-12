from translations import detect_language,T
def test_tamil_detection(): assert detect_language('விவசாய திட்டங்கள்')=='ta'
def test_english_detection(): assert detect_language('crop insurance')=='en'
def test_translation_keys_match(): assert set(T['en'])==set(T['ta'])
