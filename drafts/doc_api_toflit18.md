# Documentation de l'API de toflit18

## API des directions

#### `GET http://toflit18.medialab.sciences-po.fr/api/directions/`

##### Summary

##### Query params

##### Body/request payload

##### Response

Exemple pour `http://toflit18.medialab.sciences-po.fr/api/directions/` :

```js
{
    status: 'ok',
    code: 200,
    result: [
        {
            id: 'Amiens',
            name: 'Amiens'
        },
        // ...
    ]
}
```


## API des types de sources

#### `GET http://toflit18.medialab.sciences-po.fr/api/source_types/`

##### Summary

Retourne les types de sources de données disponibles.

##### Query params

##### Body/request payload

##### Response

La réponse est un tableau listant toutes les sources disponibles.

Exemple pour `http://toflit18.medialab.sciences-po.fr/api/source_types` :


```json
{
  "status": "ok",
  "code": 200,
  "result": [
    "1792-both semester",
    "1792-first semester",
    "Compagnie des Indes",
    "Local",
    "Local best guess",
    "National best guess",
    "National partenaires manquants",
    "National toutes directions partenaires manquants",
    "National toutes directions sans produits",
    "National toutes directions tous partenaires",
    "Objet Général",
    "Résumé",
    "Tableau Général",
    "Tableau des quantités"
  ]
}
```


## API des classifications

Source : https://github.com/medialab/toflit18/blob/master/api/classification/viz.js

#### `GET http://toflit18.medialab.sciences-po.fr/api/classification/`

##### Summary

Retourne les différents types de classification disponibles.

##### Query params

##### Body/request payload

##### Response

La réponse est un objet contenant une propriété "product" et une propriété "partner".

Chaque propriété est structurée en arbre, présentant un ensemble de propriétés, et une propriété children donnant accès aux sous-classifications disponibles.

Exemple pour `http://toflit18.medialab.sciences-po.fr/api/classification/` :


```json
{
  "status": "ok",
  "code": 200,
  "result": {
    "product": {
      "name": "Source",
      "description": "the product names as transcribed from archive volumes",
      "model": "product",
      "source": true,
      "id": "product_source",
      "slug": "source",
      "author": "TOFLIT 18",
      "parent": null,
      "groupsCount": 61795,
      "itemsCount": null,
      "unclassifiedItemsCount": 1,
      "completion": 0,
      "children": [...]
    },
    "partner": {
      "name": "Source",
      "description": "the partner names as transcribed from archive volumes",
      "model": "partner",
      "source": true,
      "id": "partner_source",
      "slug": "source",
      "author": "TOFLIT 18",
      "parent": null,
      "groupsCount": 1003,
      "itemsCount": null,
      "unclassifiedItemsCount": 1,
      "completion": 0,
      "children": [...]
    }
  }
}
```

#### `GET http://toflit18.medialab.sciences-po.fr/api/classification/:id/groups/`

##### Summary

Retourne les groupes associés à une classification en particulier

##### Query params

##### Body/request payload

##### Response

Exemple pour `http://toflit18.medialab.sciences-po.fr/api/classification/partner_source/groups/` :

```json
{
  "status": "ok",
  "code": 200,
  "result": [
    {
      "id": "**~partner_source",
      "name": "**"
    },
    {
      "id": "***~partner_source",
      "name": "***"
    },
    {
      "id": "3_evêchés~partner_source",
      "name": "3 evêchés"
    },
    {
      "id": "3_évéchés~partner_source",
      "name": "3 évéchés"
    },
    // ...
  ]
}
```

#### `GET http://toflit18.medialab.sciences-po.fr/api/classification/:id/search`

##### Summary

Renvoie les groupes de valeurs pour une classification donnée.

##### Query params

##### Body/request payload

##### Response

Exemple pour `http://toflit18.medialab.sciences-po.fr/api/classification/product_simplification/search` :

```json
{
  "status": "ok",
  "code": 200,
  "result": [
    {
      "name": "grains froment",
      "id": "grains_froment~product_simplification",
      "items": [
        {
          "name": "blé de froment"
        },
        {
          "name": "blé froment"
        },
        {
          "name": "blé millet"
        },
        {
          "name": "froment"
        },
        {
          "name": "froment grains"
        }
      ],
      "nbItems": 23
    },
    // ...
  ]
}
```


#### `GET http://toflit18.medialab.sciences-po.fr/api/classification/:id/export.:ext`


##### Summary

Export en csv ou json des données d'une classification.

:ext peut être 'json' ou 'csv'

##### Query params

##### Body/request payload

##### Response

/


#### `POST http://toflit18.medialab.sciences-po.fr/api/classification/:id/patch/review`

Pas pertinent pour l'exploration.


#### `POST http://toflit18.medialab.sciences-po.fr/api/classification/:id/patch/commit`

Pas pertinent pour l'exploration.

## API des vizs

Source : https://github.com/medialab/toflit18/blob/master/api/controllers/viz.js

### `POST http://toflit18.medialab.sciences-po.fr/api/viz/flows_per_year/:type`

##### Summary

##### Query params

##### Body/request payload

##### Response


### `POST http://toflit18.medialab.sciences-po.fr/api/line`

##### Summary

Retourne des données quantitatives organisées temporellement concernant les flux.

##### Query params

##### Body/request payload

Contient un ensemble de filtres.

Exemple :

```json
{
	"color": "#C14F4C",
	"sourceType": "National best guess"
}
```

##### Response

Exemple :

```json
{
	"status": "ok",
	"code": 200,
	"result": [
		{
			"year": 1750,
			"fs.sourceType": "National toutes directions tous partenaires",
			"count": 12083,
			"value": 388546058.9380682,
			"kg": 586272379.3366972,
			"nbr": 0,
			"litre": 33135823.7414883,
			"nb_direction": [
				"Flandre",
				"Nantes",
				"La Rochelle",
				"Bordeaux",
				"Marseille",
				"Rennes",
				"Rouen",
				"Montpellier",
				"Narbonne",
				"Amiens",
				"Châlons",
				"Bayonne",
				"Lyon",
				"Saint-Quentin",
				"Caen",
				"Bourgogne",
				"Langres",
				"Charleville"
			],
			"value_share": 12080,
			"kg_share": 7690,
			"litre_share": 283,
			"nbr_share": 0
		},
		{
			"year": 1754,
			"fs.sourceType": "Objet Général",
			"count": 7492,
			"value": 512873416.4432291,
			"kg": 0,
			"nbr": 0,
			"litre": 0,
			"nb_direction": [],
			"value_share": 7492,
			"kg_share": 0,
			"litre_share": 0,
			"nbr_share": 0
		},
        // ...
	]
}
```


### `POST http://toflit18.medialab.sciences-po.fr/api/viz/network/:partner_classification`

##### Summary

Retourne des données de flux aggrégé entre deux entités géographiques.

Valeurs possibles de :id : ['partner_source', ...] (correspond aux classifications de partenaires)

##### Query params

##### Body/request payload

Le payload contient des filtres. Exemple (à documenter) :

```json
{
	"dateMax": "1776",
	"dateMin": "1721",
	"kind": "import",
	"partnerClassification": null,
	"product": [
		{
			"id": "???_blanc~product_orthographic",
			"name": "??? blanc",
			"value": "???_blanc~product_orthographic"
		}
	],
	"productClassification": "product_orthographic",
	"sourceType": "1792-both semester"
}
```

##### Response

Exemple :

```json
{
	"status": "ok",
	"code": 200,
	"result": [
		{
			"partner": "Outre-mers",
			"direction": "Bordeaux",
			"count": 233,
			"value": 22584986.21661377
		},
		{
			"partner": "Outre-mers",
			"direction": "La Rochelle",
			"count": 402,
			"value": 14480602.406881928
		},
		// ...
	]
}
```

### `POST http://toflit18.medialab.sciences-po.fr/api/terms/:id`

##### Summary

##### Query params

##### Body/request payload

##### Response

