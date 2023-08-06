# Assignment One

### Componenti del gruppo:  
**Nome**: Simone Pierro, **matricola**: 852285, **e-mail**: s.pierro2@campus.unimib.it  
**Nome**: Andrea Pascuzzi, **matricola**: 903604, **e-mail**: a.pascuzzi2@campus.unimib.it  

### Descrizione del progetto:

Si tratta di un progetto scritto in python utilizzando il framework Django Rest Framework. 
Il codice sorgente è stato clonato dal seguente repository: https://github.com/vishavjeet1999/todo_project.git. Questo progetto prevede la creazione di elementi "ToDo" che vengono suddivisi in liste ToDo.
Nonostate la sua semplicità, è già provvisto di una parte statica (FE) e di una connessione verso un database. In questo caso il DBMS utilizzato in origine (sqlite) è stato sostituito con un DBMS PostgreSQL per poter sfruttare il PaaS fornito da Heroku per lo storing degli item ToDo.
Heroku rappresenta anche il PaaS su cui avviene il deploy dell'applicativo.
La pipeline è stata realizzata tenendo a mente la struttura DAG (Directed Acyclic Graph), anche se non è necessario specificare il tipo di struttura per un pallicazione così semplice, se in futuro si dovessero aggiungere dei requisiti e modificare la pipeline si può tenere conto di questo metodo che ne massimizza l'efficienza. 
La pipeline è suddivisa nei seguenti stage:

- **Build**: questo stage pone le basi per gli stage successivi. Al suo interno vengono installati pacchetti, requirements e le dipendenze necessarie alla corretta esecuzione della pipeline. Viene anche creato il virtual enviroment di python ed in ultimo vengono esportate le impostazioni di django relative al progetto.
- **Lint**: lo stage Lint si occupa dell'analisi statica del codice, attraverso un programma chiamato Lint. Questa parte della pipeline si occupa di controllare e segnalare errori di programmazione, bugs ed errori relativi alla struttura del codice senza effettivamente eseguire il codice.
- **Migrate**: lo stage Migrate è legato al funzionamento del framework Django e prevede il processo di migrazione dello schema della base dati verso il Database vero e proprio.
- **Test**: all'interno di questo stage è presente il test di unità sulle istanze todo create durante il processo gestito dalla pipeline. Viene usato lo strumento "Coverage", il quale permette sia di lanciare i test unità (e di integrazione quando implementati) sia di verificare l'effettiva copertura del codice da parte dei test menzionati.
- **Deploy**: questo stage prevede il deploy vero e proprio dell'applicativo. Come citato in precedenza il PaaS utilizzato è Heroku. Abbiamo preferito utilizzare una piattaforma che ci offrisse già alcune funzionalità come il bilanciamento del carico e l'assegnazione delle risorse. Inoltre Heroku offre la possibilità di abilitare un modulo legato al DBMS PostgreSQL, gestendo in maniera semi-automatica l'integrazione con l'applicativo Django.


### Altre note
- i test di unità e d'integrazione non coprono tutti gli snippet di codice, si concentrano più sulla parte dimostrativa che quantitativa. Questo perchè si vuole riporre il focus sulla costruzione della pipeline.
- Heroku fa riferimento al branch main per implementare le change. Viene gestito all'interno della parte di deploy.
