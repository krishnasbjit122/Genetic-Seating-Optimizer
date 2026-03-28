# 🧬 Genetic Algorithm for Exam Seating Arrangement

**Optimizing Exam Seating Using Evolutionary Computation**
*Developed by Krishna*

This full-stack application uses a **Genetic Algorithm (GA)** to solve the complex problem of exam seating. It automatically arranges students to ensure that those taking the same subject are not sitting next to each other, thus minimizing cheating and maximizing space utilization.

## 🚀 Features
- **Intelligent Optimization**: Uses Tournament Selection, Crossover, and Mutation to find the best seating plan.
- **Dynamic Seating Grid**: Interactive visualization of the exam hall.
- **Evolution Tracking**: Real-time graph showing fitness improvement over generations.
- **Premium UI**: Dark mode dashboard with smooth animations.
- **Export to PDF**: Generate and download ready-to-print seating arrangements.
- **Customizable Params**: Adjust population size, mutation rate, and generations.

## 🛠 Tech Stack
- **Backend**: Python (FastAPI)
- **Frontend**: React.js, Tailwind CSS
- **Visualization**: Recharts, Framer Motion
- **PDF Generation**: jsPDF, html2canvas

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- Node.js & npm

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Usage
1. Open `http://localhost:5173`.
2. Upload the `students_sample.csv` (provided in the root folder).
3. Adjust the Room Size (Rows × Columns).
4. Click **Run GA Optimizer**.
5. View the generated plan and the fitness improvement chart.
6. Export the result as PDF.

## 🧠 Core Logic
The application treats student placement as a "chromosome." 
- **Gene**: A seat (represented by student ID or empty).
- **Fitness Function**: Penalizes subject clashes (same subject students sitting in 8-neighbor proximity).
- **Evolution**: The algorithm iterates through generations, keeping the best arrangements and mixing them to evolve a near-perfect result.
