Harjoitustyön aiheena on tehdä roolipeli henkinen tekstiseikkailupeli.

Pelissä on etukäteen kirjoitettu lyhyt runko, jossa on pelin päätapahtumat ja peli etenee kronologisesti rungon mukaan.

Pelissä pelaaja voi kuitenkin tehdä suhteellisen vapaasti asioita tekoälyn avulla, pelaaja voi jutella muille hahmoille ja tekoäly hoitaa täysin vastausdialogin.

Tekoälylle on asetettu erilaisia tooleja, jotka rajoittavat pelaajan pelaamista tietyllä tavalla, esimerkiksi toiselle alueelle siirryttäessä, tekoäly käyttää 
esim. move_to() toolia, jonka avulla tarkastetaan onko paikka jonne pelaaja haluaa liikkua pelialueella. (Täten pelaaja ei voi tehdä luonnottomia toimia, kuten lentää avaruuteen)

Pelaajan promptit ja tekoälyn vastaukset tallennetaan tiedostoon, jota tekoäly seuraa ja täten "muistaa" aiemmat keskustelun ja pelin nykytilanteen 
