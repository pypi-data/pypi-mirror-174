# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snprimer']

package_data = \
{'': ['*']}

install_requires = \
['bump2version>=1.0.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'gget>=0.3.11,<0.4.0',
 'myvariant>=1.0.0,<2.0.0',
 'pre-commit>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'snprimer',
    'version': '0.1.1',
    'description': 'Small python library to search snp in primer by position or by sequence.',
    'long_description': '# SNPrimer\n\nSmall python library to search snp in primer by position or by sequence.\n\n## Installation\n\n`pip install snprimer``\n\n## Usage\n\n### 🎯 By position 🎯\n\n```python\nfrom snprimer import PositionRange\n\nposition = PositionRange("chr8",19818430, 19818440)\nprint(position)\n# PositionRange(chr=\'chr8\', start=19818430, end=19818440, strand=None, snp=[SNP(id=\'chr8:g.19818436C>G\', rsid=\'rs316\', vaf=0.15300000000000002), SNP(id=\'chr8:g.19818436C>T\', rsid=\'rs316\', vaf=0.15300000000000002)])\nfor snp in position.get_snp(max_vaf=0.05):\n    print(snp)\n#SNP(id=\'chr8:g.19818436C>G\', rsid=\'rs316\', vaf=0.15300000000000002)\n#SNP(id=\'chr8:g.19818436C>T\', rsid=\'rs316\', vaf=0.15300000000000002)\n```\n\n### 🔤 By sequence 🔤\n```python\nfrom snprimer import Primer\n\nprimer = Primer("CACACAGATCAGAGGGCCAAC")\nprint(primer)\n#Primer(seq=\'CACACAGATCAGAGGGCCAAC\', position_ranges=[PositionRange(chr=\'chr1\', start=26774827, end=26774847, strand=\'+\', snp=[SNP(id=\'chr1:g.26774827G>A\', rsid=\'rs2075289787\', vaf=0), SNP(id=\'chr1:g.26774830A>G\', rsid=\'rs986550282\', vaf=0.0), SNP(id=\'chr1:g.26774842T>C\', rsid=\'rs1440652363\', vaf=0.0)])])\nprimer.infos(max_vaf=0)\n#CACACAGATCAGAGGGCCAAC has snp with vaf > 0 : [SNP(id=\'chr1:g.26774827G>A\', rsid=\'rs2075289787\', vaf=0), SNP(id=\'chr1:g.26774830A>G\', rsid=\'rs986550282\', vaf=0.0), SNP(id=\'chr1:g.26774842T>C\', rsid=\'rs1440652363\', vaf=0.0)]\n```\n',
    'author': 'Benoitdw',
    'author_email': 'bw@oncodna.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Benoitdw/SNPrimer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
