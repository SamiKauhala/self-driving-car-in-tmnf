## Tietokoneen ajama auto simuloidussa ympäristössä

### Tehtävä
Luo tietokoneen ajama auto simuloidussa ympäristössä esim. videopelissä. Valintani olivat rajoitettu Linuxin ilmaisiin peleihin ja simulaattoreihin. Valitsin TrackMania Nations Forever sen monipuolisten ominaisuuksien ja yksinkertaisten ohjauksen takia.

### Lähestymistavat
- Oikeasta maailmasta löytyvien itse ajavien autojen tapa; Käyttää linjojen- ja reunantunnistusta tai hahmojentunnistusta.
- Konvoluutio neuroverkot; Käyttää kuvia ja suuntia opettamaan neuroverkkoa tunnistamaan miten autoa ohjataan. Päätin käyttää Googlen Inception V3 verkkomallia.

### Tulokset
Ensimmäiselle lähestymistavalle syntyi ongelmia radan leveyden takia. En voinut luoda luotettavia kulkuväyliä. Päätin jättää tämän toteuttamatta.

Seuraavalle lähestymistavalle syntyi ongelmia treenidatan puutteen takia. Minulla oli vain 100 tuhatta tietuetta suuri datasetti. Saavutin tämän avulla noin 86% tarkkuuden ennustuksille.

### Havaintoja
Treenatessani neuroverkkoa huomasin, että osa alijoukoista tuottivat huomattavasti pienemmän tarkkuuden ennustuksille. Oletan, että vaihtelevat tulokset johtuvat poikkeavuuksista datasetissä. Näiden poikkeavuuksien poistaminen olisi hyvin työlästä tai vaikeaa, joten päätin jättää ne datasettiin.

### Kuvat
Muutamia graafeja Tensorboardista.

##### Validointi tarkkuus<br />
<img src="resources/validation-accuracy.png" alt="Validaation tarkkuus" />

##### Validoinnin hävikki<br />
<img src="resources/validation-loss.png" alt="Validaation hävikki" />

### Videot
- [Treenattu rata](https://youtu.be/CAi4YIlSLm0)
- [Treenaamaton rata](https://youtu.be/S2kOVLtNqkg)
 
Videoista voidaan todeta, että treenattu malli toimii huonommin treenaamattomassa ympäristössä. Sille ei myös voida kertoa, että se ajaa väärään suuntaan.

### Puutteita & Ongelmia
Puutteellinen treenidata ja sen luonne tekevät luotettavan mallin treenaamisesta hyvin hankalaa. En myöskään tasapainottanut datasettiä ajanpuutteen takia. Tämä johti siihen, että malli ennustaa tiettyjä suuntia herkemmin, kuin toisia.

### Parannuksia & Potentiaali
Ajatuksia, miten voitaisiin parantaa tuloksia.

##### Käytetään reunantunnistusta ja linjoja ennustamaan nopeus ja käännökset?
Voisi olla hyvä idea toteuttaa. Ei välttämättä vaatisi konvoluutio verkkomallia, mutta tämä lähestymistapa on laskennallisesti raskas.

###### Hough linjoja reunantunnistamisesta
<img src="resources/hough-lines.jpg" alt="Hough linjoja" width="320" height="240" />

##### Käytä toissijaista konvoluutio neuroverkkoa tunnistamaan nopeus?
Tällä hetkellä ei taida olla tapaa päästä käsiksi pelissä oleviin tietoihin, joten emme voi matkia todellista maailmaa, jossa kaikki autoon liittyvä tieto olisi saatavilla. Olisi kuitenkin mahdollista opettaa toissijaiselle mallille tunnistamaan nopeus treenidatasta ja käyttää siitä johdettuja ennustuksia nopeuden hallintaan.

<img src="resources/speed.jpg" alt="Nopeus" width="160" height="120" />

##### Luoda enemmän treenidataa kaikista ympäristöistä?
Minulla oli vain 100 tuhatta tietuetta treenidataa, yhdestä ympäristöstä ja valaistuksesta. Olisi parempi, jos treenidataa olisi kaikista ympäristöistä ja valaistuksista.

##### Olion tunnistus ja reunojen tunnistus?
Saattaisi olla järkevää opettaa neuroverkkoa tunnistamaan auto ja reunat, joiden avulla voitaisiin opettaa verkkoa pitämään auto linjojen välissä.

##### Lisää vahvistettu opetus?
Tämän avulla voitaisiin vähentää käyttäjän tuottamaa treenidataa pitemmällä aikavälillä.

##### Muita ideoita
Ajattelin käyttää geneettistä algoritmiä, joiden avulla voitaisiin opettaa neuroverkkoa paremmaksi sukupolvi kerrallaan.

### Lähteet & Inspiraatio
- https://github.com/Sentdex/pygta5

### Lisätietoja
- Reuna- ja linjojentunnistus koodi löytyy v0.01 kansiosta.

##### Ohjelmistot & Versiot
- mss 3.2.1
- pynput 1.3.10
- tflearn 0.3.2
- tensorflow-gpu 1.8.0
- numpy 1.14.5
- opencv-python 3.4.1