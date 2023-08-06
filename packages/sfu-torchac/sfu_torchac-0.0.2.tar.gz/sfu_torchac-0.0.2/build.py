from typing import Dict, Any

from torch.utils.cpp_extension import BuildExtension, CppExtension


def build(setup_kwargs: Dict[str, Any]) -> None:
    setup_kwargs.update({
        'ext_modules': [
            CppExtension(
                name='torchac_backend_cpu',
                sources=['sfu_torchac/backend/torchac.cpp'],
            )
        ],
        'cmdclass': {'build_ext': BuildExtension},
    })
