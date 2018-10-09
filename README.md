# Observations

## Dependances python

Lancer le script en ligne de commande:

```sh
$ ./scripts/observations.py M45 2018-09-08 lapalma
```

Il devrait ouvrir le navigateur par defaut et montrer un graph.

Resoudre les dependences si besoin. Penser qu'il faudrat aussi ces dépendances de façon globale pour l'utilisateurs 
des processus apache (www-data dans notre cas).

## Pour installer sous apache (exemple sous Ubuntu):

```sh
# apt-get install -y apache2 libapache2-mod-wsgi
# cp observations.conf /etc/apache2/sites-available/
# ln -s /etc/apache2/sites-available/observations.conf /etc/apache2/sites-enabled/observations.conf
# mkdir -p /var/www/observations/astropyconfig
# mkdir -p /var/www/observations/astropycache
# chown -R www-data:www-data /var/www/observations/astropyconfig
# chown -R www-data:www-data /var/www/observations/astropycache
# sudo cp -R scripts /var/www/observations/
# sudo cp -R public /var/www/observations
```


## Lancer et débuguer

Normalement ...
```sh
# systemctl restart apache2
```
... devrait suffire. 

Se connecter à http://localhost, au moins le HTML devrait apparaitre. Si l'application ne fonctionne pas correctement
faire un:
```sh
# tail -f /var/log/apache2/error.log
```
... pour voir les messages d'erreur.

