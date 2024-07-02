# Python-Code-Helpers

A general library mostly centred around boilerplate logging nonsense and interacting with Oracle databases.

```python
import bis_code_helpers

# Set up logging with sensible formatting
logger = bis_code_helpers.setup_logging(...)

# Create a sqlalchemy engine with oracledb backend
engine = bis_code_helpers.create_engine(...)

# Get something from a DB
result_dataframe = bis_code_helpers.execute_select_query_on_db(...)

# Do something to a DB
bis_code_helpers.execute_action_query_on_db(...)

# and more...
```

> Requires the ORACLE_HOME environment variable to be set to a valid 64bit client tools install.

## Installation
There is no prebuilt package in PyPI, install straight from GitHub
### Latest commit
`pip install --upgrade git+https://github.com/Wits-Business-Intelligence-Services/Python-Code-Helpers.git`

### With release version
`pip install --upgrade git+https://github.com/Wits-Business-Intelligence-Services/Python-Code-Helpers.git@1.7.0`

### requirements.txt
`bis_code_helpers @ git+https://github.com/Wits-Business-Intelligence-Services/Python-Code-Helpers.git`