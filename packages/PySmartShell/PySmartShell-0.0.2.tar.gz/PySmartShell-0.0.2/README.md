# Progetto PySmartShell
##### rev. 0.1 del 01/11/2022
#


## Comandi

#### Generali
Attivare un livello di log tra _DEBUG_, INFO, _WARNING_, _ERROR_, _CRITICAL_:
```shell 
python main.py --log-level DEBUG
```

Visualizzare un valore di configurazione generale:
```shell 
python main.py --get-conf key
```

Impostare un valore di configurazione generale:
```shell 
python main.py --set-conf key=value
```
#
#### Lavorare con le actions

Eseguire una _actions_:
```shell 
python main.py actionName
```

Visualizzare un valore di configurazione riguardante un'azione:
```shell 
python main.py actionName --get-conf key
```

Impostare un valore di configurazione riguardante un'azione:
```shell 
python main.py actionName --set-conf key=value
```

#
#### Comandi di aiuto

Per avere lo usage dell'intero script:
```shell 
python main.py -h
```

Per avere lo usage di una particolare _action_:
```shell 
python main.py actionName -h
```

#
## Lavorare con le actions

Le _actions_ vengono caricate in maniera automatica dallo script che per default andrà a cercare nella cartella ```/actions```, tuttavia è possibile specificare una percorso diverso avvalendosi del comando:

```shell 
python main.py --set-conf actionsPath="<percorsoDellaCartella>"
```

**N.B:** Verranno caricate soltanto le classi che hanno lo stesso nome la cartella e il file.

Ecco un esempio della struttura interna che la cartella deve avere per permettere allo script il caricamento automatico:
```project 
actions
└─── NamedEntityRecognitionAction (folder)
│    │ NamedEntityRecognitionAction.py (file)
│
└─── OtherActionToDoAction (folder)
│    │    OtherActionToDoAction.py (file)
│    │
│    └─── sublib (folder)
│    │    │ SubLib1.py    
│    │    │ SubLib2.py    
...  ...    ...
```

#### Tipi di _action_

Il progetto mette a dispozione due classi astratte dalle quali implementare nuove _actions_:
- _AbstractAction_;
- _AbstractActionWithConfiguration_.

La prima è la classe base dalla quale viene a sua volta estesa la _AbstractActionWithConfiguration_ la quale, offre in più la possibilità di settare valori di configurazione dal file preposto e di reperirne tramite chiave (vedi la sezione "Lavorare con le actions").


##### _AbstractAction_

Per implementare una nuova classe da _AbstractAction_ bisogna definire:
- l'attributo _name_;
- l'attributo _helpInfo_;
- il metodo astratto _executeVertical_;
- il metodo _getArgsSchema_ (facoltativo).

L'attributo _name_ è il nome con il quale è possibile accedere, tramite questo progetto, alla _action_ implementata.

L'attributo _helpInfo_ è il testo visualizzato dal progetto quando viene chiamato il comando di help (vedi la sezione "Comandi di aiuto").

Il metodo _executeVertical_ è dove viene espletata la funzione che la _action_ deve portare a termine. Per fare ciò è possibile avvalersi di altri file a patto che siano contenuti nella stessa cartella della nuova _action_.

Qualora la _action_ avesse necessità di integrare dati con argomenti esterni è possibile fruttare il metodo _getArgsSchema_.
Esso tornerà una lista di istanze della classe _Argument_, i quali saranno gli argomenti di cui la _action_ potrà aver bisogno di funzionare e saranno automaticamente disponibili da script (vedi la sezione "Lavorare con le actions").

Esempio di implementazione:
```python
class OtherActionToDoAction(AbstractAction):
  name:str = 'otherActionToDo'
  helpInfo:str = 'Help info to explain what OtherActionToDoAction do'

  @staticmethod
  def getArgsSchema() -> list[Argument]:
    return [ Argument.create(longCommand='filePath') ]

  def executeVertical(self, args:dict):
    instruction1
    instruction2
    instruction3

```


##### _AbstractActionWithConfiguration_

L'implementazione di una classe dalla classe astratta _AbstractActionWithConfiguration_ avviene nella stessa maniera di _AbstractAction_, con l'unica differenza riguardante il metodo _getArgsSchema_ che, nel caso in cui la _action_ abbia bisogno di argomenti fruibili tramite script, deve estendere il metodo dalla classe padre.

Questa classe presenta in più i metodi per reperire

Esempio di implementazione:
```python
class OtherActionToDoWithConfAction(AbstractActionWithConfiguration):
  name:str = 'otherActionToDoWithConf'
  helpInfo:str = 'Help info to explain what OtherActionToDoAction do'

  @staticmethod
  def getArgsSchema() -> list[Argument]:
    return AbstractActionWithConfiguration.getArgsSchema() + [ 
      Argument.create(longCommand='filePath') 
    ]

  def executeVertical(self, args:dict):
    instruction1
    instruction2
    instruction3

```

#
#
#### Classe Argument
La classe _Argument_ è l'astrazione degli argomenti che una _action_ può aver bisogno per espletare il suo fine e che saranno fruibili tramite lo script.
E' possibile istanziare una classe _Argument_ tramite il metodo statico _create_ passando gli argomenti:
- _longCommand_ - stringa che rappresenta il comando in forma estesa (es. _--file_) [obbligatorio]
- _shortCommand_ - stringa che rappresenta il comando in forma corta (es. _--f_) [opzionale]
- _type_: - esprime il tipo dell'argomento tra _int_, _float_, _str_ [opzionale]
- _helpInfo_ - stringa che rappresenta la stringa di help [opzionale]
- _isRequired_ - booleano che specifica se è un argomento obbligatorio o meno [opzionale]

#


#
**Colageo Mirko** <mirko.colageo@gmail.com>