-open the terminal in the direction that cotain doker-compose.yml file run (make sure you already install docker) : docker-compose up


-localhost:800/api/products --> to see all published and authenticated products or creat a new product

-localhost:800/api/products/(int:pk) --> see detail of the product with id = pk.
(ex: localhost:800/api/products/1) 

-localhost:800/api/products/(int:pk)/update --> to update product with id = pk 

-localhost:800/api/products/(int:pk)/delete --> delete product with id = pk

-localhost:800/api/products/(int:pk)/comment --> add comment to the product with id = pk

-localhost:800/api/products/(int:pk)/vote --> add vote/unvote the product with id = pk



