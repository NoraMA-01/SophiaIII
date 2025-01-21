
# ezLocalai

**Key Links:**
- [DevXT](https://devxt.com)
- [ezLocalai](https://github.com/DevXT-LLC/ezlocalai)
- [Sophia III](https://github.com/Nora-MA-01/Sophia-III)

## Overview

ezLocalai provides an API that simplifies the use of local models, enabling them to handle multimodal tasks effortlessly. This tool integrates text-to-speech (TTS) and voice cloning features, facilitating easy voice-to-text communication. Additionally, it enables offline image generation after initial setup. Designed as a drop-in replacement for OpenAI APIs, ezLocalai offers extended functionality and enhanced capabilities for local models.

When integrated with Sophia III, ezLocalai transforms your computer into a powerful automation engine, offering even more advanced functionalities like automatic scaling of tokens and model management.

## Key Features
- **Local Models**: Run and manage local models without needing to rely on external services.
- **Multimodal Capabilities**: Handle text, voice, and image inputs for more robust interactions.
- **Voice Cloning & TTS**: Clone voices by uploading a short voice sample, enabling personalized text-to-speech generation.
- **Offline Image Generation**: Generate images offline once the initial setup is complete.
- **OpenAI Style API**: Compatible with OpenAI-style endpoints for ease of use as a seamless drop-in API replacement.
- **Scalable Token Handling**: Automatically scales based on desired token limits, configurable in your `.env` file.

### Hardware Requirements
- **Minimum VRAM for optimal performance**: For models like `Meta-Llama-3-8B-Instruct`, running 32k context requires 23GB VRAM.
- **Supported Hardware**: Currently supports NVIDIA GPUs or CPU. VRAM can be managed by adjusting `GPU_LAYERS` in the `.env` file for more efficient use.
- **Performance on lower specs**: Running models like `phi-2-dpo` with 16GB VRAM works well with a 16k max context. VRAM usage can be reduced by lowering max tokens.

## Quick Start Guide

To get started with ezLocalai, follow the instructions on the official [GitHub page](https://github.com/DevXT-LLC/ezlocalai). Once you have it installed and running with your desired models, integrate it with Sophia III by following these steps:

### 1. Update your agent settings
- **Set `AI_PROVIDER`** to `ezlocalai`.
- **Set `EZLOCALAI_API_KEY`** to the API key you configured with ezLocalai.
- **Set `EZLOCALAI_API_URL`** to the URL where ezLocalai is running (default: `http://YOUR_LOCAL_IP:8091`).
- **Set `EZLOCALAI_MODEL`** to the model you are running with ezLocalai.
- **Set `EZLOCALAI_MAX_TOKENS`** to your desired maximum number of input tokens.
- **Set `EZLOCALAI_TEMPERATURE`** to control randomness in the model’s responses (between `0` and `1`, default is `1.33`).
- **Set `EZLOCALAI_TOP_P`** to the top_p value you want to use for generation (between `0` and `1`, default is `0.95`).
- **Set `EZLOCALAI_VOICE`** to the voice you want to use for the generated audio. The default is `DukeNukem`. You can add cloning TTS voices to `ezlocalai` by placing any ~10-second `.wav` file in the `voices` directory of the `ezlocalai` repository and then setting the `VOICE` variable to the name of the file (without the `.wav` extension).
