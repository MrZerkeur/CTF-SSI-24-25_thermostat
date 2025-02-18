Solve :

Après avoir un peu explorer, on peut aller sur /robots.txt et découvrir un path vers le login admin.
On y va donc et on arrive sur un panneau de login. On essaye une SQLi très simple ```' or 1=1; --```, mais on se prend une erreur car il y a une vérification de caractères.
En fouillant un peu dans le code de la page et avec des essais, on se rend compte que la vérification est seulement côté client, donc avec un outil comme Burp Suite, on peut modifier la requête et la faire avec ```' or 1=1; --```, ce qui fonctionne et nous laisse nous connecter en tant qu'admin.
Sur cette page admin, on voit une note destinée aux devs qui dit qu'en faisant une certaine requête sur l'API avec un certain uuid de Charlie, on obtient des données sensibles, on cherche donc à obtenir cet uuid.

Toujours dans le même champ d'input, on peut injecter des commandes SQL.

Tout d'abord on peut guess le nom des tables et colonnes mais admettons que ça ne soit pas le cas.

Pour trouver la table, on utilise ce payload pour connaitre le nombre de table :
```
' OR (SELECT COUNT(*) FROM sqlite_master WHERE type='table')=2 --&
```
On apprend donc qu'il y a 2 tables.

Ensuite on essaye de connaître le nom de la table :
```
' OR (SELECT SUBSTR(name,1,1) FROM sqlite_master WHERE type='table' LIMIT 1)='u' --
```
Après ça, on avance lettre par lettre pour trouver le nom complet

Même principe une fois qu'on a trouvé la table, mais avec les colonnes.

Trouvé le nombre de colonnes :
```
' OR (SELECT COUNT(*) FROM pragma_table_info('users'))=4 -- 
```

Puis pour énumérer chacunes, lettre par lettre :
```
' OR (SELECT SUBSTR(name,1,1) FROM pragma_table_info('users') LIMIT 1)='i' -- 
```

Une fois le nom de la table et de la colonne souhaitée obtenu, on va récupérer le contenu caractère par caractère
```
' OR (SELECT SUBSTR(uuid,1,1) FROM users WHERE username='Charlie')='5' --
```

Avec ça, on obient le bon uuid et on peut donc faire la requête pour obtenir le FLAG :)