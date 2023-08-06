# dapla-statbank-client
Used internally by SSB (Statistics Norway).
Validates and transfers data from Dapla to Statbank.
Gets data from public and internal statbank.


### Transferring
```python
from statbank import StatbankClient
stat_client = StatbankClient(loaduser = "LASTEBRUKER")
# Fill out password
stat_client.transfer(df_06399, tabellid="06339")
```
The simplest form of usage, is directly-transferring using the transfer-method under the client-class. If the statbanktable expects multiple "deltabeller", dataframes must be passed in a list, in the correct order.

### Building datasets
You can validate the data using the validate-method, without starting a transfer, like this:
Validation will happen by default on user-side, in Python, using the "UttrekksBeskrivelse" (filbeskrivelse).
Validation happens on the number of tables, number of columns, code usage in categorical columns, code usage in "suppression-columns" (prikkekolonner), and on timeformats (both length and characters used).

```python
stat_client.validate(df_06339, tableid="06339")
```

You can also look at the "filbeskrivelse" which is returned in its own local class: StatbankUttrekksBeskrivelse
```python
description_06339 = stat_client.get_description(tableid="06339")
print(description_06339)
# Interesting attributes
description_06339.deltabelltitler
description_06339.variabler
description_06339.kodelister
description_06339.prikking
```

### Getting apidata

```python
df_06339 = stat_client.apidata_all("06339", include_id=True)
```
`apidata_all`, does not need a specified query, it will build its own query, trying to get *all the data* from the table. This might be too much, resulting in an error.

The `include_id`-parameter is a bit *magical*, it gets both codes and value-columns for categorical columns, and tries to merge these next to each other, it also makes a check if the content is the same, then it will not include the content twice.

If you want to specify a query, to limit the response, use the method `apidata` instead.\
Here we are requesting an "internal table" which only people at SSB have access to, with a specified URL and query.
```python
query = {'query': [{'code': 'Region', 'selection': {'filter': 'vs:Landet', 'values': ['0']}}, {'code': 'Alder', 'selection': {'filter': 'vs:AldGrupp19', 'values': ['000', '001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028', '029', '030', '031', '032', '033', '034', '035', '036', '037', '038', '039', '040', '041', '042', '043', '044', '045', '046', '047', '048', '049', '050', '051', '052', '053', '054', '055', '056', '057', '058', '059', '060', '061', '062', '063', '064', '065', '066', '067', '068', '069', '070', '071', '072', '073', '074', '075', '076', '077', '078', '079', '080', '081', '082', '083', '084', '085', '086', '087', '088', '089', '090', '091', '092', '093', '094', '095', '096', '097', '098', '099', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119+']}}, {'code': 'Statsbrgskap', 'selection': {'filter': 'vs:Statsborgerskap', 'values': ['000']}}, {'code': 'Tid', 'selection': {'filter': 'item', 'values': ['2022']}}], 'response': {'format': 'json-stat2'}}

df_folkemengde = stat_client.apidata("https://i.ssb.no/pxwebi/api/v0/no/prod_24v_intern/START/be/be01/folkemengde/Rd0002Aa",
                                     query,
                                     include_id = True
                                    )
```

`apidata_rotate` is a thin wrapper around pivot_table. Stolen from: https://github.com/sehyoun/SSB_API_helper/blob/master/src/ssb_api_helper.py
```python
df_folkemengde_rotert = stat_client.rotate(df_folkemengde, 'tidskolonne', "verdikolonne")
```

To import the apidata-functions outside the client (no need for password) do the imports like this:
```python
from statbank.apidata import apidata_all, apidata, apidata_rotate
```


### Batches
For the non-apidata-methods, there are "twin" batch-methods. 
For .transfer there is .transfer_batch and so on.
Alternatively you can just run the methods above multiple times...

To transfer many tables at the same time.
```python
transfers = stat_client.transfer_batch({"06339": df_06399,
                                        "05300": df_05300})
print(transfers["05300"])
```

To validate many tables at the same time.
```python
stat_client.validate_batch({"06339": df_06399,
                            "05300": df_05300})
```

To get many descriptions at once send a list of tableids.
```python
descriptions = stat_client.validate_batch(["06339","05300"])
print(descriptions["06339"])
```

### Saving and restoring Uttrekksbeskrivelser and Transfers as json
\*Might still be in development

From `stat_client.transfer()` you will recieve a StatbankTransfer object, from `stat_client.get_description` a StatbankUttrekksBeskrivelse-object. These can be serialized and saved to disk, and later be restored.

```python
filbesk_06339 = stat_client.get_description("06339")
filbesk_06339.to_json("path.json")
# Later the file can be restored with
filbesk_06339_new = stat_client.read_description_json("path.json")
```

Some deeper data-structures, like the dataframes in the transfer will not be serialized and stored with the transfer-object in its json.

---
### Version history

- 0.0.1 Client, transfer, description, apidata. Quite a lot of work done already. Pre-alpha.
