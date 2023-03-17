-open the terminal in the direction that contain doker-compose.yml file run (make sure you already install docker) : docker-compose up

-note: you have to run the comment and vote server to fully functional https://github.com/leducthai/django-rest-framework-comment-vote


-localhost:800/api/products --> to see all published and authenticated products or creat a new product

-localhost:800/api/products/(int:pk) --> see detail of the product with id = pk.
(ex: localhost:800/api/products/1) 

-localhost:800/api/products/(int:pk)/update --> to update product with id = pk 

-localhost:800/api/products/(int:pk)/delete --> delete product with id = pk

-localhost:800/api/products/(int:pk)/comment --> add comment to the product with id = pk

-localhost:800/api/products/(int:pk)/vote --> add vote/unvote the product with id = pk

-localhost:800/api/search/?q=thai&published=True --> support searching product with title or content that include the word "thai" (you can always use other word or phrase) and published = True (you can use '0' or 'False' to denote False)



