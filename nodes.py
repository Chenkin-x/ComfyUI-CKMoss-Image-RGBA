"""Load the RGBA F2VAE into ComfyUI's normal sampling and image workflow."""
import torch
import comfy.sd
import comfy.utils
import comfy.model_management
import folder_paths


class MossRGBAVAELoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {'required': {'vae_name': (folder_paths.get_filename_list('vae'),)}}

    RETURN_TYPES = ('VAE',)
    FUNCTION = 'load'
    CATEGORY = 'MOSS/RGBA'

    def load(self, vae_name):
        path = folder_paths.get_full_path_or_raise('vae', vae_name)
        state = comfy.utils.load_torch_file(path, safe_load=True)
        assert state['encoder.conv_in.weight'].shape[1] == 4, 'Select moss_rgba_vae.safetensors.'
        # Explicit four-channel architecture; latent layout stays FLUX.2-compatible.
        config = {'params': {'embed_dim': 32, 'ddconfig': {
            'double_z': True, 'z_channels': 32, 'resolution': 256,
            'in_channels': 4, 'out_ch': 4, 'ch': 128, 'ch_mult': [1, 2, 4, 4],
            'num_res_blocks': 2, 'attn_resolutions': [], 'dropout': 0.,
            'batch_norm_latent': True,
        }}}
        vae = comfy.sd.VAE(sd=state, config=config, dtype=torch.float32)
        vae.output_channels = 4
        vae.latent_channels = 128
        vae.downscale_ratio = vae.upscale_ratio = 16
        vae.pad_channel_value = 1.0
        vae.memory_used_decode = lambda shape, dtype: (2178 * shape[2] * shape[3] * 256
                                                      * comfy.model_management.dtype_size(dtype))
        return (vae,)


class MossRGBASplit:
    @classmethod
    def INPUT_TYPES(cls):
        return {'required': {'rgba': ('IMAGE',)}}

    RETURN_TYPES = ('IMAGE', 'MASK')
    RETURN_NAMES = ('image', 'mask')
    FUNCTION = 'split'
    CATEGORY = 'MOSS/RGBA'

    def split(self, rgba):
        # ComfyUI mask convention: 1 = transparent, 0 = opaque.
        return (rgba[..., :3], 1.0 - rgba[..., 3])


NODE_CLASS_MAPPINGS = {'MossRGBAVAELoader': MossRGBAVAELoader, 'MossRGBASplit': MossRGBASplit}
NODE_DISPLAY_NAME_MAPPINGS = {'MossRGBAVAELoader': 'Load MOSS RGBA VAE',
                            'MossRGBASplit': 'Split RGBA Image'}
