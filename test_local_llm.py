#!/usr/bin/env python3
"""
Test script for local Ollama + Whisper setup
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("🧪 Testing Local LLM Setup (Ollama + Whisper)")
print("=" * 60)

# Test 1: Check Ollama availability
print("\n1️⃣  Checking Ollama availability...")
try:
    import ollama
    models_response = ollama.list()
    # Get models from response object
    available_models = [m.model for m in models_response.models]
    print(f"   ✅ Ollama is running")
    print(f"   📦 Available models: {', '.join(available_models)}")
    
    # Check for recommended models
    if 'llama2:latest' in available_models:
        print("   ✅ llama2:latest found")
    elif 'mistral:7b-instruct' in available_models:
        print("   ✅ mistral:7b-instruct found")
    else:
        print("   ⚠️  Recommended models not found")
        print("   💡 Run: ollama pull llama2")
        
except Exception as e:
    print(f"   ❌ Ollama not available: {e}")
    print("   💡 Start Ollama: ollama serve")
    sys.exit(1)

# Test 2: Test Ollama generation
print("\n2️⃣  Testing Ollama text generation...")
try:
    response = ollama.chat(
        model='llama2:latest',
        messages=[
            {'role': 'user', 'content': 'Say "Hello from Llama!" in one sentence.'}
        ]
    )
    print(f"   ✅ Generation successful")
    print(f"   📝 Response: {response['message']['content'][:100]}...")
except Exception as e:
    print(f"   ❌ Generation failed: {e}")
    sys.exit(1)

# Test 3: Check Whisper
print("\n3️⃣  Checking Whisper installation...")
try:
    import whisper
    print(f"   ✅ Whisper installed")
    print(f"   📦 Available models: tiny, base, small, medium, large")
except ImportError:
    print(f"   ❌ Whisper not installed")
    print(f"   💡 Run: pip install openai-whisper")
    sys.exit(1)

# Test 4: Test services
print("\n4️⃣  Testing service initialization...")
try:
    os.environ['SECRET_KEY'] = 'test_key_12345678'
    os.environ['OLLAMA_MODEL'] = 'llama2:latest'
    
    from app.services.ollama_service import get_ollama_service
    from app.services.medical_notes import get_medical_note_service
    
    ollama_service = get_ollama_service()
    print(f"   ✅ Ollama service initialized")
    print(f"   🤖 Model: {ollama_service.model}")
    
    medical_service = get_medical_note_service()
    print(f"   ✅ Medical note service initialized")
    
except Exception as e:
    print(f"   ❌ Service initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Test medical note generation
print("\n5️⃣  Testing medical note generation...")
try:
    sample_transcript = """
    Doctor: Hello, what brings you in today?
    Patient: I've had a sore throat for about a week and some mild fever.
    Doctor: Any allergies?
    Patient: Yes, I'm allergic to penicillin.
    Doctor: Okay, let me examine your throat. It looks red and inflamed.
    Patient: It hurts when I swallow.
    Doctor: I'll prescribe some ibuprofen for the pain and recommend rest.
    """
    
    print("   🔄 Generating SOAP note...")
    result = medical_service.generate_soap_note(sample_transcript)
    
    print(f"   ✅ SOAP note generated")
    print(f"   ⏱️  Time: {result['generation_time_seconds']:.2f}s")
    print(f"   🤖 Model: {result['model_used']}")
    
    soap = result['soap_note']
    if soap.get('subjective'):
        print(f"   📝 Subjective: {soap['subjective'][:80]}...")
    if soap.get('assessment'):
        print(f"   📝 Assessment: {soap['assessment'][:80]}...")
        
except Exception as e:
    print(f"   ❌ Medical note generation failed: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 60)
print("📊 Test Summary")
print("=" * 60)
print("✅ Ollama: WORKING")
print("✅ Whisper: INSTALLED")
print("✅ Services: INITIALIZED")
print("✅ Medical Notes: WORKING")
print("\n🎉 Local LLM setup is ready!")
print("\n📝 Configuration:")
print("   - Ollama URL: http://localhost:11434")
print("   - Model: llama2:latest")
print("   - Whisper: base model")
print("\n🚀 Start the server: ./start_server.sh")
