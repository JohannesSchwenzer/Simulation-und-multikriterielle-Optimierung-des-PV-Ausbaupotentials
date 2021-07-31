# Simulation und multikriterielle Optimierung des Photovoltaik Potentials zur Stromversorgung im Quatierskonzept QUARREE 100.

Please note that this project was for my master's thesis at a german civil project, where german was the language used in presenting the results and publications.
Therefore this repository is in german as well.

Die im Repository enthaltenen Skripte dienen der Evaluierung des Photovoltaikpotentials als integrativer
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


## Simulation

Zur Veranschaulichung wurde der Simulationscode pro Haushalt in drei Blöcke
aufgeteilt. Codeblock 1 modelliert die Struktur des Energiesystems und die Interaktion
zwischen Stromerzeugung und Verbrauch. In Codeblock 2 werden die
in Block 1 errechneten Output Werte genutzt um die Optimierungsparameter zu berechnen. Die Output Werte aus Codeblock 2
werden in Form einer m *x* n Matrix ausgegeben und bilden die im Abschnitt Optimierungsalgorithmus
beschriebene Entscheidungsmatrix. Der dritte Codeblock besteht aus TOPSIS Optimierung und gibt den Wert der
optimalen Anlagengröße aus. Nachdem Codeblock 3 abgeschlossen ist, werden alle
Output Werte für den jeweiligen Haushalt gespeichert und das Script beginnt
erneut bei Codeblock 1 für den nächsten Haushalt bis das gesamte Quartier simuliert
wurde.

![grafik](https://user-images.githubusercontent.com/45041403/127740693-8ca350e8-7d81-4531-b9ce-6ed76cc7c313.png)

**Abb. 1:** *Schematische Darstellung der Struktur des modellierten Energiesystems.
Codeblock 1 simuliert die Interaktion zwischen Energieverbrauch und Energieerzeugung
über i Zeitschritte und j Dachausnutzungsgrade pro k Batteriekapazitäten je Haushalt .*




![grafik](https://user-images.githubusercontent.com/45041403/127740816-58aa2ccb-812f-4dbc-bb44-22203eaa318b.png)

**Abb. 2:** *Schematische Darstellung der Simulationsstruktur zur Berechnung der
Optimierungsparameter in Codeblock 2 und anschließender Evaluation mittels TOPSIS
Optimierung in Codeblock 3. Über i Zeitschritte und j Dachausnutzungsgrade wird die
optimale Dachausnutzung und Batteriekapazität nach n Optimierungsparametern ausgegeben.*



## Outputs/Ergebnisse
*Simulation_und_Optimierung.py* gibt die optimale Ausbaukapazität pro Haushalt, abhängig von den gewählten Optimierungs- und Systemparametern aus.
Zur Verdeutlichung der Struktur der Simulationsergebnisse sind in Abbildung 3
die Ergebnismatrizen für drei der sieben Optimierungsparameter für einen Beispielhaushalt,
sowie das Ergebnis der TOPSIS Optimierung dargestellt.

![grafik](https://user-images.githubusercontent.com/45041403/127740147-cd19a616-ea83-4076-95df-24ee9e9e4b7d.png)

**Abb. 3:**  *Simulationsergebnis für Autarkie, CO2-Reduktion und jährliche Rendite,
sowie TOPSIS Optimum nach Batteriekapazität und PV-Flächenausnutzung für
einen Beispielhaushalt.*

Sowohl die Werte der optimalen Anlagendimension, als auch die aller Optimierungskriterien, sowie Last- und Einspeisekurven werden aus der Simulation ausgegeben und können visualisiert oder für weitere Optimierungen genutzt werden. Einige Beispieloutputs sind in den folgenden Abbildungen dargestellt.   

![grafik](https://user-images.githubusercontent.com/45041403/127742658-c2906930-0d73-42f1-86a9-7b0b9feef2f7.png)

**Abb. 4:** *Optimale Anlagendimensionen aller Verbraucher im Quartier. Die weißen
Zahlen innerhalb der Kreissegmente geben die Anzahl der einzelnen Verbraucher an.
Die Zahlen im Mittelpunkt zeigen die Gesamtsumme und den Durchschnittswert für die
jeweiligen Verbrauchertypen an.*

![grafik](https://user-images.githubusercontent.com/45041403/127742858-fa91780f-0968-421c-a8c7-0a072bb89f04.png)

**Abb. 5:** *Jährliche PV-Strom Produktion. Der äußere Kreis gibt das Verhältnis
zwischen Stromproduktion von Einfamilienhäusern (EFH), Mehrfamilienhäusern
(MFH) und Gewerbe (GW) an. Die weißen Zahlen innerhalb der Kreissegmente geben
die absolute jährliche Stromgeneration der Verbrauchertypen in kWh an. Die inneren
Kreissegmente bilden das jeweilige Verhältnis zwischen Eigenverbrauch und Netzeinspeisung
ab.*

![grafik](https://user-images.githubusercontent.com/45041403/127742893-8a1dfe19-ca98-464e-9f2e-e23d5deff166.png)

**Abb. 6:** *Zeitlich aufgelöste Darstellung von kumulierter PV-Einspeisung und
kumuliertem Netzbezug im Quartier für jeweils 3 Tage im April und November. Die
linke Grafik zeigt den Zeitraum vom 21.–23. April, die rechte Grafik den Zeitraum vom
21.–23. November.*

## Datenstruktur
Die Simulation benötigt für jeden Haushalt die Dachflächen [m²] und die Ausrichtung der respektiven Dachflächen, sowie ein zeitlich aufgelöstes Lastprofil [kWh] und
Strahlungsdaten [W/m²] in derselben zeitlichen Auflösung (ist das Lastprofil stündlich müssen auch die Strahlungsdaten stündlich sein). Beim Nutzen von Wetterdaten die nur Horizontale Direktstrahlung und Diffusstrahlung beinhalten muss die geneigte Globalstrahlung zusätzlich berechnet werden. Eine gute Methode liefert [[Klucher, Thomas M.]](#klucher) .
(Ein Skript zur Umrechnung von Strahlung auf horizontaler zu geneigter Ebene kann ich auf Wunsch bereitstellen.)
Zur Erstellung von zeitlich aufgelösten Lastprofilen ist der [Load Profile Generator](#https://www.loadprofilegenerator.de/) zu empfehlen.
Je nach Optimierungskriterium werden weitere Zeitreihen benötigt, für CO²-Reduktion die spezifische CO² Emmission des deutschen Strommix [kg/kWh], für die Berechnung des Grid Support Coefficient nach [[Klein et al.]](#klein) die Börsentstrompreise [€/MWh] und zur Abschätzung des Konfliktpotentials mit Windenergie die Einsman Einsätze mit netzengpassbedingter Abregelung. 

Zur Simulation des Stadtquartiers sind anonymisierte Datensätze in den bereitgestellten *csv* Datensätzen vorhanden, sodass die Simulation innerhalb des Repository Out-of-the-box funktionieren sollte. (Pfade müssen angepasst werden)

Für die reine Batterieauslegung kann die *zeitoptimierte_Simulation.py* verwendet werden.

## Kontakt
johannes.m.schwenzer@gmail.com 



## References
<a name="abcde"> 
[Behzadian et al.]  Behzadian, Majid, et al. "A state-of the-art survey of TOPSIS applications." Expert Systems with applications 39.17 (2012): 13051-13069. </a>

<a name="klucher"> 
[Klucher, Thomas M.] Klucher, Thomas M. "Evaluation of models to predict insolation on tilted surfaces." Solar energy 23.2 (1979): 111-114. </a>

<a name="klein"> 
[Klein et al.]Klein, Konstantin, et al. "Grid support coefficients for electricity-based heating and cooling and field data analysis of present-day installations in Germany." Applied Energy 162 (2016): 853-867. </a>
