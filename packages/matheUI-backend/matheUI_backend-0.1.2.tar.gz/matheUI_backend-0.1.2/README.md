# MatheUI-2.0
little funny games

## set-up package

clone the package to your local machine. e.g. to your current working directory:

```
git clone https://github.com/Priapos1004/MatheUI-2.0
```

go into the 'MatheUI-2.0' folder

```
cd MatheUI-2.0/
```

install the package to your activated virtual environment

```
pip install -e .
```

Now you can use the package. e.g.:

```
from matheUI.backend import AgentUndercover

auc = AgentUndercover()
auc.generate_round(player_number=7, spy_number=2, places_groups="standard")
```

--> in the '[examples](examples)' folder you can find notebooks with code snippets that explain the usage of the package
