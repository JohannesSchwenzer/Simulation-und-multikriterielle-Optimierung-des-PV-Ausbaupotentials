# Simulation und multikriterielle Optimierung des Photovoltaik Potentials zur Stromversorgung im Quatierskonzept QUARREE 100.

Please note that this project was for my master's thesis at a german civil project, where german was the language used in presenting the results and publications.
Therefore this repository is in german as well.

Das Repository dient der Evaluierung des Photovoltaikpotentials als integrativer
Bestandteil des Konzepts zur regenerativen Energieversorgung im Stadtquartier
Rüsdorfer Kamp, Schleswig Holstein. Untersucht wurde der optimale
Ausbaugrad im Hinblick auf Netzdienlichkeit, Emmissionsreduktion und wirtschaftlicher
Realisierbarkeit für 91 Einfamilien-, 40 Mehrfamilienhaushalte und
14 Gewerbeverbraucher, sowie dessen Einfluss auf die Gesamtenergiebilanz des
Stadtquartiers. Des Weiteren können Konfliktpotentiale mit Windenergieeinspeisung betrachtet und mögliche
Lösungsansätze untersucht werden.

## Optimierungsalgorithmus

Als Grundlage des Optimierungsalgorithmus dient die TOPSIS Methodik (*Technique of Order Preference Similarity to the Ideal Solution*).
TOPSIS Optimierung nutzt eine Entscheidungsmatrix
aus den Ergebnissen aller vorhandenen Lösungen und einen Gewichtungsvektor
der einzelnen Optimierungskriterien. Die generelle Methodik lässt sich in 5 Teilschritte untergliedern.
Eine detallierte Literatur Review zur TOPSIS Optimierung liefern [[Behzadian et al.]](#abcde)

#### Normalisierung der Entscheidungsmatrix

Um die Werte in der Entscheidunsgmatrix X numerisch vergleichen zu können,
werden diese zuerst durch Vektor Normalisierung dimensionslos gemacht.

![grafik](https://user-images.githubusercontent.com/45041403/127736379-865caf99-58e4-434d-a7a3-b7d0d1495e75.png)


#### Berechnung der gewichteten, normalisierten Entscheidungsmatrix

Die durch Formel 3.1 errechnete normalisierte Entscheidungsmatrix R wird nun
mit dem Gewichtungsvektor W multipliziert um die unterschiedlichen Wertungen
der Optimierungskriterien abzubilden.

![grafik](https://user-images.githubusercontent.com/45041403/127736595-7065f94f-8818-4024-9869-79cd55843813.png)


#### Berechnung der Ideal- und Antiideallösung

Aus der in Formel 3.2 errechneten normalisierten, gewichteten Entscheidungsmatrix
V wird über Formel 3.3 die Ideallösung berechnet.

![grafik](https://user-images.githubusercontent.com/45041403/127736647-eae79ed9-3553-4c2a-a305-8bbb5995327b.png)

I’ bildet die Menge der Nutzenskriterien ab und I” die Menge der Kostenkriterien.
Die Ideallösung A* besteht also aus den höchsten Werten der Nutzenskriterien
und den niedrigsten Werten der Kostenkriterien aus der normalisierten, gewichteten
Entscheidungsmatrix V. Analog kann über Formel 3.4 die Antiideallösung
bestimmt werden.

![grafik](https://user-images.githubusercontent.com/45041403/127736741-755e6c35-77c5-475f-9374-541390852b00.png)


#### Berechnung der Abstände zur Ideal- und Antiideallösung
 
Im nächsten Schritt wird der Abstand D der einzelnen Lösungen zur Ideal- und
Antiideallösung über Formel 3.5 & 3.6 berechnet.

![grafik](https://user-images.githubusercontent.com/45041403/127736767-ac9ed85d-10fd-4efe-b61e-9f2d93d04c21.png)


#### Berechnung der relativen Nähe
Aus den in Formel 3.5 & 3.6 errechneten Abständen kann nun die relative Nähe
C* über Formel 3.7 errechnet werden. Der Wert der relativen Nähe liegt zwischen
0 und 1. Eine Lösung ist besser je näher ihr Wert an 1 ist.

![grafik](https://user-images.githubusercontent.com/45041403/127736800-f68d4048-0e05-4374-8d64-6f1244d63b3e.png)




## Anwendung
Zur Simulation verschiedener PV-Ausbaukapazitäten und Speichergrößen, sowie zur Berechnung der Optimalsystemauslegung
kann das Skript "Simulation_und_Optimierung" genutzt werden. Die notwendigen Daten und Pfade sind mitgeliefert 
und können individuell angepasst werden. Als Umgebung ist jede Python 3 fähige Programmierumgebung geeignet.
Die einzelnen Parameter sind erklärt und können angepasst werden.

Für die reine Batterieauslegung kann die "zeitoptimierte_Simulation" verwendet werden.

Fragen an:  johannes.m.schwenzer@gmail.com oder Johannes.Schwenzer@siamese-pixel.de



## References
<a name="abcde"> 
[Behzadian et al.]  Behzadian, Majid, et al. "A state-of the-art survey of TOPSIS applications." Expert Systems with applications 39.17 (2012): 13051-13069. </a>
