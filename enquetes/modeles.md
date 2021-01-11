# Étude du modèle de TOFLIT18

Toflit regroupe des données sur le commerce français de 1716 à 1821. Il documente plus de 500 000 flux de marchandises.

Le coeur de la base est constitué par des `sources` qui documente un ensemble de `flux` de marchandise correspondant à :

* la `direction` ("douanière" ?) ayant rapporté le flux
* le `produit` échangé et sa quantité & coût
* le `type` d'échange : import ou export
* le `partenaire` commercial qui peut être une entité géographique ou politique
* ... (à compléter)

Sur cette base de données primaires, la base contient aussi des données secondaires qui permettent d'agréger les `flux` primaires selon des `classifications` permettant de grouper les `produits` et les `partenaires` selon des ensembles plus grands.

## Liste des sources toflit

### National best guess

This autoselects the best source about trade by product x partner for the whole of France in each year. This is "National toutes directions tous partenaires" for 1750, "Objet Général" from 1754 to 1782, "Résumé" in 1787-1789 and 1797-1821.

### Local best guess

This autoselects the best source about trade by product x partner x direction in each year. The selected sources are mostly of the "Local" (1714-1780), except for 1750 when we use "National toutes directions tous partenaires".

### Objet Général

were produced from 1752 to 1788\. They contain trade by product x partner for the whole of France. They always include the value of the flows. From 1771, they include quantities and / or unit prices. The 1752 Objet Général does not include imports from the West Indies. We have added to the Objet Général imports through the French East Indian Company when available on the same year (up to 1771)

### Résumé

cover the 1787-1789 and 1797-1821\. They contain trade by class of products x partner for the whole of France. They include the value of the flows.

### National toutes directions partenaires manquant

They contain trade by product x partner x direction for the whole of France and some partners.
### National toutes directions tous partenaires

contain trade by product x partner x direction for the whole of France. They includes values and quantities. They only exist for 1750 (though the 1789 year is nearly covered in the same way)
### Local

sources contain data for trade by a specific direction by product x partner x direction. They include unit prices and quantites (and sometimes also values). They exist from 1714 to 1780.

### 1792 first semester

contains trade by product x partner for the whole of France for the first semester of 1792\. They include mainly quantities.

## National partenaires manquants

contain trade by product x partner for the whole of France and a small number of partners (Angleterre, Barbarie, États-Unis, Russie for individual years in the 1780s).

### 1792-both semester

contains trade by product x continent for the whole of Frane for 1792\. They contain a mix of quantities and values (but never both for a single flow)
    
### Tableau des quantités

covers 1822 and 1823\. It contains trade by product x partner for the whole of France. They include mainly quantities.

### Tableau des marchandises

covers 1819 and 1821\. It contains trade by product for the whole of France. They include mainly quantites and tolls paid.

### Tableau Général

include bilateral trade from 1716\. We have completed the original "Tableau Général" with various other sources giving the same information at various date (up to 1792) or for the French East India Compagny.

## Liste des classifications de produit toflit

Elles permettent de regrouper les flux selon des groupements de produits.

```
- Source(source)
  - Orthographic normalization(orthographic)
    - Simplification(simplification)
      - Beaver(beaver)
      - Canada(canada)
      - Coffee(coffee)
      - Cotton(coton)
      - Eden Treaty(edentreaty)
      - Grains(grains)
      - Hamburg(hamburg)
      - Textile vertical differenciation in SITC(luxe_dans_SITC)
      - Textile vertical differenciation in type(luxe_dans_type)
      - Medicinal products(medicinales)
      - China(porcelaine)
      - Revolution and Empire(revolutionempire)
        - Revolution and Empire – aggregate(RE_aggregate)
        - Three sector classifications(threesectors)
        - Three sector classifications based on the Montesquieu database(threesectorsM)
      - SITC18(sitc)
        - SITC18_English(sitc_EN)
        - SITC18_French(sitc_FR)
        - Simplified SITC(sitc_simplEN)
      - Textile type(type_textile)
      - Ulrich(ulrich)
      - Venitian Glass Beads(v_glass_beads)
```

## Liste des classifications de partenaire toflit

Elles permettent de regrouper les flux selon des groupements de partenaires.

```
- Source(source)
  - Orthographic normalization(orthographic)
    - Simplification(simplification)
      - Africa(africa)
      - Grouping(grouping)
      - O’Brien(obrien)
      - Source Names(sourcename)
      - War(wars)
```

# Étude du modèle de PORTIC/NAVIGO


