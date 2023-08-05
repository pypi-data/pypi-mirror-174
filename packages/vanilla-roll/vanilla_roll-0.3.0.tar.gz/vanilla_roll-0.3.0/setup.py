# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vanilla_roll',
 'vanilla_roll.array_api',
 'vanilla_roll.array_api_extra',
 'vanilla_roll.array_api_image',
 'vanilla_roll.geometry',
 'vanilla_roll.io',
 'vanilla_roll.rendering']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.0,<2.0.0']

extras_require = \
{'cupy': ['cupy>=11.2.0,<12.0.0'],
 'dicom': ['pydicom>=2.3.0,<3.0.0'],
 'mha': ['metaimageio>=1.0.0,<2.0.0'],
 'nifti': ['nibabel>=4.0.0,<5.0.0'],
 'torch': ['torch>=1.8.0,<2.0.0']}

setup_kwargs = {
    'name': 'vanilla-roll',
    'version': '0.3.0',
    'description': 'A simple array based volume renderer',
    'long_description': '# vanilla-roll\n[![Build][build-shiled]][build-url]\n[![Version][version-shield]][version-url]\n[![Downloads][download-shield]][download-url]\n[![Contributors][contributors-shield]][contributors-url]\n[![Issues][issues-shield]][issues-url]\n[![Codecov][codecov-shield]][codecov-url]\n[![Apache License 2.0 License][license-shield]][license-url]\n\nvanilla-roll is volume renderer using array-api as backend.\n\n## Why vanilla-roll ?\n[VTK](https://vtk.org/) is one of the most excellent volume renderers in the world.\nIt has good performance and many features.\nBut I think that the installation process is not easy.\nSo vanilla-roll is motivated to solve this problem.\n\n## Features\n- [ ] IO\n  - [x] MRA\n  - [x] NIFTI\n  - [x] DICOM\n  - [ ] NRRD\n- [ ] Rendering Algorithm\n  - [x] Sampling\n  - [x] Shear-Warp\n  - [ ] Raycast\n- [ ] Rendering Mode\n  - [x] MIP\n  - [x] MinP\n  - [x] Average\n  - [ ] VolumeRendering\n      - [x] Ambient\n      - [ ] Shading\n- [ ] Backend\n  - [x] numpy\n  - [x] pytorch\n  - [x] cupy\n  - [ ] jax\n  - [ ] numbda\n\n\n## Installation\n```bash\n$ pip install vanilla-roll\n```\nvanilla-roll supports following extras\n\n* torch\n* dicom\n* mha\n* nifti\n\n\n## Example\nCode\n\n```python\nimport urllib.request\nfrom pathlib import Path\nfrom tempfile import TemporaryDirectory\n\nimport numpy as np\nimport skimage.io\n\nimport vanilla_roll as vr\n\n# from A high-resolution 7-Tesla fMRI dataset from complex natural stimulation with an audio movie\n# https://www.openfmri.org/dataset/ds000113/\nMRA_FILE_URL = "https://s3.amazonaws.com/openneuro/ds000113/ds000113_unrevisioned/uncompressed/sub003/angio/angio001.nii.gz"  # noqa: E501\n\n\ndef fetch_mra_volume() -> vr.volume.Volume:\n    with TemporaryDirectory() as tmpdir:\n        mra_file = Path(tmpdir) / "mra.nii.gz"\n        urllib.request.urlretrieve(MRA_FILE_URL, mra_file)\n        return vr.io.read_nifti(mra_file)\n\n\ndef save_result(ret: vr.rendering.types.RenderingResult, path: str):\n    img_array = vr.rendering.convert_image_to_array(ret.image)\n    skimage.io.imsave(path, np.from_dlpack(img_array))  # type: ignore\n\n\ndef main():\n    volume = fetch_mra_volume()\n    ret = vr.render(volume, mode=vr.rendering.mode.MIP())\n    save_result(ret, f"result.png")\n\n\nif __name__ == "__main__":\n    main()\n```\n\nOutput\n\n![output](https://raw.githubusercontent.com/ar90n/vanilla-roll/assets/images/simple.png)\n\nIf you need more exmplaes, please check the [examples](https://github.com/ar90n/vanilla-roll/tree/main/examples).\n\n## For development\n### Install Poery plugins\n```bash\n$ poetry self add \'poethepoet[poetry_plugin]\'\n```\n\n### Install all extra packages\n```bash\n$ poetry poe install-all-extras\n```\n\n### Run tests\n```bash\n$ poetry poe test\n```\n\n### Run linter and formatter\n```bash\n$ poetry poe check\n```\n\n## See Also\n\n## License\n[Apache-2.0](https://github.com/ar90n/vanilla-roll/blob/main/LICENSE)\n\n[download-shield]: https://img.shields.io/pypi/dm/vanilla-roll?style=flat\n[download-url]: https://pypi.org/project/vanilla-roll/\n[version-shield]: https://img.shields.io/pypi/v/vanilla-roll?style=flat\n[version-url]: https://pypi.org/project/vanilla-roll/\n[build-shiled]: https://img.shields.io/github/workflow/status/ar90n/vanilla-roll/CI%20testing/main\n[build-url]: https://github.com/ar90n/vanilla-roll/actions/workflows/ci-testing.yml\n[contributors-shield]: https://img.shields.io/github/contributors/ar90n/vanilla-roll.svg?style=flat\n[contributors-url]: https://github.com/ar90n/vanilla-roll/graphs/contributors\n[issues-shield]: https://img.shields.io/github/issues/ar90n/vanilla-roll.svg?style=flat\n[issues-url]: https://github.com/ar90n/vanilla-roll/issues\n[license-shield]: https://img.shields.io/github/license/ar90n/vanilla-roll.svg?style=flat\n[license-url]: https://github.com/ar90n/vanilla-roll/blob/main/LICENSE\n[codecov-shield]: https://codecov.io/gh/ar90n/vanilla-roll/branch/main/graph/badge.svg?token=8GKU96ODLY\n[codecov-url]: https://codecov.io/gh/ar90n/vanilla-roll\n',
    'author': 'Masahiro Wada',
    'author_email': 'argon.argon.argon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ar90n/vanilla_roll',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
