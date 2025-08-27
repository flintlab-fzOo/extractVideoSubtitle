제공해주신 `Qwen-Image-Edit` 모델은 기본적으로 **하나의 입력 이미지**와 **텍스트 프롬프트**를 받아 이미지를 편집하는 방식으로 작동합니다. 즉, 파이프라인(`pipeline(**inputs)`)에 직접적으로 두 개의 서로 다른 "입력 이미지"를 동시에 넣어 하나의 결과 이미지를 생성하는 기능은 `Quick Start` 예시에서 명시적으로 보여주지 않습니다.

그러나 "두 가지 이미지를 적용"하는 시나리오는 다음과 같이 해석될 수 있습니다:

1.  **각 이미지를 독립적으로 편집하고 각각의 결과 이미지 생성:** 가장 직관적인 방법입니다. 첫 번째 이미지를 프롬프트로 편집하고, 두 번째 이미지를 다른 프롬프트로 편집하여 각각의 결과물을 얻는 방식입니다.
2.  **연속 편집 (Chained Editing):** 첫 번째 이미지를 편집한 결과물을 두 번째 편집의 입력 이미지로 사용하는 방식입니다. 제공된 "서예 작품" 예시가 이에 해당합니다.
3.  **이미지 합성 후 편집:** 두 이미지를 사전에 파이썬 코드(PIL 등)로 합성하거나 특정 마스크를 생성하여 하나의 입력 이미지로 만든 다음, 이 합성된 이미지를 모델에 넣어 편집하는 방식입니다.

요청하신 내용을 바탕으로 **각 이미지를 독립적으로 편집하여 각각의 결과 이미지를 생성하는 샘플 코드**를 제공해 드리겠습니다. 이는 두 개의 파일 경로를 인수로 받아 각각 편집을 수행하는 가장 일반적이고 직접적인 구현 방법입니다.

먼저, 예시 실행을 위해 **`input1.png`**와 **`input2.png`**라는 두 개의 이미지 파일을 현재 스크립트가 실행될 디렉토리에 준비해주세요.

```python
import os
from PIL import Image
import torch
import sys

# diffusers 라이브러리 설치 확인 및 안내 (설치되어 있다면 이 부분은 스킵됩니다)
try:
    from diffusers import QwenImageEditPipeline
except ImportError:
    print("diffusers 라이브러리가 설치되어 있지 않습니다. 설치를 시도합니다.")
    print("pip install git+https://github.com/huggingface/diffusers")
    try:
        os.system("pip install git+https://github.com/huggingface/diffusers")
        from diffusers import QwenImageEditPipeline
        print("diffusers 라이브러리 설치 및 불러오기 완료.")
    except Exception as e:
        print(f"diffusers 설치에 실패했습니다: {e}")
        print("수동으로 'pip install git+https://github.com/huggingface/diffusers'를 실행해주세요.")
        sys.exit(1)

def edit_image_with_qwen(
    image_path: str,
    prompt: str,
    output_filename: str,
    pipeline: QwenImageEditPipeline,
    device: str = "cuda",
    dtype=torch.bfloat16,
    seed: int = 0
):
    """
    Qwen-Image-Edit 파이프라인을 사용하여 이미지를 편집하고 저장합니다.

    Args:
        image_path (str): 입력 이미지 파일의 경로.
        prompt (str): 이미지를 편집하기 위한 텍스트 프롬프트.
        output_filename (str): 결과 이미지를 저장할 파일명.
        pipeline (QwenImageEditPipeline): 로드된 QwenImageEditPipeline 인스턴스.
        device (str): 모델을 실행할 장치 ('cuda' 또는 'cpu').
        dtype: 모델에 사용할 데이터 타입 (예: torch.bfloat16).
        seed (int): 난수 생성기 시드 (재현성을 위해).
    """
    if not os.path.exists(image_path):
        print(f"오류: 입력 이미지 파일이 존재하지 않습니다: {image_path}")
        return

    try:
        image = Image.open(image_path).convert("RGB")
        print(f"\n--- '{image_path}' 이미지 편집 시작 ---")
        print(f"프롬프트: '{prompt}'")

        inputs = {
            "image": image,
            "prompt": prompt,
            "generator": torch.manual_seed(seed),
            "true_cfg_scale": 4.0,  # 설정값은 예시에서 가져옴
            "negative_prompt": "bad anatomy, blurry, low quality, deformed, malformed",
            "num_inference_steps": 50, # 추론 스텝 수
        }

        with torch.inference_mode():
            output = pipeline(**inputs)
            output_image = output.images[0]
            output_image.save(output_filename)
            print(f"편집된 이미지가 '{os.path.abspath(output_filename)}' 에 저장되었습니다.")

    except Exception as e:
        print(f"'{image_path}' 편집 중 오류 발생: {e}")

if __name__ == "__main__":
    # 1. Qwen-Image-Edit 파이프라인 로드
    print("Qwen-Image-Edit 파이프라인을 로드 중입니다. (시간이 다소 소요될 수 있습니다.)")
    try:
        # GPU 사용 가능 여부 확인
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if device == "cuda" and torch.cuda.is_bf16_supported() else torch.float16 if device == "cuda" else torch.float32

        pipeline = QwenImageEditPipeline.from_pretrained("Qwen/Qwen-Image-Edit", torch_dtype=dtype)
        pipeline.to(device)
        pipeline.set_progress_bar_config(disable=None)
        print(f"파이프라인 로드 완료 (Device: {device}, Dtype: {dtype})")
    except Exception as e:
        print(f"파이프라인 로드 중 오류 발생: {e}")
        print("GPU 메모리가 부족하거나, CUDA 설정에 문제가 있을 수 있습니다.")
        sys.exit(1)

    # 2. 첫 번째 이미지와 프롬프트
    image1_path = "./input1.png"
    prompt1 = "Change the background to a beautiful sunset sky, make the rabbit wear a small hat."
    output1_filename = "./output_image_edit_1.png"

    # 3. 두 번째 이미지와 프롬프트
    image2_path = "./input2.png"
    prompt2 = "Add a pair of sunglasses to the cat, and change its fur color to blue."
    output2_filename = "./output_image_edit_2.png"

    # 4. 각 이미지에 대해 편집 함수 호출
    edit_image_with_qwen(image1_path, prompt1, output1_filename, pipeline, device, dtype, seed=0)
    edit_image_with_qwen(image2_path, prompt2, output2_filename, pipeline, device, dtype, seed=1)

    print("\n모든 이미지 편집 프로세스가 완료되었습니다.")
```

### 코드 설명:

1.  **`diffusers` 라이브러리 설치 확인:** 스크립트 시작 부분에서 `diffusers`가 설치되어 있지 않으면 자동으로 설치를 시도합니다.
2.  **`edit_image_with_qwen` 함수:**
    *   `image_path`, `prompt`, `output_filename`, `pipeline` 등의 매개변수를 받습니다.
    *   지정된 `image_path`에서 이미지를 로드하고 `RGB` 형식으로 변환합니다.
    *   제공된 프롬프트와 기타 설정(seed, CFG 스케일, 네거티브 프롬프트, 추론 스텝)을 사용하여 `inputs` 딕셔너리를 구성합니다.
    *   `pipeline(**inputs)`를 호출하여 이미지 편집을 실행합니다.
    *   결과 이미지를 `output_filename`으로 저장합니다.
    *   파일이 없거나 편집 중 오류가 발생하면 메시지를 출력합니다.
3.  **메인 실행 블록 (`if __name__ == "__main__":`)**:
    *   **파이프라인 로드:** `QwenImageEditPipeline.from_pretrained("Qwen/Qwen-Image-Edit")`를 사용하여 모델을 로드합니다. GPU 사용 가능 여부를 확인하고, `bfloat16`을 지원하면 사용하며, 아니면 `float16` 또는 `float32`를 사용합니다. 이 과정은 모델을 처음 다운로드할 때 시간이 다소 소요될 수 있습니다.
    *   **입력 및 출력 정의:** `image1_path`, `prompt1`, `output1_filename`과 `image2_path`, `prompt2`, `output2_filename` 변수를 정의합니다.
    *   **함수 호출:** 정의된 첫 번째 이미지와 프롬프트로 `edit_image_with_qwen` 함수를 호출하고, 이어서 두 번째 이미지와 프롬프트로 다시 호출합니다.

### 사용 방법:

1.  **환경 설정:**
    *   Python 환경을 준비합니다. (Python 3.8 이상 권장)
    *   CUDA가 설치된 NVIDIA GPU가 권장됩니다. (CPU에서도 동작하지만 매우 느립니다.)
    *   `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118` (또는 본인의 CUDA 버전에 맞게 설치)
    *   `pip install Pillow` (PIL 라이브러리)
    *   스크립트가 자동으로 `diffusers`를 설치하려고 시도하지만, 문제가 생기면 수동으로 `pip install git+https://github.com/huggingface/diffusers`를 실행해주세요.
2.  **이미지 준비:**
    *   스크립트와 같은 디렉토리에 **`input1.png`**와 **`input2.png`** 라는 이름의 이미지 파일을 준비합니다. (예: 토끼 사진, 고양이 사진 등)
3.  **스크립트 실행:**
    *   위 코드를 `qwen_edit_two_images.py` 등으로 저장합니다.
    *   터미널에서 `python qwen_edit_two_images.py` 명령어를 실행합니다.

스크립트가 성공적으로 실행되면, `output_image_edit_1.png`와 `output_image_edit_2.png` 파일이 생성될 것입니다.