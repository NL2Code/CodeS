import warnings

from .base_visualizer_client import MeshCatVisualizerBase

__version__ = "0.6.0"

try:
    import sapien.core as sapien

    from .sapien_visualizer_client import (
        bind_visualizer_to_sapien_scene,
        create_sapien_visualizer,
        get_visualizer,
    )
except ImportError as e:
    warnings.warn(str(e))
    warnings.warn(
        f"\nNo Sapien python library installed. Disable Sapien Visualizer.\n "
        f"If you want to Sapien Visualizer, please consider install it via: pip3 install sapien"
    )

try:
    from isaacgym import gymapi

    from .isaac_visualizer_client import (
        bind_visualizer_to_gym,
        create_isaac_visualizer,
        set_gpu_pipeline,
    )
except ImportError as e:
    warnings.warn(str(e))
    warnings.warn(
        f"\nNo isaacgym python library installed. Disable IsaacGym Visualizer.\n"
        f"If you want to IsaacGym Visualizer, please consider install it via the following URL: "
        f"https://developer.nvidia.com/isaac-gym"
    )
