# panther-utils
Panther SDK utilities repo

## Match Filters

The `deep_exists` filter allows you to filter events based on a field match. Use `deep_not_exists` for the inverse.

```python
from panther_sdk import detection
from panther_utils import match_filters

# example: alert if a security log has a warning message
detection.Rule(
    rule_id="My.Custom.Rule",
    log_types=["Security.Logs"],
    severity=detection.SeverityMedium,
    filters=[
        match_filters.deep_exists(path="warning.message"),
    ]
)
```


The `deep_equal` filter allows you to filter events based on a field match. Use `deep_not_equal` for the inverse.

```python
from panther_sdk import detection
from panther_utils import match_filters

# example: match server logs with insecure POST requests
detection.Rule(
    rule_id="My.Custom.Rule",
    log_types=["ServerLogs.HTTP"],
    filters=[
        match_filters.deep_equal(path="request.method", value="POST"),
        match_filters.deep_equal(path="request.use_ssl", value=False),
    ]
)
```

The `deep_equal_pattern` filter allows you to filter events based on a pattern. Use `deep_not_equal_pattern` for the inverse.

```python
from panther_sdk import detection
from panther_utils import match_filters

# example: match server logs with /api/ in their path
detection.Rule(
    rule_id="My.Custom.Rule",
    log_types=["ServerLogs.HTTP"],
    severity=detection.SeverityMedium,
    filters=[
        match_filters.deep_equal_pattern(path="request.url", pattern=".+\/api\/.+"),
    ]
)
```

The `deep_in` filter allows you to filter events based on a pattern. Use `deep_not_in` for the inverse.

```python
from panther_sdk import detection
from panther_utils import match_filters

# example: match server logs with POST or PUT requests
detection.Rule(
    rule_id="My.Custom.Rule",
    log_types=["ServerLogs.HTTP"],
    severity=detection.SeverityMedium,
    filters=[
        match_filters.deep_in(path="request.method", value=["POST", "PUT"]),
    ]
)
```

#### All available filters in `match_filters`
Listed below are all the available filters in the `match_filters` module alongside the underlying comparison performed. 

| filter                       | performs comparison via:                 |
|------------------------------|------------------------------------------|
| `deep_exists`                | `actual is None`                         |
| `deep_not_exists`            | `actual is not None`                     |
| `deep_equal`                 | `actual == value`                        |
| `deep_not_equal`             | `actual != value`                        |
| `deep_equal_pattern`         | `re.compile(pattern).search(actual)`     |
| `deep_not_equal_pattern`     | `not re.compile(pattern).search(actual)` |
| `deep_in`                    | `actual in value`                        |
| `deep_not_in`                | `actual not in value`                    |
| `deep_less_than`             | `<`                                      |
| `deep_less_than_or_equal`    | `<=`                                     |
| `deep_greater_than`          | `>`                                      |
| `deep_greater_than_or_equal` | `>=`                                     |
| `deep_between`               | `val_min <= actual <= val_max`           |
| `deep_between_exclusive`     | `val_min < actual < val_max`             |

## Network Filters
The `ips_in_cidr` filter allows you to filter events based whether IPs are in a CIDR range. The optional `path` argument can target a dot-separated path to a single IP string or a list of IP strings. The `path` argument defaults to the Panther field `p_any_ip_addresses`. This filter uses the python [ipaddress](https://docs.python.org/3.9/library/ipaddress.html#) module to perform the comparison.

```python
from panther_sdk import detection
from panther_utils import network_filters

# example: match server logs coming from 10.x.x.x
detection.Rule(
    rule_id="My.Custom.Rule",
    log_types=["ServerLogs.HTTP"],
    filters=[
        network_filters.ips_in_cidr(cidr = "10.0.0.0/8"), # by default, source IPs from p_any_ip_addresses
    ]
)

# example: match server logs coming from 192.168.x.x
detection.Rule(
    rule_id="Internal.Logs",
    log_types=["Custom.InternalLogs"],
    filters=[
        network_filters.ips_in_cidr(cidr = "192.168.0.0/16", path="custom.path.to.ips"), 
    ]
)
```
