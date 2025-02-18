Solve :

Après avoir un peu explorer, on peut aller sur /robots.txt et découvrir un path vers le login admin.
On y va donc et on arrive sur un panneau de login. On essaye une SQLi très simple ```' or 1=1; --```, mais on se prend une erreur car il y a une vérification de caractères.
En fouillant un peu dans le code de la page et avec des essais, on se rend compte que la vérification est seulement côté client, donc avec un outil comme Burp Suite, on peut modifier la requête et la faire avec ```' or 1=1; --```, ce qui fonctionne et nous laisse nous connecter en tant qu'admin.
Sur cette page admin, on voit une note destinée aux devs qui dit qu'en faisant une certaine requête sur l'API avec un certain uuid de Charlie, on obtient des données sensibles, on cherche donc à obtenir cet uuid.