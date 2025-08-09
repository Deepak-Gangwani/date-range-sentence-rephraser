from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import calendar

# DATE RANGE GENERATOR ----------------------------------------------------
def generate_date_list(range_key):
    """
    returns list of ISO date strings depending on the range_key
    supported values: till_yesterday, till_tomorrow, next_month, last_7_days, this_week
    """
    today = date.today()

    if range_key == 'till_yesterday':
        start = date(1970,1,1)  # optionally you can set your own default start
        end = today - timedelta(days=1)

    elif range_key == 'till_tomorrow':
        start = date(1970,1,1)
        end = today + timedelta(days=1)

    elif range_key == 'next_month':
        # list of every date in next month
        first_of_next = (today.replace(day=1) + relativedelta(months=1))
        year = first_of_next.year
        month = first_of_next.month
        _, days = calendar.monthrange(year, month)
        start = date(year, month, 1)
        end = date(year, month, days)

    elif range_key == 'last_7_days':
        end = today
        start = today - timedelta(days=6)  # include today => 7 days total

    elif range_key == 'this_week':
        # ISO week: Monday is weekday()==0
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)

    else:
        raise ValueError('Unsupported range key')

    # If we used sentinel start earlier, restrict output size; for 'till' examples returning large ranges might be undesired.
    # We'll produce list from start to end inclusive.
    delta_days = (end - start).days
    if delta_days < 0:
        return []

    # limit returned list size to 10k for safety
    max_days = min(delta_days, 10000)
    date_list = [(start + timedelta(days=i)).isoformat() for i in range(max_days + 1)]
    return date_list


# REPHRASER HELPERS ------------------------------------------------------
# We'll try to use language_tool_python for grammar corrections if available.
# For paraphrasing variants we'll use simple synonym substitution via NLTK WordNet as a fallback.

try:
    import language_tool_python
    TOOL_AVAILABLE = True
    tool = language_tool_python.LanguageTool('en-US')
except Exception:
    TOOL_AVAILABLE = False
    tool = None

# NLTK WordNet setup
try:
    from nltk.corpus import wordnet as wn
    from nltk import word_tokenize, pos_tag
    NLTK_AVAILABLE = True
except Exception:
    NLTK_AVAILABLE = False

def grammar_correct(text):
    if TOOL_AVAILABLE and tool:
        matches = tool.check(text)
        corrected = language_tool_python.utils.correct(text, matches)
        return corrected
    else:
        # fallback - return original, or very simple capitalization fix
        return text

def simple_paraphrases(text, max_variants=5):
    """
    Produce up to max_variants paraphrases:
     - first variant: grammar-corrected (if available)
     - other variants: attempt synonym replacement of some nouns/adjectives/verbs
    This is a heuristic fallback (not a true paraphraser).
    """
    variants = []
    corrected = grammar_correct(text)
    variants.append(corrected)

    if not NLTK_AVAILABLE:
        # Can't do synonyms; duplicate corrected with minor tweaks
        while len(variants) < max_variants:
            variants.append(corrected)
        return variants[:max_variants]

    # We'll perform simple synonym swaps for some words
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)

    def pos_to_wordnet(tag):
        if tag.startswith('J'):
            return wn.ADJ
        if tag.startswith('V'):
            return wn.VERB
        if tag.startswith('N'):
            return wn.NOUN
        if tag.startswith('R'):
            return wn.ADV
        return None

    import random
    # Build list of candidate indices to swap (prefer nouns/verbs/adjectives)
    candidates = []
    for i, (tok, tag) in enumerate(tags):
        wn_pos = pos_to_wordnet(tag)
        if wn_pos:
            candidates.append((i, tok, wn_pos))

    # Try several attempts to create distinct variants
    attempts = 0
    seen = set([corrected])
    while len(variants) < max_variants and attempts < 20:
        attempts += 1
        new_tokens = tokens.copy()
        # randomly pick up to 2 candidates to swap
        picks = random.sample(candidates, min(2, len(candidates))) if candidates else []
        changed = False
        for (i, orig_tok, wn_pos) in picks:
            synsets = wn.synsets(orig_tok, pos=wn_pos)
            if not synsets:
                continue
            # pick a random lemma different from original
            lemmas = [l.name().replace('_',' ') for s in synsets for l in s.lemmas() if l.name().lower() != orig_tok.lower()]
            if not lemmas:
                continue
            new_tok = random.choice(lemmas)
            new_tokens[i] = new_tok
            changed = True

        if not changed:
            continue

        candidate = ' '.join(new_tokens)
        # simple cleanup spacing around punctuation
        candidate = candidate.replace(" ,", ",").replace(" .", ".").replace(" '", "'")
        if candidate not in seen:
            seen.add(candidate)
            variants.append(candidate)

    # If still fewer than required, pad with corrected text
    while len(variants) < max_variants:
        variants.append(corrected)

    return variants[:max_variants]
