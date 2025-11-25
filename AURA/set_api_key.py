from utils.config_manager import update_config

# Set your API key properly
api_key = "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"
success = update_config('openai_api_key', api_key)

if success:
    print("✅ API key saved to config!")
else:
    print("❌ Failed to save API key")