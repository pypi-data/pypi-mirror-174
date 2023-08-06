# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myoquant']

package_data = \
{'': ['*']}

install_requires = \
['cellpose>=2.1.0,<3.0.0',
 'csbdeep>=0.7.2,<0.8.0',
 'imageio>=2.21.1,<3.0.0',
 'pandas>=1.4.3,<2.0.0',
 'rich',
 'scikit-image>=0.19.3,<0.20.0',
 'stardist>=0.8.3,<0.9.0',
 'tensorflow>=2.9.1,<3.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['myoquant = myoquant.__main__:app']}

setup_kwargs = {
    'name': 'myoquant',
    'version': '0.1.5',
    'description': 'MyoQuant🔬: a CLI tool to automatically quantify pathological features in muscle fiber histology images.',
    'long_description': '![Twitter Follow](https://img.shields.io/twitter/follow/corentinm_py?style=social) ![Demo Version](https://img.shields.io/badge/Demo-https%3A%2F%2Flbgi.fr%2FMyoQuant%2F-9cf) ![PyPi](https://img.shields.io/badge/PyPi-https%3A%2F%2Fpypi.org%2Fproject%2Fmyoquant%2F-blueviolet) ![Pypi verison](https://img.shields.io/pypi/v/myoquant) ![PyPi Python Version](https://img.shields.io/pypi/pyversions/myoquant) ![PyPi Format](https://img.shields.io/pypi/format/myoquant) ![GitHub last commit](https://img.shields.io/github/last-commit/lambda-science/MyoQuant) ![GitHub](https://img.shields.io/github/license/lambda-science/MyoQuant) \n\n# MyoQuant🔬: a tool to automatically quantify pathological features in muscle fiber histology images\n\n<p align="center">\n  <img src="https://i.imgur.com/mzALgZL.png" alt="MyoQuant Banner" style="border-radius: 25px;" />\n</p>\n\nMyoQuant🔬 is a command-line tool to automatically quantify pathological features in muscle fiber histology images.  \nIt is built using CellPose, Stardist, custom neural-network models and image analysis techniques to automatically analyze myopathy histology images. Currently MyoQuant is capable of quantifying centralization of nuclei in muscle fiber with HE staining and anomaly in the mitochondria distribution in muscle fibers with SDH staining.  \n\nAn online demo with a web interface is available at [https://lbgi.fr/MyoQuant/](https://lbgi.fr/MyoQuant/). This project is free and open-source under the AGPL license, feel free to fork and contribute to the development. \n\n#### *Warning: This tool is still in early phases and active development.*\n\n## How to install\n\n### Installing from PyPi (Preferred)\n**MyoQuant package is officially available on PyPi (pip) repository. [https://pypi.org/project/myoquant/](https://pypi.org/project/myoquant/) ![Pypi verison](https://img.shields.io/pypi/v/myoquant)** \n\nUsing pip, you can simply install MyoQuant in a python environment with a simple: `pip install myoquant`\n\n### Installing from sources (Developers)\n\n1. Clone this repository using `git clone https://github.com/lambda-science/MyoQuant.git`\n2. Create a virtual environment by using `python -m venv .venv`\n3. Activate the venv by using `source .venv/bin/activate`\n4. Install MyoQuant by using `pip install -e .`\n\n## How to Use\n\nTo use the command-line tool, first activate your venv in which MyoQuant is installed: `source .venv/bin/activate`  \nThen you can perform SDH or HE analysis. You can use the command `myoquant --help` to list available commands.\n\n- **For SDH Image Analysis** the command is:  \n  `myoquant sdh-analysis IMAGE_PATH`  \n  Don\'t forget to run `myoquant sdh-analysis --help` for information about options.\n- **For HE Image Analysis** the command is:  \n  `myoquant he-analysis IMAGE_PATH`  \n   Don\'t forget to run `myoquant he-analysis --help` for information about options.\n\n_If you\'re running into an issue such as `myoquant: command not found` please check if you activated your virtual environment with the package installed. And also you can try to run it with the full command: `python -m myoquant sdh-analysis --help`_\n\n## Contact\nCreator and Maintainer: [**Corentin Meyer**, 3rd year PhD Student in the CSTB Team, ICube — CNRS — Unistra](https://cmeyer.fr)  <corentin.meyer@etu.unistra.fr>\n\n## Citing MyoQuant🔬\n[placeholder]  \n\n## Examples\n\nFor HE Staining analysis, you can download this sample image: [HERE](https://www.lbgi.fr/~meyer/SDH_models/sample_he.jpg)  \nFor SDH Staining analysis, you can download this sample image: [HERE](https://www.lbgi.fr/~meyer/SDH_models/sample_sdh.jpg)\n\n1. Example of successful SDH analysis with: `myoquant sdh-analysis sample_sdh.jpg`\n\n![image](https://user-images.githubusercontent.com/20109584/198278737-24d69f61-058e-4a41-a463-68900a0dcbb6.png)\n\n2. Example of successful HE analysis with: `myoquant he-analysis sample_he.jpg`\n\n![image](https://user-images.githubusercontent.com/20109584/198280366-1cb424f5-50af-45f9-99d1-34e191fb2e20.png)\n\n## Advanced information\n\nFor the SDH Analysis our custom model will be downloaded and placed inside the myoquant package directory. You can also download it manually here: [https://lbgi.fr/~meyer/SDH_models/model.h5](https://lbgi.fr/~meyer/SDH_models/model.h5) and then you can place it in the directory of your choice and provide the path to the model file using:  \n`myoquant sdh-analysis IMAGE_PATH --model_path /path/to/model.h5`\n\n## Partners\n\n<p align="center">\n  <img src="https://i.imgur.com/m5OGthE.png" alt="Partner Banner" style="border-radius: 25px;" />\n</p>\n\nMyoQuant is born within the collaboration between the [CSTB Team @ ICube](https://cstb.icube.unistra.fr/en/index.php/Home) led by Julie D. Thompson, the [Morphological Unit of the Institute of Myology of Paris](https://www.institut-myologie.org/en/recherche-2/neuromuscular-investigation-center/morphological-unit/) led by Teresinha Evangelista, the [imagery platform MyoImage of Center of Research in Myology](https://recherche-myologie.fr/technologies/myoimage/) led by Bruno Cadot, [the photonic microscopy platform of the IGMBC](https://www.igbmc.fr/en/plateformes-technologiques/photonic-microscopy) led by Bertrand Vernay and the [Pathophysiology of neuromuscular diseases team @ IGBMC](https://www.igbmc.fr/en/igbmc/a-propos-de-ligbmc/directory/jocelyn-laporte) led by Jocelyn Laporte\n',
    'author': 'Corentin Meyer',
    'author_email': 'corentin.meyer@etu.unistra.fr',
    'maintainer': 'Corentin Meyer',
    'maintainer_email': 'corentin.meyer@etu.unistra.fr',
    'url': 'https://lbgi.fr/MyoQuant/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
