# Natural-Stupidity
### RTU RDBD0 2.kursa priekšmeta MI pamati 1. praktiskā darba 14. komandas darba koda krātuve
----------------
#### Spēles palaišanai jāizmanto `main.py` fails. Ir iespēja pailaist konsoles versiju caur `cli.py`
---------------

1) Cilvēks **norāda** spēlē izmantojamas skaitļu **virknes garumu**, kas var būt diapazonā **no 15 līdz 25** skaitļiem. 

2) Dators **randomā** saģenerē skaitļu virkni atbilstoši uzdotajam garumam **tikai ar 1 un 0**.

3) Cilvēks **izvēlas, kas veic pirmo gājienu** - cilvēks vai dators

4) Cilvēks **izvēlās kādu algoritmu izmantot** - Minimaksa algoritmu vai Alfa-beta algoritmu

5) Spēles **sākumstāvoklis** ir ģenerētā skaitļu virkne. Katram spēlētājam ir **0 punktu**. 

6) Spēlētāji izpilda **gājienus pēc kārtas**, aizvietojot **divu blakusstāvošu skaitļu pāri ar vienu ciparu**, balstoties uz šādiem nosacījumiem: 
   	* `0 0` → `1` un dod **1 punktu spēlētāja** punktu skaitam; 
	* `0 1` → `0` un dod **1 punktu pretinieka** punktu skaitam;
	* `1 0` → `1` un **atņem 1 punktu no pretinieka** punktu skaita;
	* `1 1` → `0` un **atņem 1 punktu no spēlētāja** punktu skaita.

	Katrā gājienā var aizvietot tikai vienu skaitļu pāri. 

7) Spēle **beidzas**, kad ir iegūts **viens skaitlis**. Uzvar spēlētājs, kam ir vairāk punktu. Ja punktu skaits ir vienāds, tad rezultāts ir neizšķirts.

8) Uzsākt spēli **atkārtoti** pēc spēles pabeigšanas.

-------------------------------------------------------------

> (Nokopēts pa tiešo no ORTUSa) Izstrādājot programmatūru, studentu komandai obligāti ir jārealizē: 
> * Spēles koka vai tā daļas glabāšana datu struktūras veidā (klases, saistītie saraksti).
>
> * Spēles koka vai tā daļas ģenerēšana atkarībā no spēles sarežģītības un studentu komandai pieejamiem skaitļošanas resursiem;
>
> * Heiristiskā novērtējuma funkcijas izstrāde;
>
> * Minimaksa algoritms un Alfa-beta algoritms (kas abi var būt realizēti kā Pārlūkošana uz priekšu pār n-gājieniem);
>
> * 10 eksperimenti ar katru no algoritmiem, fiksējot datora un cilvēka uzvaru skaitu, datora apmeklēto virsotņu skaitu, datora vidējo laiku gājiena izpildei.

--------------------------------------------------------------------
Tādējādi izstrādājot darbu, studentu komandai ir jāizpilda šādi soļi:

- [x] Jāsaņem spēle no mācībspēka;

- [x] Jāizvēlas programmēšanas vide/valoda;

- [x] Jāizveido datu struktūra spēles stāvokļu glabāšanai;

- [x] Jāprojektē, jārealizē un jātestē spēles algoritmi;

- [x] Jāveic eksperimenti ar abiem algoritmiem;

- [ ] Jāsagatavo atskaite par izstrādāto spēli un tā ir jāiesniedz e-studiju kursā;

- [ ] Jāatbild uz jautājumiem par mākslīgā intelekta rīku izmantošanu spēles izstrādē;

- [ ] Jāveic komandas dalībnieku savstarpējā vērtēšana;

- [x] Jāpiesakās aizstāvēšanas laikam;

- [ ] Jāaizstāv izstrādātais darbs.
