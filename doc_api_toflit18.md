# Documentation de l'API de toflit18

## API des directions

#### `GET http://toflit18.medialab.sciences-po.fr/api/directions/`

##### Summary

##### Query params

##### Body/request payload

##### Response

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

##### Query params

##### Body/request payload

##### Response


## API des classifications

Source : https://github.com/medialab/toflit18/blob/master/api/classification/viz.js

#### `GET http://toflit18.medialab.sciences-po.fr/api/classification/`

##### Summary

##### Query params

##### Body/request payload

##### Response

#### `GET http://toflit18.medialab.sciences-po.fr/api/classification/:id/groups/`

##### Summary

##### Query params

##### Body/request payload

##### Response

#### `GET http://toflit18.medialab.sciences-po.fr/api/classification/group/:id`

##### Summary

##### Query params

##### Body/request payload

##### Response

#### `GET http://toflit18.medialab.sciences-po.fr/api/classification/:id/search`

##### Summary

##### Query params

##### Body/request payload

##### Response


#### `GET http://toflit18.medialab.sciences-po.fr/api/classification/:id/export.:ext`

##### Summary

##### Query params

##### Body/request payload

##### Response


#### `POST http://toflit18.medialab.sciences-po.fr/api/classification/:id/patch/review`

##### Summary

##### Query params

##### Body/request payload

##### Response


#### `POST http://toflit18.medialab.sciences-po.fr/api/classification/:id/patch/commit`

##### Summary

##### Query params

##### Body/request payload

##### Response


## API des vizs

Source : https://github.com/medialab/toflit18/blob/master/api/controllers/viz.js

### `POST http://toflit18.medialab.sciences-po.fr/api/viz/flows_per_year/:type`

##### Summary

##### Query params

##### Body/request payload

##### Response


### `POST http://toflit18.medialab.sciences-po.fr/api/line`

##### Summary

##### Query params

##### Body/request payload

##### Response


### `POST http://toflit18.medialab.sciences-po.fr/api/network/:id`

##### Summary

##### Query params

##### Body/request payload

##### Response


### `POST http://toflit18.medialab.sciences-po.fr/api/terms/:id`

##### Summary

##### Query params

##### Body/request payload

##### Response

