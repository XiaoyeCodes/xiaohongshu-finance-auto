#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Quick Draw - 快速绘图脚本（支持图片参考）
使用 Google Nano Banana Pro (Gemini 3 Pro Image) API 生成图片

Usage:
    # 文生图
    python3 draw.py --prompt "图片描述" [--resolution 1K|2K|4K] [--api-key KEY]
    
    # 图生图（参考图片）
    python3 draw.py --prompt "图片描述" --image "参考图片路径" [--resolution 1K|2K|4K] [--api-key KEY]
"""

import argparse
import os
import sys
import base64
from datetime import datetime
from pathlib import Path

# Set up proxy for Gemini API (Lightning Cat Accelerator)
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8086'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8086'


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment, then .env file."""
    if provided_key:
        return provided_key
    
    # Try environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    # Try .env file in workspace
    env_file = Path(r"C:\Users\danwe\.qclaw\workspace\.env")
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip()
    
    return None


def generate_filename(prompt: str, has_reference: bool = False) -> str:
    """Generate filename from prompt and timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    # Extract keywords from prompt for filename
    words = prompt.lower().split()
    # Keep only alphabetic words, limit to 5 words
    keywords = [w for w in words if w.isalpha()][:5]
    name = "-".join(keywords) if keywords else "image"
    
    # Add reference indicator if using image reference
    prefix = "ref-" if has_reference else ""
    return f"{timestamp}-{prefix}{name}.png"


def main():
    parser = argparse.ArgumentParser(description="Quick Draw - 快速生成图片（支持图片参考）")
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="图片描述/prompt"
    )
    parser.add_argument(
        "--image", "-i",
        help="参考图片路径（可选，用于图生图/图片参考）"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default="1K",
        help="输出分辨率：1K (默认), 2K, 或 4K"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gemini API key (可选，会从环境变量或.env 文件读取)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default=r"C:\Users\danwe\.qclaw\workspace",
        help="输出目录 (默认：工作区)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set GEMINI_API_KEY environment variable", file=sys.stderr)
        print("  3. Add GEMINI_API_KEY to .env file", file=sys.stderr)
        sys.exit(1)

    # Import here after checking API key to avoid slow import on error
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage
    from io import BytesIO

    # Configure proxy - force all API requests through local proxy (FlashCat VPN)
    # This allows using Smart Mode instead of Global Mode
    # Set environment variables for proxy (use HTTP proxy for both)
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8086'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8086'
    
    print(f"[Proxy] Using proxy: http://127.0.0.1:8086 (FlashCat VPN)")

    # Initialize client (will use proxy from environment variables)
    client = genai.Client(api_key=api_key)

    # Set up output path
    has_reference = args.image is not None
    output_filename = generate_filename(args.prompt, has_reference)
    output_path = Path(args.output_dir) / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"正在生成图片，分辨率：{args.resolution}...")
    if has_reference:
        print(f"参考图片：{args.image}")
    print(f"Prompt: {args.prompt}")

    try:
        # Build contents - simplified approach
        if has_reference:
            # Load reference image as PIL Image
            ref_image = PILImage.open(args.image)
            if ref_image.mode in ('RGBA', 'P'):
                ref_image = ref_image.convert('RGB')
            
            # Convert to bytes
            img_buffer = BytesIO()
            ref_image.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()
            
            # Create image part directly from bytes
            image_part = types.Part.from_bytes(
                data=img_bytes,
                mime_type='image/png'
            )
            
            # Create text part
            text_part = types.Part()
            text_part.text = args.prompt
            
            # Build contents as a list of parts (not Content objects)
            contents = [image_part, text_part]
            print("模式：图生图（带图片参考）")
        else:
            # Text-only prompt - same as backup script
            contents = args.prompt
            print("模式：文生图")

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(
                    image_size=args.resolution
                )
            )
        )

        # Process response and convert to PNG - same as backup script
        image_saved = False
        for part in response.parts:
            if part.text is not None:
                print(f"Model response: {part.text}")
            elif part.inline_data is not None:
                # Convert inline data to PIL Image and save as PNG
                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                # Ensure RGB mode for PNG
                if image.mode == 'RGBA':
                    rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])
                    rgb_image.save(str(output_path), 'PNG')
                elif image.mode == 'RGB':
                    image.save(str(output_path), 'PNG')
                else:
                    image.convert('RGB').save(str(output_path), 'PNG')
                image_saved = True

        if image_saved:
            full_path = output_path.resolve()
            print(f"\n[SUCCESS] Image generated!")
            print(f"[PATH] {full_path}")
            print(f"\n{full_path}")  # Last line: just the path for easy parsing
        else:
            print("Error: No image was generated in the response.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
