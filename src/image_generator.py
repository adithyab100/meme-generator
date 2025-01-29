import numpy as np
import torch
from diffusers import StableDiffusionPipeline
import os
import sys
from typing import Optional
import gc

class ImageGenerator:
    def __init__(self, model_name: str):
        print("Initializing ImageGenerator...")
        print(f"Python version: {sys.version}")
        print(f"Numpy version: {np.__version__}")
        print(f"Torch version: {torch.__version__}")
        
        self.device, self.dtype = self._get_optimal_device()
        print(f"Using device: {self.device} with dtype: {self.dtype}")
        
        try:
            print("Loading StableDiffusionPipeline...")
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_name,
                torch_dtype=self.dtype,
                safety_checker=None,  # Disable safety checker during load
                requires_safety_checker=False  # Prevent safety checker requirement
            )
            
            # Common optimizations
            if self.device.type == "cuda":
                self._optimize_for_cuda()
            elif self.device.type == "mps":
                self._optimize_for_mps()
            else:
                self._optimize_for_cpu()
                
            print(f"Successfully initialized pipeline on {self.device}")
        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            self._fallback_to_cpu()

    def _get_optimal_device(self) -> tuple:
        """Determine the optimal device and dtype"""
        if torch.cuda.is_available():
            return torch.device("cuda"), torch.float16
        elif torch.backends.mps.is_available():
            return torch.device("mps"), torch.float32
        return torch.device("cpu"), torch.float32

    def _optimize_for_cuda(self):
        """Optimizations for CUDA devices"""
        self.pipe = self.pipe.to(self.device)
        torch.cuda.empty_cache()
        # Enable xformers memory efficient attention if available
        try:
            self.pipe.enable_xformers_memory_efficient_attention()
        except:
            pass

    def _optimize_for_mps(self):
        """Optimizations for MPS devices"""
        # MPS-specific settings
        torch.mps.empty_cache()
        os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
        
        # Move components individually with error handling
        components = [self.pipe.unet, self.pipe.text_encoder, self.pipe.vae]
        for component in components:
            try:
                component.to(self.device)
            except Exception as e:
                print(f"Error moving component to MPS: {str(e)}")
                self._fallback_to_cpu()
                break

    def _optimize_for_cpu(self):
        """Optimizations for CPU"""
        self.pipe.to("cpu")
        # Use memory-efficient attention on CPU
        try:
            self.pipe.enable_attention_slicing()
        except:
            pass

    def _fallback_to_cpu(self):
        """Fallback to CPU with proper cleanup"""
        print("Initiating fallback to CPU...")
        try:
            if self.device.type == "cuda":
                torch.cuda.empty_cache()
            elif self.device.type == "mps":
                torch.mps.empty_cache()
            
            self.device = torch.device("cpu")
            self.dtype = torch.float32
            self.pipe.to("cpu")
            gc.collect()
            print("Successfully moved to CPU")
        except Exception as e:
            print(f"Critical error during CPU fallback: {str(e)}")
            raise RuntimeError("Failed to initialize on any device")

    def generate_image(self, prompt: str):
        """Generate an image based on text prompt"""
        try:
            print(f"Generating image for prompt: {prompt}")
            
            # Common generation parameters
            base_kwargs = {
                "prompt": prompt,
                "num_inference_steps": 40,
                "guidance_scale": 7.5,
                "height": 512,
                "width": 512
            }
            
            # Device-specific adjustments
            if self.device.type == "mps":
                # MPS-specific memory management
                torch.mps.empty_cache()
                gc.collect()
                return self.pipe(**base_kwargs).images[0]
            
            elif self.device.type == "cuda":
                # CUDA optimization
                with torch.autocast("cuda"):
                    return self.pipe(**base_kwargs).images[0]
            
            else:  # CPU
                self.pipe.enable_attention_slicing()
                return self.pipe(**base_kwargs).images[0]
            
        except RuntimeError as e:
            if "device but got CPU" in str(e) or "MPS" in str(e):
                print("Device mismatch detected, retrying with CPU...")
                self._fallback_to_cpu()
                return self.generate_image(prompt)
            raise
        except Exception as e:
            print(f"Generation error: {str(e)}")
            raise