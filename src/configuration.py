import argparse

from src.llm_interact import llm_provider_choices


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Anki cards generator server")
    llm_providers = llm_provider_choices()
    default_llm_provider = llm_providers[0]
    parser.add_argument(
        "--llm-provider",
        choices=llm_providers,
        default=default_llm_provider,
        help=f"LLM provider to use (default: {default_llm_provider})",
    )
    return parser.parse_args()
