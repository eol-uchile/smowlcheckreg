def plugin_settings(settings):
    settings.SMOWLCHECKREG_URL = settings.ENV_TOKENS.get('SMOWLCHECKREG_URL', '')
    settings.SMOWL_KEY = settings.ENV_TOKENS.get('SMOWL_KEY', '')
    settings.SMOWL_ENTITY = settings.ENV_TOKENS.get('SMOWL_ENTITY', '')