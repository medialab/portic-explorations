Exploration des bases PORTIC et client pour faciliter (?) l'accès conjoint
===

# Lancer le lab

```
pip3 install -r requirements.txt
jupyter lab
```

Puis aller à : http://localhost:8888/lab

à voir plus en détail : https://github.com/medialab/toflit18_data/blob/master/base/bdd_centrale.csv.zip (données avec toutes les jointures)

# [WIP] procédure d'installation

```
pip install -r requirements.txt

pip install --upgrade notebook  # need jupyter_client >= 4.2 for sys-prefix below
jupyter nbextension install --sys-prefix --py vega  # not needed in notebook >= 5.3
jupyter nbextension enable --py --sys-prefix ipyleaflet  # can be skipped for notebook 5.3 and above
jupyter nbextension enable --py --sys-prefix ipysigma
```