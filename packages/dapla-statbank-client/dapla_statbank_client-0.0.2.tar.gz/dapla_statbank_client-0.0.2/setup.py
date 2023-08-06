# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statbank']

package_data = \
{'': ['*']}

install_requires = \
['autoflake>=1.7.6,<2.0.0',
 'bump2version>=1.0.1,<2.0.0',
 'dapla-toolbelt>=1.3.3,<2.0.0',
 'flake8-bugbear>=22.9.23,<23.0.0',
 'flake8-builtins>=2.0.0,<3.0.0',
 'flake8-comprehensions>=3.10.0,<4.0.0',
 'flake8-debugger>=4.1.2,<5.0.0',
 'flake8-eradicate>=1.4.0,<2.0.0',
 'flake8-logging-format>=0.8.1,<0.9.0',
 'flake8>=5.0.4,<6.0.0',
 'ipywidgets>=8.0.2,<9.0.0',
 'isort>=5.10.1,<6.0.0',
 'mypy>=0.982,<0.983',
 'pandas>=1.5.0,<2.0.0',
 'pep8-naming>=0.13.2,<0.14.0',
 'pre-commit>=2.20.0,<3.0.0',
 'pyjstat>=2.3.0,<3.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pyupgrade>=3.1.0,<4.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'dapla-statbank-client',
    'version': '0.0.2',
    'description': 'Handles data transfer Statbank <-> Dapla for Statistics Norway',
    'long_description': '# dapla-statbank-client\nUsed internally by SSB (Statistics Norway).\nValidates and transfers data from Dapla to Statbank.\nGets data from public and internal statbank.\n\n\n### Transferring\n```python\nfrom statbank import StatbankClient\nstat_client = StatbankClient(loaduser = "LASTEBRUKER")\n# Fill out password\nstat_client.transfer(df_06399, tabellid="06339")\n```\nThe simplest form of usage, is directly-transferring using the transfer-method under the client-class. If the statbanktable expects multiple "deltabeller", dataframes must be passed in a list, in the correct order.\n\n### Building datasets\nYou can validate the data using the validate-method, without starting a transfer, like this:\nValidation will happen by default on user-side, in Python, using the "UttrekksBeskrivelse" (filbeskrivelse).\nValidation happens on the number of tables, number of columns, code usage in categorical columns, code usage in "suppression-columns" (prikkekolonner), and on timeformats (both length and characters used).\n\n```python\nstat_client.validate(df_06339, tableid="06339")\n```\n\nYou can also look at the "filbeskrivelse" which is returned in its own local class: StatbankUttrekksBeskrivelse\n```python\ndescription_06339 = stat_client.get_description(tableid="06339")\nprint(description_06339)\n# Interesting attributes\ndescription_06339.deltabelltitler\ndescription_06339.variabler\ndescription_06339.kodelister\ndescription_06339.prikking\n```\n\n### Getting apidata\n\n```python\ndf_06339 = stat_client.apidata_all("06339", include_id=True)\n```\n`apidata_all`, does not need a specified query, it will build its own query, trying to get *all the data* from the table. This might be too much, resulting in an error.\n\nThe `include_id`-parameter is a bit *magical*, it gets both codes and value-columns for categorical columns, and tries to merge these next to each other, it also makes a check if the content is the same, then it will not include the content twice.\n\nIf you want to specify a query, to limit the response, use the method `apidata` instead.\\\nHere we are requesting an "internal table" which only people at SSB have access to, with a specified URL and query.\n```python\nquery = {\'query\': [{\'code\': \'Region\', \'selection\': {\'filter\': \'vs:Landet\', \'values\': [\'0\']}}, {\'code\': \'Alder\', \'selection\': {\'filter\': \'vs:AldGrupp19\', \'values\': [\'000\', \'001\', \'002\', \'003\', \'004\', \'005\', \'006\', \'007\', \'008\', \'009\', \'010\', \'011\', \'012\', \'013\', \'014\', \'015\', \'016\', \'017\', \'018\', \'019\', \'020\', \'021\', \'022\', \'023\', \'024\', \'025\', \'026\', \'027\', \'028\', \'029\', \'030\', \'031\', \'032\', \'033\', \'034\', \'035\', \'036\', \'037\', \'038\', \'039\', \'040\', \'041\', \'042\', \'043\', \'044\', \'045\', \'046\', \'047\', \'048\', \'049\', \'050\', \'051\', \'052\', \'053\', \'054\', \'055\', \'056\', \'057\', \'058\', \'059\', \'060\', \'061\', \'062\', \'063\', \'064\', \'065\', \'066\', \'067\', \'068\', \'069\', \'070\', \'071\', \'072\', \'073\', \'074\', \'075\', \'076\', \'077\', \'078\', \'079\', \'080\', \'081\', \'082\', \'083\', \'084\', \'085\', \'086\', \'087\', \'088\', \'089\', \'090\', \'091\', \'092\', \'093\', \'094\', \'095\', \'096\', \'097\', \'098\', \'099\', \'100\', \'101\', \'102\', \'103\', \'104\', \'105\', \'106\', \'107\', \'108\', \'109\', \'110\', \'111\', \'112\', \'113\', \'114\', \'115\', \'116\', \'117\', \'118\', \'119+\']}}, {\'code\': \'Statsbrgskap\', \'selection\': {\'filter\': \'vs:Statsborgerskap\', \'values\': [\'000\']}}, {\'code\': \'Tid\', \'selection\': {\'filter\': \'item\', \'values\': [\'2022\']}}], \'response\': {\'format\': \'json-stat2\'}}\n\ndf_folkemengde = stat_client.apidata("https://i.ssb.no/pxwebi/api/v0/no/prod_24v_intern/START/be/be01/folkemengde/Rd0002Aa",\n                                     query,\n                                     include_id = True\n                                    )\n```\n\n`apidata_rotate` is a thin wrapper around pivot_table. Stolen from: https://github.com/sehyoun/SSB_API_helper/blob/master/src/ssb_api_helper.py\n```python\ndf_folkemengde_rotert = stat_client.rotate(df_folkemengde, \'tidskolonne\', "verdikolonne")\n```\n\nTo import the apidata-functions outside the client (no need for password) do the imports like this:\n```python\nfrom statbank.apidata import apidata_all, apidata, apidata_rotate\n```\n\n\n### Batches\nFor the non-apidata-methods, there are "twin" batch-methods. \nFor .transfer there is .transfer_batch and so on.\nAlternatively you can just run the methods above multiple times...\n\nTo transfer many tables at the same time.\n```python\ntransfers = stat_client.transfer_batch({"06339": df_06399,\n                                        "05300": df_05300})\nprint(transfers["05300"])\n```\n\nTo validate many tables at the same time.\n```python\nstat_client.validate_batch({"06339": df_06399,\n                            "05300": df_05300})\n```\n\nTo get many descriptions at once send a list of tableids.\n```python\ndescriptions = stat_client.validate_batch(["06339","05300"])\nprint(descriptions["06339"])\n```\n\n### Saving and restoring Uttrekksbeskrivelser and Transfers as json\n\\*Might still be in development\n\nFrom `stat_client.transfer()` you will recieve a StatbankTransfer object, from `stat_client.get_description` a StatbankUttrekksBeskrivelse-object. These can be serialized and saved to disk, and later be restored.\n\n```python\nfilbesk_06339 = stat_client.get_description("06339")\nfilbesk_06339.to_json("path.json")\n# Later the file can be restored with\nfilbesk_06339_new = stat_client.read_description_json("path.json")\n```\n\nSome deeper data-structures, like the dataframes in the transfer will not be serialized and stored with the transfer-object in its json.\n\n---\n### Version history\n\n- 0.0.1 Client, transfer, description, apidata. Quite a lot of work done already. Pre-alpha.\n',
    'author': 'Statistics Norway',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
