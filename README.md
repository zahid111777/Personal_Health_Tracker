🏥 Personal Health Tracker: AI-Powered Health DashboardPersonal Health Tracker is a secure, full-stack application designed to aggregate daily health vitals and transform tracking metrics into clear, human-centered insights. The platform leverages statistical pipelines to handle historical baseline metrics—processing trends, anomaly detections, and biometric correlations—while a resilient multi-provider LLM fallback matrix translates complex analytical data into doctor-ready PDF health reports and interactive coaching summaries.🚀 Key FeaturesDaily Vitals Logging: Seamless entry tracking for weight, blood pressure, heart rate, sleep hours, sleep quality, mood scores, energy levels, water intake, steps, and daily calories.Statistical Trend Engine: Computes running moving averages, multi-metric chart overlays, and GitHub-style log-frequency contribution heatmaps.Algorithmic Anomaly Detection: Applies automated data distribution mapping (Z-score for normal distributions and IQR checks for skewed datasets) to isolate unusual vital fluctuations before leveraging AI to explain potential contextual causes.Biometric Correlation Mapping: Uses SciPy to calculate Pearson correlation coefficients. Filters out noise by displaying only statistically significant relationships ($p < 0.05$) via an interactive visual matrix.Goal Management & Streaks: Visualizes real-time progress toward personal health milestones using interactive target rings alongside a consecutive-day logging streak counter.Multi-LLM Resilience Chain: Combines an abstract provider orchestrator parsing requests across Groq ➔ OpenRouter ➔ Gemini ➔ OpenAI clients to safeguard runtime availability and bypass individual token limits.Doctor-Ready PDF Reports: Compiles historical graphs, data parameters, flagged outliers, and structural executive summaries into a downloadable PDF built using ReportLab.🛠️ Tech StackBackend ArchitectureFramework: Python 3.11+, FastAPI (Asynchronous REST API)Database & ORM: SQLAlchemy, SQLite (Local file-based architecture)Security & Encryption: JWT (via python-jose), bcrypt password hashing, and Fernet (AES-128) symmetric encryption for locking user-hosted provider credentials at rest.Data Processing: pandas, numpy, and scipy.stats.Document Compilation: reportlab & matplotlib (server-side graph rendering).Frontend ArchitectureFramework: Next.js 14 (App Router) with React & TypeScript.Styling & UI: Tailwind CSS, shadcn/ui core component primitives (Radix UI).State Management & Data Fetching: @tanstack/react-query (server state synchronization) and Zustand (client session storage).Data Visualization: Recharts (Dynamic responsive lines, bars, matrices, and progress rings).📂 Project StructurePlaintextpersonal-health-tracker/
├── backend/                 # FastAPI Python Application
│   ├── data/                # Hardcoded reference constants & catalogs
│   ├── models/              # Declarative SQLAlchemy schema maps
│   ├── routers/             # Endpoint route controllers (Auth, Logs, Analytics, Export)
│   ├── schemas/             # Pydantic contract validation validation models
│   └── services/            # Statistical computations & LLM engine integrations
└── frontend/                # Next.js Application
    ├── app/                 # App Router route targets and sub-views
    ├── components/          # Reusable visualization components (Charts, Heatmaps, Chats)
    ├── hooks/               # Encapsulated React Query state hooks
    └── lib/                 # Core Axios clients, authentication utilities, and helper maps
⚙️ Local Infrastructure Setup1. Clone the RepositoryBashgit clone https://github.com/yourusername/personal-health-tracker.git
cd personal-health-tracker
2. Initialize the Backend ServiceBashcd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
Create a secure .env configuration file in the root of your backend/ workspace:Code snippetSECRET_KEY=YOUR_SECURE_JWT_SECRET_SIGNING_KEY
ALGORITHM=HS256
DATABASE_URL=sqlite:///./health_tracker.db
FERNET_KEY=YOUR_FERNET_SYMMETRIC_ENCRYPTION_KEY

GROQ_API_KEY=YOUR_GROQ_API_KEY
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
Launch the application using Uvicorn:Bashuvicorn main:app --host 127.0.0.1 --port 8000 --reload
3. Initialize the Frontend ApplicationBashcd ../frontend
npm install
Create a local environment file .env.local within the root of your frontend/ workspace:Code snippetNEXT_PUBLIC_API_URL=http://localhost:8000
Start the interactive Next.js development server:Bashnpm run dev
Open your browser and navigate to http://localhost:3000 to interact with the platform.