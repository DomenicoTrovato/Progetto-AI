# 🧠 **QuestMaster** – Agentic AI per Narrative Interattive  
> Progetto finale – Corso *Agentic AI* (A.A. 2024-2025)  
> **Scadenza consegna:** 30 settembre 2025 – 23:59 (CET)

![License MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python&logoColor=white)
![PDDL Inside](https://img.shields.io/badge/PDDL-powered-blueviolet)

---

## 📚 Indice

1. [Descrizione](#descrizione)
2. [Funzionalità chiave](#funzionalità-chiave)
3. [Architettura a due fasi](#architettura-a-due-fasi)
4. [Struttura del progetto](#struttura-del-progetto)
5. [Requisiti](#requisiti)
6. [Installazione rapida](#installazione-rapida)
7. [Esecuzione passo-passo](#esecuzione-passo-passo)
8. [Esempi di output](#esempi-di-output)
9. [Tech Stack](#tech-stack)
10. [Linee guida di sviluppo](#linee-guida-di-sviluppo)
11. [Contributi](#contributi)
12. [Autori & crediti](#autori--crediti)
13. [Licenza](#licenza)

---

## Descrizione

**QuestMaster** è un sistema *agentico* in **due fasi** che affianca l’autore nella creazione di esperienze narrative interattive:

* **Fase 1 – Story Generation & Planning**:  
  Genera in modo iterativo un problema di pianificazione PDDL valido, a partire da un documento di **lore**.
* **Fase 2 – Interactive Story Game**:  
  Trasforma la storia validata in una web-app a bivi pienamente giocabile.

L’obiettivo è coniugare **coerenza logica** (classical planning) e **creatività generativa** (LLM) mantenendo l’autore “in the loop” per un controllo fine della trama.

---

## Funzionalità chiave

| Categoria | Feature |
|-----------|---------|
| **Generazione** | ✨ Creazione automatica di `domain.pddl` e `problem.pddl` con commenti inline |
| **Validazione** | ✅ Verifica con *Fast Downward* dell’esistenza di almeno un piano |
| **Reflection Agent** | 🔁 Correzione iterativa di incoerenze logiche con dialogo autore-agente |
| **Web Game** | 🌐 Conversione PDDL → HTML con scelte interattive e (opz.) illustrazioni di stato |
| **Local LLM** | 🤖 Supporto a modelli *on-device* via **Ollama** + **LangChain** |
| **Modularità** | 🧩 Codice separato in `phase1/` e `phase2/` per massima manutenibilità |

---

## Architettura a due fasi

### Fase 1 – Story Generation

```mermaid
graph TD
    A[Lore Document] --> B[LLM Prompt]
    B --> C{Genera PDDL}
    C -->|domain & problem| D[Fast Downward]
    D -->|✓| E[Storia valida]
    D -->|✗| F[Reflection Agent]
    F --> C

### FASE 2 - Interactive story game
graph TD
    G(domain/problem PDDL) --> H[LLM Prompt]
    H --> I[HTML Generator]
    I --> J[index.html (+ assets)]
    J --> K[Player]

QuestMaster/
├── phase1/
│   ├── lore.txt            # Input iniziale
│   ├── generate_pddl.py    # Parser lore → PDDL
│   ├── validator.py        # Wrapper Fast Downward
│   ├── refine_agent.py     # Reflection loop
│   ├── domain.pddl         # Output
│   └── problem.pddl        # Output
├── phase2/
│   ├── game_generator.py   # PDDL → HTML
│   ├── index.html          # Web-game finale
│   └── assets/             # (Opz.) immagini
├── models/                 # Modelli LLM locali
│   └── llama3_8b.gguf
├── requirements.txt
└── README.md


Requisiti
Categoria	Versione consigliata
Python	≥ 3.10
Fast Downward	23.12
LangChain	≥ 0.3.1
Ollama	≥ 0.1.35
FAISS (opz.)	≥ 1.7
Browser moderno	Chrome / Firefox / Edge
Per l'installazione
pip install -r requirements.txt

# 1. Clona il repo
git clone https://github.com/<tuo-utente>/QuestMaster.git
cd QuestMaster

# 2. Crea e attiva un venv
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. (Facoltativo) Avvia il modello LLaMA in Ollama
ollama serve &
ollama pull llama3:8b

# 5. Esegui end-to-end
make all          # oppure segui la sezione successiva

Autori 
Ruolo	Nome
Studenti	Angelo Paldinom, Domenico Trovato, Alessandro Pata



