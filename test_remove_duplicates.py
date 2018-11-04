from unittest import TestCase
from Ranker import *

reccs = [Recommendation("Super Duper",10,'1','a', 1),
         Recommendation("Duper Super", 8, '2', 'a', 0.5),
         Recommendation("Eureka", 20, '3', 'b', 1),
         Recommendation("Pappy's", 7, '4', 'c', 0.3),
         Recommendation("SmashBurger", 6, '5', 'd', 1),
         Recommendation("Super Duper", 2, '6', 'a', -0.9),
         Recommendation("Snack Shack", 8, '7', 'e', .75)]

reccs_drm = [Recommendation("Super Duper",12.2,'1','a', 0.2),
             Recommendation("Eureka", 20, '3', 'b', 1),
             Recommendation("Pappy's", 7, '4', 'c', 0.3),
             Recommendation("SmashBurger", 6, '5', 'd', 1),
             Recommendation("Snack Shack", 8, '7', 'e', .75)]

Reccs = {hash(r): r for r in reccs}

r = ranking(Reccs)
print(r)