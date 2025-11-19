#!/usr/bin/env python3
"""
List Available Gemini Models

This script lists all available Gemini models and their pricing information.
"""

import google.generativeai as genai

# Configuration
API_KEY = "AIzaSyC68Y9pohX1X88ejs2jt_K0522tFSRUXms"  # Your Google Gemini API key

def list_available_models():
    """
    List all available Gemini models and their details.
    """
    try:
        # Configure the Gemini client
        genai.configure(api_key=API_KEY)
        print("✓ Connected to Google Gemini API")

        # Get all available models
        models = genai.list_models()

        print("\n🤖 Available Gemini Models:")
        print("=" * 60)

        free_models = []
        paid_models = []

        for model in models:
            model_name = model.name.replace('models/', '')
            methods = model.supported_generation_methods

            # Check if model supports generateContent (text generation)
            if 'generateContent' in methods:
                # Try to determine pricing (this is approximate based on model names)
                is_free = any(keyword in model_name.lower() for keyword in ['flash', '1.0'])

                model_info = {
                    'name': model_name,
                    'methods': methods,
                    'description': getattr(model, 'description', 'No description available')
                }

                if is_free:
                    free_models.append(model_info)
                else:
                    paid_models.append(model_info)

        # Display free models first
        if free_models:
            print("\n🆓 FREE MODELS:")
            print("-" * 30)
            for model in free_models:
                print(f"📌 {model['name']}")
                print(f"   Methods: {', '.join(model['methods'])}")
                print(f"   Description: {model['description']}")
                print()

        # Display paid models
        if paid_models:
            print("\n💰 PAID MODELS:")
            print("-" * 30)
            for model in paid_models:
                print(f"📌 {model['name']}")
                print(f"   Methods: {', '.join(model['methods'])}")
                print(f"   Description: {model['description']}")
                print()

        print(f"\n📊 Summary:")
        print(f"   Free models: {len(free_models)}")
        print(f"   Paid models: {len(paid_models)}")
        print(f"   Total models: {len(free_models) + len(paid_models)}")

        if free_models:
            print(f"\n✅ Recommended free models: {', '.join([m['name'] for m in free_models])}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Gemini Models Lister")
    print("=" * 40)
    list_available_models()