from django.conf import settings

any_lang = ('any', 'Any')

def languages():
    languages = tuple(settings.CONTENT_LANGUAGES)

    if any_lang not in languages:
        languages = languages + (any_lang, )

    return languages

def fallback_languages(language):
    """ given a language, provide a list of alternatives, prioritized """
    langs = [language]
    if language != any_lang[0]:
        langs.append(any_lang[0])
    return langs

def language_slug(slugs, slug, language):
    """
        slugs is a mapping of lang->slug,
        slug is a default slug,
        language is the language you want the slug for
    """
    lslug = slugs.get(language, slug)
    if lslug is None and language == any_lang[0]:
        ## Use fallback? XXX
        return slugs.values()[0]  # any

    ## may still be None, let caller fail, for now
    return lslug

