from assistant.matcher import detect_language, load


def test_intents():
    m = load()
    assert m.reply("what is elliott wave?")["intent"] == "elliott_wave"
    assert m.reply("course ki fee kitni hai")["intent"] == "fees"
    assert m.reply("do you give certificates")["intent"] == "certificate"


def test_typo_tolerance():
    assert load().reply("waht courss do you ofer")["intent"] == "courses"


def test_fallback():
    assert load().reply("zzzz qqqq")["intent"] == "fallback"


def test_language():
    assert detect_language("fee kitni hai") == "roman-urdu"
    assert detect_language("hello") == "english"
    assert detect_language("کتنی فیس ہے") == "urdu"
