import base64
import json
import os
import time
from io import BytesIO

import comfy.utils
import requests
import torch
from PIL import Image

from .utils import pil2tensor, tensor2pil


baseurl = "https://ai.t8star.cn"


def get_config():
    try:
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Comflyapi.json")
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except Exception:
        return {}


def save_config(config):
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Comflyapi.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)


class Comfly_nano_banana2_edit_ZYX:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "mode": (["text2img", "img2img"], {"default": "text2img"}),
                "model": (["nano-banana-2", "nano-banana-pro", "nano-banana-pro-2k", "nano-banana-pro-4k"], {"default": "nano-banana-pro"}),
                "aspect_ratio": (["auto", "16:9", "4:3", "4:5", "3:2", "1:1", "2:3", "3:4", "5:4", "9:16", "21:9"], {"default": "auto"}),
                "image_size": (["1K", "2K", "4K"], {"default": "2K"}),
            },
            "optional": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "image3": ("IMAGE",),
                "image4": ("IMAGE",),
                "image5": ("IMAGE",),
                "image6": ("IMAGE",),
                "image7": ("IMAGE",),
                "image8": ("IMAGE",),
                "image9": ("IMAGE",),
                "image10": ("IMAGE",),
                "image11": ("IMAGE",),
                "image12": ("IMAGE",),
                "image13": ("IMAGE",),
                "image14": ("IMAGE",),
                "apikey": ("STRING", {"default": ""}),
                "task_id": ("STRING", {"default": ""}),
                "response_format": (["url", "b64_json"], {"default": "url"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2147483647}),
                "skip_error": ("BOOLEAN", {"default": False, "tooltip": "Return a blank result instead of raising when generation fails."}),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image", "image_url", "task_id", "response")
    FUNCTION = "generate_image"
    CATEGORY = "zhenzhen/Google"

    def __init__(self):
        self.api_key = get_config().get("api_key", "")
        self.timeout = 600

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}"
        }

    def image_to_base64(self, image_tensor):
        """Convert tensor to base64 string"""
        if image_tensor is None:
            return None

        pil_image = tensor2pil(image_tensor)[0]
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def generate_image(
        self,
        prompt,
        mode="text2img",
        model="nano-banana-2",
        aspect_ratio="auto",
        image_size="2K",
        image1=None,
        image2=None,
        image3=None,
        image4=None,
        image5=None,
        image6=None,
        image7=None,
        image8=None,
        image9=None,
        image10=None,
        image11=None,
        image12=None,
        image13=None,
        image14=None,
        apikey="",
        task_id="",
        response_format="url",
        seed=0,
        skip_error=False,
    ):
        if apikey.strip():
            self.api_key = apikey
            config = get_config()
            config["api_key"] = apikey
            save_config(config)

        if not self.api_key:
            error_message = "API key not found in Comflyapi.json"
            print(error_message)
            blank_image = Image.new("RGB", (1024, 1024), color="white")
            blank_tensor = pil2tensor(blank_image)
            if not skip_error:
                raise RuntimeError(f"[Comfly_nano_banana2_edit_ZYX] {error_message}")
            return (blank_tensor, "", "", json.dumps({"status": "failed", "message": error_message}))

        try:
            pbar = comfy.utils.ProgressBar(100)
            pbar.update_absolute(10)

            if task_id.strip():
                print(f"Querying task status for task_id: {task_id}")
                return self._query_task_status(task_id, pbar)

            print(f"Creating new async task with mode: {mode}")
            final_prompt = prompt

            if mode == "text2img":
                headers = self.get_headers()
                headers["Content-Type"] = "application/json"

                payload = {
                    "prompt": final_prompt,
                    "model": model,
                    "aspect_ratio": aspect_ratio,
                }

                if model == "nano-banana-2" or model == "nano-banana-pro":
                    payload["image_size"] = image_size

                if response_format:
                    payload["response_format"] = response_format

                if seed > 0:
                    payload["seed"] = seed

                params = {"async": "true"}

                print(f"Submitting text2img async request: {payload}")
                response = requests.post(
                    f"{baseurl}/v1/images/generations",
                    headers=headers,
                    params=params,
                    json=payload,
                    timeout=self.timeout,
                )
            else:
                headers = self.get_headers()

                all_images = [image1, image2, image3, image4, image5, image6, image7, image8, image9, image10, image11, image12, image13, image14]

                files = []
                image_count = 0
                for img in all_images:
                    if img is not None:
                        pil_img = tensor2pil(img)[0]
                        buffered = BytesIO()
                        pil_img.save(buffered, format="PNG")
                        buffered.seek(0)
                        files.append(("image", (f"image_{image_count}.png", buffered, "image/png")))
                        image_count += 1

                print(f"Processing {image_count} input images")

                data = {
                    "prompt": final_prompt,
                    "model": model,
                    "aspect_ratio": aspect_ratio,
                }

                if model == "nano-banana-2" or model == "nano-banana-pro":
                    data["image_size"] = image_size

                if response_format:
                    data["response_format"] = response_format

                if seed > 0:
                    data["seed"] = str(seed)

                params = {"async": "true"}

                print(f"Submitting img2img async request with {image_count} images")
                response = requests.post(
                    f"{baseurl}/v1/images/edits",
                    headers=headers,
                    params=params,
                    data=data,
                    files=files,
                    timeout=self.timeout,
                )

            pbar.update_absolute(30)

            if response.status_code != 200:
                error_message = f"API Error: {response.status_code} - {response.text}"
                print(error_message)
                blank_image = Image.new("RGB", (1024, 1024), color="white")
                blank_tensor = pil2tensor(blank_image)
                if not skip_error:
                    raise RuntimeError(f"[Comfly_nano_banana2_edit_ZYX] {error_message}")
                return (blank_tensor, "", "", json.dumps({"status": "failed", "message": error_message}))

            result = response.json()
            print(f"API response: {result}")

            if "task_id" in result:
                returned_task_id = result["task_id"]

                result_info = {
                    "status": "pending",
                    "task_id": returned_task_id,
                    "model": model,
                    "mode": mode,
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "image_size": image_size if model == "nano-banana-2" or model == "nano-banana-pro" else None,
                    "seed": seed if seed > 0 else None,
                    "message": "Async task created successfully. Please use this task_id to query the result.",
                }

                print(f"[ASYNC_RESPONSE] {json.dumps(result_info, ensure_ascii=False)}")

                blank_image = Image.new("RGB", (512, 512), color="lightgray")
                blank_tensor = pil2tensor(blank_image)
                pbar.update_absolute(100)

                print(f"Waiting for task completion: {returned_task_id}")
                max_attempts = 60
                attempt = 0

                while attempt < max_attempts:
                    time.sleep(5)
                    attempt += 1

                    try:
                        query_url = f"{baseurl}/v1/images/tasks/{returned_task_id}"
                        query_response = requests.get(
                            query_url,
                            headers=headers,
                            timeout=self.timeout,
                        )

                        if query_response.status_code == 200:
                            query_result = query_response.json()
                            actual_status = "unknown"
                            actual_data = None

                            if "data" in query_result and isinstance(query_result["data"], dict):
                                actual_status = query_result["data"].get("status", "unknown")
                                actual_data = query_result["data"].get("data")

                            print(f"Task status (attempt {attempt}): {actual_status}")

                            if actual_status == "completed" or actual_status == "success" or actual_status == "done" or actual_status == "finished" or actual_status == "SUCCESS" or (actual_status == "unknown" and actual_data):
                                if actual_data:
                                    generated_tensors = []
                                    image_urls = []

                                    data_items = actual_data.get("data", []) if isinstance(actual_data, dict) else actual_data
                                    if not isinstance(data_items, list):
                                        data_items = [data_items]

                                    for item in data_items:
                                        try:
                                            if "b64_json" in item and item["b64_json"]:
                                                image_data = base64.b64decode(item["b64_json"])
                                                image_stream = BytesIO(image_data)
                                                generated_image = Image.open(image_stream)
                                                generated_image.verify()
                                                image_stream.seek(0)
                                                generated_image = Image.open(image_stream)
                                                if generated_image.mode != "RGB":
                                                    generated_image = generated_image.convert("RGB")
                                                generated_tensor = pil2tensor(generated_image)
                                                generated_tensors.append(generated_tensor)
                                            elif "url" in item and item["url"]:
                                                image_url = item["url"]
                                                image_urls.append(image_url)
                                                img_response = requests.get(image_url, timeout=self.timeout)
                                                img_response.raise_for_status()
                                                image_stream = BytesIO(img_response.content)
                                                generated_image = Image.open(image_stream)
                                                generated_image.verify()
                                                image_stream.seek(0)
                                                generated_image = Image.open(image_stream)
                                                if generated_image.mode != "RGB":
                                                    generated_image = generated_image.convert("RGB")
                                                generated_tensor = pil2tensor(generated_image)
                                                generated_tensors.append(generated_tensor)
                                        except Exception as e:
                                            print(f"Error processing image item: {str(e)}")
                                            continue

                                    if generated_tensors:
                                        combined_tensor = torch.cat(generated_tensors, dim=0)
                                        first_image_url = image_urls[0] if image_urls else ""
                                        final_result_info = {
                                            "status": "success",
                                            "task_id": returned_task_id,
                                            "model": model,
                                            "mode": mode,
                                            "prompt": prompt,
                                            "aspect_ratio": aspect_ratio,
                                            "image_size": image_size if model == "nano-banana-2" or model == "nano-banana-pro" else None,
                                            "seed": seed if seed > 0 else None,
                                            "images_count": len(generated_tensors),
                                            "image_url": first_image_url,
                                            "all_urls": image_urls,
                                        }
                                        pbar.update_absolute(100)
                                        return (combined_tensor, first_image_url, returned_task_id, json.dumps(final_result_info))

                            elif actual_status == "failed" or actual_status == "error" or actual_status == "FAILURE":
                                error_msg = query_result.get("error", "Unknown error")
                                print(f"Task failed: {error_msg}")
                                blank_image = Image.new("RGB", (1024, 1024), color="red")
                                blank_tensor = pil2tensor(blank_image)
                                pbar.update_absolute(100)
                                if not skip_error:
                                    raise RuntimeError(f"[Comfly_nano_banana2_edit_ZYX] {error_msg}")
                                return (blank_tensor, "", "", json.dumps({"status": "failed", "task_id": returned_task_id, "message": error_msg}))

                        else:
                            print(f"Query failed with status {query_response.status_code}")

                    except Exception as e:
                        print(f"Error querying task status: {str(e)}")

                print("Task polling timed out")
                blank_image = Image.new("RGB", (512, 512), color="yellow")
                blank_tensor = pil2tensor(blank_image)
                pbar.update_absolute(100)
                if not skip_error:
                    raise RuntimeError("[Comfly_nano_banana2_edit_ZYX] Task polling timed out")
                return (blank_tensor, "", returned_task_id, json.dumps({"status": "timeout", "task_id": returned_task_id, "message": "Task polling timed out. Please query manually."}))

            elif "data" in result and result["data"]:
                print(f"Sync mode detected, processing {len(result['data'])} images directly")
                generated_tensors = []
                image_urls = []
                response_info = f"Generated {len(result['data'])} images using {model}\n"

                if model == "nano-banana-2" or model == "nano-banana-pro":
                    response_info += f"Image size: {image_size}\n"

                response_info += f"Aspect ratio: {aspect_ratio}\n"

                if mode == "img2img":
                    response_info += f"Input images: {image_count}\n"

                if seed > 0:
                    response_info += f"Seed: {seed}\n"

                data_items = result.get("data", [])
                if not isinstance(data_items, list):
                    data_items = [data_items]

                for i, item in enumerate(data_items):
                    try:
                        pbar.update_absolute(50 + (i + 1) * 40 // len(data_items))

                        if "b64_json" in item and item["b64_json"]:
                            image_data = base64.b64decode(item["b64_json"])
                            image_stream = BytesIO(image_data)
                            generated_image = Image.open(image_stream)
                            generated_image.verify()
                            image_stream.seek(0)
                            generated_image = Image.open(image_stream)
                            if generated_image.mode != "RGB":
                                generated_image = generated_image.convert("RGB")
                            generated_tensor = pil2tensor(generated_image)
                            generated_tensors.append(generated_tensor)
                            response_info += f"Image {i + 1}: Base64 data\n"
                        elif "url" in item and item["url"]:
                            image_url = item["url"]
                            image_urls.append(image_url)
                            response_info += f"Image {i + 1}: {image_url}\n"
                            img_response = requests.get(image_url, timeout=self.timeout)
                            img_response.raise_for_status()
                            image_stream = BytesIO(img_response.content)
                            generated_image = Image.open(image_stream)
                            generated_image.verify()
                            image_stream.seek(0)
                            generated_image = Image.open(image_stream)
                            if generated_image.mode != "RGB":
                                generated_image = generated_image.convert("RGB")
                            generated_tensor = pil2tensor(generated_image)
                            generated_tensors.append(generated_tensor)
                    except Exception as e:
                        print(f"Error processing image item {i}: {str(e)}")
                        continue

                pbar.update_absolute(100)

                if generated_tensors:
                    combined_tensor = torch.cat(generated_tensors, dim=0)
                    first_image_url = image_urls[0] if image_urls else ""

                    import uuid

                    sync_task_id = f"sync_{uuid.uuid4().hex[:16]}"

                    result_info = {
                        "status": "success",
                        "task_id": sync_task_id,
                        "model": model,
                        "mode": mode,
                        "prompt": prompt,
                        "aspect_ratio": aspect_ratio,
                        "image_size": image_size if model == "nano-banana-2" or model == "nano-banana-pro" else None,
                        "seed": result.get("seed", seed) if seed > 0 else None,
                        "images_count": len(generated_tensors),
                        "image_url": first_image_url,
                        "all_urls": image_urls,
                    }

                    print(f"[SYNC_RESPONSE] {json.dumps(result_info, ensure_ascii=False)}")

                    return (combined_tensor, first_image_url, sync_task_id, json.dumps(result_info))
                else:
                    error_message = "Failed to process any images"
                    print(error_message)
                    blank_image = Image.new("RGB", (1024, 1024), color="white")
                    blank_tensor = pil2tensor(blank_image)
                    if not skip_error:
                        raise RuntimeError(f"[Comfly_nano_banana2_edit_ZYX] {error_message}")
                    return (blank_tensor, "", "", json.dumps({"status": "failed", "message": error_message}))

            else:
                error_message = f"Unexpected API response format: {result}"
                print(error_message)
                blank_image = Image.new("RGB", (1024, 1024), color="white")
                blank_tensor = pil2tensor(blank_image)
                if not skip_error:
                    raise RuntimeError(f"[Comfly_nano_banana2_edit_ZYX] {error_message}")
                return (blank_tensor, "", "", json.dumps({"status": "failed", "message": error_message}))

        except Exception as e:
            error_message = f"Error in image generation: {str(e)}"
            print(error_message)
            import traceback

            traceback.print_exc()
            blank_image = Image.new("RGB", (1024, 1024), color="white")
            blank_tensor = pil2tensor(blank_image)
            if not skip_error:
                raise
            return (blank_tensor, "", "", json.dumps({"status": "failed", "message": error_message}))

    def _query_task_status(self, task_id, pbar):
        try:
            headers = self.get_headers()
            headers["Content-Type"] = "application/json"

            query_url = f"{baseurl}/v1/images/tasks/{task_id}"
            print(f"Querying task status: {query_url}")
            response = requests.get(
                query_url,
                headers=headers,
                timeout=self.timeout,
            )

            pbar.update_absolute(50)

            if response.status_code != 200:
                error_message = f"Query Error: {response.status_code} - {response.text}"
                print(error_message)
                blank_image = Image.new("RGB", (1024, 1024), color="white")
                blank_tensor = pil2tensor(blank_image)
                return (blank_tensor, "", "", json.dumps({"status": "query_failed", "task_id": task_id, "message": error_message}))

            result = response.json()
            print(f"Task status response: {result}")

            actual_status = "unknown"
            actual_data = None

            if "data" in result and isinstance(result["data"], dict):
                actual_status = result["data"].get("status", "unknown")
                actual_data = result["data"].get("data")

            if actual_status == "completed" or actual_status == "success" or actual_status == "done" or actual_status == "finished" or actual_status == "SUCCESS" or (actual_status == "unknown" and actual_data):
                if "data" in result and result["data"]:
                    generated_tensors = []
                    image_urls = []
                    response_info = "Task completed successfully\n"
                    response_info += f"Task ID: {task_id}\n"
                    response_info += f"Generated {len(result['data'])} images\n"

                    data_items = result.get("data", [])
                    if not isinstance(data_items, list):
                        data_items = [data_items]

                    for i, item in enumerate(data_items):
                        try:
                            pbar.update_absolute(50 + (i + 1) * 40 // len(data_items))

                            if "b64_json" in item and item["b64_json"]:
                                image_data = base64.b64decode(item["b64_json"])
                                image_stream = BytesIO(image_data)
                                generated_image = Image.open(image_stream)
                                generated_image.verify()
                                image_stream.seek(0)
                                generated_image = Image.open(image_stream)
                                if generated_image.mode != "RGB":
                                    generated_image = generated_image.convert("RGB")
                                generated_tensor = pil2tensor(generated_image)
                                generated_tensors.append(generated_tensor)
                                response_info += f"Image {i + 1}: Base64 data\n"
                            elif "url" in item and item["url"]:
                                image_url = item["url"]
                                image_urls.append(image_url)
                                response_info += f"Image {i + 1}: {image_url}\n"
                                img_response = requests.get(image_url, timeout=self.timeout)
                                img_response.raise_for_status()
                                image_stream = BytesIO(img_response.content)
                                generated_image = Image.open(image_stream)
                                generated_image.verify()
                                image_stream.seek(0)
                                generated_image = Image.open(image_stream)
                                if generated_image.mode != "RGB":
                                    generated_image = generated_image.convert("RGB")
                                generated_tensor = pil2tensor(generated_image)
                                generated_tensors.append(generated_tensor)
                        except Exception as e:
                            print(f"Error processing image item {i}: {str(e)}")
                            continue

                    pbar.update_absolute(100)

                    if generated_tensors:
                        combined_tensor = torch.cat(generated_tensors, dim=0)
                        first_image_url = image_urls[0] if image_urls else ""
                        return (combined_tensor, first_image_url, task_id, json.dumps({"status": "success", "task_id": task_id, "images_count": len(generated_tensors), "image_url": first_image_url, "all_urls": image_urls}))
                    else:
                        error_message = "No valid images in completed task"
                        print(error_message)
                        blank_image = Image.new("RGB", (1024, 1024), color="white")
                        blank_tensor = pil2tensor(blank_image)
                        return (blank_tensor, "", "", json.dumps({"status": "failed", "task_id": task_id, "message": error_message}))
                else:
                    error_message = "Task completed but no image data"
                    print(error_message)
                    blank_image = Image.new("RGB", (1024, 1024), color="white")
                    blank_tensor = pil2tensor(blank_image)
                    return (blank_tensor, "", "", json.dumps({"status": "failed", "task_id": task_id, "message": error_message}))

            elif actual_status == "processing" or actual_status == "pending" or actual_status == "in_progress":
                blank_image = Image.new("RGB", (512, 512), color="yellow")
                blank_tensor = pil2tensor(blank_image)
                pbar.update_absolute(100)
                return (blank_tensor, "", "", json.dumps({"status": actual_status, "task_id": task_id, "message": "Task is still processing. Please query again later."}))

            elif actual_status == "failed" or actual_status == "error":
                error_msg = result.get("error", "Unknown error")
                blank_image = Image.new("RGB", (512, 512), color="red")
                blank_tensor = pil2tensor(blank_image)
                pbar.update_absolute(100)
                return (blank_tensor, "", "", json.dumps({"status": "failed", "task_id": task_id, "message": error_msg}))

            else:
                blank_image = Image.new("RGB", (512, 512), color="gray")
                blank_tensor = pil2tensor(blank_image)
                pbar.update_absolute(100)
                return (blank_tensor, "", "", json.dumps({"status": actual_status, "task_id": task_id, "message": f"Unknown task status: {actual_status}", "raw_response": result}))

        except Exception as e:
            error_message = f"Error querying task status: {str(e)}"
            print(error_message)
            import traceback

            traceback.print_exc()
            blank_image = Image.new("RGB", (1024, 1024), color="white")
            blank_tensor = pil2tensor(blank_image)
            return (blank_tensor, "", "", json.dumps({"status": "query_error", "task_id": task_id, "message": error_message}))


__all__ = ["Comfly_nano_banana2_edit_ZYX"]
